import sys
import re

print("\nWelcome to the ISA simulator! - Designed by <Daniela>")

#sys.argv = ['isa-sim.py' ,50, './test_1/program_1.txt','./test_1/data_mem_1.txt']
#sys.argv= ['isa-sim.py',800,'./test_2/program_2.txt','./test_2/data_mem_2.txt']
sys.argv= ['isa-sim.py',30,'./test_3/program_3.txt','./test_3/data_mem_3.txt']


if len(sys.argv) < 4:
    print('Too few arguments.')
    sys.exit(-1)
elif (len(sys.argv) > 4):
    print('Too many arguments.')
    sys.exit(-1)

'''
The max_cycles variable contains the max_cycles passed to the script as argument.
'''
max_cycles = int(sys.argv[1])

'''
This class models the register file of the processor. It contains 16 8-bit unsigned
registers named from R0 to R15 (the names are strings). R0 is read only and
reads always 0 (zero). When an object of the class RegisterFile is instantiated,
the registers are generated and initialized to 0.
'''
class RegisterFile:
    def __init__(self):
        self.registers = {}
        for i in range(0, 16):
            self.registers['R'+str(i)] = 0

    '''
    This method writes the content of the specified register.
    '''
    def write_register(self, register, register_value):
        if register in self.registers:
            if register == 'R0':
                print('WARNING: Cannot write R0. Register R0 is read only.')
            else:
                self.registers[register] = register_value % 256
        else:
            print('Register ' + str(register) + ' does not exist. Terminating execution.')
            sys.exit(-1)

    '''
    This method reads the content of the specified register.
    '''
    def read_register(self, register):
        if register in self.registers:
            return self.registers[register]
        else:
            print('Register ' + str(register) + ' does not exist. Terminating execution.')
            sys.exit(-1)

    '''
    This method prints the content of the specified register.
    '''
    def print_register(self, register):
        if register in self.registers:
            print(register + ' = ' + str(self.registers[register]))
        else:
            print('Register ' + str(register) + ' does not exist. Terminating execution.')
            sys.exit(-1)

    '''
    This method prints the content of the entire register file.
    '''
    def print_all(self):
        print('Register file content:')
        for i in range(0, 16):
            self.print_register('R' + str(i))


'''
This class models the data memory of the processor. When an object of the
class DataMemory is instantiated, the data memory model is generated and au-
tomatically initialized with the memory content specified in the file passed as
second argument of the simulator. The memory has 256 location addressed form
0 to 255. Each memory location contains an unsigned 8-bit value. Uninitialized
data memory locations contain the value zero.
'''
class DataMemory:
    def __init__(self):
        self.data_memory = {}
        print('\nInitializing data memory content from file.')
        try:
            with open(sys.argv[3], 'r') as fd:
                file_content = fd.readlines()
        except:
             print('Failed to open data memory file. Terminating execution.')
             sys.exit(-1)
        file_content = ''.join(file_content)
        file_content = re.sub(r'#.*?\n', ' ', file_content)
        file_content = re.sub(r'#.*? ', ' ', file_content)
        file_content = file_content.replace('\n', '')
        file_content = file_content.replace('\t', '')
        file_content = file_content.replace(' ', '')
        file_content_list = file_content.split(';')
        file_content = None
        while '' in file_content_list:
            file_content_list.remove('')
        try:
            for entry in file_content_list:
                address, data = entry.split(':')
                self.write_data(int(address), int(data))
        except:
            print('Malformed data memory file. Terminating execution.')
            sys.exit(-1)
        print('Data memory initialized.')

    '''
    This method writes the content of the memory location at the specified address.
    '''
    def write_data(self, address, data):
        if address < 0 or address > 255:
            print("Out of range data memory write access. Terminating execution.")
            sys.exit(-1)
        self.data_memory[address] = data % 256

    '''
    This method reads the content of the memory location at the specified address.
    '''
    def read_data(self, address):
        if address < 0 or address > 255:
            print("Out of range data memory read access. Terminating execution.")
            sys.exit(-1)
        if address in self.data_memory:
            return self.data_memory[address]
        else:
            self.data_memory[address] = 0
            return 0

    '''
    This method prints the content of the memory location at the specified address.
    '''
    def print_data(self, address):
        if address < 0 or address > 255:
            print('Address ' + str(address) + ' does not exist. Terminating execution.')
            sys.exit(-1)
        if address in self.data_memory:
            print('Address ' + str(address) + ' = ' + str(self.data_memory[address]))
        else:
            print('Address ' + str(address) + ' = 0')

    '''
    This method prints the content of the entire data memory.
    '''
    def print_all(self):
        print('Data memory content:')
        for address in range(0, 256):
            self.print_data(address)

    '''
    This method prints the content only of the data memory that have been used
    (initialized, read or written at least once).
    '''
    def print_used(self):
        print('Data memory content (used locations only):')
        print("\n")
        for address in range(0, 256):
            if address in self.data_memory:
                print('Address ' + str(address) + ' = ' + str(self.data_memory[address]))


