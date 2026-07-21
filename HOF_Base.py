from string import Template
from types import GeneratorType
import sqlite3
import sys
import os
        
class ericcode:
    mapping = {'a': 11, 'b': 12, 'c':13,'d':21,'e':22,'f':23,'g':31,'h':32,'i':33,'j':41,'k':42,'l':43,'m':51,'n':52,'o':53,'p':61,'q':62,'r':63,'s':71,'t':72,'u':73,'v':81,'w':82,'x':83,'y':91,'z':92,'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
    def retstr(self) -> str:
        returnstring = ''.join(self.eric)
        if len(returnstring) < 6:
            returnstring = returnstring + '0'
        return returnstring
    def __init__(self, code: str) -> None:
        self.eric = map(str,[self.mapping[c] for c in (code.lower() if isinstance(code, str) else str(code))])
    def __len__(self) -> int:
        return len(''.join(self.eric))
    def __str__(self) -> str:
        returnstring = ''.join(self.eric)
        if len(returnstring) < 6:
            returnstring = returnstring + '0'
        return returnstring
    def __int__(self) -> int:
        return int(str(self.retstr()))
class gorbacode:
    mapping = {'a': 11, 'b': 12, 'c':13,'d':21,'e':22,'f':23,'g':31,'h':32,'i':33,'j':41,'k':42,'l':43,'m':51,'n':52,'o':53,'p':61,'q':62,'r':63,'s':71,'t':72,'u':73,'v':81,'w':82,'x':83,'y':91,'z':92,'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
    def __init__(self) -> None:
        raise NotImplementedError("Gorba code is not implemented yet")
    '''
    I dont know what code gorba uses, so I will leave this empty for now
    '''


class HOF_Hanover:
    name = 'Default'
    servicetrip = 'Not In Service'
    ddu : list['Busstop_DDU'] = []
    stopreporter : list['Busstop_Stopreporter'] = []
    termini : list['Termini'] = []
    infosystem : list['Infosystem'] = []
    ddu_expected_keys_set = {'RTNO', 'Outbound_dir', 'Inbound_dir', 'Outbound_price', 'Inbound_price', 'sectiontimes_Y', 'sectiontimes_Z'}
    # ddu_exp_k_datatypes = [str,str,str,float,float,int,int]
    ddu_exp_k_datatypes = ["TEXT","TEXT","TEXT","REAL","REAL","INTEGER","INTEGER"]
    
    stopreporter_expected_keys_set = {'name', 'EngDisplay', 'ChiSeconds', 'EngSeconds', 'Outbound_sectionfare', 'Inbound_sectionfare', 'comment'}
    # stopreporter_exp_k_datatypes = [str,str,int,int,float,float,str]
    stopreporter_exp_k_datatypes = ["TEXT","TEXT","INTEGER","INTEGER","REAL","REAL","TEXT"]
    
    termini_expected_keys_set = {'allexit', 'eric', 'destination', 'busfull', 'flip', 'RTID'}
    # termini_exp_k_datatypes = [bool,str,str,str,str,str]
    termini_exp_k_datatypes = ["BOOL","TEXT","TEXT","TEXT","TEXT","TEXT"]
    
    infosystem_expected_keys_set = {'single_or_dual_dir', 'route', 'dir1', 'dir2', 'bustoplist1', 'bustoplist2'}
    # infosystem_exp_k_datatypes = [bool,str,str,str,str,str]
    infosystem_exp_k_datatypes = ["BOOL","TEXT","TEXT","TEXT","TEXT","TEXT"]
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
$ChiSeconds $EngSeconds
$Outbound_sectionfare
$Inbound_sectionfare
.........................$comment
''')
    ddu_template = Template('''[addbusstop]
$RTNO
$Outbound_dir \t\t$sectiontimes_Y
$Inbound_dir \t\t$sectiontimes_Z
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
    def __init__(self,name:str='Default',servicetrip:str='Not In Service') -> None:
        self.name = name
        self.servicetrip = servicetrip


    class Termini:
        def __init__(self,allexit:bool = False, eric: str = "", destination: str = '', busfull: str = '', flip: list[str] = [], RTID: str = '') -> None: #flip is a list of strings, eric will be inputted as '289XZ' and converted to 2899192
            self._allexit = '_allexit' if allexit else ''
            self._eric = eric
            self._destination = destination
            self._busfull = busfull
            self._flip = flip
            self._flup4 = flip[3] if len(flip) > 3 else ''
            self._flup3 = flip[2] if len(flip) > 2 else ''
            self._flup2 = flip[1] if len(flip) > 1 else ''
            self._flup1 = flip[0] if len(flip) > 0 else ''
            self._RTID = RTID

        @property
        def eric(self) -> str:
            return str(self._eric)
        @eric.setter
        def eric(self, value: str) -> None:
            self._eric = str(ericcode(value))
            self._RTID = value[:3]
        @property
        def RTID(self) -> str:
            return str(self._RTID)
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
            return HOF_Hanover.termini_template.substitute(allexit=self._allexit, eric=self._eric, destination=self._destination, busfull=self._busfull, pai_page4 = self._flup4, pai_page3 = self._flup3, pai_page2 = self._flup2,pai_page1 = self._flup1,RTID=self._RTID)

    class Busstop_Stopreporter:
        def __init__(self, name:str = '',EngDisplay:str = '',ChiSeconds:int = 0,EngSeconds:int = 0,Outbound_sectionfare:float = 0.0,Inbound_sectionfare:float = 0.0,comment: str = '') -> None:
            self._name = name
            self._EngDisplay = EngDisplay
            self._ChiSeconds = str(ChiSeconds).rjust(2,'0')
            self._EngSeconds = str(EngSeconds).rjust(2,'0')
            self._Outbound_sectionfare = f"${Outbound_sectionfare:.1f}" if isinstance(Outbound_sectionfare,float) and Outbound_sectionfare != -1.0 else comment if comment != '' else name
            self._Inbound_sectionfare = f"${Inbound_sectionfare:.1f}" if isinstance(Inbound_sectionfare,float) and Inbound_sectionfare != -1.0 else comment if comment != '' else name
            self._Autoskip = False
            self._pages = 1
            self._engscroll = self._EngDisplay.count('@') // 2
            self._comment = comment


        @property
        def name(self) -> str:
            return self._name

        @name.setter
        def name(self, value: str) -> None:
            modified_name = value
            if self._engscroll > 2 and not modified_name[-1] == '!':
                modified_name += "!"
            if self._pages == 2 and not (modified_name[0:1] == '!' or modified_name[0:2] == '_!'):
                modified_name = '!' + modified_name
            if self._pages == 3 and not (modified_name[0:2] == '!!' or modified_name[0:3] == '_!!'):
                modified_name = '!' + modified_name
            if self._Autoskip and not modified_name[-1] == '_':
                modified_name += "_"
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
        def Outbound_sectionfare(self) -> float | str:
            return float(self._Outbound_sectionfare.strip('$')) if self._Outbound_sectionfare.lstrip("$").replace(".","").isnumeric() else self._name

        @Outbound_sectionfare.setter
        def Outbound_sectionfare(self, value: float) -> None:
            self._Outbound_sectionfare = f"${value:.1f}" if value != -1.0 else self._name

        @property
        def Inbound_sectionfare(self) -> float | str:
            return float(self._Inbound_sectionfare.strip('$')) if self._Inbound_sectionfare.lstrip("$").replace(".","").isnumeric() else self._name

        @Inbound_sectionfare.setter
        def Inbound_sectionfare(self, value: float) -> None:
            self._Inbound_sectionfare = f"${value:.1f}" if value != -1.0 else self._name
        def __str__(self) -> str:
            return HOF_Hanover.stopreporter_template.substitute(name=self._name, EngDisplay=self._EngDisplay, ChiSeconds=self._ChiSeconds, EngSeconds=self._EngSeconds, Outbound_sectionfare=self._Outbound_sectionfare, Inbound_sectionfare=self._Inbound_sectionfare,comment=self._comment)
        
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
            def __init__(self,bus_stops:list[str] = [],rtno:str = '') -> None:
                self._busstops = bus_stops
                self._rtno = rtno
                self._amount_of_stops = len(bus_stops)
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
            def __str__(self) -> str:
                return HOF_Hanover.busstop_list_template.substitute(amount_of_stops=self._amount_of_stops + 1, rtno=self._rtno, busstops=self.busstops)
            def __repr__(self) -> list[int | str | list[str]]:
                return [self._amount_of_stops, self._rtno, self._busstops]
            def __iter__(self) -> list[str]:
                return self._busstops


        def __init__(self,single_or_dual_dir:bool = True,route:str='',dir1:str='',dir2:str='',bustoplist1:list[str]=[],bustoplist2:list[str]=[]) -> None: 
            #route must be inputted as '289X', we will automaticllu add Y and Z at the end
            #single_or_dual_dir with True being dual direction and False being single direction
            self._single_or_dual_dir = single_or_dual_dir
            self._trip1 = self.trip(f"{route}Y",dir1,route)
            self._trip2 = self.trip(f"{route}Z",dir2,route)
            
            self._busstop_list1 = self.busstop_list(bustoplist1,route)
            self._busstop_list2 = self.busstop_list(bustoplist2,route)
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
    def add_stopreporter(self, name:str = '',EngDisplay:str = '',ChiSeconds:int = 0,EngSeconds:int = 0,Outbound_sectionfare:float = 0.0,Inbound_sectionfare:float = 0.0,comment:str = "") -> None:
        self.stopreporter.append(self.Busstop_Stopreporter(name,EngDisplay,ChiSeconds,EngSeconds,Outbound_sectionfare,Inbound_sectionfare,comment))
    def add_terminus(self,allexit:bool = False, eric: str = '', destination: str = '', busfull: str = '', flip: list[str] = [], RTID: str = '') -> None:
        self.termini.append(self.Termini(allexit, eric, destination, busfull, flip, RTID))
    # def add_infosystem(self,eric:str =  '',Destination:str = '',RouteNo:str = '') -> None:
    #     self.infosystem.append(self.Infosystem.trip(eric,Destination,RouteNo))
    # def add_busstop_list(self,bus_stops:list[str] = [],rtno:str = '') -> None:
    #     self.infosystem.append(self.Infosystem.busstop_list(bus_stops,rtno))
    def add_infosystem(self,single_or_dual_dir:bool,route:str='',dir1:str='',dir2:str='',bustoplist1:list[str]=[],bustoplist2:list[str]=[]) -> None:
        self.infosystem.append(self.Infosystem(single_or_dual_dir,route,dir1,dir2,bustoplist1,bustoplist2))
    def showfullhof(self) -> str:
        returnstring = '\n'.join([''.join(self.header_template.substitute(name = self.name,servicetrip = self.servicetrip)),'\n'.join((str(i) for i in self.termini)),'\n'.join(str(i) for i in self.ddu),'\n'.join((str(i) for i in self.stopreporter)),'\n'.join((str(i) for i in self.infosystem))])
        return returnstring
    def export_hof(self, filename: str) -> None:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            f.write(self.showfullhof())
            print(f"Exported to {filename}, all comments have been destroyed.")
    def save_to_db(self, filename: str) -> None:
        database_file = sqlite3.connect(f'{filename}')
        c = database_file.cursor()
        c.execute(f'''CREATE TABLE IF NOT EXISTS ddu (
                RTNO TEXT, Outbound_dir TEXT, Inbound_dir TEXT,
                Outbound_price REAL, Inbound_price REAL,
                sectiontimes_Y INTEGER, sectiontimes_Z INTEGER)''')
        c.execute(f'''CREATE TABLE IF NOT EXISTS stopreporter (
                name TEXT, EngDisplay TEXT, ChiSeconds INTEGER,
                EngSeconds INTEGER, Outbound_sectionfare REAL,
                Inbound_sectionfare REAL, comment TEXT)''')
        c.execute(f'''CREATE TABLE IF NOT EXISTS termini (
                allexit BOOL, eric TEXT, destination TEXT, busfull TEXT,
                flip4 TEXT, flip3 TEXT, flip2 TEXT, flip1 TEXT, RTID TEXT)''')
        c.execute(f'''CREATE TABLE IF NOT EXISTS infosystem (
                single_or_dual_dir BOOL, route TEXT,
                dir1 TEXT, dir2 TEXT, bustoplist1 TEXT, bustoplist2 TEXT)''')
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
        c.executemany('INSERT INTO stopreporter VALUES (?,?,?,?,?,?,?)', [(i.name, i.EngDisplay, i.ChiSeconds, i.EngSeconds, i.Outbound_sectionfare, i.Inbound_sectionfare, i.comment) for i in self.stopreporter])
        c.executemany('INSERT INTO termini VALUES (?,?,?,?,?,?,?,?,?)', [(i.allexit, i.eric, i.destination, i.busfull, i.flip[3] if len(i.flip) > 3 else '', i.flip[2] if len(i.flip) > 2 else '', i.flip[1] if len(i.flip) > 1 else '', i.flip[0] if len(i.flip) > 0 else '', i.RTID) for i in self.termini])
        c.executemany('INSERT INTO infosystem VALUES (?,?,?,?,?,?)', [(i.single_or_dual_dir, i.route, i.direction1, i.direction2, str(i.busstop_list1_class.db_export), str(i.busstop_list2_class.db_export)) for i in self.infosystem])

        database_file.commit()
        database_file.close()

        print(f"Saved to {filename}")

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
        self.stopreporter = [self.Busstop_Stopreporter(*i) for i in c.fetchall()]
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
            ls[index][4] = ls[index][4][1:-1].replace("'","").split(', ')
            ls[index][5] = ls[index][5][1:-1].replace("'","").split(', ')
        self.infosystem = [self.Infosystem(*i) for i in ls]
        database_file.close()
        print(f"Loaded from {filename}")

    def load_from_hof(self, filename: str) -> None:
        try:
            hof_entry = HOF_Hanover()
            with open(filename, 'r',encoding="utf-8") as f:
                lines = [line.strip() for line in f]
            i = 0
            while i < len(lines):
                line = lines[i]
                if line == "[name]":
                    hof_entry.name = lines[i + 1]
                    i += 2
                elif line == "[servicetrip]":
                    hof_entry.servicetrip = lines[i + 1]
                    i += 2
                elif line == "[addterminus]":
                    # param = lines[i].replace("[addterminus]", "").strip()
                    hof_entry.add_terminus(
                        False,
                        lines[i + 1],
                        lines[i + 2],
                        lines[i + 3],
                        lines[i + 4 : i + 8][::-1],
                        lines[i + 8]
                    )
                    i += 9
                elif line == "[addterminus_allexit]":
                    hof_entry.add_terminus(
                        True,
                        lines[i + 1],
                        lines[i + 2],
                        lines[i + 3],
                        lines[i + 4 : i + 8][::-1],
                        lines[i + 8]
                    )
                    i += 9
                elif line == "[addbusstop]":
                    # print(len(lines[i + 1]), len(lines[i + 3]),lines[i + 3],lines[i + 1])
                    stop_name = lines[i + 1]
                    if len(stop_name) < 1:
                        i +=1
                        continue
                    if len(stop_name) >= 5 or (len(time_parts := lines[i + 3].split()) <= 2 and time_parts[0].isdigit()):
                        # parse full stopreporter
                        chi_sec, eng_sec = 0, 0
                        time_parts = lines[i + 3].split()
                        if len(time_parts) >= 1:
                            chi_sec = int(time_parts[0])
                        if len(time_parts) >= 2 and time_parts[1].isdigit():
                            eng_sec = int(time_parts[1])
                        inbound_price = -1.0
                        if lines[i + 4].startswith('$'):
                            inbound_price = float(lines[i + 4].lstrip('$'))
                            # print(inbound_price)
                        outbound_price = -1.0
                        if lines[i + 5].startswith('$'):
                            outbound_price = float(lines[i + 5].lstrip('$'))
                            # print("op",outbound_price)
                        hof_entry.add_stopreporter(
                            stop_name,
                            lines[i + 2],
                            chi_sec,
                            eng_sec,
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
                        sectiontimes_Y = int(lines[i + 2][-1])
                        sectiontimes_Z = int(lines[i + 3][-1])
                        inbound_price = float(lines[i + 4].lstrip('$')) if lines[i + 4].startswith('$') else 0.0
                        outbound_price = float(lines[i + 5].lstrip('$')) if lines[i + 5].startswith('$') else 0.0
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
                        endidx = startidx + int(lines[i + 1])
                        # print(lines[startidx:endidx])
                        self.infosystem[-1].busstop_list2_class.busstops = lines[startidx:endidx]
                        self.infosystem[-1].busstop_list2 = lines[startidx:endidx]
                        self.infosystem[-1]._busstop_list2._busstops= lines[startidx:endidx]
                        # print(self.infosystem[-1].busstop_list2_class.db_export)
                        
                        self.infosystem[-1].trip2_class.Destination = lines[startidx:endidx][-2] if len(lines[startidx:endidx]) > 1 else ""
                        i = endidx
                    else:
                        busstop_count_1 = int(lines[i + 1])
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
        print(f"Loaded from {filename}")

    def new_from_map(self, map_location: str) -> None:
        # self.name = mapname
        # self.servicetrip = mapname
        # file_ls = os.listdir(f"{map_location}\\TTData") #Please give map location as a folder
        # files_pending = [i for i in file_ls if i.endswith('.ttp')]
        # seta = set()
        # route_sets = set()
        # for i in files_pending:
        #     stations = []
        #     with open(f"{map_location}\\TTData\\{i}", 'r',encoding="utf-8") as f:
        #         lines = [line.strip() for line in f]
        #     for index,line in enumerate(lines):
        #         if line == '[trip]':
        #             trip = lines[index+1]
        #             termini = lines[index+2]
        #             rtno = lines[index+3]
        #         if line == '[station]':
        #             stations.append(f"_{lines[index+3]}")
        #             stations.append(f"_PleaseHoldTheHandrail_HKBTS_KMB")
        #             stations.append(f"{lines[index+3]}")
        #     seta.add((rtno,termini,tuple(stations)))
        # files_pending = [i for i in file_ls if i.endswith('.ttc')]
        raise NotImplementedError("Map loading not able to be implemented.")
        # print(seta)
        

        # print(self.showfullhof())
        # print(self.name,self.servicetrip)




class Hanover_KMB_NEW(HOF_Hanover):
    Holdthehandrail = True # able to be changed by user
    HOFCLASS = HOF_Hanover
    def __init__(self, name: str = 'Default', servicetrip: str = 'Not In Service') -> None:
        self.HOFCLASS = HOF_Hanover(name, servicetrip)
