
import serial
from serial.tools import list_ports
import os
import time

# Open files for reading commands and for writing log
file_input_config = open("C:\\WORK\\QuickConfig\\QuickConfig_Input.dat", "r")
file_log = open("C:\\WORK\\QuickConfig\\log_IOA_1stversion.txt", "w")

#Number of terminals present in the setup
n_terminals = 4

# Define ports 
#PortConfigurator = 'COM4'
#PortESG = 'COM9'

portnames = []
ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
        portnames.append(port + desc + hwid)


#PortConfiguratorString = 'Silicon'
#PortESGString = 'Périphérique série'

PortConfigurator = ''
PortESG = ''


ports = serial.tools.list_ports.grep('Silicon')
for port in ports :
    print('Name Silicon',port.name)
    PortConfigurator = port.name   


ports = serial.tools.list_ports.grep('Périphérique')
for port in ports :
    print('Name Periph',port.name)
    PortESG = port.name
       

ser = serial.Serial()
ser.baudrate =115200
ser.port = PortConfigurator
ser.parity = 'N' 
ser.bytesize=8
ser.stopbits=1
ser.timeout=1 # To prevent it from hanging (waiting too long for an answer)
ser.xonxoff = False  # We do not have control of it, therefore we switch it off


# Open port for Configurator
if ser.is_open :
    ser.close()

ser.open()
print(ser.is_open)
print(ser.name)
print("SETTINGS: ",ser.get_settings())

ser.flushInput()
ser.flushOutput()

file_log.write('=============== Port ' + PortConfigurator + ' open =============== \n')

# Function for sending and receiving quick configuration commands via serial port, and write output in a log file
def SendCommands(listtosend,listtosend_names):
    commands_tosend = listtosend
    commands_tosend_names = listtosend_names
    for icommand, command_tosend in enumerate(commands_tosend):
        command_tosend_bytes = bytes.fromhex(command_tosend)
        #Send to serial port and read the answer
        ser.write(command_tosend_bytes)
        answer = ser.readline()
        ##answer = ser.read(ser.in_waiting) 
        answer_string = answer.decode('utf-8')
        file_log.write('Command : ' + listtosend_names[icommand] + ' --- '+ command_tosend_bytes[0:24].decode('ascii')+"... etc.  \n")
        file_log.write('Answer: ' + answer_string + "\n\n")

        #if icommand == 0:
        #   ser.send_break(duration=0.25) 
    return 


# Data - commands to be sent via serial port 
command_list = file_input_config.readlines()

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

restoreparams_commandnames = ['Mode Test', 'Raz Param', 'Mode Normal']
restoreparams_commands = [b'TST::MODE::TEST\r', b'TST<CFG::RAZ::PARAM\r',b'TST::MODE::NORMAL\r']

resetsave_commandnames = ['Reset Save']
resetsave_commands = [b'TST::RST::SAVE\r']

audiomode_commandnames = ['Mode audio']
audiomode_commands = [b'TST<CFG::MODE::AUDIO\r']

bridge_commandnames = command_names[0:4]
bridge_commands = commands[0:4]

freq_commandnames = command_names[4:12]
freq_commands = commands[4:12]

quickset_status_commandnames = command_names[12:14]
quickset_status_commands = commands[12:14]

quickset_rad_commandnames = command_names[14:18]
quickset_rad_commands = commands[14:18]

quickset_std_commandnames = command_names[18:22]
quickset_std_commands = commands[18:22]

quickset_name_commandnames = command_names[22:26]
quickset_name_commands = commands[22:26]

esg_rad_std_name_commandnames = command_names[26:29]
esg_rad_std_name_commands = commands[26:29]





