import serial 
import time

from FindPorts import *
#from Bridge import *
#from OpenPort import *
from SerialWrapper import *
from parsejson_newdict import *

file_log_name = "C:\\WORK\\QuickConfig\\log_QC_withClasses_newdict.txt"
filename_json = 'commands.json'

#configurator = 'Silicon'
esg = 'Périphérique'

nterminals = 4

# Find the names of the ports 
ports        = Ports(filename_json)
configurator = ports.port_config()
#esg          = ports.port_esg() ## French characters !!!
PortConfigurator = ports.find_port(configurator)
PortESG          = ports.find_port(esg)

################   CONFIGURATOR - TERMINALS   ######################

# Open port for configurator
def main(): 
  # Open output file
  file_log = open(file_log_name,"w")

  
  ser = SerialWrapper(PortConfigurator)
  ser.closeport()  #fction of SerialWrapper
  
  time.sleep(2)

  # Open port 
  ser.openport()  #fction of SerialWrapper
  file_log.write('\n\n ============== Port Configurator ' + PortConfigurator + ' open =============== \n\n')

  # Read commands to be sent to the devices
  serial_command = SerialCommands(filename_json)

  # Do stuff
  for i_slot in range(nterminals):
      file_log.write('\n\n ---------------   SLOT ' + str(i_slot+1) + ' ----------------- \n\n')
      
      answers_log  = []
      commands_log = []
      
      # Bridge for each slot, with UART breaks before and after
      ser.sendbreak(0.25)
      bridge_string = 'BRIDGE'+str(i_slot+1)
      bridge = serial_command.commands_dict('BRIDGE')[bridge_string]
      #print('Bridge',bridge)
      ser.write_read_save(bridge,commands_log,answers_log)
      ser.sendbreak(0.25)

      # RAZ - the same for each slot
      queue_raz = serial_command.queue_raz()
      for command in queue_raz:
          #print('RAZ'+str(iraz) + command)
          ser.write_read_save_Ascii(command,commands_log,answers_log)
          
      # Quick Config for each slot : Status0, RAD, Freq1-8, STD, NAME, Status1
      qc_queue = serial_command.queue_qc(i_slot)
      for command in qc_queue:
          print('QUEUE COM',command)
          ser.write_read_save(command,commands_log,answers_log)
          
     
      for i in range(len(commands_log)):
          file_log.write('Command : ' + ' --- '+ commands_log[i] + "\n")
          file_log.write('Answer: ' + answers_log[i] + "\n\n")
      
      commands_log = []
      answers_log  = []

      # RESET SAVE - the same for each slot; needs time to save
      command = serial_command.commands_dict('RES_SAVE')['RES_SAVE'] 
      ser.write_read_save_Ascii(command,commands_log,answers_log)
      for i in range(len(commands_log)):
          file_log.write('Command : ' + ' --- '+ commands_log[i] + "\n")
          file_log.write('Answer: ' + answers_log[i] + "\n\n")
     
      ser.timeout = 5
      for i in range(6):
          ans = ser.readData()  
          file_log.write('Answer: ' + ans + "\n\n") 
      ser.timeout = 1
  

      commands_log = []
      answers_log  = []

      # MODE AUDIO - the same for each slot
      command = serial_command.commands_dict('MODE')['MODE_AUDIO']
      ser.write_read_save_Ascii(command,commands_log,answers_log)
      
          
      for i in range(len(commands_log)):
          file_log.write('Command : ' + ' --- '+ commands_log[i] + "\n")
          file_log.write('Answer: ' + answers_log[i] + "\n\n")

  ser.closeport()   #fction of SerialWrapper
  file_log.write('=============== Port Configurator ' + PortConfigurator + ' closed =============== \n\n\n')
  
 
  ##########  ESG  #############
  file_log.write('\n\n ============== Port ESG ' + PortESG + ' open =============== \n\n')

  ser.port = PortESG 
  ser.openport()

  commands_log = []
  answers_log  = []

  # Restore parameters - RAZ
  queue_raz = serial_command.queue_raz()
  for command in queue_raz:
      #print('RAZ'+str(iraz) + command)
      ser.write_read_save_Ascii(command,commands_log,answers_log)

    
  # Quick configuration
  qc_queue = serial_command.queue_qc_esg()
  for command in qc_queue:
      ser.write_read_save(command,commands_log,answers_log)

  for i in range(len(commands_log)):
          file_log.write('Command : ' + ' --- '+ commands_log[i] + "\n")
          file_log.write('Answer: ' + answers_log[i] + "\n\n")

  commands_log = []
  answers_log  = []

  # RESET SAVE - the same for each slot; needs time to save
  command = serial_command.commands_dict('RES_SAVE')['RES_SAVE'] 
  ser.write_read_save_Ascii(command,commands_log,answers_log)
  for i in range(len(commands_log)):
      file_log.write('Command : ' + ' --- '+ commands_log[i] + "\n")
      file_log.write('Answer: ' + answers_log[i] + "\n\n")
     
      ser.timeout = 5
      for i in range(6):
          ans = ser.readData()  
          file_log.write('Answer: ' + ans + "\n\n") 
      ser.timeout = 1
  
  
  
  # Close port
  ser.closeport()

  file_log.write('\n\n ============== Port ESG ' + PortESG + ' closed =============== \n\n')

  # Close output file
  file_log.close()
 
  
    

main()


