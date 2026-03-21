from string import Template
from types import GeneratorType
import sqlite3
import sys
import os
import hashlib
import multiprocessing
import re

class ericcode:
    mapping = {'a': 11, 'b': 12, 'c':13,'d':21,'e':22,'f':23,'g':31,'h':32,'i':33,'j':41,'k':42,'l':43,'m':51,'n':52,'o':53,'p':61,'q':62,'r':63,'s':71,'t':72,'u':73,'v':81,'w':82,'x':83,'y':91,'z':92,'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
    oristring = ''
    def retstr(self) -> str:
        returnstring = ''.join(self.eric)
        if (len(returnstring) - len(self.oristring) == 1 and returnstring[-1] != 0) or (len(returnstring) < 6 and returnstring[-1] != 0):
            returnstring = returnstring + '0'
        return returnstring
    def __init__(self, code: str) -> None:
        self.oristring = code
        self.eric = list(map(str,[self.mapping[c] for c in (code.lower() if isinstance(code, str) else str(code))]))
    def __len__(self) -> int:
        return len(''.join(self.eric))
    def __str__(self) -> str:
        returnstring = ''.join(self.eric)
        # if len(returnstring) < 6:
        #     returnstring = returnstring + '0'
        #     if len(eric) - len(name) == 1 or len(eric) < 6:
        # eric = eric + '0'
        # if ((len(returnstring) - len(self.oristring) == 1 or len(returnstring) < 6) and returnstring[-1] != "0") :
        #     returnstring = returnstring + '0'
        return returnstring
    def __int__(self) -> int:
        return int(str(self.retstr()))
    
    @property
    def orig(self) -> str:
        return self.oristring
    

            
class gorbacode:
    mapping = {'a': 11, 'b': 12, 'c':13,'d':21,'e':22,'f':23,'g':31,'h':32,'i':33,'j':41,'k':42,'l':43,'m':51,'n':52,'o':53,'p':61,'q':62,'r':63,'s':71,'t':72,'u':73,'v':81,'w':82,'x':83,'y':91,'z':92,'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
    def __init__(self) -> None:
        raise NotImplementedError("Gorba code is not implemented yet")
    '''
    I dont know what code gorba uses, so I will leave this empty for now
    '''
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))
def search_in_slice(sliceee, name):
    for index, stop in enumerate(sliceee):
        if stop.name == name:
            return stop, index
    return None, -1

