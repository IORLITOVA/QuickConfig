import json

class SerialCommands:
    def __init__(self, filename):
        json_filename     = filename 
        path_to_directory = "C:\\WORK\\QuickConfig\\"
        path_to_file      = path_to_directory + json_filename 

        f = open(path_to_file)
        self.data = json.load(f)
        f.close()

    def commands_dict(self,keyword):
        qc_commands_dict = self.data[keyword]
        return qc_commands_dict

    def commands(self,keyword):
        print(keyword)
        qc_commands = [k for k in self.data[keyword].values()]
        return qc_commands

    def command_names(self,keyword):
        qc_command_names = [v for v in self.data[keyword].keys()]
        return qc_command_names 

     
    def queue_qc(self,slot):
        status = self.commands_dict('STATUS') 
        rad    = self.commands_dict('RAD')['RAD'+str(slot+1)]
        freq   = self.commands('FREQ')
        #print('freq',freq)
        std    = self.commands_dict('STD')['STD'+str(slot+1)]
        name   = self.commands_dict('NAME')['NAME'+str(slot+1)]

         
        q = [status['STATUS0'],
             rad,
             *freq,
             std,
             name,
             status['STATUS1']
        ]
        return q
    
    '''
    def queue_qc_names(self,slot):
        status = self.commands_dict('STATUS').keys() 
        rad    = self.commands_dict('RAD')['RAD'+str(slot+1)]
        freq   = self.commands('FREQ')
        #print('freq',freq)
        std    = self.commands_dict('STD')['STD'+str(slot+1)]
        name   = self.commands_dict('NAME')['NAME'+str(slot+1)]

         
        q = [status['STATUS0'],
             rad[slot],
             *freq,
             std[slot],
             name[slot],
             status['STATUS1']
        ]
        return q  
    '''

    def queue_qc_esg(self):
        status = self.commands_dict('STATUS') 
        rad    = self.commands_dict('RAD')['ESG_RAD']
        freq   = self.commands('FREQ')
        #print('freq',freq)
        std    = self.commands_dict('STD')['ESG_STD']
        name   = self.commands_dict('NAME')['ESG_NAME']

        q = [status['STATUS0'],
             rad,
             *freq,
             std,
             name,
             status['STATUS1']
        ]
        return q


    def queue_raz(self):
        mode = self.commands_dict('MODE')
        raz  = self.commands_dict('RAZ')   
    
        q = [mode['MODE_TEST'],
             raz['RAZ'],
             mode['MODE_NORMAL']
        ]
        return q




       





