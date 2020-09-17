"""CPU functionality."""
import sys
HLT = 0b00000001 # HLT 
MUL = 0b10100010 # MUL  R0,R1
LDI = 0b10000010 # LDI R0,8
PRN = 0b01000111 # PRN R0
PUSH = 0b01000101# Push
POP = 0b01000110 # Pop
SP = 0b0111 # 7
CALL = 0b01010000 # Call
RET = 0b00010001 # RET
ADD = 0b10100000 # ADD
class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        # Step 1: Constructor
        self.reg = [0] * 8 # R0 - R7
        self.ram = [0] * 256 #  256 bites memory
        self.pc = 0
        self.running = False
        self.branchtable = {}
        self.branchtable[HLT] = self.htl_instruction
        self.branchtable[MUL] = self.mult_instruction
        self.branchtable[LDI] = self.ldi_instruction
        self.branchtable[PRN] = self.prn_instruction
        self.branchtable[PUSH] = self.push_instruction
        self.branchtable[POP] = self.pop_instruction
        self.branchtable[CALL] = self.call_instruction
        self.branchtable[RET] = self.ret_instruction
        self.branchtable[ADD] = self.add_instruction
    # Step 2: RAM methods (ram_read & ram_write)
    def ram_read(self, address):
        return self.ram[address]
    def ram_write(self, value, address):
        self.ram[address] = value
    
    def ret_instruction(self):
        self.pc = self.pop_value() 

    def push_value(self, value):
        # Decrement SP
        self.reg[SP] -= 1

        # Copy the value to the SP address
        top_of_stack_addr = self.reg[SP]
        self.ram[top_of_stack_addr] = value
    def pop_value(self):
        # Get the top of stack addr
        top_of_stack_addr = self.reg[SP]

        # get the value at the top of the stack
        value = self.ram[top_of_stack_addr]
        # increment the SP
        self.reg[SP] += 1
        return value
    def add_instruction(self): 
        reg_numA = self.ram[self.pc+1]
        reg_numB = self.ram[self.pc+2]
        self.alu("ADD", reg_numA, reg_numB)
        self.pc += 3
    def call_instruction(self):
        # Compute the return addr
        return_addr = self.pc + 2
        #Push return addr on stack
        self.push_value(return_addr)
        #Get the value from the operand reg
        reg_num = self.ram[self.pc + 1]
        value = self.reg[reg_num]
        # set the pc to that value
        self.pc = value

    def run(self):
        self.running = True
        while self.running: 
            ir = self.ram[self.pc]
            self.branchtable[ir]()

    def load(self):
    
        if len(sys.argv) != 2:
            print("usage: comp.py filename")
            sys.exit(1)

        try:
            address = 0

            with open(sys.argv[1]) as f:
                for line in f:
                    t = line.split('#')
                    n = t[0].strip()

                    if n == '':
                        continue

                    try:
                        n = int(n, 2)
                    except ValueError:
                        print(f"Invalid number '{n}'")
                        sys.exit(1)

                    self.ram[address] = n
                    address += 1

        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)
        # """Load a program into memory."""
        # address = 0
        # # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()
    # Step 3: run() method
    '''def run(self):

        """Run the CPU."""
        self.running = True
        while self.running:
            ir = self.ram[self.pc] # Instruction Register, copy of the currently-executing intruction
            if ir ==0b00000001: # HTL -- Halt
                # self.running = False
                self.htl_instruction()
            elif ir == 0b10100010:
                self.mult_instruction()
            elif ir == 0b10000010: # SAVE_REG -- LDI
                self.ldi_instruction()
            elif ir == 0b01000111: # PRINT_REG
                reg_num = self.ram[self.pc+1]
                print(self.reg[reg_num])
                self.pc += 2
            else:
                print(f"Unknown instrution {ir}") '''

    # Step 4: HTL instruction handler
    def htl_instruction(self):
        self.running = False
    # Step 5: LDI instruction
    def ldi_instruction(self):
        reg_num = self.ram[self.pc+1]
        value = self.ram[self.pc+2]
        self.reg[reg_num] = value
        self.pc += 3
    # Step 6: PRN instruction
    def prn_instruction(self):
        reg_num = self.ram[self.pc+1]
        print(self.reg[reg_num])
        self.pc += 2
    def mult_instruction(self):
        reg_numA = self.ram[self.pc+1]
        reg_numB = self.ram[self.pc+2]
        self.alu("MUL", reg_numA, reg_numB)
        self.pc += 3
    def push_instruction(self):
        # Decrement SP
        self.reg[SP] -= 1
        # Get the reg num to push
        reg_num = self.ram[self.pc + 1]
        # Get the value to push
        value = self.reg[reg_num]
        # Copy the value to the SP address
        top_of_stack_addr = self.reg[SP]
        self.ram[top_of_stack_addr] = value
        # print(memory[0xea:0xf4])
        self.pc += 2

    def pop_instruction(self): 
        # Get reg to pop into
        reg_num = self.ram[self.pc + 1]
        # Get the top of the stack addr
        top_of_stack_addr = self.reg[SP]
        # Get the value at the top of the stack
        value = self.ram[top_of_stack_addr]
        # Store the value in the register
        self.reg[reg_num] = value
        # increment SP
        self.reg[SP] += 1
        self.pc += 2 