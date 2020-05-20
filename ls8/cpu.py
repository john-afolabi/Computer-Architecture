"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

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
        LDI = 130
        PRN = 71
        HLT = 1
        MUL = 162

        while True:
            self.ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if self.ir == HLT:
                sys.exit()
            elif self.ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif self.ir == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif self.ir == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3