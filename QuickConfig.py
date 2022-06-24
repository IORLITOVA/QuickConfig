import serial
from serial.tools import list_ports
import os

#path = os.getcwd()
#print('PWD',path)
# /Users/mbp/Documents/my-project/python-snippets/notebook

# Open files for reading commands and for writing log
file_input_config = open("C:\\Users\\IOA\\QuickConf-DockLight\\QuickConfig_Input_IOA.dat", "r")
file_log = open("C:\\Users\\IOA\\QuickConf-DockLight\\log_IOA.txt", "w")

#Number of terminals present in the setup
n_terminals = 4

# Define ports 
PortConfigurator = 'COM4'
PortESG = 'COM8'

ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))

#print(serial.tools.list_ports())

#ser = serial.Serial(port = 'COM4',baudrate =115200,parity = 'N',bytesize=8,ser.stopbits=1)
ser = serial.Serial()
ser.baudrate =115200
ser.port = PortConfigurator
#ser.port = 'COM6'
ser.parity = 'N' 
ser.bytesize=8
ser.stopbits=1
ser.timeout=1 # To prevent it from hanging (waiting too long for an answer)
ser.xonxoff = False  # We do not have control of it, therefore we switch it off

# Open port for Configurator
ser.open()
print(ser.is_open)
print(ser.name)

file_log.write('=============== Port ' + PortConfigurator + ' open =============== \n')

# Function for sending and receiving quick configuration commands via serial port, and write output in a log file
def SendCommands(listtosend,listtosend_names):
    commands_tosend = listtosend
    commands_tosend_names = listtosend_names
    ser.send_break(duration=0.25)
    for icommand, command_tosend in enumerate(commands_tosend):
        command_tosend_bytes = bytes.fromhex(command_tosend)
        #print("bytes object created using fromhex():")
        #print('cmd sent',command_tosend_bytes)
        #Send to serial port and read the answer
        ser.write(command_tosend_bytes)
        answer = ser.readline()
        ##answer = ser.read(ser.in_waiting) 
        #print ('answer',answer) 
        answer_string = answer.decode('utf-8')
        file_log.write(listtosend_names[icommand] + ' --- '+ command_tosend_bytes[0:24].decode('ascii')+"\n")
        #file_log.write(command_tosend_bytes[0:10].decode('ascii'))
        file_log.write(answer_string)
    return 


# Data - commands to be sent via serial port 
command_list = file_input_config.readlines()
#print(command_list)

command_names = []
commands = []

for line in command_list: 
        command_name = line.split(': ')[0]
        command_hex = line.split(': ')[1].split('\n')[0]
        print(command_name)
        print(command_hex)
        
        command_names.append(command_name)
        commands.append(command_hex)

print("ALL COMMANDS",command_names)

bridge_commandnames = command_names[0:4]
bridge_commands = commands[0:4]
#print(bridge_commandnames)

freq_commandnames = command_names[4:12]
freq_commands = commands[4:12]
#print(freq_commandnames)

quickset_status_commandnames = command_names[12:14]
quickset_status_commands = commands[12:14]
#print(quickset_status_commandnames)

quickset_rad_commandnames = command_names[14:18]
quickset_rad_commands = commands[14:18]
#print(quickset_rad_commandnames)

quickset_std_commandnames = command_names[18:22]
quickset_std_commands = commands[18:22]
#print(quickset_std_commandnames)

quickset_name_commandnames = command_names[22:26]
quickset_name_commands = commands[22:26]
#print(quickset_name_commandnames)

esg_rad_std_name_commandnames = command_names[26:29]
esg_rad_std_name_commands = commands[26:29]
#print(esg_rad_std_name_commandnames)


# Reset all before configuration: 
#command_for_reset = 

#ser.write(b'TST::MODE::TEST\r')
#print(ser.readline())