'''
This class models the data memory of the processor. When an object of the class
InstructionMemory is instantiated, the instruction memory model is generated
and automatically initialized with the program specified in the file passed as first
argument of the simulator. The memory has 256 location addressed form 0 to
255. Each memory location contains one instruction. Uninitialized instruction
memory locations contain the instruction NOP.
'''
class InstructionMemory:
    def __init__(self):
        self.instruction_memory = {}
        print('\nInitializing instruction memory content from file.')
        try:
            with open(sys.argv[2], 'r') as fd:
                file_content = fd.readlines()
        except:
             print('Failed to open program file. Terminating execution.')
             sys.exit(-1)
        file_content = ''.join(file_content)
        file_content = re.sub(r'#.*?\n', '', file_content)
        file_content = re.sub(r'#.*? ', '', file_content)
        file_content = re.sub(r'\s*[\n\t]+\s*', '', file_content)
        file_content = re.sub('\s\s+', ' ',  file_content)
        file_content = file_content.replace(': ', ':')
        file_content = file_content.replace(' :', ':')
        file_content = file_content.replace(', ', ',')
        file_content = file_content.replace(' ,', ',')
        file_content = file_content.replace('; ', ';')
        file_content = file_content.replace(' ;', ';')
        file_content = file_content.strip()
        file_content = file_content.replace(' ', ',')
        file_content_list = file_content.split(';')
        file_content = None
        while '' in file_content_list:
            file_content_list.remove('')
        try:
            for entry in file_content_list:
                address, instruction_string = entry.split(':')
                instruction = instruction_string.split(',')
                if len(instruction)<1 or len(instruction)>4:
                    raise Exception('Malformed program.')
                self.instruction_memory[int(address)] = {'opcode': str(instruction[0]), 'op_1':'-','op_2':'-','op_3':'-' }
                if len(instruction)>1:
                    self.instruction_memory[int(address)]['op_1'] = str(instruction[1])
                if len(instruction)>2:
                    self.instruction_memory[int(address)]['op_2'] = str(instruction[2])
                if len(instruction)>3:
                    self.instruction_memory[int(address)]['op_3'] = str(instruction[3])
        except:
            print('Malformed program memory file. Terminating execution.')
            sys.exit(-1)
        print('Instruction memory initialized.')

    '''
    This method returns the OPCODE of the instruction located in the instruction
    memory location in the specified address. For example, if the instruction is ADD
    R1, R2, R3;, this method returns ADD.
    '''
    def read_opcode(self, address):
        if address < 0 or address > 255:
            print("Out of range instruction memory access. Terminating execution.")
            sys.exit(-1)
        if address in self.instruction_memory:
            return self.instruction_memory[address]['opcode']
        else:
            return 'NOP'
    

    '''
    This method returns the first operand of the instruction located in the instruc-
    tion memory location in the specified address. For example, if the instruction
    is ADD R1, R2, R3;, this method returns R1.
    '''
    def read_operand_1(self, address):
        if address < 0 or address > 255:
            print("Out of range instruction memory access. Terminating execution.")
            sys.exit(-1)
        if address in self.instruction_memory:
            return self.instruction_memory[address]['op_1']
        else:
            return '-'

    '''
    This method returns the second operand of the instruction located in the instruc-
    tion memory location in the specified address. For example, if the instruction
    is ADD R1, R2, R3;, this method returns R2.
    '''
    def read_operand_2(self, address):
        if address < 0 or address > 255:
            print("Out of range instruction memory access. Terminating execution.")
            sys.exit(-1)
        if address in self.instruction_memory:
            return self.instruction_memory[address]['op_2']
        else:
            return '-'

    '''
    This method returns the third operand of the instruction located in the instruc-
    tion memory location in the specified address. For example, if the instruction
    is ADD R1, R2, R3;, this method returns R3.
    '''
    def read_operand_3(self, address):
        if address < 0 or address > 255:
            print("Out of range instruction memory access. Terminating execution.")
            sys.exit(-1)
        if address in self.instruction_memory:
            return self.instruction_memory[address]['op_3']
        else:
            return '-'

    '''
    This method prints the instruction located at the specified address.
    '''
    def print_instruction(self, address):
        if address < 0 or address > 255:
            print("Out of range instruction memory access. Terminating execution.")
            sys.exit(-1)
        if address in self.instruction_memory:
            print(self.read_opcode(address), end='')
            if self.read_operand_1(address)!='-':
                print(' ' + self.read_operand_1(address), end='')
            if self.read_operand_2(address)!='-':
                print(', ' + self.read_operand_2(address), end='')
            if self.read_operand_3(address)!='-':
                print(', ' + self.read_operand_3(address), end='')
            print(';')
        else:
            print('NOP;')

    '''
    This method prints the content of the entire instruction memory (i.e., the pro-
    gram).
    '''
    def print_program(self):
        print('Instruction memory content (program only, the rest are NOP):')
        for address in range(0, 256):
            if address in self.instruction_memory:
                print('Address ' + str(address) + ' = ', end='')
                self.print_instruction(address)

