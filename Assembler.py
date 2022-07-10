class Assembler:
    def __init__(self, linesOfCode):
        self.lines = linesOfCode
        self.length = len(self.lines)
        
        for line in range(self.length): 
            self.lines[line] = self.lines[line].replace(",","").replace("("," ").replace(")","").split()
            
        #c = 0
        #for l in range(len(self.lines)):
        #    if(len(self.lines[l]) > 1):
        #        self.lines[l].append(c*32)
        #        c = c + 1
        #print(self.lines)
        
        self.RegistersDict,self.opDict,self.JumpsDict,self.Mem = self.InitDicts()
        
        
    def GetBinary(self,n,length = 5):
        return "{0:b}".format(n).zfill(length)
    
    def InitDicts(self):
        RegistersDict,opDict,JumpsDict,Mem = {},{},{},{}
        
        #Mem_Dict
        Mem[80] = 2
        
        #Registers Needed
        RegistersDict["$zero"] = [self.GetBinary(0),0]
        RegistersDict["$at"] = [self.GetBinary(1),5]
        for i in range(0,8):
            RegistersDict["$t" + str(i)] = [self.GetBinary(i+8),5]
        for i in range(0,8):
            RegistersDict["$s" + str(i)] = [self.GetBinary(i+16),0]
        for i in range(8,10):
            RegistersDict["$t" + str(i)] = [self.GetBinary(i+16),0]

        #Instructions Needed
        opDict["add"] = [self.GetBinary(0),self.GetBinary(32,6)]
        opDict["addi"] = [self.GetBinary(8)]
        opDict["and"] = [self.GetBinary(0),self.GetBinary(36,6)]
        opDict["andi"] = [self.GetBinary(12)]
        opDict["sub"] = [self.GetBinary(0),self.GetBinary(34,6)]
        opDict["or"] = [self.GetBinary(0),self.GetBinary(37,6)]
        opDict["ori"] = [self.GetBinary(13)]
        opDict["nor"] = [self.GetBinary(0),self.GetBinary(39,6)]
        opDict["sll"] = [self.GetBinary(0),self.GetBinary(0,6)]
        opDict["sra"] = [self.GetBinary(0),self.GetBinary(3,6)]
        opDict["srl"] = [self.GetBinary(0),self.GetBinary(2,6)]
        opDict["slt"] = [self.GetBinary(0),self.GetBinary(42,6)]
        opDict["slti"] = [self.GetBinary(10)]
        opDict["lui"] = [self.GetBinary(15)]
        opDict["lw"] = [self.GetBinary(35)]
        opDict["sw"] = [self.GetBinary(43)]
        opDict["beq"] = [self.GetBinary(4)]
        opDict["bne"] = [self.GetBinary(5)]
        opDict["j"] = [self.GetBinary(2)]
        
        #Jumps Dict
        i = 0
        for l in self.lines:
            if (l[0].find(":") != -1):
                JumpsDict[l[0][:-1]] = i
            i = i + 1
        """
        i = 0
        for l in self.lines:
            if (l[0].find(":") != -1):
                JumpsDict[l[0][:-1]] = i - len(JumpsDict)
            i = i + 1
        """
        
        #print(JumpsDict)
        return RegistersDict,opDict,JumpsDict,Mem
    def Nor(self,bstr):
        bstr = bstr.lstrip("0")
        bstr = bstr.replace("0","2").replace("1","0").replace("2","1")
        #print(self.BinaryToDecimal(bstr))
        bstr = self.BinaryToDecimal(bstr)
        return bstr
    # Binary to decimal
    def BinaryToDecimal(self,bstr):
        return int(bstr,2)
    # Binary to Hex
    def GetHex(self,bstr):
        return '%0*X' % ((len(bstr) + 3) // 4, int(bstr, 2))
    
    def Op(self,line,opType,Index = None):
        if(opType == 'R'):
            shamt = self.GetBinary(0)
            if(line[0] == 'add'):
                #Perform Operation
                self.RegistersDict[line[1]][1] = self.RegistersDict[line[2]][1] + self.RegistersDict[line[3]][1]
                #print(self.RegistersDict)
                #Return Hexadecimal Representation
                bin_array = self.opDict['add'][0] + self.RegistersDict[line[2]][0]+ \
                self.RegistersDict[line[3]][0]+self.RegistersDict[line[1]][0]+shamt+self.opDict['add'][1]
                Hex = self.GetHex(bin_array)
                return Hex,None
            elif(line[0] == 'sub'):
                #Perform Operation
                self.RegistersDict[line[1]][1] = self.RegistersDict[line[2]][1] - self.RegistersDict[line[3]][1]
                #print(self.RegistersDict)
                #Return Hexadecimal Representation
                bin_array = self.opDict['sub'][0] + self.RegistersDict[line[2]][0]+ \
                self.RegistersDict[line[3]][0]+self.RegistersDict[line[1]][0]+shamt+self.opDict['sub'][1]
                Hex = self.GetHex(bin_array)
                return Hex,None
            elif(line[0] == 'and'):
                #Perform Operation
                self.RegistersDict[line[1]][1] = self.RegistersDict[line[2]][1] & self.RegistersDict[line[3]][1]
                #print(self.RegistersDict)
                #Return Hexadecimal Representation
                bin_array = self.opDict['and'][0] + self.RegistersDict[line[2]][0]+ \
                self.RegistersDict[line[3]][0]+self.RegistersDict[line[1]][0]+shamt+self.opDict['and'][1]
                Hex = self.GetHex(bin_array)
                return Hex,None
            elif(line[0] == 'or'):
                #Perform Operation
                self.RegistersDict[line[1]][1] = self.RegistersDict[line[2]][1] | self.RegistersDict[line[3]][1]
                #print(self.RegistersDict)
                #Return Hexadecimal Representation
                bin_array = self.opDict['or'][0] + self.RegistersDict[line[2]][0]+ \
                self.RegistersDict[line[3]][0]+self.RegistersDict[line[1]][0]+shamt+self.opDict['or'][1]
                Hex = self.GetHex(bin_array)
                return Hex,None
            elif(line[0] == 'nor'):
                #Perform Operation
                n = self.GetBinary(self.RegistersDict[line[2]][1] | self.RegistersDict[line[3]][1])
                #print(n)
                n = self.Nor(n)
                self.RegistersDict[line[1]][1] = n
                #print(self.RegistersDict)
                #Return Hexadecimal Representation
                bin_array = self.opDict['nor'][0] + self.RegistersDict[line[2]][0]+ \
                self.RegistersDict[line[3]][0]+self.RegistersDict[line[1]][0]+shamt+self.opDict['nor'][1]
                Hex = self.GetHex(bin_array)
                return Hex,None
            elif(line[0] == 'slt'):
                #Perform Operation
                self.RegistersDict[line[1]][1] = int(self.RegistersDict[line[2]][1] < self.RegistersDict[line[3]][1])
                #print(self.RegistersDict)
                #Return Hexadecimal Representation
                bin_array = self.opDict['slt'][0] + self.RegistersDict[line[2]][0]+ \
                self.RegistersDict[line[3]][0]+self.RegistersDict[line[1]][0]+shamt+self.opDict['slt'][1]
                Hex = self.GetHex(bin_array)
                return Hex,None
            elif(line[0] == 'sll'):
                shamt = self.GetBinary(int(line[3]))
                #Perform Operation
                self.RegistersDict[line[1]][1] = self.RegistersDict[line[2]][1] << int(line[3])
                #print(self.RegistersDict)
                #Return Hexadecimal Representation
                bin_array = self.opDict['sll'][0] + self.GetBinary(0) + \
                self.RegistersDict[line[2]][0]+self.RegistersDict[line[1]][0]+shamt+self.opDict['sll'][1]
                Hex = self.GetHex(bin_array)
                return Hex,None
            elif(line[0] == 'srl'):
                shamt = self.GetBinary(int(line[3]))
                #Perform Operation
                self.RegistersDict[line[1]][1] = self.RegistersDict[line[2]][1] >> int(line[3])
                #print(self.RegistersDict)
                #Return Hexadecimal Representation
                bin_array = self.opDict['sll'][0] + self.GetBinary(0) + \
                self.RegistersDict[line[2]][0]+self.RegistersDict[line[1]][0]+shamt+self.opDict['srl'][1]
                Hex = self.GetHex(bin_array)
                return Hex,None
                
                
        elif(opType == 'I'):
            if(line[0] == 'addi'):
                #Perform Operation
                self.RegistersDict[line[1]][1] = self.RegistersDict[line[2]][1] + int(line[3])
                #print(self.RegistersDict)
                #Return Hexadecimal Representation
                bin_array = self.opDict['addi'][0] + self.RegistersDict[line[2]][0]+ \
                self.RegistersDict[line[1]][0]+self.GetBinary(int(line[3]),16)
                Hex = self.GetHex(bin_array)
                return Hex,None
            elif(line[0] == 'andi'):
                #Perform Operation
                self.RegistersDict[line[1]][1] = self.RegistersDict[line[2]][1] & int(line[3])
                #print(self.RegistersDict)
                #Return Hexadecimal Representation
                bin_array = self.opDict['andi'][0] + self.RegistersDict[line[2]][0]+ \
                self.RegistersDict[line[1]][0]+self.GetBinary(int(line[3]),16)
                Hex = self.GetHex(bin_array)
                return Hex,None
            elif(line[0] == 'ori'):
                #Perform Operation
                self.RegistersDict[line[1]][1] = self.RegistersDict[line[2]][1] | int(line[3])
                #print(self.RegistersDict)
                #Return Hexadecimal Representation
                bin_array = self.opDict['ori'][0] + self.RegistersDict[line[2]][0]+ \
                self.RegistersDict[line[1]][0]+self.GetBinary(int(line[3]),16)
                Hex = self.GetHex(bin_array)
                return Hex,None
            elif(line[0] == 'slti'):
                #Perform Operation
                self.RegistersDict[line[1]][1] = int(self.RegistersDict[line[2]][1] < int(line[3]))
                #print(self.RegistersDict)
                #Return Hexadecimal Representation
                bin_array = self.opDict['slti'][0] + self.RegistersDict[line[2]][0]+ \
                self.RegistersDict[line[1]][0]+self.GetBinary(int(line[3]),16)
                Hex = self.GetHex(bin_array)
                return Hex,None  
            elif(line[0] == 'lui'):
                #Perform Operation
                self.RegistersDict[line[1]][1] = int(line[3])
                #print(self.RegistersDict)
                #Return Hexadecimal Representation
                bin_array = self.opDict['lui'][0] + self.GetBinary(0) + \
                self.RegistersDict[line[1]][0]+self.GetBinary(int(line[2]),16)
                Hex = self.GetHex(bin_array)
                return Hex,None
            elif(line[0] == 'beq'):
                #Perform Operation
                index = Index 
                return_index = Index
                #print("Index of Line itself: ", index)
                if(self.RegistersDict[line[1]][1] == self.RegistersDict[line[2]][1]):
                    return_index = self.JumpsDict[line[3]]
                
                index = self.JumpsDict[line[3]]
                #print("Index of Jump Needed: ",index)
                #print("Resulting offset: ", index - Index - 1)
                bin_array = self.opDict['beq'][0] + self.RegistersDict[line[1]][0]+\
                self.RegistersDict[line[2]][0]+self.GetBinary(int(index - Index - 1),16)
                Hex = self.GetHex(bin_array)
                return Hex,return_index
            elif(line[0] == 'bne'):
                #Perform Operation
                index = Index
                return_index = Index
                #Return Hexadecimal Representation
                if(self.RegistersDict[line[1]][1] != self.RegistersDict[line[2]][1]):
                    return_index = self.JumpsDict[line[3]] 
                
                index = self.JumpsDict[line[3]]   
                bin_array = self.opDict['bne'][0] + self.RegistersDict[line[1]][0]+\
                self.RegistersDict[line[2]][0]+self.GetBinary(int(index - Index - 1),16)
                Hex = self.GetHex(bin_array)
                return Hex,return_index
            elif(line[0] == 'sw'):
                self.Mem[self.RegistersDict[line[3]][1] + int(line[2])] = self.RegistersDict[line[1]][1]
                bin_array = self.opDict['sw'][0] + self.RegistersDict[line[3]][0]+\
                self.RegistersDict[line[1]][0]+self.GetBinary(int(line[2]),16)
                Hex = self.GetHex(bin_array)
                return Hex,None
                
            elif(line[0] == 'lw'):
                # This will always return the initialized value 80 in the Memory
                # I assumed Memory pre-located with the value 2 
                self.Mem[self.RegistersDict[line[1]][1]] = self.Mem[80]
                bin_array = self.opDict['lw'][0] + self.RegistersDict[line[3]][0]+\
                self.RegistersDict[line[1]][0]+self.GetBinary(int(line[2]),16)
                Hex = self.GetHex(bin_array)
                return Hex,None
        else:
            if(line[0] == 'j'):
                #Perform Operation - Get Address
                #self.RegistersDict[line[1]][1] = self.RegistersDict[line[2]][1] + int(line[3])
                #print(self.RegistersDict)
                i = self.JumpsDict[line[1]]
                #Return Hexadecimal Representation
                Add = self.GetBinary(self.JumpsDict[line[1]]*32 , 32)
                #print(Add)
                #print(Add[4:])
                #print(Add[4:-2])
                bin_array = self.opDict['j'][0] + self.GetBinary(self.JumpsDict[line[1]]*32 , 32)[4:-2]
                Hex = self.GetHex(bin_array)
                return Hex,i
            #Should Return Address
        
    def GetString(self,Tokens):
        s = ""
        for l in Tokens:
            s = s + " " + l
        return s 
            
    def AssemblyToMachine(self):
        R = ['add','sub','and','or','nor','sll','sra','srl','slt']
        Shift = ['sll','sra','srl']
        I = ['addi','ori','andi','slti','lui','lw','sw','beq','bne']
        J = ['j']
        for i in range(self.length):
            print("Line of Code: ", self.GetString(self.lines[i]))
            if(i == self.length - 1 and len(self.lines[i]) ==1):
                return 
            
            values = list(self.JumpsDict.values())
            l = self.lines[i]
            if(i in values):
                l = l[1:]
            
            if(l[0] in R):
                Machine ,_ = self.Op(l,opType =  'R')
                print("Machine Code: 0x",Machine)
            elif(l[0] in I):
                Machine , n = self.Op(l,opType =  'I',Index = i)
                if(n is not None):
                    i = n
                print("Machine Code: 0x",Machine)
                  
            elif(l[0] in J):
                Machine,i = self.Op(l,opType =  'J')
                print("Machine Code: 0x",Machine)
            
            else: 
                pass
            
    
#Read File into Lines
#lines = open('MIPS.txt', 'r').read()
lines = open('MIPS2.txt', 'r').readlines()
#lines = 'nor $t0, $t1, $at'
#lines = lines.replace(":",":\n").split("\n")

#Remove Empty Strings
#lines = [l for l in lines if l !='']

if __name__ == '__main__':
    assembler = Assembler(lines).AssemblyToMachine()