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


    @staticmethod
    def _resolve_immediate(token, current_addr, labels):
        token = token.strip()
        if token.lstrip('-').isdigit():
            return int(token)
        if token not in labels:
            raise ValueError(f"Unknown label '{token}'")
        target_addr = labels[token]
        return target_addr - (current_addr + 1)
    

    # Encodes a single assembly instruction
    def _encode(self, mnemonic, operands, addr, labels):
        instruction = 0

        if mnemonic in REGISTER_MNEMONICS:
            rd = reg_num(operands[0])
            rs = reg_num(operands[1])
            rt = reg_num(operands[2])
            func = {'add': FUNC_ADD, 'sub': FUNC_SUB, 'slt': FUNC_SLT}[mnemonic]
            instruction |= (OPC_R_ADD_SUB_SLT << 12) & 0xF000
            instruction |= (rd << 9) & 0x0E00
            instruction |= (rs << 6) & 0x01C0
            instruction |= (rt << 3) & 0x0038
            instruction |= func & 0x0007
            return instruction

        if mnemonic == 'addi':
            rd = reg_num(operands[0])
            rs = reg_num(operands[1])
            imm = self._resolve_immediate(operands[2], addr, labels)
            instruction |= (OPC_ADDI << 12) & 0xF000
            instruction |= (rd << 9) & 0x0E00
            instruction |= (rs << 6) & 0x01C0
            instruction |= imm & 0x003F
            return instruction

        if mnemonic == 'li':
            rd = reg_num(operands[0])
            imm = self._resolve_immediate(operands[1], addr, labels)
            instruction |= (OPC_LI << 12) & 0xF000
            instruction |= (rd << 9) & 0x0E00
            instruction |= imm & 0x003F
            return instruction

        if mnemonic == 'lui':
            rd = reg_num(operands[0])
            imm = self._resolve_immediate(operands[1], addr, labels)
            instruction |= (OPC_LUI << 12) & 0xF000
            instruction |= (rd << 9) & 0x0E00
            instruction |= imm & 0x003F
            return instruction

        if mnemonic == 'lw':
            rd = reg_num(operands[0])
            rs = reg_num(operands[1])
            imm = self._resolve_immediate(operands[2], addr, labels)
            instruction |= (OPC_LW << 12) & 0xF000
            instruction |= (rd << 9) & 0x0E00
            instruction |= (rs << 6) & 0x01C0
            instruction |= imm & 0x003F
            return instruction

        if mnemonic == 'sw':
            rd = reg_num(operands[0])
            rs = reg_num(operands[1])
            imm = self._resolve_immediate(operands[2], addr, labels)
            instruction |= (OPC_SW << 12) & 0xF000
            instruction |= (rd << 9) & 0x0E00
            instruction |= (rs << 6) & 0x01C0
            instruction |= imm & 0x003F
            return instruction

        if mnemonic in BRANCH_MNEMONICS:
            rd = reg_num(operands[0])
            rs = reg_num(operands[1])
            imm = self._resolve_immediate(operands[2], addr, labels)
            opcode = OPC_BEQ if mnemonic == 'beq' else OPC_BNE
            instruction |= (opcode << 12) & 0xF000
            instruction |= (rd << 9) & 0x0E00
            instruction |= (rs << 6) & 0x01C0
            instruction |= imm & 0x003F
            return instruction

        if mnemonic in JUMP_MNEMONICS:
            imm = self._resolve_immediate(operands[0], addr, labels)
            opcode = OPC_JMP if mnemonic == 'jmp' else OPC_JAL
            instruction |= (opcode << 12) & 0xF000
            instruction |= imm & 0x0FFF
            return instruction

        raise ValueError(f"Unknown mnemonic '{mnemonic}'")
    

    # reads data files
    def init_memory(self, data_file):
        with open(data_file, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                line = line.split('#', 1)[0].strip()
                if not line:
                    continue
                self.memory[DATA_BASE + i] = int(line, 16) & 0xFFFF

    #  reads the machine word at the current pc from memory, then increments pc by one (moving on to the next instruction).
    def fetch(self):
        instruction = self.memory[self.pc]
        self.pc += 1
        return instruction
    
    # takes a raw 16-bit machine word and extracts every possible field from it
    @staticmethod
    def decode(instruction):
        opcode = (instruction >> 12) & 0x000F
        rd = (instruction >> 9) & 0x7
        rs = (instruction >> 6) & 0x7
        rt = (instruction >> 3) & 0x7
        func = instruction & 0x07
        i_imm = sign_extend(instruction & 0x003F, 6)
        j_imm = sign_extend(instruction & 0x0FFF, 12)
        return opcode, rd, rs, rt, func, i_imm, j_imm
    

    # based on opcode (and func, when relevant),performs the actual operation of the instruction
    def execute(self, decoded):
        opcode, rd, rs, rt, func, i_imm, j_imm = decoded

        if opcode == OPC_R_ADD_SUB_SLT:
            if func == FUNC_ADD:
                self.regs[rd] = (self.regs[rs] + self.regs[rt]) & 0xFFFF
            elif func == FUNC_SUB:
                self.regs[rd] = (self.regs[rs] - self.regs[rt]) & 0xFFFF
            elif func == FUNC_SLT:
                self.regs[rd] = 1 if self.regs[rs] < self.regs[rt] else 0

        elif opcode == OPC_ADDI:
            self.regs[rd] = (self.regs[rs] + i_imm) & 0xFFFF

        elif opcode == OPC_LI:
            self.regs[rd] = i_imm & 0xFFFF

        elif opcode == OPC_LUI:
            self.regs[rd] = (i_imm << 10) & 0xFFFF

        elif opcode == OPC_LW:
            addr = (self.regs[rs] + i_imm) & 0x1FF
            self.regs[rd] = self.memory[addr]

        elif opcode == OPC_SW:
            addr = (self.regs[rs] + i_imm) & 0x1FF
            self.memory[addr] = self.regs[rd]

        elif opcode == OPC_JMP:
            self.pc = self.pc + j_imm

        elif opcode == OPC_JAL:
            self.regs[7] = self.pc
            self.pc = self.pc + j_imm


    # Predicts branch outcome (Taken/Not-Taken) per selected method; read-only, no BPT mutation.
    def branch_prediction(self, branch_addr):
       
        method = self.prediction_method

        if method == 'ST':
            return True

        if method == 'SN':
            return False

        if method == 'D1':
            last = self.BPT.get(branch_addr, False)
            return last

        if method == 'D2':
            state = self.BPT.get(branch_addr, 1)  
            return state >= 2  

        if method == 'IQ':
            state = self.BPT.get(branch_addr, 3)  
            return state >= 4   

        raise ValueError(f"Unknown prediction method '{method}'")



    # Updates BPT state for branch_addr based on actual outcome (Taken/Not-Taken); mutates state, no prediction logic.
    def update_branch_prediction(self, branch_addr, actual_taken):
           
        method = self.prediction_method

        if method in ('ST', 'SN'):
            return 

        if method == 'D1':
            self.BPT[branch_addr] = actual_taken
            return

        if method == 'D2':
            state = self.BPT.get(branch_addr, 1)
            state = min(state + 1, 3) if actual_taken else max(state - 1, 0)
            self.BPT[branch_addr] = state
            return

        if method == 'IQ':
            state = self.BPT.get(branch_addr, 3)
            state = min(state + 1, 7) if actual_taken else max(state - 1, 0)
            self.BPT[branch_addr] = state
            return



    # Main fetch-decode-execute loop with branch prediction, misprediction penalty, and timeout/end-of-program checks.
    def run(self, timeout_cycles):
       
        start_time = time.perf_counter()
        timeout_cycles = int(timeout_cycles)

        while True:
           
            if self.num_cycles > timeout_cycles:
                print('timeout for executing program! Something has a bug')
                self.timed_out = True
                break

           
            if self.pc >= self.num_program_instructions:
                break  

           
            raw = self.fetch()
            decoded = self.decode(raw)
            opcode = decoded[0]
            i_imm = decoded[5]   

            if opcode in (OPC_BEQ, OPC_BNE):
                
                _, rd, rs, rt, func, i_imm, j_imm = decoded
                branch_addr = self.pc - 1
                predicted_taken = self.branch_prediction(branch_addr)

        
                if opcode == OPC_BEQ:
                    actual_taken = (self.regs[rd] == self.regs[rs])
                else: 
                    actual_taken = (self.regs[rd] != self.regs[rs])

              
                target_pc = self.pc + i_imm
                if actual_taken:
                    self.pc = target_pc

               
                self.num_branches += 1

                if predicted_taken != actual_taken:     
                    self.num_stalls += 1
                    self.num_cycles += BRANCH_PENALTY
         
                self.update_branch_prediction(branch_addr, actual_taken)

            else:
                self.execute(decoded)

          
            self.num_instructions += 1
            self.num_cycles += 1

     
        self.sim_runtime_ms = (time.perf_counter() - start_time) * 1000.0



    # Computes accuracy/speedup metrics and writes the formatted final report to report_file.
    def report(self, report_file):
       
        if self.num_branches > 0:
            correct = self.num_branches - self.num_stalls
            accuracy = round(100.0 * correct / self.num_branches)
        else:
            accuracy = 0   

       
        baseline_cycles = self.num_instructions + BRANCH_PENALTY * self.num_branches
        speedup = (baseline_cycles / self.num_cycles) if self.num_cycles > 0 else 1.0


        lines = []
        lines.append("tiny processor report file")
        lines.append(f"simulation runtime: {self.sim_runtime_ms:.3f} ms")
        lines.append(f"number of instructions: {self.num_program_instructions}")      
        lines.append(f"number of simulation cycles: {self.num_cycles}")                
        lines.append(f"number of executed instructions: {self.num_instructions}")     
        lines.append(f"number of stalls: {self.num_stalls}")                           
        lines.append(f"prediction accuracy: %{accuracy}")                             
        lines.append(f"speedup: {speedup:.2f}")
        lines.append("")
        lines.append(f"program counter value: {self.pc}")                             
        lines.append("registers value:")


        for i in range(NUM_REGS):
            lines.append(f"regs[{i}]:0x{self.regs[i] & 0xFFFF:04X}")

        lines.append("")
        lines.append("memory content value:")

        for addr in range(MEM_SIZE):
            value = self.memory[addr]
            if value != 0:
                lines.append(f"memory[{addr}] = 0x{value & 0xFFFF:04X}")


        lines.append("others is 0x0000")  
        report_text = "\n".join(lines) + "\n"

        
        print("Performance Metrics:")
        print("Number of Cycles:", self.num_cycles)

        with open(report_file, 'w') as file:
            file.write(report_text)

"""

# Placeholder for manual/ad-hoc testing of the simulator class; currently unused.
def tester():
    pass

# Entry point guard: runs tester() only when this file is executed directly, not when imported.
if __name__ == '__main__':
    tester()

"""