# Quick configuration of each terminal: 
for slot in range(n_terminals):
    slot_commandnames = [#bridge_commandnames[slot],\
                      #restoreparams_commandnames,\
                      quickset_status_commandnames[0],\
                      quickset_rad_commandnames[slot],\
                      *freq_commandnames,\
                      quickset_std_commandnames[slot],\
                      quickset_name_commandnames[slot],\
                      quickset_status_commandnames[1], \
                      #resetsave_commandnames,\
                      #audiomode_commandnames \
                      ]


    slot_commands      = [#bridge_commands[slot],\
                      #restoreparams_commands,\
                      quickset_status_commands[0],\
                      quickset_rad_commands[slot],\
                      *freq_commands,\
                      quickset_std_commands[slot],\
                      quickset_name_commands[slot],\
                      quickset_status_commands[1],\
                      #resetsave_commands,\
                      #audiomode_commands \
                      ]

    

    file_log.write('---------------   SLOT ' + str(slot+1) + ' ----------------- \n')

    # Configure terminals 
    # Break before bridge, otherwise no answer from bridge command
    ser.send_break(duration=0.25)

    # Bridge
    command_tosend = bridge_commands[slot] 
    command_tosend_bytes = bytes.fromhex(command_tosend)
    ser.write(command_tosend_bytes)
    answer = ser.readline()
    answer_string = answer[:20].decode('utf-8')
    file_log.write('Command : ' + bridge_commandnames[slot] +"\n")
    file_log.write('Answer: ' + answer_string + "\n")

    # Break after bridge, otherwise 1st command after bridge does not answer
    ser.send_break(duration=0.25) 
    
    for icommand, command_tosend in enumerate(restoreparams_commands):
        ser.write(command_tosend)
        answer = ser.readline()
        answer_string = answer.decode('utf-8')
        file_log.write('Command : ' + restoreparams_commandnames[icommand] +"\n")
        file_log.write('Answer: ' + answer_string + "\n")    
    

    SendCommands(slot_commands,slot_commandnames)
    
    end_of_resetsave = 'CFG<TST::SN::'

    ser.write(resetsave_commands[0])
    ser.timeout = 2
    
    
    for i in range(6):
      answer = ser.readline()
      answer_string = answer[0:18].decode('utf-8')
      print(answer_string)
      file_log.write('Answer: ' + answer_string + "\n")
      # Do NOT do WHILE, because if no string at all, it will continue forever
      #   

    
    
    
    #time.sleep(10)
  
    '''
    answer = ser.read_until(b'CFG<TST::SN::')
    print ('answer',answer)
    '''

    '''
    try:
        answer = ser.read_until(b'CFG<TST::SN::')
    except UnicodeDecodeError:
        time.sleep(1)
    '''
    
    ser.timeout = 1
    ser.write(audiomode_commands[0])
    answer = ser.readline()

    answer_string = answer.decode('utf-8')
    file_log.write('Command : ' + audiomode_commandnames[0] +"\n")
    file_log.write('Answer: ' + answer_string + "\n")
    
 

# Close port for configurator 
ser.close()
file_log.write('=============== Port ' + PortConfigurator + ' closed =============== \n\n')
    

# Open port for ESG, do the config for ESG
ser.port = PortESG
if ser.isOpen():
   ser.close()


ser.open()
print(ser.is_open)
print(ser.name)

ser.flushInput()
ser.flushOutput()

file_log.write('=============== Port ' + PortESG + ' open =============== \n\n')

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

file_log.write('---------------   ESG  ----------------- \n\n')

for icommand, command_tosend in enumerate(restoreparams_commands):
        #Send to serial port and read the answer
        ser.write(command_tosend)
        answer = ser.readline()
        answer_string = answer.decode('utf-8')
        file_log.write('Command : ' + restoreparams_commandnames[icommand] +"\n")
        file_log.write('Answer: ' + answer_string + "\n")    

SendCommands(esg_commands,esg_commandnames)

ser.write(resetsave_commands[0])
answer = ser.readline()
answer_string = answer.decode('utf-8')
file_log.write('Command : ' + resetsave_commandnames[0] +"\n")
file_log.write('Answer: ' + answer_string + "\n")

ser.timeout=5
for i in range(6):
      answer = ser.readline()
      answer_string = answer[0:50].decode('utf-8')
      print(answer_string)
      file_log.write('Answer: ' + answer_string + "\n")


# Close port
ser.close()
file_log.write(' ===============  Port ' + PortESG + ' closed =============== \n')

file_input_config.close()
file_log.close()

# See here for implementing errors etc. : https://github.com/pyserial/pyserial/blob/master/serial/serialposix.py