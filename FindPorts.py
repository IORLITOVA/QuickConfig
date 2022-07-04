import serial
from serial.tools import list_ports

import json

class Ports:
    def __init__(self, filename):
        json_filename     = filename 
        path_to_directory = "C:\\WORK\\QuickConfig\\"
        path_to_file      = path_to_directory + json_filename 

        f = open(path_to_file)
        self.data = json.load(f)
        f.close()

    def port_config(self):
        config_name = self.data["Ports"]["Configurator"]
        print(config_name)
        return config_name

    def port_esg(self):
        esg_name = self.data["Ports"]["ESG"]
        print(esg_name)
        return esg_name

    def find_port(self,name):
        ports = serial.tools.list_ports.grep(name)
        for port in ports :
            portname = port.name   
        return portname

