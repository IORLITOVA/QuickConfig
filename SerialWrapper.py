import serial

class SerialWrapper:
    global commands_log
    global answers_log 

    def __init__(self, device):
        self.ser = serial.Serial(device,baudrate=115200,
                    bytesize=8,
                    parity = 'N',
                    stopbits=1,
                    timeout=1,
                    xonxoff=False)
        print('PORT **********',self.ser.port)
        
        

    def openport(self):
        self.ser.open()
        self.ser.flushInput()
        self.ser.flushOutput()

        print('PORT OPEN')

    def closeport(self):
        self.ser.close()
        print('PORT CLOSED') 

    def sendbreak(self,time):    
        self.ser.send_break(duration=time)

    def sendData(self, commandhex):
        print(commandhex)
        commandbytes = bytes.fromhex(commandhex)
        self.ser.write(commandbytes)
        print('OK')
        commandbytes_part = commandbytes[0:24].decode('ascii')
        return commandbytes_part
        
    def sendDataAscii(self,commandascii):
        command_binary = commandascii.encode()
        self.ser.write(command_binary)
        print('OK ASCII')
        return commandascii


    def readData(self):
        answer = self.ser.readline()
        answer_string = answer[:25].decode('utf-8')
        #print(answer_string)
        print('ANSWER OK')
        return answer_string
        
    

    def write_read_save(self,command,table_commands,table_answers):
        #global commands_log
        #global answers_log 
        com = self.sendData(command) 
        ans = self.readData()
        table_commands.append(com)
        table_answers.append(ans)
        
        #commands_log.append(com)
        #answers_log.append(ans) 
     
    def write_read_save_Ascii(self,command,table_commands,table_answers):
        #global commands_log
        #global answers_log 
        com = self.sendDataAscii(command) 
        ans = self.readData()
        table_commands.append(com)
        table_answers.append(ans)
        
        #commands_log.append(com)
        #answers_log.append(ans)  
        #data += "\r\n"
        #self.ser.write(data.encode())