# Quick configuration of terminals: 
for slot in range(n_terminals):
    slot_commandnames = [bridge_commandnames[slot],\
                      quickset_status_commandnames[0],\
                      quickset_rad_commandnames[slot],\
                      *freq_commandnames,\
                      quickset_std_commandnames[slot],\
                      quickset_name_commandnames[slot],\
                      quickset_status_commandnames[1] \
                      ]


    slot_commands      = [bridge_commands[slot],\
                      quickset_status_commands[0],\
                      quickset_rad_commands[slot],\
                      *freq_commands,\
                      quickset_std_commands[slot],\
                      quickset_name_commands[slot],\
                      quickset_status_commands[1] \
                      ]

    #print(slot_commandnames)

    file_log.write('---------------   SLOT ' + str(slot+1) + ' ----------------- \n')

    # Configure terminals    
    SendCommands(slot_commands,slot_commandnames)
    

# Close port for terminals 
ser.close()
file_log.write('=============== Port ' + PortConfigurator + ' closed =============== \n')
    

# Open port for ESG, do the configs
ser.port = PortESG
ser.open()
file_log.write('=============== Port ' + PortESG + ' open =============== \n')

print("SETTINGS: ",ser.get_settings())

esg_commandnames = [quickset_status_commandnames[0],\
                    esg_rad_std_name_commandnames[0],\
                    *freq_commandnames,\
                    esg_rad_std_name_commandnames[1],\
                    esg_rad_std_name_commandnames[2],\
                    quickset_status_commandnames[1]\
                   ]

esg_commands = [quickset_status_commands[0], \
                    esg_rad_std_name_commands[0], \
                    *freq_commands,\
                    esg_rad_std_name_commands[1], \
                    esg_rad_std_name_commands[2], \
                    quickset_status_commands[1] \
                ]
print('ESG----------',esg_commandnames)

file_log.write('---------------   ESG  ----------------- \n')

SendCommands(esg_commands,esg_commandnames)




        
#tosend = "CFG::SLOT::01;115200;N\x0D"
#tosend = "43 46 47 3A 3A 53 4C 4F 54 3A 3A 30 31 3B 31 31 35 32 30 30 3B 4E 0D" #bridge slot 01
#tosend = "54 53 54 3C 43 46 47 3A 33 35 3A 51 55 49 43 4B 53 45 54 3A 52 41 57 3A 02 6B 02 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0D 0A" #Quickset status 0
#tosend = "54 53 54 3C 43 46 47 3A 33 35 3A 51 55 49 43 4B 53 45 54 3A 52 41 57 3A 32 87 02 04 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0D 0A" #Quickset status 1
#tosend = "54 53 54 3C 43 46 47 3A 36 33 3A 51 55 49 43 4B 53 45 54 3A 52 41 57 3A BA CC 02 02 00 00 41 00 00 00 02 02 00 04 04 01 05 00 00 00 00 01 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0D 0A" Quickset RAD Slot1
#tosend = "54 53 54 3C 43 46 47 3A 39 31 3A 51 55 49 43 4B 53 45 54 3A 52 41 57 3A 18 DF 02 03 00 00 B2 E0 21 B5 7C 4D FA 25 38 72 20 4A AF 56 41 FD 41 75 74 6F 6D 61 74 69 63 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 04 02 04 02 00 03 01 00 FF 7F 00 00 00 00 02 00 00 00 00 00 00 00 00 00 0D 0A" #Quickset STD Slot1
#tosend = "54 53 54 3C 43 46 47 3A 3A 55 4E 41 4D 45 3A 3A 43 2E 20 52 45 46 0D 0A" #Quickset NAME Slot1

#qso = bytes.fromhex(tosend)
#print("bytes object created using fromhex():")
#print(qso)


#ser.write(qso)
#ans = ser.read(20)
#ans = ser.readline()
#ans = ser.read(ser.in_waiting) 
#print('ans',ans)
#ans_string = ans.decode('utf-8')
#file_log.write(ans_string)


# Close port

#print(ser.is_open)

ser.close()
file_log.write(' ===============  Port ' + PortESG + ' closed =============== \n')

file_input_config.close()
file_log.close()