import pathlib
import os


class OMSIMap:
    def __init__(self, globalcfg):
        r"""
        Initialize OMSIMap with path to global.cfg file of an OMSI 2 map.
        
        Args:
            globalcfg: Path to global.cfg file
                e.g., F:\SteamLibrary\steamapps\common\OMSI 2\maps\Newcastle Pro - Left Path\global.cfg
        """
        self.globalcfg = globalcfg
        self.basefilelocation = pathlib.Path(globalcfg).parent
        self.ttpfiles = [f for f in pathlib.Path(f"{self.basefilelocation}/TTData").glob("*.ttp")]
        
        self.stations = []  # List of (stopname, stopid) tuples
        self.trips = {}     # Dict: { route_code: {"destination": str, "route_short": str, "stops": [stopid, ...]}, ... }
        
    
    def _parse_ttp_file(self, filepath):
        """
        Parse a .ttp file and extract trip and station data.
        
        Returns:
            List of trip dicts with keys: route_code, destination, route_short, stops
        """
        trips_in_file = []
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.readlines()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return trips_in_file
        
        i = 0
        while i < len(content):
            line = content[i]
            
            if line.strip() == "[trip]":
                # [trip] section format (with blank line after header):
                # [trip]
                # {blank}
                # {route_code}
                # {route_short}
                # {blank}
                # ... (later: [station_typ2] entries)
                #
                # OR (older format without blank after [trip]):
                # [trip]
                # {route_code}
                # {destination}
                # {route_short}
                
                # Check if next line is blank
                next_idx = i + 1
                if next_idx < len(content) and content[next_idx].strip() == "":
                    # New format with blank line
                    route_code = content[i + 2].strip() if i + 2 < len(content) else ""
                    route_short = content[i + 3].strip() if i + 3 < len(content) else ""
                    destination = ""  # Blank in new format
                    start_from = i + 4
                else:
                    # Old format without blank line
                    route_code = content[i + 1].strip() if i + 1 < len(content) else ""
                    destination = content[i + 2].strip() if i + 2 < len(content) else ""
                    route_short = content[i + 3].strip() if i + 3 < len(content) else ""
                    start_from = i + 4
                
                trip_data = {
                    "route_code": route_code,
                    "destination": destination,
                    "route_short": route_short,
                    "stops": []
                }
                
                # Scan forward to collect all [station_typ2] entries for this trip
                # until we hit the next major section (like [profile], [station], etc.)
                j = start_from
                while j < len(content):
                    stripped = content[j].strip()
                    if stripped == "[station_typ2]":
                        stop_id = content[j + 1].strip() if j + 1 < len(content) else ""
                        if stop_id:
                            trip_data["stops"].append(stop_id)
                        j += 2
                    elif stripped.startswith("[") and stripped != "[station_typ2]":
                        # Hit next major section (like [profile], [station], etc.)
                        break
                    else:
                        j += 1
                
                if trip_data["route_code"]:  # Only add if route_code is non-empty
                    trips_in_file.append(trip_data)
                i = j
            else:
                i += 1
        
        return trips_in_file
    
    
    def load_stops(self):
        """
        Load bus stops from Busstops.cfg if it exists.
        If not, parse stops from [station] entries in .ttp files.
        
        Populates self.stations with (stopname, stopid) tuples.
        """
        busstopfile = self.basefilelocation / "TTData" / "Busstops.cfg"
        
        if busstopfile.exists():
            # Parse from Busstops.cfg
            try:
                with open(busstopfile, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip() == "[busstop]":
                            stopname = f.readline().strip()
                            f.readline()  # skip zone_id line (useless)
                            stopid = f.readline().strip()
                            f.readline()  # skip time_value line (useless)
                            f.readline()  # skip first 0
                            f.readline()  # skip second 0
                            
                            if stopname and stopid:
                                self.stations.append((stopname, stopid))
            except Exception as e:
                print(f"Error parsing Busstops.cfg: {e}")
                self._load_stops_from_ttp()
        else:
            # Fallback: parse from [station] entries in .ttp files
            self._load_stops_from_ttp()
    
    
    def _load_stops_from_ttp(self):
        """
        Fallback parser: extract stops from [station] entries in .ttp files.
        Used when Busstops.cfg doesn't exist.
        """
        for ttp_file in self.ttpfiles:
            try:
                with open(ttp_file, "r", encoding="utf-8") as f:
                    content = f.readlines()
            except Exception as e:
                print(f"Error reading {ttp_file}: {e}")
                continue
            
            i = 0
            while i < len(content):
                if content[i].strip() == "[station]":
                    # [station] format:
                    # [station]
                    # {stopid_nonrepeated}
                    # {sequence}
                    # {stopname}
                    # {zone}
                    # ... (floats for coords, etc.)
                    
                    if i + 3 < len(content):
                        stopid = content[i + 1].strip()
                        # skip i+2 (sequence)
                        stopname = content[i + 3].strip()
                        
                        if stopid and stopname:
                            # Check if not already added (avoid duplicates)
                            if (stopname, stopid) not in self.stations:
                                self.stations.append((stopname, stopid))
                    i += 1
                else:
                    i += 1
    
    
    def load_trips(self):
        """
        Load trips (routes) from all .ttp files.
        
        Populates self.trips with structure:
        {
            route_code: {
                "destination": str,
                "route_short": str,
                "stops": [stopid1, stopid2, ...]
            },
            ...
        }
        """
        for ttp_file in self.ttpfiles:
            trips_in_file = self._parse_ttp_file(ttp_file)
            for trip in trips_in_file:
                route_code = trip["route_code"]
                # Use route_code as key; if duplicate, last one wins (or could merge)
                self.trips[route_code] = {
                    "destination": trip["destination"],
                    "route_short": trip["route_short"],
                    "stops": trip["stops"]
                }
                        
                        
            
    