class HOF_Hanover:
    name = 'Default'
    servicetrip = 'Not In Service'
    ddu : list['Busstop_DDU'] = []
    stopreporter : list['Busstop_Stopreporter'] = []
    termini : list['Termini'] = []
    infosystem : list['Infosystem'] = []
    handrail_flag = True
    header_template = Template('''------------------------------------------
Created with Hof Creator for GX7767 Hoilun
https://github.com/FreeHK-Lunity/GX_hof_creator/
------------------------------------------

#####################
    General Info     
#####################
[name]
$name

[servicetrip]
$servicetrip

stringcount_terminus
6

stringcount_busstop
4
#####################
    Destination
#####################
''')
    termini_template = Template('''[addterminus$allexit]
$eric
$destination
$busfull
$pai_page4
$pai_page3
$pai_page2
$pai_page1
$RTID
.........................
''')
    stopreporter_template = Template('''[addbusstop]
$name
$EngDisplay
$Line2String
$Outbound_sectionfare
$Inbound_sectionfare
.........................$comment
''')
    ddu_template = Template('''[addbusstop]
$RTNO
$Outbound_dir          $sectiontimes_Y
$Inbound_dir           $sectiontimes_Z
$Outbound_price
$Inbound_price
.........................
''')
    trip_template = Template('''[infosystem_trip]
$ericcode
$Destination
$ericcode
$routenoanddir
''')
    busstop_list_template = Template('''\n[infosystem_busstop_list]
$amount_of_stops
$rtno
$busstops

''')
    
    header_template_v2 = Template('''------------------------------------------
Created with Hof Creator for GX7767 Hoilun
https://github.com/FreeHK-Lunity/GX_hof_creator/
------------------------------------------
[name]
$name

[servicetrip]
$servicetrip

[global_strings]
0

stringcount_terminus
6

stringcount_busstop
4
''')
    
    termini_full_template_v2 = Template('''[addterminus_list]
$termini
[end]
''')
    
    termini_template_v2 = Template('''$allexit\t$eric\t$destination\t$busfull\t$pai_page4\t$pai_page3\t$pai_page2\t$pai_page1\t$RTID''')
    
    stopreporter_full_template_v2 = Template('''[addbusstop_list]
$ls_ddu
$ls_stopreporter                                 
[end]
''')
    stopreporter_template_v2 = Template('''$name\t$EngDisplay\t$Line2String\t$Outbound_sectionfare\t$Inbound_sectionfare\t$comment''')
    ddu_template_v2 = Template('''$RTNO\t$Outbound_dir        $sectiontimes_Y\t$Inbound_dir        $sectiontimes_Z\t$Outbound_price\t$Inbound_price''')

									
    def __init__(self,name:str='Default',servicetrip:str='Not In Service') -> None:
        self.name = name
        self.servicetrip = servicetrip
        


    class Termini:
        def __init__(self,allexit:bool = False, eric: str = "", destination: str = '', busfull: str = '', flip: list[str] = [], RTID: str = '') -> None: #flip is a list of strings, eric will be inputted as '289XZ' and converted to 2899192
            self._allexit = '_allexit' if allexit else ''
            self._eric = ericcode(eric)
            self._destination = destination
            self._busfull = busfull
            self._flip = flip
            self._flup4 = flip[3] if len(flip) > 3 else ''
            self._flup3 = flip[2] if len(flip) > 2 else ''
            self._flup2 = flip[1] if len(flip) > 1 else ''
            
            self._flup1 = flip[0] if len(flip) > 0 else ''
            self._RTID = self._eric.orig if RTID == '' else RTID

        @property
        def eric(self) -> str:
            return str(self._eric.orig)
        @eric.setter
        def eric(self, value: str) -> None:
            self._eric = ericcode(value)
            self._RTID = self._eric.orig
        @property
        def RTID(self) -> str:
            # return str(self._RTID)
            return f'{self._eric.orig.rjust(6,'0')}+{self._destination}'
        @property
        def destination(self) -> str:
            return str(self._destination)
        @destination.setter
        def destination(self, value: str) -> None:
            self._destination = value
        @property
        def busfull(self) -> str:
            return str(self._busfull)
        @busfull.setter
        def busfull(self, value: str) -> None:
            self._busfull = value
        @property
        def flip(self) -> list[str]:
            # return self._flip
            return [a.replace("/","\\") for a in self._flip]
        @flip.setter
        def flip(self, value: list[str]) -> None:
            self._flip = value
            self._flup4 = value[3] if len(value) > 3 else ''
            self._flup3 = value[2] if len(value) > 2 else ''
            self._flup2 = value[1] if len(value) > 1 else ''
            self._flup1 = value[0] if len(value) > 0 else ''
        @property
        def allexit(self) -> str:
            return self._allexit
        @allexit.setter
        def allexit(self, value: bool) -> None:
            self._allexit = '_allexit' if value else ''
        
        
        def __str__(self) -> str:
            return HOF_Hanover.termini_template.substitute(allexit=self._allexit, eric=self._eric.retstr(), destination=self._destination, busfull=self._busfull, pai_page4 = self._flup4, pai_page3 = self._flup3, pai_page2 = self._flup2,pai_page1 = self._flup1,RTID=self.RTID)

    class Busstop_Stopreporter:
        def __init__(self, name:str = '',EngDisplay:str = '',ChiSeconds:int = 0,EngSeconds:int = 0,ManSeconds:int = 0,Outbound_sectionfare:float = 0.0,Inbound_sectionfare:float = 0.0,comment: str = '',provided_id:str = "",parent=None) -> None:
            self._name = name
            self._parent = parent  # Store reference to parent instance
            self._EngDisplay = EngDisplay
            self._ChiSeconds = str(ChiSeconds).rjust(2,'0')
            self._EngSeconds = str(EngSeconds).rjust(2,'0')
            self._ManSeconds = str(ManSeconds).rjust(2,'0')
            self._raw_Outbound_sectionfare = Outbound_sectionfare
            self._raw_Inbound_sectionfare = Inbound_sectionfare
            self._Autoskip = False
            self._pages = 1
            self._engscroll = self._EngDisplay.count('@') // 2
            self._comment = comment
            # Generate a unique busstopID based on name and EngDisplay
            unique_str = f"{name}-{EngDisplay}"
            self.busstopID = hashlib.md5(unique_str.encode('utf-8')).hexdigest()[:8] if provided_id == "" else provided_id

        @property
        def _Outbound_sectionfare(self) -> str:
            handrail_flag = self._parent.handrail_flag if self._parent is not None else HOF_Hanover.handrail_flag
            return f"${self._raw_Outbound_sectionfare:.1f}" if isinstance(self._raw_Outbound_sectionfare,float) and self._raw_Outbound_sectionfare != -1.0 else self._comment if self._comment != '' else "No_PHTH" if not handrail_flag and "WELCOME ONBOARD" in self._EngDisplay else self._name if "dingdong" not in self._name.lower() else "SectionFare"

        @property
        def _Inbound_sectionfare(self) -> str:
            handrail_flag = self._parent.handrail_flag if self._parent is not None else HOF_Hanover.handrail_flag
            return f"${self._raw_Inbound_sectionfare:.1f}" if isinstance(self._raw_Inbound_sectionfare,float) and self._raw_Inbound_sectionfare != -1.0 else self._comment if self._comment != '' else "No_PHTH" if not handrail_flag and "WELCOME ONBOARD" in self._EngDisplay else self._name if "dingdong" not in self._name.lower() else "SectionFare"

        @property
        def name(self) -> str:
            return self._name

        @name.setter
        def name(self, value: str) -> None:
            modified_name = value
            # if self._engscroll > 2 and not modified_name[-1] == '!':
            #     modified_name += "!"
            # if self._pages == 2 and not (modified_name[0:1] == '!' or modified_name[0:2] == '_!'):
            #     modified_name = '!' + modified_name
            # if self._pages == 3 and not (modified_name[0:2] == '!!' or modified_name[0:3] == '_!!'):
            #     modified_name = '!' + modified_name
            # if self._Autoskip and not modified_name[-1] == '_':
            #     modified_name += "_"
            self._name = modified_name

        @property
        def EngDisplay(self) -> str:
            return self._EngDisplay

        @EngDisplay.setter
        def EngDisplay(self, value: str) -> None:
            self._EngDisplay = value
            self._engscroll = self._EngDisplay.count('@') / 2
            if self._engscroll >= 2:
                self._name = self._name #this is to trigger the setter of name to add the exclamation mark
        @property
        def ChiSeconds(self) -> int:
            return int(self._ChiSeconds)

        @ChiSeconds.setter
        def ChiSeconds(self, value: int) -> None:
            self._ChiSeconds = str(value).rjust(2, '0')

        @property
        def EngSeconds(self) -> int:
            return int(self._EngSeconds)

        @EngSeconds.setter
        def EngSeconds(self, value: int) -> None:
            self._EngSeconds = str(value).rjust(2, '0')
            
        @property
        def ManSeconds(self) -> int:
            return int(self._ManSeconds)
        @ManSeconds.setter
        def ManSeconds(self, value: int) -> None:
            self._ManSeconds = str(value).rjust(2, '0')

        @property
        def Line2String(self) -> str:
            temp = f"{str(self.ChiSeconds).rjust(2, '0') if self.ChiSeconds != 0 else 'NS'} {str(self.EngSeconds).rjust(2, '0') if self.EngSeconds != 0 else 'NS'}{" " + str(sum([self.ChiSeconds, self.EngSeconds, self.ManSeconds])).rjust(2, '0') if self.ManSeconds > 0 else ' NS' if self.ManSeconds == -1 else ''}"
            if temp == "NS NS NS":
                return "NoSound"
            return temp
            
        
        


        @property
        def Outbound_sectionfare(self) -> float | str:
            return float(self._Outbound_sectionfare.strip('$')) if self._Outbound_sectionfare.lstrip("$").replace(".","").isnumeric() else self._name if "dingdong" not in self._name.lower() else "SectionFare"

        @Outbound_sectionfare.setter
        def Outbound_sectionfare(self, value: float) -> None:
            self._raw_Outbound_sectionfare = value

        @property
        def Inbound_sectionfare(self) -> float | str:
            return float(self._Inbound_sectionfare.strip('$')) if self._Inbound_sectionfare.lstrip("$").replace(".","").isnumeric() else self._name if "dingdong" not in self._name.lower() else "SectionFare"

        @Inbound_sectionfare.setter
        def Inbound_sectionfare(self, value: float) -> None:
            self._raw_Inbound_sectionfare = value
        def __str__(self) -> str:

            
            return HOF_Hanover.stopreporter_template.substitute(name=self._name, EngDisplay=self._EngDisplay, Line2String=self.Line2String, Outbound_sectionfare=self._Outbound_sectionfare, Inbound_sectionfare=self._Inbound_sectionfare,comment=self._comment)
        
        def add_chi_page(self) -> None:
            if self._pages == 3:
                print("GPSHoilun does not support more than 3 pages")
                return
            self._pages += 1
            self._name = self._name #this is to trigger the setter of name to add the exclamation mark
        @property
        def pass_autoskip(self) -> bool:
            return self._Autoskip
        @pass_autoskip.setter
        def pass_autoskip(self, value: bool) -> None:
            self._Autoskip = value
            self._name = self._name #this is to trigger the setter of name to add the underscore
        # def set_pass(self, value: bool) -> None:
        #     self._Autoskip = value
        @property
        def comment(self) -> str:
            return self._comment
        @comment.setter
        def comment(self, value: str) -> None:
            self._comment = value

        
    class Busstop_DDU:
        def __init__(self, RTNO:str = '',Outbound_dir:str = '',Inbound_dir:str = '',Outbound_price:float = 0.0,Inbound_price:float = 0.0,sectiontimes_Y:int = 0,sectiontimes_Z:int = 0) -> None: 
            self._RTNO = RTNO
            self._Outbound_dir = Outbound_dir
            self._Inbound_dir = Inbound_dir
            self._Outbound_price = f"${float(Outbound_price):.1f}" 
            self._Inbound_price = f"${float(Inbound_price):.1f}" 
            self._sectiontimes_Y = sectiontimes_Y
            self._sectiontimes_Z = sectiontimes_Z
        @property
        def RTNO(self) -> str:
            return self._RTNO
        @RTNO.setter
        def RTNO(self, value: str) -> None:
            self._RTNO = value
        @property
        def Outbound_dir(self) -> str:
            return self._Outbound_dir
        @Outbound_dir.setter
        def Outbound_dir(self, value: str) -> None:
            self._Outbound_dir = value
        @property
        def Inbound_dir(self) -> str:
            return self._Inbound_dir
        @Inbound_dir.setter
        def Inbound_dir(self, value: str) -> None:
            self._Inbound_dir = value
        @property
        def Outbound_price(self) -> float:
            return float(self._Outbound_price.strip('$'))
        @Outbound_price.setter
        def Outbound_price(self, value: float) -> None:
            self._Outbound_price = f"${value:.1f}"
        @property
        def Inbound_price(self) -> float:
            return float(self._Inbound_price.strip('$'))
        @Inbound_price.setter
        def Inbound_price(self, value: float) -> None:
            self._Inbound_price = f"${value:.1f}"
        @property
        def sectiontimes_Y(self) -> int:
            return self._sectiontimes_Y
        @sectiontimes_Y.setter
        def sectiontimes_Y(self, value: int) -> None:
            self._sectiontimes_Y = value
        @property
        def sectiontimes_Z(self) -> int:
            return self._sectiontimes_Z
        @sectiontimes_Z.setter
        def sectiontimes_Z(self, value: int) -> None:
            self._sectiontimes_Z = value
        def __str__(self) -> str:
            return HOF_Hanover.ddu_template.substitute(RTNO=self._RTNO, Outbound_dir=self._Outbound_dir, Inbound_dir=self._Inbound_dir, Outbound_price=self._Outbound_price, Inbound_price=self._Inbound_price, sectiontimes_Y=self._sectiontimes_Y, sectiontimes_Z=self._sectiontimes_Z)
        
    class Infosystem:
        '''
        Modifications of the Infosystem class will be made for enforcing the correct format of infosystems
        (infosystem_trip and infosystem_busstop_list needs to be in a pair for the correct format, and both needs to be in a pair for GPSHoilun to read the hof correctly)
        '''
        valid_infosystem = Template('''
------------------1st direction-------------
$trip1
////////////////////////////////////////////
$stoplist1
------------------2nd direction-------------
$trip2
////////////////////////////////////////////
$stoplist2
.............................................
''')
        class trip:
            def __init__(self,eric:str =  '',Destination:str = '',RouteNo:str = '') -> None:
                self._ericcode = str(ericcode(eric))
                self._Destination = Destination
                self._routeno = RouteNo
            @property
            def ericcode(self) -> str:
                return str(self._ericcode)
            @ericcode.setter
            def ericcode(self, value: str) -> None:
                self._ericcode = str(ericcode(value))
            @property
            def Destination(self) -> str:
                return self._Destination
            @Destination.setter
            def Destination(self, value: str) -> None:
                self._Destination = value
            @property
            def routeno(self) -> str:
                return self._routeno
            @routeno.setter
            def routeno(self, value: str) -> None:
                self._routeno = f"{value}"
            def __str__(self) -> str:
                return HOF_Hanover.trip_template.substitute(ericcode=self._ericcode, Destination=self._Destination, routenoanddir=f"{self._routeno}")
            def __repr__(self) -> list[str]:
                return [self._ericcode, self._Destination, self._routeno]
        class busstop_list():
            def __init__(self,bus_stops:list[str] = [],rtno:str = '',busstop_ids:list[str] = []) -> None:
                self._busstops = bus_stops
                self._rtno = rtno
                self._amount_of_stops = len(bus_stops)
                self.bustops_withid = ["" for _ in range(len(bus_stops))] if busstop_ids == [] else busstop_ids
            @property
            def busstops(self) -> str:
                return '\n'.join(self._busstops)
            @busstops.setter
            def busstops(self, value: list[str]) -> None:
                self._busstops = value
                self._amount_of_stops = len(value)
            @busstops.deleter
            def busstops(self, deleteion_pos) -> None:
                del self._busstops[deleteion_pos]
                self._amount_of_stops = len(self._busstops)
            @property
            def rtno(self) -> str:
                return self._rtno
            @rtno.setter
            def rtno(self, value: str) -> None:
                self._rtno = value
            @property
            def amount_of_stops(self) -> int:
                return self._amount_of_stops
            @amount_of_stops.setter
            def amount_of_stops(self, value: int) -> None:
                self._amount_of_stops = value
            @property
            def db_export(self) -> list:
                return self._busstops
            @property
            def db_export_withid(self) -> str:
                return "\n".join(self.bustops_withid)
            def __str__(self) -> str:
                return HOF_Hanover.busstop_list_template.substitute(amount_of_stops=self._amount_of_stops + 1, rtno=self._rtno, busstops=self.busstops)
            def __repr__(self) -> list[int | str | list[str]]:
                return [self._amount_of_stops, self._rtno, self._busstops]
            def __iter__(self) -> list[str]:
                return self._busstops


        def __init__(self,single_or_dual_dir:bool = True,route:str='',dir1:str='',dir2:str='',bustoplist1:list[str]=[],bustoplist2:list[str]=[],busstoplist1_ids:list[str]=[], busstoplist2_ids:list[str]=[]) -> None: 
            #route must be inputted as '289X', we will automaticllu add Y and Z at the end
            #single_or_dual_dir with True being dual direction and False being single direction
            self._single_or_dual_dir = single_or_dual_dir
            self._trip1 = self.trip(f"{route}Y",dir1,route)
            self._trip2 = self.trip(f"{route}Z",dir2,route)
            
            self._busstop_list1 = self.busstop_list(bustoplist1,route,busstoplist1_ids)
            self._busstop_list2 = self.busstop_list(bustoplist2,route, busstoplist2_ids)
            self._db_export_bsl1 = self._busstop_list1.db_export
            self._db_export_bsl2 = self._busstop_list2.db_export
            

        @property
        def single_or_dual_dir(self) -> bool:
            return self._single_or_dual_dir
        @single_or_dual_dir.setter
        def single_or_dual_dir(self, value: bool) -> None:
            self._single_or_dual_dir = value
        @property
        def direction1(self) -> str:
            return self._trip1.Destination
        @direction1.setter
        def direction1(self, value: str) -> None:
            self._trip1.Destination = value
        @property
        def direction2(self) -> str:
            return self._trip2.Destination
        @direction2.setter
        def direction2(self, value: str) -> None:
            self._trip2.Destination = value
        @property
        def route(self) -> str:
            return self._trip1.routeno
        @route.setter
        def route(self, value: str) -> None:
            self._trip1.routeno = value
            self._trip2.routeno = value
            self._busstop_list1.rtno = value
            self._busstop_list2.rtno = value
        @property
        def busstop_list1(self) -> str:
            return str(self._busstop_list1)
        @busstop_list1.setter
        def busstop_list1(self, value: list[str]) -> None:
            self._busstop_list1.busstops = value
        @property
        def busstop_list2(self) -> str:
            return str(self._busstop_list2)
        @busstop_list2.setter
        def busstop_list2(self, value: list[str]) -> None:
            self._busstop_list2.busstops = value
        #enable direct access to trip and busstop_list
        @property
        def trip1_class(self) -> trip:
            return self._trip1
        @property
        def trip2_class(self) -> trip:
            return self._trip2
        @property
        def busstop_list1_class(self) -> busstop_list:
            return self._busstop_list1
        @property
        def busstop_list2_class(self) -> busstop_list:
            return self._busstop_list2
        @property
        def db_export_bsl1(self) -> list:
            return self.busstop_list1_class.db_export
        @property
        def db_export_bsl2(self) -> list:
            return self.busstop_list2_class.db_export
        @property
        def db_export_bsl1_withid(self) -> str:
            return "\n".join(self.busstop_list1_class.bustops_withid)
        @property
        def db_export_bsl2_withid(self) -> str:
            return "\n".join(self.busstop_list2_class.bustops_withid)
        def __str__(self) -> str:
            return self.valid_infosystem.substitute(trip1=self._trip1, stoplist1=self._busstop_list1, trip2=self._trip2, stoplist2=self._busstop_list2)
        


        

        
        
        #check busstop validicity
    def check_busstoplist(self) -> bool:
        flag = True
        # Preprocess stopreporter to a set of names for O(1) lookup
        stopreporter_names = {k.name for k in self.stopreporter}
        
        for info in self.infosystem:
            for bus_stop in info.busstop_list1_class._busstops + info.busstop_list2_class._busstops:
                if bus_stop not in stopreporter_names:
                    print(f"Busstop {str(bus_stop)} not found in stopreporter")
                    flag = False

        return flag
    
    def add_ddu(self, RTNO:str = '',Outbound_dir:str = '',Inbound_dir:str = '',Outbound_price:float = -1.0,Inbound_price:float = -1.0,sectiontimes_Y:int = 0,sectiontimes_Z:int = 0) -> None:
        self.ddu.append(self.Busstop_DDU(RTNO,Outbound_dir,Inbound_dir,Outbound_price,Inbound_price,sectiontimes_Y,sectiontimes_Z))
    def add_stopreporter(self, name:str = '',EngDisplay:str = '',ChiSeconds:int = 0,EngSeconds:int = 0,ManSeconds: int = 0,Outbound_sectionfare:float = 0.0,Inbound_sectionfare:float = 0.0,comment:str = "",provided_id:str = '') -> None:
        self.stopreporter.append(self.Busstop_Stopreporter(name,EngDisplay,ChiSeconds,EngSeconds,ManSeconds,Outbound_sectionfare,Inbound_sectionfare,comment, provided_id = provided_id, parent=self))
    def add_terminus(self,allexit:bool = False, eric: str = '', destination: str = '', busfull: str = '', flip: list[str] = [], RTID: str = '') -> None:
        self.termini.append(self.Termini(allexit, eric, destination, busfull, flip, RTID))
    # def add_infosystem(self,eric:str =  '',Destination:str = '',RouteNo:str = '') -> None:
    #     self.infosystem.append(self.Infosystem.trip(eric,Destination,RouteNo))
    # def add_busstop_list(self,bus_stops:list[str] = [],rtno:str = '') -> None:
    #     self.infosystem.append(self.Infosystem.busstop_list(bus_stops,rtno))
    # def add_infosystem(self,single_or_dual_dir:bool,route:str='',dir1:str='',dir2:str='',bustoplist1:list[str]=[],bustoplist2:list[str]=[]) -> None:
    #     self.infosystem.append(self.Infosystem(single_or_dual_dir,route,dir1,dir2,bustoplist1,bustoplist2))
    def add_infosystem(self,hasid:bool = False, single_or_dual_dir:bool = True, route:str='', dir1:str='', dir2:str='', bustoplist1:list[str]=[], bustoplist2:list[str]=[],busstoplist1_ids:list[str]=[], busstoplist2_ids:list[str]=[]) -> None:
        if hasid:
            # print("Adding infosystem with id")
            self.infosystem.append(self.Infosystem(single_or_dual_dir, route, dir1, dir2, bustoplist1, bustoplist2, busstoplist1_ids, busstoplist2_ids))
        else:
            # print("Adding infosystem without id")
            self.infosystem.append(self.Infosystem(single_or_dual_dir, route, dir1, dir2, bustoplist1, bustoplist2))
            self.fill_busttoplist_with_id()
    def _sync_stopreporter_parent(self) -> None:
        for stop in self.stopreporter:
            if stop._parent is not self:
                stop._parent = self
    def showfullhof(self) -> str:
        self._sync_stopreporter_parent()
        returnstring = '\n'.join([''.join(self.header_template.substitute(name = self.name,servicetrip = self.servicetrip)),'\n'.join((str(i) for i in self.termini)),'\n'.join(str(i) for i in self.ddu),'\n'.join((str(i) for i in self.stopreporter)),'\n'.join((str(i) for i in self.infosystem))])
        return returnstring
    def show_hof_v2(self) -> str:
        self._sync_stopreporter_parent()
        list_termini = [self.termini_template_v2.substitute(allexit="{ALLEX}" if i.allexit == '_allexit' else "", eric=i._eric.retstr(), destination=i.destination, busfull=i.busfull, pai_page4=i.flip[3] if len(i.flip) > 3 else '', pai_page3=i.flip[2] if len(i.flip) > 2 else '', pai_page2=i.flip[1] if len(i.flip) > 1 else '', pai_page1=i.flip[0] if len(i.flip) > 0 else '', RTID=str(i.RTID)) for i in self.termini]
        list_stopreporter = [self.stopreporter_template_v2.substitute(name=i.name, EngDisplay=i.EngDisplay, Line2String=i.Line2String, Outbound_sectionfare=i.Outbound_sectionfare, Inbound_sectionfare=i.Inbound_sectionfare, comment=i.comment) for i in self.stopreporter]
        list_ddu = [self.ddu_template_v2.substitute(RTNO=i.RTNO, Outbound_dir=i.Outbound_dir, sectiontimes_Y=i.sectiontimes_Y, Inbound_dir=i.Inbound_dir, sectiontimes_Z=i.sectiontimes_Z, Outbound_price=i.Outbound_price, Inbound_price=i.Inbound_price) for i in self.ddu]
        returnstring = '\n'.join([
            self.header_template_v2.substitute(name=self.name, servicetrip=self.servicetrip),
            self.termini_full_template_v2.substitute(termini='\n'.join(list_termini)),
            self.stopreporter_full_template_v2.substitute(ls_ddu='\n'.join(list_ddu), ls_stopreporter='\n'.join(list_stopreporter)),
            '\n'.join(str(i) for i in self.infosystem)
        ])
        
        # returnstring = '\n'.join([
        #     self.header_template_v2.substitute(name=self.name, servicetrip=self.servicetrip),
        #     self.termini_full_template_v2.substitute(termini='\n'.join(str(i) for i in self.termini)),
        #     self.stopreporter_full_template_v2.substitute(ls_ddu='\n'.join(str(i) for i in self.ddu), ls_stopreporter='\n'.join(str(i) for i in self.stopreporter)),
        #     '\n'.join(str(i) for i in self.infosystem)
        # ])
        return returnstring
    def export_hof(self, filename: str) -> None:
        with open(filename, 'w') as f:
            f.write(self.showfullhof())
            print(f"Exported to {filename}, all comments have been destroyed.")
    def export_hof_v2(self, filename: str) -> None:
        with open(filename, 'w') as f:
            f.write(self.show_hof_v2())
            print(f"Exported to {filename}, all comments have been destroyed.")
    def save_to_db(self, filename: str) -> None:
        database_file = sqlite3.connect(f'{filename}')
        c = database_file.cursor()
        c.execute('DROP TABLE IF EXISTS ddu')
        c.execute('DROP TABLE IF EXISTS stopreporter')
        c.execute('DROP TABLE IF EXISTS termini')
        c.execute('DROP TABLE IF EXISTS infosystem')
        c.execute(f'''CREATE TABLE IF NOT EXISTS ddu (
                RTNO TEXT, Outbound_dir TEXT, Inbound_dir TEXT,
                Outbound_price REAL, Inbound_price REAL,
                sectiontimes_Y INTEGER, sectiontimes_Z INTEGER)''')

        c.execute(f'''CREATE TABLE IF NOT EXISTS stopreporter (
                name TEXT, EngDisplay TEXT, ChiSeconds INTEGER,
                EngSeconds INTEGER,ManSeconds INTEGER, Outbound_sectionfare REAL,
                Inbound_sectionfare REAL, comment TEXT, busstopID TEXT primary key)''')
        c.execute(f'''CREATE TABLE IF NOT EXISTS termini (
                allexit BOOL, eric TEXT, destination TEXT, busfull TEXT,
                flip4 TEXT, flip3 TEXT, flip2 TEXT, flip1 TEXT, RTID TEXT)''')
        c.execute(f'''CREATE TABLE IF NOT EXISTS infosystem (
                single_or_dual_dir BOOL, route TEXT,
                dir1 TEXT, dir2 TEXT, bustoplist1 TEXT, bustoplist2 TEXT,busstoplist1_withid TEXT,busstoplist2_withid TEXT)''')
        c.execute('DELETE FROM ddu')
        c.execute('DELETE FROM stopreporter')
        c.execute('DELETE FROM termini')
        c.execute('DELETE FROM infosystem')
        # for i in self.infosystem:
            # print(i.busstop_list2_class.db_export)
        # for i in self.stopreporter:
            # if i.name[:9] == "_DingDong":
                # print(i._Inbound_sectionfare, i._Outbound_sectionfare,"|",i.Inbound_sectionfare, i.Outbound_sectionfare)
        c.executemany('INSERT INTO ddu VALUES (?,?,?,?,?,?,?)', [(i.RTNO, i.Outbound_dir, i.Inbound_dir, i.Outbound_price, i.Inbound_price, i.sectiontimes_Y, i.sectiontimes_Z) for i in self.ddu])
        # c.executemany('INSERT INTO stopreporter VALUES (?,?,?,?,?,?,?,?)', [(i.name, i.EngDisplay, i.ChiSeconds, i.EngSeconds, i.Outbound_sectionfare, i.Inbound_sectionfare, i.comment,i.busstopID) for i in self.stopreporter])
        for i in self.stopreporter:
            c.execute('INSERT INTO stopreporter VALUES (?,?,?,?,?,?,?,?,?)', (i.name, i.EngDisplay, i.ChiSeconds, i.EngSeconds, i.ManSeconds, i.Outbound_sectionfare, i.Inbound_sectionfare, i.comment, i.busstopID))
        c.executemany('INSERT INTO termini VALUES (?,?,?,?,?,?,?,?,?)', [(i.allexit, i.eric, i.destination, i.busfull, i.flip[3] if len(i.flip) > 3 else '', i.flip[2] if len(i.flip) > 2 else '', i.flip[1] if len(i.flip) > 1 else '', i.flip[0] if len(i.flip) > 0 else '', i.RTID) for i in self.termini])
        c.executemany('INSERT INTO infosystem VALUES (?,?,?,?,?,?,?,?)', [(i.single_or_dual_dir, i.route, i.direction1, i.direction2, "\n".join(i.busstop_list1_class.db_export), "\n".join(i.busstop_list2_class.db_export), i.busstop_list1_class.db_export_withid, i.busstop_list2_class.db_export_withid) for i in self.infosystem])

        database_file.commit()
        database_file.close()

        print(f"Saved to {filename}")

    
    def fill_busttoplist_with_id(self) -> None:
        """
        Efficiently populates bus stop IDs by creating a lookup map.
        This avoids repeated searches and multiprocessing overhead.
        """
        # Create a lookup dictionary for O(1) access. This is much faster.
        stop_name_to_id_map = {stop.name: stop.busstopID for stop in self.stopreporter}

        def _ensure_id_list_size(busstop_list) -> None:
            if len(busstop_list.bustops_withid) != len(busstop_list._busstops):
                busstop_list.bustops_withid = [""] * len(busstop_list._busstops)
    
        for info in self.infosystem:
            _ensure_id_list_size(info.busstop_list1_class)
            _ensure_id_list_size(info.busstop_list2_class)
            # Process first bus stop list
            for index, stop_name in enumerate(info.busstop_list1_class.db_export):
                existing_id = info.busstop_list1_class.bustops_withid[index]
                if existing_id:
                    continue
                busstop_id = stop_name_to_id_map.get(stop_name)
                if busstop_id:
                    info.busstop_list1_class.bustops_withid[index] = busstop_id
                else:
                    if info.busstop_list1_class._busstops[index] == "":
                        pass
                    else:
                        print(f"Warning: Busstop '{stop_name}' not found in stopreporter.")
    
            # Process second bus stop list
            for index, stop_name in enumerate(info.busstop_list2_class.db_export):
                existing_id = info.busstop_list2_class.bustops_withid[index]
                if existing_id:
                    continue
                busstop_id = stop_name_to_id_map.get(stop_name)
                if busstop_id:
                    info.busstop_list2_class.bustops_withid[index] = busstop_id
                else:
                    if info.busstop_list2_class._busstops[index] == "":
                        pass
                    else:
                        print(f"Warning: Busstop '{stop_name}' not found in stopreporter.")
    
    # ...existing code...
        # for i in self.infosystem:
        #     # print(i.busstop_list1_class.db_export)
        #     for index, j in enumerate(i.busstop_list1_class.db_export):
        #         for k in self.stopreporter:
        #             if k.name == j:
        #                 i.busstop_list1_class.bustops_withid[index] = k.busstopID
        #     for index, j in enumerate(i.busstop_list2_class.db_export):
        #         for k in self.stopreporter:
        #             if k.name == j:
        #                 i.busstop_list2_class.bustops_withid[index] = k.busstopID


    def load_from_db(self, filename: str) -> None:


        database_file = sqlite3.connect(filename)
        c = database_file.cursor()
        c.execute(f'''SELECT * FROM ddu''')
        # self.ddu = [self.Busstop_DDU(*i) for i in c.fetchall()]
        ls = c.fetchall()
        for index, i in enumerate(ls):
            ls[index] = list(i)
            ls[index][3] = f"{float(ls[index][3]):.1f}" if (isinstance(ls[index][3],float) or ls[index][3].replace(".","").isnumeric()) else -1.0
            ls[index][4] = f"{float(ls[index][4]):.1f}" if (isinstance(ls[index][4],float) or ls[index][4].replace(".","").isnumeric()) else -1.0
            # print(ls[index])
        self.ddu = [self.Busstop_DDU(*i) for i in ls]
        c.execute(f'''SELECT * FROM stopreporter''')
        self.stopreporter = [self.Busstop_Stopreporter(*i, parent=self) for i in c.fetchall()]
        # for i in c.fetchall():

        c.execute(f'''SELECT * FROM termini''')
        
        ls = c.fetchall()
        
        for index, i in enumerate(ls):
            # ls[index] = list(i)
            # ls[index][0] = True if ls[index][0] == "_allexit" else False
            # for i in ls[index][4:8]:
            #     if i != '':
            #         flips.append(i)
            # print(ls[index],i)
            flips = []
            newls = []
            newls.append(True if ls[index][0] == "_allexit" else False)
            newls.append(ls[index][1])
            newls.append(ls[index][2])
            newls.append(ls[index][3])
            for i in ls[index][4:8]:
                if i != '':
                    flips.append(i)
            newls.append(flips)
            newls.append(ls[index][8])
            # print(newls)
            self.add_terminus(*newls)


                                
        c.execute(f'''SELECT * FROM infosystem''')
        ls = c.fetchall()
        for index, i in enumerate(ls):
            ls[index] = list(i)
            ls[index][4] = ls[index][4].strip().split('\n') if isinstance(ls[index][4], str) else []
            ls[index][5] = ls[index][5].strip().split('\n') if isinstance(ls[index][5], str) else []
            ls[index][6] = ls[index][6].strip().split('\n') if isinstance(ls[index][6], str) else []
            ls[index][7] = ls[index][7].strip().split('\n') if isinstance(ls[index][7], str) else []
            # ls[index][5] = ls[index][5][1:-1].replace("'","").split(', ')
        self.infosystem = [self.Infosystem(*i) for i in ls]
        database_file.close()
        print(f"Loaded from {filename}")

    def load_from_hof(self, filename: str) -> None | int | tuple[None, list[str]]:
        bsl_v2 = False
        tls_v2 = False
        try:
            hof_entry = HOF_Hanover()
            parse_warnings: list[str] = []

            def _add_warning(field_name: str, raw_value: str, fallback_value: int | float, line_index: int) -> None:
                parse_warnings.append(
                    f"Line {line_index + 1}: {field_name} failed to read from '{raw_value}', using fallback {fallback_value}."
                )

            def _safe_non_negative_int(raw_value: str, field_name: str, line_index: int, allow_ns: bool = False) -> int:
                if allow_ns and raw_value == "NS":
                    return 0
                try:
                    value = int(raw_value)
                except (TypeError, ValueError):
                    _add_warning(field_name, str(raw_value), 0, line_index)
                    return 0
                if value < 0:
                    _add_warning(field_name, str(raw_value), 0, line_index)
                    return 0
                return value

            def _safe_ddu_section(raw_value: str, field_name: str, line_index: int) -> int:
                if not isinstance(raw_value, str) or len(raw_value) < 1:
                    _add_warning(field_name, str(raw_value), 0, line_index)
                    return 0
                suffix = raw_value[-1]
                if not suffix.isdigit():
                    # _add_warning(field_name, str(raw_value), 0, line_index) # Allow non-digit suffixes (e.g., "NoSound") but treat them as 0q
                    return 0
                return _safe_non_negative_int(suffix, field_name, line_index)

            def _safe_price(
                raw_value: str,
                field_name: str,
                line_index: int,
                fallback_value: float,
                allow_missing_prefix: bool,
            ) -> float:
                if not isinstance(raw_value, str):
                    _add_warning(field_name, str(raw_value), fallback_value, line_index)
                    return fallback_value
                if not raw_value.startswith('$'):
                    if raw_value and not allow_missing_prefix:
                        _add_warning(field_name, raw_value, fallback_value, line_index)
                    return fallback_value
                try:
                    value = float(raw_value.replace(",", ".").lstrip('$'))
                except (TypeError, ValueError):
                    _add_warning(field_name, raw_value, fallback_value, line_index)
                    return fallback_value
                if value < fallback_value:
                    _add_warning(field_name, raw_value, fallback_value, line_index)
                    return fallback_value
                return value
            try:
                with open(filename, 'r',encoding="utf-8") as f:
                    lines = [line.strip() for line in f]
            except UnicodeDecodeError:
                try:
                    with open(filename, 'r') as f:
                        lines = [line.strip() for line in f]
                except UnicodeDecodeError:
                    return 989
            except FileNotFoundError:
                print(f"File {filename} not found.")
                return
            except Exception as e:
                print(f"An error occurred while reading the file: {e}")
                return
                    
            i = 0
            while i < len(lines):
                line = lines[i]
                if line == "[name]":
                    hof_entry.name = lines[i + 1]
                    i += 2
                elif line == "[servicetrip]":
                    hof_entry.servicetrip = lines[i + 1]
                    i += 2
                elif tls_v2:
                    datum = line.split('\t')
                    conversion = [True if datum[0] == '{ALLEX}' else False]
                    conversion.extend(datum[1:]) # type: ignore
                    # param1 = lines[i + 8].split("+")
                    # if len(param1) == 1:
                    #     eric1 = lines[i+2]
                    #     out1 = param1[0].strip()
                    # else:
                    #     eric1 = param1[0].strip()
                    #     out1 = param1[1].strip()
                    param1 = conversion[-1].split("+") # type: ignore
                    if len(param1) == 1:
                        eric1 = conversion[1]
                        out1 = param1[0].strip()
                    else:
                        eric1 = param1[0].strip()
                        out1 = param1[1].strip()
                    hof_entry.add_terminus(
                        conversion[0],
                        conversion[1],
                        eric1,
                        conversion[2],
                        conversion[3:7][::-1],
                        out1
                    )
                    i +=1
                    continue
                elif bsl_v2:
                    datum = line.split('\t')
                    if len(datum) < 2:
                        i += 1
                        continue
                    # print(datum)
                    stop_name = datum[0]
                    if len(stop_name) < 1:
                        i += 1
                        continue
                    if len(stop_name) >= 5 or (len(time_parts := datum[1].split()) <= 2 and len(time_parts) > 0 and time_parts[0].isdigit()):
                        # parse full stopreporter
                        chi_sec, eng_sec, man_sec = 0, 0, 0
                        time_parts = datum[1].split()
                        if time_parts == ["NoSound"]:
                            chi_sec, eng_sec, man_sec = 0,0,0
                        else:
                            if len(time_parts) >= 1:
                                chi_sec = _safe_non_negative_int(time_parts[0], "ChiSeconds", i, allow_ns=True)
                            if len(time_parts) >= 2:
                                eng_sec = _safe_non_negative_int(time_parts[1], "EngSeconds", i, allow_ns=True)
                            if len(time_parts) == 3:
                                if time_parts[2] == "NS":
                                    man_sec = 0
                                else:
                                    total_sec = _safe_non_negative_int(time_parts[2], "TotalSeconds", i)
                                    man_sec = total_sec - chi_sec - eng_sec
                                    if man_sec < 0:
                                        _add_warning("ManSeconds", time_parts[2], 0, i)
                                        man_sec = 0
                        # if len(time_parts) >= 1 and time_parts[0].isdigit():
                        #     chi_sec = int(time_parts[0])
                        # elif 
                        # if len(time_parts) >= 2 and time_parts[1].isdigit():
                        #     eng_sec = int(time_parts[1])
                        # if len(time_parts) == 3:
                        #     man_sec = int(time_parts[2]) - chi_sec - eng_sec
                        inbound_price = -1.0
                        if len(datum) > 2:
                            inbound_price = _safe_price(
                                datum[2],
                                "Inbound_sectionfare",
                                i,
                                -1.0,
                                allow_missing_prefix=False,
                            )
                        outbound_price = -1.0
                        if len(datum) > 3:
                            outbound_price = _safe_price(
                                datum[3],
                                "Outbound_sectionfare",
                                i,
                                -1.0,
                                allow_missing_prefix=False,
                            )
                        hof_entry.add_stopreporter(
                            stop_name,
                            datum[4] if len(datum) > 4 else "",
                            chi_sec,
                            eng_sec,
                            man_sec,
                            inbound_price,
                            outbound_price,
                            comment=datum[5] if len(datum) > 5 else ""
                        )
                        
                        i += 6
                    else:
                        # parse DDU
                        outbound_dir_raw = datum[1] if len(datum) > 1 else ""
                        inbound_dir_raw = datum[2] if len(datum) > 2 else ""
                        sectiontimes_Y = _safe_ddu_section(outbound_dir_raw, "sectiontimes_Y", i)
                        sectiontimes_Z = _safe_ddu_section(inbound_dir_raw, "sectiontimes_Z", i)
                        inbound_price = _safe_price(
                            datum[3] if len(datum) > 3 else "",
                            "Inbound_price",
                            i,
                            0.0,
                            allow_missing_prefix=True,
                        )
                        outbound_price = _safe_price(
                            datum[4] if len(datum) > 4 else "",
                            "Outbound_price",
                            i,
                            0.0,
                            allow_missing_prefix=True,
                        )
                        hof_entry.add_ddu(
                            stop_name,
                            outbound_dir_raw[:-1].strip(),
                            inbound_dir_raw[:-1].strip(),
                            inbound_price,
                            outbound_price,
                            sectiontimes_Y,
                            sectiontimes_Z
                        )
                        
                        i += 5
                        continue
                elif line == '[addterminus_list]':
                    # bsl_v2 = True
                    tls_v2 = True
                elif line == '[addbusstop_list]':
                    # tls_v2 = True
                    bsl_v2 = True
                    
                elif line == '[end]':
                    bsl_v2 = False
                    tls_v2 = False
                    continue
                elif line == "[addterminus]":
                    # param = lines[i].replace("[addterminus]", "").strip()
                    param1 = lines[i + 8].split("+")
                    if len(param1) == 1:
                        eric1 = lines[i+1].strip()
                        out1 = param1[0].strip()
                    else:
                        eric1 = re.sub(r'^0+(?=\d|\w)', '', param1[0].strip()) # remove leading zeros for ericcode
                        out1 = param1[1].strip()
                    print(eric1,lines[i + 2],lines[i + 3],lines[i + 4 : i + 8][::-1],out1)
                    hof_entry.add_terminus(
                        False,
                        eric1,
                        lines[i + 2],
                        # eric1,
                        lines[i + 3],
                        lines[i + 4 : i + 8][::-1],
                        out1
                    )
                    i += 9
                elif line == "[addterminus_allexit]":
                    param1 = lines[i + 8].split("+")
                    if len(param1) == 1:
                        eric1 = lines[i+1].strip()
                        out1 = param1[0].strip()
                    else:
                        eric1 = param1[0].strip()
                        out1 = param1[1].strip()
                    hof_entry.add_terminus(
                        True,
                        eric1,
                        lines[i + 2],
                        # eric1,
                        lines[i + 3],
                        lines[i + 4 : i + 8][::-1],
                        out1
                    )
                    i += 9
                elif line == "[addbusstop]":
                    # print(len(lines[i + 1]), len(lines[i + 3]),lines[i + 3],lines[i + 1])
                    stop_name = lines[i + 1]
                    if len(stop_name) < 1:
                        i +=1
                        continue
                    if len(stop_name) >= 5 or (len(time_parts := lines[i + 3].split()) <= 2 and len(time_parts) > 0 and time_parts[0].isdigit()):
                        print(stop_name, lines[i + 3])
                        time_parts = lines[i + 3].split()
                        print(time_parts)
                        # parse full stopreporter
                        chi_sec, eng_sec, man_sec = 0, 0, 0
                        if time_parts == ["NoSound"]:
                            pass
                        else:
                            if len(time_parts) >= 1:
                                chi_sec = _safe_non_negative_int(time_parts[0], "ChiSeconds", i + 3, allow_ns=True)
                            if len(time_parts) >= 2:
                                eng_sec = _safe_non_negative_int(time_parts[1], "EngSeconds", i + 3, allow_ns=True)
                            if len(time_parts) == 3:
                                if time_parts[2] == "NS":
                                    man_sec = 0
                                else:
                                    total_sec = _safe_non_negative_int(time_parts[2], "TotalSeconds", i + 3)
                                    man_sec = total_sec - chi_sec - eng_sec
                                    if man_sec < 0:
                                        _add_warning("ManSeconds", time_parts[2], 0, i + 3)
                                        man_sec = 0
                        inbound_price = -1.0
                        inbound_price = _safe_price(
                            lines[i + 4],
                            "Inbound_sectionfare",
                            i + 4,
                            -1.0,
                            allow_missing_prefix=False,
                        )
                        outbound_price = -1.0
                        outbound_price = _safe_price(
                            lines[i + 5],
                            "Outbound_sectionfare",
                            i + 5,
                            -1.0,
                            allow_missing_prefix=False,
                        )
                        if len(lines[i + 2]) > 0 and ((lines[i + 2][-1] in ['T','Y','Z','R'] or len(lines[i + 2]) <= 3 ) and lines[i + 2][:-1].strip().isdigit() and (time_parts != ["NoSound"] and len(time_parts) > 0 and (not time_parts[0].isnumeric() and len(time_parts) <= 3))):
                            # Telargo! Not supported
                            return 990
                        hof_entry.add_stopreporter(
                            stop_name,
                            lines[i + 2],
                            chi_sec,
                            eng_sec,
                            man_sec,
                            inbound_price,
                            outbound_price
                        )
                        
                        i += 7
                    else:
                        # parse DDU
                        # print(lines[i])
                        # print(lines[i+1])
                        # print(lines[i+2])
                        # print(lines[i+3])
                        # print(lines[i+4])
                        # print(lines[i+5])
                        sectiontimes_Y = _safe_ddu_section(lines[i + 2], "sectiontimes_Y", i + 2)
                        sectiontimes_Z = _safe_ddu_section(lines[i + 3], "sectiontimes_Z", i + 3)
                        inbound_price = _safe_price(
                            lines[i + 4],
                            "Inbound_price",
                            i + 4,
                            0.0,
                            allow_missing_prefix=True,
                        )
                        outbound_price = _safe_price(
                            lines[i + 5],
                            "Outbound_price",
                            i + 5,
                            0.0,
                            allow_missing_prefix=True,
                        )
                        hof_entry.add_ddu(
                            stop_name,
                            lines[i + 2][:-1].strip(),
                            lines[i + 3][:-1].strip(),
                            inbound_price,
                            outbound_price,
                            sectiontimes_Y,
                            sectiontimes_Z
                        )
                        i += 6
                    
                elif line == "[infosystem_busstop_list]":
                    # busstop_count_1 = int(lines[i + 1])
                    # busstop_count_2 = int(lines[i + 2])
                    # start_idx = i + 3
                    # end_idx_1 = start_idx + busstop_count_1
                    # end_idx_2 = end_idx_1 + busstop_count_2
                    # hof_entry.infosystem[-1].busstop_list1_class.busstops = lines[start_idx:end_idx_1]
                    # hof_entry.infosystem[-1].busstop_list2_class.busstops = lines[end_idx_1:end_idx_2]
                    # i = end_idx_2
                    if len(self.infosystem) > 0 and self.infosystem[-1].route == lines[i + 2]:
                        
                        startidx = i + 3
                        endidx = startidx + _safe_non_negative_int(lines[i + 1], "infosystem_busstop_count", i + 1)
                        # print(lines[startidx:endidx])
                        self.infosystem[-1].busstop_list2_class.busstops = lines[startidx:endidx]
                        self.infosystem[-1].busstop_list2 = lines[startidx:endidx]
                        self.infosystem[-1]._busstop_list2._busstops= lines[startidx:endidx]
                        self.infosystem[-1].busstop_list2_class.bustops_withid = ["" for _ in range(len(lines[startidx:endidx]))] # reset the busstop ids
                        # print(self.infosystem[-1].busstop_list2_class.db_export)
                        
                        self.infosystem[-1].trip2_class.Destination = lines[startidx:endidx][-2] if len(lines[startidx:endidx]) > 1 else ""
                        i = endidx
                    else:
                        busstop_count_1 = _safe_non_negative_int(lines[i + 1], "infosystem_busstop_count", i + 1) - 1
                        rtno = lines[i + 2]
                        startidx = i + 3
                        endidx = startidx + busstop_count_1
                        bsl1 = lines[startidx:endidx]
                        hof_entry.add_infosystem(
                            single_or_dual_dir=True,
                            route=rtno,
                            dir1=bsl1[-2],
                            dir2="",
                            bustoplist1=bsl1,
                            bustoplist2=[]
                        )
                        i = endidx
                
                else:
                    i += 1
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno) 
            print(e)
            print(f"Error loading from {filename}")
            return
        # print(hof_entry.showfullhof())
        self.name = hof_entry.name
        self.servicetrip = hof_entry.servicetrip
        self.ddu = hof_entry.ddu
        self.stopreporter = hof_entry.stopreporter
        self.termini = hof_entry.termini
        self.infosystem = hof_entry.infosystem
        # temp = [i.name for i in self.stopreporter]
        # if 'Blank' not in temp:
        #     self.add_stopreporter(name='Blank', EngDisplay='', ChiSeconds=0, EngSeconds=0, Outbound_sectionfare=0.0, Inbound_sectionfare=0.0, comment='', provided_id='Blank')
        seta = set()
        for i in self.stopreporter:
            seta.add(i.busstopID)
        if len(seta) != len(self.stopreporter):
            print("Duplicate busstop IDs found, removing duplicates...")
            seen_ids = set()
            unique_stopreporter = []
            for i in self.stopreporter:
                if i.busstopID not in seen_ids:
                    unique_stopreporter.append(i)
                    seen_ids.add(i.busstopID)
            self.stopreporter = unique_stopreporter
        # temp = {i.busstopID: i for i in self.stopreporter}
        # if not temp.get('89352f27'):
        #     self.add_stopreporter(name='Blank', EngDisplay='', ChiSeconds=0, EngSeconds=0, Outbound_sectionfare=0.0, Inbound_sectionfare=0.0, comment='', provided_id='89352f27')
        # lsa = [i.busstopID for i in self.stopreporter]
        
        print(f"Loaded from {filename}")
        if parse_warnings:
            return (None, parse_warnings)

    def new_from_map(self, map_location: str) -> None:
        r"""
        Initialize HOF_Hanover from an OMSI 2 map directory.
        
        Args:
            map_location: Path to map root directory or path to global.cfg file
                e.g., F:\SteamLibrary\steamapps\common\OMSI 2\maps\Newcastle Pro - Left Path
                or    F:\SteamLibrary\steamapps\common\OMSI 2\maps\Newcastle Pro - Left Path\global.cfg
        """
        from pathlib import Path
        from mapParser import OMSIMap
        
        # Ensure we have a path to global.cfg
        map_path = Path(map_location)
        if map_path.is_file() and map_path.name == 'global.cfg':
            global_cfg = str(map_path)
        elif map_path.is_dir():
            global_cfg = str(map_path / 'global.cfg')
        else:
            global_cfg = str(map_path)
        
        if not Path(global_cfg).exists():
            raise FileNotFoundError(f"global.cfg not found at {global_cfg}")
        
        # Parse map data
        try:
            omsi_map = OMSIMap(global_cfg)
            omsi_map.load_stops()
            omsi_map.load_trips()
        except Exception as e:
            raise RuntimeError(f"Failed to parse map: {e}")
        
        # Initialize data lists
        self.termini = []
        self.stopreporter = []
        self.ddu = []
        self.infosystem = []
        
        # Create a mapping of stop_id -> stop name for infosystem generation.
        stop_id_map = {stop_id: stop_name for stop_name, stop_id in omsi_map.stations}
        
        # Direction letters for duplicate routes (from compiler.py mapping_2)
        # Index 0→Z, 1→Y, 2→X, 3→W, 4→V, 5→U, 6→T, 7→S, 8→R, 9→Q
        direction_letters = ['Z', 'Y', 'X', 'W', 'V', 'U', 'T', 'S', 'R', 'Q']
        
        # Group trips by route_short to detect duplicates
        routes_by_short = {}
        for route_code, trip_data in omsi_map.trips.items():
            route_short = trip_data["route_short"]
            destination = trip_data["destination"]
            if route_short not in routes_by_short:
                routes_by_short[route_short] = []
            routes_by_short[route_short].append((route_code, destination, trip_data))

        # Keep per-direction metadata for infosystem generation.
        route_entries_by_short = {}
        
        # Create Termini entries with direction assignment for duplicates
        for route_short, routes in routes_by_short.items():
            route_entries_by_short[route_short] = []
            for idx, (route_code, destination, trip_data) in enumerate(routes):
                # Assign direction letter if multiple routes with same short code
                if len(routes) > 1:
                    direction = direction_letters[idx] if idx < len(direction_letters) else 'Z'
                    eric_str = f"{route_short}{direction}"
                else:
                    eric_str = route_short

                route_entries_by_short[route_short].append(
                    {
                        "eric": eric_str,
                        "route_code": route_code,
                        "destination": destination if destination else route_code,
                        "stops": trip_data.get("stops", []),
                    }
                )
                
                # Convert to numeric eric code (e.g., "100Y" -> "100Y" stays as string)
                # The ericcode class will handle the conversion
                self.add_terminus(
                    allexit=False,
                    eric=eric_str,
                    destination=destination if destination else route_code,
                    busfull="",
                    flip=[],
                    RTID=""
                )
        
        # Create Busstop_Stopreporter entries from all loaded stops
        autoskip_id_map = {}
        for stop_name, stop_id in omsi_map.stations:
            autoskip_id = f"{stop_id}_SKIP"
            autoskip_id_map[stop_id] = autoskip_id
            self.add_stopreporter(
                name=stop_name,
                EngDisplay=stop_name,
                ChiSeconds=0,
                EngSeconds=0,
                ManSeconds=0,
                Outbound_sectionfare=-1.0,  # Use -1 to trigger default display logic
                Inbound_sectionfare=-1.0,
                comment="",
                provided_id=stop_id
            )
            self.add_stopreporter(
                name=f"_{stop_name}",
                EngDisplay=stop_name,
                ChiSeconds=0,
                EngSeconds=0,
                ManSeconds=0,
                Outbound_sectionfare=-1.0,  # Use -1 to trigger default display logic
                Inbound_sectionfare=-1.0,
                comment="",
                provided_id=autoskip_id
            )
        self.add_stopreporter(
            name="_PleaseHoldTheHandrail_HKBTS_KMB",
            EngDisplay="PLEASE HOLD THE@HANDRAIL",
            ChiSeconds=3,
            EngSeconds=3,
            ManSeconds=0,
            Outbound_sectionfare=0.0,
            Inbound_sectionfare=0.0,
            comment="",
            provided_id="PHTH_KMB"
        )

        def _destination_suffix(destination: str) -> str:
            """Build deterministic route marker suffix, e.g. OLY/SL from destination text."""
            dest = destination.strip()
            if "_" in dest:
                dest = dest.split("_", 1)[1]
            tokens = [re.sub(r"[^A-Za-z0-9]", "", t) for t in dest.upper().split()]
            tokens = [t for t in tokens if t]
            if not tokens:
                return "DIR"
            if len(tokens) == 1:
                token = tokens[0]
                return token[:3] if len(token) >= 3 else token
            return "".join(t[0] for t in tokens[:3])

        def _expand_infosystem_stops(stop_ids: list[str]) -> tuple[list[str], list[str]]:
            """Expand each stop to _name, handrail, name triple in trip order with IDs."""
            expanded = []
            expanded_ids = []
            for stop_id in stop_ids:
                stop_name = stop_id_map.get(stop_id)
                if not stop_name:
                    continue
                expanded.append(f"_{stop_name}")
                expanded_ids.append(autoskip_id_map.get(stop_id, f"{stop_id}_SKIP"))
                expanded.append("_PleaseHoldTheHandrail_HKBTS_KMB")
                expanded_ids.append("PHTH_KMB")
                expanded.append(stop_name)
                expanded_ids.append(stop_id)
            return expanded, expanded_ids

        # Build infosystem pairs per route short code.
        for route_short, entries in route_entries_by_short.items():
            if not entries:
                continue

            first = entries[0]
            second = entries[1] if len(entries) > 1 else None

            first_suffix = _destination_suffix(first["destination"])
            first_lines = [f"~{route_short}_{first_suffix}"]
            first_ids = [""]
            first_expanded, first_expanded_ids = _expand_infosystem_stops(first["stops"])
            first_lines.extend(first_expanded)
            first_ids.extend(first_expanded_ids)
            first_lines.append(f"#{route_short}_{first_suffix}")
            first_ids.append("")
            first_lines.append("blank")
            first_ids.append("")

            if second is not None:
                second_suffix = _destination_suffix(second["destination"])
                second_lines = [f"~{route_short}_{second_suffix}"]
                second_ids = [""]
                second_expanded, second_expanded_ids = _expand_infosystem_stops(second["stops"])
                second_lines.extend(second_expanded)
                second_ids.extend(second_expanded_ids)
                second_lines.append(f"#{route_short}_{second_suffix}")
                second_ids.append("")
                second_lines.append("blank")
                second_ids.append("")
                second_destination = "blank"
            else:
                second_lines = ["blank"]
                second_ids = [""]
                second_destination = "blank"

            self.add_infosystem(
                hasid=True,
                single_or_dual_dir=second is not None,
                route=route_short,
                dir1="blank",
                dir2=second_destination,
                bustoplist1=first_lines,
                bustoplist2=second_lines,
                busstoplist1_ids=first_ids,
                busstoplist2_ids=second_ids,
            )

            # Ensure infosystem_trip eric matches assigned termini direction codes.
            current_info = self.infosystem[-1]
            current_info.trip1_class.ericcode = first["eric"]
            if second is not None:
                current_info.trip2_class.ericcode = second["eric"]
        
        # Update name and servicetrip from map metadata if available
        map_name = Path(global_cfg).parent.name
        self.name = map_name
        self.servicetrip = map_name
        
        print(f"Loaded HOF from map: {map_name}")
        print(f"  Termini (routes): {len(self.termini)}")
        print(f"  Stops: {len(self.stopreporter)}")
        print(f"  Infosystems: {len(self.infosystem)}")

        

        # print(self.showfullhof())
        # print(self.name,self.servicetrip)




class Hanover_KMB_NEW(HOF_Hanover): #UNUSED, TO BE MERGED INTO BIG CLASS LATER. WIDE ADOPTION NOT YET HAPPENED 
    Holdthehandrail = True # able to be changed by user
    HOFCLASS = HOF_Hanover
    def __init__(self, name: str = 'Default', servicetrip: str = 'Not In Service') -> None:
        self.HOFCLASS = HOF_Hanover(name, servicetrip)
