#hof editing module
import json
class hof_read:
    def __init__(self, filename):
        self.filename = filename
        self.friendlyname = ''
        self.num = 0
        self.next_line_is_the_name = False
        self.next_line_is_the_servicetrip = False
        self.servicetrip_validiacy = False
        self.servicetrip = ''
        self.list_of_dest_electronic_disps = []
        self.dist_of_dest_electronic_disps = {}
        self.valid_lines_of_addterminus = 0
        self.next_line_is_section = False
        self.commentcount = 0
        self.num_of_addterminus = 0
        self.rtno = ""

    def read_str(self, section): #only for single lined sections
        self.next_line_is_section = False
        with open(self.filename, 'r', encoding='utf-8') as f:
            hof = f.readlines()
            for i in hof:
                if i == f'{section}\n':
                    self.next_line_is_section = True
                    # print('next line is section')
                elif self.next_line_is_section:
                    value = i
                    self.next_line_is_section = False
                    break
        return value.strip('\n')
    def json_ex_pai(self,stringcount_terminus,commentcount):
        def create_list_of_dest_electronic_disps(self,stringcount_terminus,commentcount):
            list_of_dest_electronic_disps = []
            with open(self.filename, 'r', encoding='utf-8') as f:
                hof = f.readlines()
                for i in hof:
                    #print(int(int(stringcount_terminus)+1+int(commentcount)))
                    self.num += 1
                    # print(i.strip('\n'),self.num)
                    if i == '[addterminus]\n' or i == '[addterminus_allexit]\n':
                        self.num = 0
                        self.next_line_is_section = True
                        
                        self.num_of_addterminus += 1
                    if self.num == int(int(stringcount_terminus)+2+int(commentcount)) and not self.num_of_addterminus<=1:
                        self.num = 0
                        self.next_line_is_section = False
                        break
                    elif self.next_line_is_section:
                        list_of_dest_electronic_disps.append(i.strip('\n'))
            return list_of_dest_electronic_disps

        def fit_addterminus_into_dictionary(self, list_of_dest_electronic_disps):
            '''
            first value = eric code
            second value = TTDATA name
            third value = busfull name
            fourth value = fourth electronic display
            fifth value = third electronic display
            sixth value = second electronic display
            seventh value = first electronic display
            eighth value = readable eric code (comment)
            any other value after 7 = comment, will not be read by omsi
            '''
            '''
            show it like this:
            {name:TTDATA_name,properties:{
                eric_code:eric_code,
                TTData_name:TTData_name,
                busfull_name:busfull_name,
                electronic_displays:{1:1,2:2,3:3,4:4},
                readable_eric_code:readable_eric_code
                }
            }
            '''
            self.num = 0
            addterminus_count = 0
            dist_of_dest_electronic_disps = {}
            for i in list_of_dest_electronic_disps:
                
                self.num += 1
                if i == '[addterminus]' or i == '[addterminus_allexit]':
                    self.num = 0
                    self.next_line_is_section = True
                    addterminus_count += 1
                    addterminus_state = i

                if self.num == 1 and self.next_line_is_section:
                    eric_code = i
                elif self.num == 2 and self.next_line_is_section:
                    
                    entry = {}
                    entry['properties'] = {}
                    entry['properties']['eric_code'] = eric_code
                    entry['properties']['TTData_name'] = i
                    if addterminus_state == '[addterminus_allexit]':
                        entry['properties']['PassAllExit'] = True
                    else:
                        entry['properties']['PassAllExit'] = False
                    dist_of_dest_electronic_disps[f'entry_{addterminus_count - 1}'] = entry
                    dist_of_dest_electronic_disps[f'entry_{addterminus_count - 1}']['name'] = i
                elif self.num == 3 and self.next_line_is_section:
                    dist_of_dest_electronic_disps[f'entry_{addterminus_count - 1}']['properties']['busfull_name'] = i
                elif self.num == 4 and self.next_line_is_section:
                    dist_of_dest_electronic_disps[f'entry_{addterminus_count - 1}']['properties']['electronic_displays'] = {}
                    dist_of_dest_electronic_disps[f'entry_{addterminus_count - 1}']['properties']['electronic_displays'][1] = i
                elif self.num == 5 and self.next_line_is_section:
                    dist_of_dest_electronic_disps[f'entry_{addterminus_count - 1}']['properties']['electronic_displays'][2] = i
                elif self.num == 6 and self.next_line_is_section:
                    dist_of_dest_electronic_disps[f'entry_{addterminus_count - 1}']['properties']['electronic_displays'][3] = i
                elif self.num == 7 and self.next_line_is_section:
                    dist_of_dest_electronic_disps[f'entry_{addterminus_count - 1}']['properties']['electronic_displays'][4] = i
                elif self.num == 8 and self.next_line_is_section:
                    dist_of_dest_electronic_disps[f'entry_{addterminus_count - 1}']['properties']['readable_eric_code'] = i
                elif self.num > 8 and self.next_line_is_section:
                    comment_no = self.num - 8
                    dist_of_dest_electronic_disps[f'entry_{addterminus_count - 1}']['properties'][f'comment_{comment_no}'] = i
                elif self.num > 10:
                    self.next_line_is_section = False
            with open(f"{self.filename}_termini.json", "w") as outfile:
                    # write the dictionary to the file
                json.dump(dist_of_dest_electronic_disps,outfile, indent = 8)
            return dist_of_dest_electronic_disps
        self.list_of_dest_electronic_disps = create_list_of_dest_electronic_disps(self,stringcount_terminus,commentcount)
        self.dist_of_dest_electronic_disps = fit_addterminus_into_dictionary(self,self.list_of_dest_electronic_disps)
        return self.dist_of_dest_electronic_disps
    







    def json_ex_busstop(self,stringcount_busstop,commentcount):
        def create_list_of_dest_electronic_disps(self,stringcount_busstop,commentcount):
            list_of_dest_electronic_disps = []
            addterminus_count = 0
            self.next_line_is_section = False
            with open(self.filename, 'r', encoding='utf-8') as f:
                hof = f.readlines()
                for i in hof:
                    self.num += 1
                    #print(int(int(stringcount_terminus)+1+int(commentcount)))
                    # print(i.strip('\n'),self.num)
                    if i == '[addbusstop]\n':
                        self.num = 0
                        self.next_line_is_section = True
                        
                        self.num_of_addterminus += 1
                        # print('next line is section')
                    if self.num == int(int(stringcount_busstop)+2+int(commentcount)) and not self.num_of_addterminus<=1:
                        self.num = 0
                        self.next_line_is_section = False
                        break
                    elif self.next_line_is_section:
                        list_of_dest_electronic_disps.append(i.strip('\n'))
            return list_of_dest_electronic_disps
        

        def fit_addbusstop_into_dictionary(self, list_of_dest_electronic_disps):
            type_of_addbusstop = ''
            dist_of_addbusstop = {}
            saved_value_1 = ''
            saved_value_2 = ''
            saved_value_3 = ''
            saved_value_4 = ''
            addterminus_count = 0
            for i in list_of_dest_electronic_disps:
                # print(i)
                self.num += 1
                if i == '[addbusstop]':
                    self.num = 0
                    self.next_line_is_section = True
                    addterminus_count += 1
                    addterminus_state = i
                if self.num == 1 and self.next_line_is_section:
                    saved_value_1 = i
                elif self.num == 2 and self.next_line_is_section:
                    saved_value_2 = i
                elif self.num == 3 and self.next_line_is_section:
                    saved_value_3 = i
                elif self.num == 4 and self.next_line_is_section:
                    saved_value_4 = i
                    '''if int(saved_value_1[1]) == type(int) and int(saved_value_2[:-1]) == type(int) and int(saved_value_3[:-1]) == type(int):
                        type_of_addbusstop = 'DDU'
                    else:
                        type_of_addbusstop = 'BUSSTOP'''
                    # print(saved_value_1,saved_value_2,saved_value_3,saved_value_4)
                    if '@' in saved_value_2 and ('$' in saved_value_4 or '$' in i):
                        type_of_addbusstop = 'section'
                    elif ('$' in saved_value_4 or '$' in i) and '0' in saved_value_3:
                        type_of_addbusstop = 'section'
                    elif '@' in saved_value_2 and ('$' not in saved_value_4 or '$' not in i):
                        type_of_addbusstop = 'BUSSTOP'
                    elif '' == saved_value_4 or '' == i or '0' in saved_value_3:
                        type_of_addbusstop = 'BUSSTOP'
                    else:
                        type_of_addbusstop = 'DDU'
                elif self.num == 5 and self.next_line_is_section:
                    if type_of_addbusstop == 'DDU':
                        dist_of_addbusstop[f'{saved_value_1}'] = []
                        entry = {}
                        entry['properties'] = {}
                        entry['properties']['direction_y'] = saved_value_2[:-1]
                        entry['properties']['direction_z'] = saved_value_3[:-1]
                        entry['properties']['section_times_y'] = saved_value_2[-1]
                        entry['properties']['section_times_z'] = saved_value_3[-1]
                        entry['properties']['price_direction_y'] = saved_value_4
                        entry['properties']['price_direction_z'] = i
                        dist_of_addbusstop[f'{saved_value_1}'] = entry['properties']
                    elif type_of_addbusstop == 'BUSSTOP':
                        dist_of_addbusstop[f'mon_name'] = saved_value_1
                        entry = {}
                        entry['properties'] = {}
                        entry['properties']['eng mon'] = saved_value_2
                        entry['properties']['timer_1'] = saved_value_3.split(' ')[0]
                        entry['properties']['timer_2'] = saved_value_3.split(' ')[1]
                        entry['properties']['comment 1'] = saved_value_4
                        entry['properties']['comment 2'] = i
                        dist_of_addbusstop[f'{saved_value_1}'] = entry['properties']
                    elif type_of_addbusstop == 'section':
                        dist_of_addbusstop[f'mon_name'] = saved_value_1
                        entry = {}
                        entry['properties'] = {}
                        entry['properties']['eng mon'] = saved_value_2
                        entry['properties']['timer_1'] = saved_value_3.split(' ')[0]
                        entry['properties']['timer_2'] = saved_value_3.split(' ')[1]
                        entry['properties']['price_direction_y'] = saved_value_4
                        entry['properties']['price_direction_z'] = i
                        dist_of_addbusstop[f'{saved_value_1}'] = entry['properties']
                elif self.num > 7 and self.next_line_is_section:
                    self.next_line_is_section = False
            with open(f"{self.filename}_busstop.json", "w") as outfile:
                    # write the dictionary to the file
                json.dump(dist_of_addbusstop,outfile, indent = 8)
            return dist_of_addbusstop
        self.list_of_dest_electronic_disps = create_list_of_dest_electronic_disps(self,stringcount_busstop,commentcount)
        # print(self.list_of_dest_electronic_disps)

        self.dist_of_dest_electronic_disps = fit_addbusstop_into_dictionary(self,self.list_of_dest_electronic_disps)
        return self.dist_of_dest_electronic_disps
    def extract_infosystem_busstop_list(self):
        hoflines = open(self.filename, 'r', encoding='utf-8').readlines()
        busstop_list = []
        direction_Y = []
        direction_Z = []
        num = 0
        numberofstops = 0
        next_line_is_section = False
        for i in hoflines:
            num +=1
            print(num,i)
            if i == "[infosystem_busstop_list]\n":
                next_line_is_section = True
                num = 300
                continue
            if next_line_is_section:
                numberofstops = i.strip('\n')
                numberofstops = int(numberofstops)
                next_line_is_section = False
            if num == 302:
                self.rtno = i.strip('\n')
                numberofstops -=1
            #302 + numberofstops == end
            if num >=303 and num < (303 + numberofstops):
                busstop_list.append(i)
            if num >= (303 + numberofstops):
                num = 1000
                
                if direction_Y == []:
                    direction_Y = busstop_list
                    print(direction_Y,busstop_list)
                    busstop_list = []
                else:
                    direction_Z = busstop_list
                    print(direction_Z,busstop_list)
                    busstop_list = []
        #     {
        #     "busstoplist": { 
        #         "bus_rtno": "bus_rtno",
        #         "busstoplist_Y": [],
        #         "busstoplist_Z": []
        #     }
        busstop_dict = {}
        busstop_dict['bus_rtno'] = self.rtno
        busstop_dict['busstoplist_Y'] = direction_Y
        busstop_dict['busstoplist_Z'] = direction_Z
        with open(f"{self.filename}_busstoplist.json", "w") as outfile:
            # write the dictionary to the file
            json.dump(busstop_dict,outfile, indent = 8)


    # def infobustop_tojson(self,busstop_list):
    #     '''
    #     {
    #     "busstoplist": { 
    #         "bus_rtno": "bus_rtno",
    #         "busstoplist": []
    #     }
        
    #     '''

    #     return busstop_dict


        

        
    
if __name__ == "__main__" and len(sys.argv) == 2:
    hof = hof_read(sys.argv[1])
    hof.json_ex_pai(hof.read_str("stringcount_terminus"), "2")
    hof.json_ex_busstop(hof.read_str("stringcount_busstop"), "3")
    hof.extract_infosystem_busstop_list()








                



    
