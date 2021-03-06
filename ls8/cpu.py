"""CPU functionality."""

import sys

LDI = 130
MUL = 162
PRN = 71
HLT = 1
PUSH = 69
POP = 70
ADD = 160
CALL = 80
RET = 17


class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7

        self.branchtable = {
            LDI: self.handle_ldi,
            HLT: self.handle_hlt,
            PRN: self.handle_prn,
            MUL: self.handle_mul,
            POP: self.handle_pop,
            PUSH: self.handle_push,
            ADD: self.handle_add,
            CALL: self.handle_call,
            RET: self.handle_ret,
        }

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        if (len(sys.argv) != 2):
            print('Missing input file')
            sys.exit(1)
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    instruction_value = line.split('#')[0].strip()

                    if instruction_value:

                        num = int(instruction_value, 2)
                        self.ram[address] = num

                        address += 1
        except FileNotFoundError:
            print('File not found')
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        print('ALU', op, reg_a, reg_b)
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

        print(
            f"TRACE: %02X | %02X %02X %02X |" % (
                self.pc,
                #self.fl,
                #self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2)),
            end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            IR = self.ram[self.pc]
            try:
                if IR in self.branchtable:
                    self.branchtable[IR]()
            except ValueError:
                print(f'Invalid Opcode {hex(IR)}')

    def handle_hlt(self):
        sys.exit()

    def handle_mul(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu('MUL', operand_a, operand_b)
        self.pc += 3

    def handle_ldi(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += 3

    def handle_prn(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.reg[operand_a])
        self.pc += 2

    def handle_push(self):
        reg = self.ram_read(self.pc + 1)
        val = self.reg[reg]
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = val
        self.pc += 2

    def handle_pop(self):
        reg = self.ram_read(self.pc + 1)
        val = self.ram_read(self.reg[self.sp])
        self.reg[reg] = val
        self.reg[self.sp] += 1
        self.pc += 2

    def handle_add(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu('ADD', operand_a, operand_b)
        self.pc += 3

    def handle_call(self):
        reg = self.ram_read(self.pc + 1)
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], self.pc + 2)
        self.pc = self.reg[reg]

    def handle_ret(self):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
