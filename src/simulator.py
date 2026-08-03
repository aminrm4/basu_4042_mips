import time

BRANCH_PENALTY = 3      

NUM_REGS = 8                 
MEM_SIZE = 512                
DATA_BASE = 256                

# OPCODE values (4 bits, taken from the instruction-set table in the spec).
OPC_R_ADD_SUB_SLT = 0b0000    # R-format

# I-format
OPC_ADDI = 0b0001
OPC_LI   = 0b0010
OPC_LUI  = 0b0011
OPC_LW   = 0b0100
OPC_SW   = 0b0101
OPC_BEQ  = 0b1010 
OPC_BNE  = 0b1011
OPC_JMP  = 0b1110
OPC_JAL  = 0b1111

# FUNC values (3 bits)
FUNC_ADD = 0b001
FUNC_SUB = 0b010
FUNC_SLT = 0b100

REGISTER_MNEMONICS = {'add', 'sub', 'slt'}                 # R-format instructions
IMMEDIATE_MNEMONICS = {'addi', 'li', 'lui', 'lw', 'sw'}     # I-format (non-branch) instructions
BRANCH_MNEMONICS = {'beq', 'bne'}                            # I-format (branch) instructions
JUMP_MNEMONICS = {'jmp', 'jal'}

def sign_extend(value, bits):
    mask = 1 << (bits - 1)
    return (value ^ mask) - mask


# retunr register number
def reg_num(token):
    token = token.strip()
    if not token.startswith('rx'):
        raise ValueError(f"Expected a register like 'rx3', got '{token}'")
    return int(token[2:])

class TinyBASUSimulator:
    def __init__(self, prediction_method):
            self.regs = [0] * NUM_REGS
            self.memory = [0] * MEM_SIZE
            self.pc = 0

            self.num_cycles = 0
            self.num_instructions = 0
            self.num_stalls = 0
            self.num_branches = 0

            self.prediction_method = prediction_method
            self.BPT = {}

            self.num_program_instructions = 0
            self.sim_runtime_ms = 0.0
            self.timed_out = False


    # Assembling the plain-text assembly file into machine code
    def parse_instruction(self, asm_file):
        raw_lines = []
        with open(asm_file, 'r') as f:
            for line in f:
                line = line.split('#', 1)[0].strip()
                if not line:
                    continue

                label = None
                if ':' in line:
                    label_part, _, rest = line.partition(':')
                    label = label_part.strip()
                    line = rest.strip()

                if not line:
                    raw_lines.append((label, None))
                    continue

                parts = line.replace(',', ' ').split()
                mnemonic = parts[0].lower()
                operands = parts[1:]
                raw_lines.append((label, (mnemonic, operands)))

        labels = {}
        instructions = []
        pending_labels = []
        for label, instr in raw_lines:
            if label is not None:
                pending_labels.append(label)
            if instr is None:
                continue

            addr = len(instructions)
            for lbl in pending_labels:
                labels[lbl] = addr
            pending_labels = []
            instructions.append(instr)

        if pending_labels:
            raise ValueError(f"Label(s) {pending_labels} at end of file with no following instruction")

        machine_codes = []
        for addr, (mnemonic, operands) in enumerate(instructions):
            machine_codes.append(self._encode(mnemonic, operands, addr, labels))

        self.num_program_instructions = len(machine_codes)

        for address, inst in enumerate(machine_codes):
            self.memory[address] = inst


    