#the following class is created in order to end the execution without getting the error message from sys.exit()
class breaking(Exception): 
    pass
current_cycle=0
program_counter=0

registerFile = RegisterFile()
dataMemory = DataMemory()
instructionMemory = InstructionMemory()

print('\n\n----------------------------')
print('-----START-OF-SIMULATION----')
print('----------------------------')

#the following functions are used to create a dictionary in order to access the upcode as aritmetical operations
def addition(var_1,var_2,var_3):
    op1=registerFile.read_register(var_2)
    op2=registerFile.read_register(var_3)
    registerFile.write_register(var_1,(op1+op2))

def substraction(var_1,var_2,var_3):
    op1=registerFile.read_register(var_2)
    op2=registerFile.read_register(var_3)
    registerFile.write_register(var_1,(op1-op2))

def bitwise_or(var_1,var_2,var_3):
    op1=registerFile.read_register(var_2)
    op2=registerFile.read_register(var_3)
    registerFile.write_register(var_1,(op1 or op2))

def bitwise_and(var_1,var_2,var_3):
    op1=registerFile.read_register(var_2)
    op2=registerFile.read_register(var_3)
    registerFile.write_register(var_1,(op1 and op2))

def bitwise_not(var_1,var_2,var_3):
    op1=~(registerFile.read_register(var_2))
    registerFile.write_register(var_1, op1)

def loadImmediate(var_1,var_2,var_3):
    op1=int(var_2)
    registerFile.write_register(var_1,op1)
    
#loads the data  from the data Memory
def loadData(var_1,var_2,var_3):

    op1=registerFile.read_register(var_2)
    op1=dataMemory.read_data(op1)
    registerFile.write_register(var_1,op1)

def storeData(var_1,var_2,var_3):
    op1=registerFile.read_register(var_1)
    op2=registerFile.read_register(var_2)
    dataMemory.write_data(op2,op1)
    
def jump(var_1,var_2,var_3):
    op1=registerFile.read_register(var_1)
    program_counter=op1
    return program_counter
        
def jump_if_equal(var_1,var_2,var_3):
    op1=registerFile.read_register(var_2)
    op2=registerFile.read_register(var_3)
    if op1==op2:
        program_counter=jump(var_1,var_2,var_3)
        return program_counter
    else:
# tried "pass" at first but didn't work because of the while loop
# break doesn't work because it will stop the wile loop
#so we just return nothing
        return 

def jump_if_less(var_1,var_2,var_3):
    op1=registerFile.read_register(var_2)
    op2=registerFile.read_register(var_3)
    if op1 < op2:
        program_counter=jump(var_1,var_2,var_3)
        return program_counter
    else:
        return

def no_operation(var_1,var_2,var_3):
    pass

#the end function 
def end_execution(var_1,var_2,var_3):

    raise breaking
    


       
Operations={"ADD": addition,
            "SUB": substraction,
            "OR" : bitwise_or,
            "AND": bitwise_and,
            "NOT": bitwise_not,
            "LI" : loadImmediate,
            "LD" : loadData,
            "SD" : storeData,
            "JR" : jump,
            "JEQ": jump_if_equal,
            "JLT": jump_if_less,
            "NOP": no_operation,
            "END": end_execution}

try:
    while current_cycle < max_cycles:
        var_1=instructionMemory.read_operand_1(program_counter)
        var_2=instructionMemory.read_operand_2(program_counter)
        var_3=instructionMemory.read_operand_3(program_counter)
        
        print("The current cycle is"+" " + str(current_cycle))
        print("\n")
        registerFile.print_all()
        print('\n*************')
        print("\n")
        dataMemory.print_used()
        
        value=program_counter
        if instructionMemory.read_opcode(program_counter)=="JR" or instructionMemory.read_opcode(program_counter)=="JEQ" or instructionMemory.read_opcode(program_counter)=="JLT":
            value=Operations[instructionMemory.read_opcode(program_counter)](var_1,var_2,var_3)
            if value==None:
                program_counter+=1
                
                    
            else:
                program_counter=value
                
                    
                    
        else:
            Operations[instructionMemory.read_opcode(program_counter)](var_1,var_2,var_3)
            program_counter+=1
        print('\n-----------||---------------')
        print('-----------\/---------------')     
        
        current_cycle+=1
    print("Not enough cycles were allocated, stopping the simulation...")
    breaking()
except breaking:
    pass
print("\n")
print("Total number of cycles used : ",current_cycle)
print('\n----------------------------')
print('-------END-OF-SIMULATION----')
print('----------------------------')