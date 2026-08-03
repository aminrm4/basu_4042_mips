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