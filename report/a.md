# Computer Architecture Project
**Second Semester 1404–1405**

**Course Instructor:** Dr. Abbasi  
**Teaching Assistants:** TA Group

# Analysis and Design of Branch Prediction Methods in the TinyBASU Processor

## Abstract

### Branch Prediction Operation

Branch prediction is an important technique in the design and implementation of modern processors whose purpose is to improve the performance and execution speed of computer programs. When a program contains conditional instructions such as `if-then-else` statements and iterative structures such as `while` and `for` loops, the processor cannot determine exactly which instruction will be executed next before evaluating the condition. In other words, when encountering conditional instructions, the processor must choose one of two or more possible execution paths.

## Project Objectives

The objective of this project is to implement and analyze branch prediction algorithms and methods in a processor. For this purpose, the hypothetical **TinyBASU** processor architecture must be simulated in hardware or software, and the branch prediction algorithms must then be analyzed.

1. Investigate the operation of static and semi-dynamic branch prediction in the MIPS and TinyBASU processor architectures.
2. If an unexpected event occurs, how can static branch prediction be improved?
3. Analyze and improve the implementation of branch prediction and evaluate the efficiency of branch prediction methods.

# Introduction

## Branch Prediction

In computer architecture, **branch prediction** is a digital circuit that attempts to predict the outcome of a branch (such as an `if-then-else` structure) before its actual result is known. The purpose of branch prediction is to improve the flow of instruction execution in the processor **pipeline**.

Branch prediction plays a vital role in achieving optimal performance in pipelined microprocessor architectures.

To improve the execution of conditional programs, processors use branch prediction mechanisms. These mechanisms predict the execution path of the next instruction based on patterns extracted from previous program executions and their behavior.

For example, if a program has satisfied a particular condition in more than 90% of previous executions, the branch predictor may assume that the condition will again evaluate to true. If the prediction is correct, the processor continues execution without waiting for the condition to be evaluated, thereby reducing execution time and improving processing speed.

However, if the prediction is incorrect, the processor must roll back and execute the alternative branch before continuing execution.

In general, branch prediction improves processor performance when executing conditional programs. However, in some situations it may produce incorrect predictions. For this reason, a variety of algorithms and techniques have been developed to improve branch prediction accuracy, and modern processor architectures employ increasingly advanced branch prediction methods.

---

1. **Branch Prediction**  
2. **Pipeline**

---

# Static Branch Prediction

Static branch prediction is a method that selects a predicted instruction by examining the branch instruction itself. This method has several variants.

For example, the early MIPS architecture used **one-sided prediction**. It always assumed that a conditional branch would **not** be taken. Therefore, the processor fetched the next sequential instruction. Only when the branch instruction was evaluated and the branch condition proved true was the **Program Counter (PC)** updated to a non-sequential address.

Static prediction has one major drawback: the frequency of incorrect predictions (especially backward branches) may be greater than the number of correct predictions (typically forward branches), resulting in reduced processor and pipeline performance.

For this reason, a newer approach called **dynamic branch prediction** was developed to enable more efficient execution.

# Dynamic Branch Prediction

In dynamic branch prediction, the processor estimates whether a branch will be taken or not. The hardware can make this decision using instruction history or previously recorded execution behavior.

The simplest history-based prediction methods are:

### One-Bit Dynamic Prediction

A **one-bit counter** (a two-state finite-state machine) records the outcome of the most recent branch.

### Two-Bit Dynamic Prediction

The prediction changes only after **two consecutive incorrect predictions**. This method can be implemented using a **four-state finite-state machine**.

### Branch Penalty

When a branch is resolved during the execution stage, all instructions that have already been fetched into the pipeline must be flushed, resulting in several wasted instruction cycles.

The branch penalty for the **TinyBASU** processor (or a five-stage pipelined MIPS processor) is **3 cycles**.

**Figure 1** illustrates the state machines of the one-bit and two-bit dynamic branch prediction algorithms.
# TinyBASU Processor Architecture

The **TinyBASU** processor has an architecture similar to the **MIPS** processor and uses the same pipeline structure. The only differences between these two processors are the supported assembly instructions, the data bus width, and the number and bit-width of the registers.

The following specifications apply to this processor:

- The width of all buses and registers is **16 bits**, and memory is accessed on a **word basis**.
- The register bank contains **8 registers**. Therefore, **3 bits** are required to represent each register in an instruction.

Figure 2 shows the instruction formats and the instruction set of the TinyBASU processor architecture.

## Instruction Formats

### R-Format

| Bits | Field |
|------|-------|
| 15–12 | OP-CODE |
| 11–9 | RD |
| 8–6 | RS |
| 5–3 | RT |
| 2–0 | FUNC |

### I-Format

| Bits | Field |
|------|-------|
| 15–12 | OP-CODE |
| 11–9 | RD |
| 8–6 | RS |
| 5–0 | IMMEDIATE |

### J-Format

| Bits | Field |
|------|-------|
| 15–12 | OP-CODE |
| 11–0 | LONG IMMEDIATE |

## Instruction Set

| Instruction | OP-Code | FUNC | Assembly | Description |
|------------|---------|------|----------|-------------|
| ADD | 0000 | 001 | `add rd, rs, rt` | `reg[rd] <= reg[rs] + reg[rt]` |
| SUB | 0000 | 010 | `sub rd, rs, rt` | `reg[rd] <= reg[rs] - reg[rt]` |
| SLT | 0000 | 100 | `slt rd, rs, rt` | `reg[rd] <= bool(reg[rs] < reg[rt])` |
| ADDI | 0001 | - | `addi rd, rs, imm` | `reg[rd] <= reg[rs] + int(imm)` |
| LI | 0010 | - | `li rd, imm` | `reg[rd] <= int(imm)` |
| LUI | 0011 | - | `lui rd, imm` | `reg[rd] <= int(imm) << 10` |
| LW | 0100 | - | `lw rd, rs, imm` | `reg[rd] <= mem[rs + int(imm)]` |
| SW | 0101 | - | `sw rd, rs, imm` | `mem[rs + int(imm)] <= reg[rd]` |
| BEQ | 1010 | - | `beq rd, rs, imm` | `PC = PC + int(imm)` if `reg[rs] == reg[rt]`, otherwise `PC = PC + 1` |
| BNE | 1011 | - | `bne rd, rs, imm` | `PC = PC + int(imm)` if `reg[rs] != reg[rt]`, otherwise `PC = PC + 1` |
| JMP | 1110 | - | `jmp imm` | `PC <= PC + int(imm)` |
| JAL | 1111 | - | `jal imm` | `PC <= PC + int(imm)` and `Reg[7] <= PC + 1` |

**Figure 2.** TinyBASU Processor Instruction Formats

---

# Project Description

In this project, the objective is to implement a processor architecture simulator according to the specifications described above and evaluate different branch prediction algorithms on this processor.

The primary goal is to analyze the performance of these algorithms, reduce branch delay, and improve processor efficiency.

To assist with implementing the simulator, a sample Python implementation has been provided. You may extend the simulator by adding more details and modifying it according to your own requirements.

It is recommended to first implement the complete execution process for **three instructions** so that the simulator becomes functional, and then gradually add the remaining instructions.

# Module 1 — Analysis and Implementation of Assembly Programs

- Modify the assembly program for calculating the **30th Fibonacci number** using the **BEQ** instruction (Appendix 1).
- Modify the assembly program for calculating the **30th Fibonacci number** using the **BNE** instruction (Appendix 2).
- Write an assembly program for calculating the **factorial of 50**.

# Module 2 — Processor Instruction Execution Simulator

Design a processor simulator in any programming language.

The simulator must:

- Read an assembly program from a file.
- Execute the program.
- Produce a final report as a text file.

For guidance, you may use the sample implementations provided in **Appendices 3 and 4**.

## Simulator Inputs

- A text file containing the assembly program. Instructions are stored in processor memory addresses **0 through 255**.
- A text file specifying memory contents for addresses **256 through 511**. The *i-th* line contains a **16-bit hexadecimal value** that must be stored at memory address **255 + i**.
- The name of the output report file.
- The selected branch prediction algorithm.
- The maximum number of execution cycles (to prevent infinite loops caused by bugs in either the simulator or the assembly program).

## Simulator Output

The simulator must generate a report containing:

- Overall simulator performance (execution time)
- Number of assembly instructions
- Number of cycles required to execute the program
- Total number of executed instructions
- Instructions-per-cycle ratio (**IPC**)
- Register contents and final Program Counter (PC) value
- Number of stalls (number of times execution is halted because of branches)
- Accuracy of the branch prediction algorithm (percentage of correctly predicted branches)
- Speedup compared with execution without branch prediction

> **Note:** During the initial implementation, set the last three metrics to **zero**. They will be evaluated in Module 3.
# Module 3 — Implementation of Branch Prediction Algorithms

Modify the simulator so that it supports the following branch prediction algorithms:

- **ST** — Static Taken Branch Prediction
- **SN** — Static Not Taken Branch Prediction
- **D1** — One-Bit Dynamic Branch Prediction (Two-State Finite State Machine)
- **D2** — Two-Bit Dynamic Branch Prediction (Four-State Finite State Machine)
- **IQ** — A heuristic method designed by yourself

> You may implement a three-bit state machine or use branch prediction methods proposed in research papers.

---

# Module 4 — Performance Evaluation of Branch Prediction Algorithms and the Simulator

Execute each assembly program created in **Module 1** using the simulator and every branch prediction algorithm implemented in **Module 3**.

Store the generated reports inside the `reports` directory using the following filenames:

| ST | SN | D1 | D2 | IQ |
|----|----|----|----|----|
| `fibo_beq_st.txt` | `fibo_beq_sn.txt` | `fibo_beq_d1.txt` | `fibo_beq_d2.txt` | `fibo_beq_iq.txt` |
| `fibo_bne_st.txt` | `fibo_bne_sn.txt` | `fibo_bne_d1.txt` | `fibo_bne_d2.txt` | `fibo_bne_iq.txt` |
| `fact_st.txt` | `fact_sn.txt` | `fact_d1.txt` | `fact_d2.txt` | `fact_iq.txt` |

---

# Module 5 — Report and Analysis

Prepare a report of **at most five pages** that includes the following:

- Explain the functions used in the simulator implementation.
- Mention each function by name and describe its purpose.
- Do **not** include the entire source code in the report.
- Fully explain the function that implements the branch prediction algorithms.
- Include the corresponding source code for the branch prediction function.
- Evaluate the contents of each report generated in **Module 4**.
- For example, determine which prediction algorithm provides the highest prediction accuracy.

Also answer the following questions in the report with appropriate justification (for example, by modifying the assembly code):

- Can the prediction accuracy or the number of misprediction cycles be reduced by modifying the assembly program without changing the branch prediction algorithm?
- Does supporting or not supporting **data forwarding** in the processor pipeline affect the performance of branch prediction?
- How does increasing or decreasing the number of pipeline stages affect prediction accuracy and branch penalty cycles?

---

## References for Prediction Methods

- **ST** — Static Taken
- **SN** — Static Not Taken
- **D1** — Dynamic One-Bit Predictor
- **D2** — Dynamic Two-Bit Predictor

---

# Module 6 — Optional

Choose **one** of the following tasks and implement it.

This section is worth **bonus points**.

**Note:** This section will only be evaluated if at least **70%** of the project score has been obtained. Therefore, it is recommended to complete the required parts of the project first and then implement one of the following tasks if time permits.

The tasks are ordered from **easier to more difficult**.

### A)

Several opcode and function fields in the processor are currently unused.

Implement suitable instructions (such as multiplication, division, shift operations, or additional branch instructions) inspired by other processor architectures.

In the report, specify the **maximum number of additional instructions** that can be added and explain why.

### B)

Modify the simulator so that it supports the complete **MIPS32** instruction set.

### C)

Modify the simulator so that it supports the **RV32I** instruction set of the **RISC-V** processor.

### D)

Implement one of the branch prediction methods proposed in the following papers:

- **A Hybrid Branch Prediction Approach for High-Performance Processors** [1]
- **Design and Development of an Efficient Branch Predictor for an In-Order RISC-V Processor** [2]

### References

**[1]**

S. Nain and P. Chaudhary,
*A Hybrid Branch Prediction Approach for High-Performance Processors*,
Recent Advances in Computer Science and Communications,
Vol. 15, No. 6, pp. 883–889, 2022.

**[2]**

C. Arul Rathi,
G. Rajakumar,
T. Ananth Kumar,
T. Arun Samuel,

*Design and Development of an Efficient Branch Predictor for an In-Order RISC-V Processor*,
2020.

---

# Evaluation Criteria

The project will be evaluated based on the following criteria:

- Appropriate design (proper processor and circuit design)
- Correct implementation of the required features and understanding of the source code
- Simplicity of use and correctness of the simulator
- Code readability and sufficient documentation (comments)
- Completeness, accuracy, and correctness of all required deliverables

---

# Project Submission

- Place one assembly file and one data file for each program developed in **Module 1** inside the `asm` directory.
- Place the simulator source code (one or more files) inside the `src` directory.
- Place all report files generated by the simulator according to **Module 4** inside the `reports` directory.
- Include a **PDF report** (maximum five pages) containing the student ID, first name, and last name.
- Compress all required files into a single ZIP archive.
- The ZIP filename must be the **student ID(s)** of the project member(s).
- For optional tasks, prepare a separate report and place it together with the corresponding source code inside the `misc` directory.
- The project may be completed individually or in groups of **two students**.
- Group information must be submitted to the teaching assistants before the announced deadline.
- The deadline for project submission and upload is **23:00** on the announced date. The exact schedule for in-person or online presentations will be announced later.
# Appendices

---

# Appendix 1 — Assembly Program for Computing the 20th Fibonacci Number Using `bne`

```assembly
li rx6, 1          # rx6 = 0x1 (Fibonacci number F0)
li rx1, 1          # rx1 = 0x1 (Fibonacci number F1)
lui rx0, 0         # rx0 = zero
addi rx2, rx0, 20 # rx2 = 20 (number of iterations)
addi rx3, rx0, 2  # rx3 = 2 (counter)

loop:
add rx4, rx6, rx1     # rx4 = rx0 + rx1 (Fibonacci number Fn = Fn-1 + Fn-2)
addi rx6, rx1, 0      # rx0 = rx1 (shift the values for the next iteration)
addi rx1, rx4, 0      # rx1 = rx4
addi rx3, rx3, 1      # Increment the counter
bne rx3, rx2, loop    # Branch back to the loop if the counter != 20

add rx4, rx0, rx1     # Store the 20th Fibonacci number in register rx4
```

---

# Appendix 2 — Assembly Program for Computing the 20th Fibonacci Number Using `beq`

```assembly
# Part of Assignment. Needs some modifications

lui rx6, 1        # rx0 = 0x10000 (Fibonacci number F0)
li rx1, 1
lui rx0, 0        # rx0 = zero
addi rx2, rx0, 20 # rx2 = 20 (number of iterations)
addi rx3, rx0, 2  # rx3 = 2 (counter)

loop:
add rx4, rx6, rx1      # rx4 = rx0 + rx1 (Fibonacci number Fn = Fn-1 + Fn-2)
addi rx6, rx1, 0       # rx0 = rx1 (shift the values for the next iteration)
addi rx1, rx4, 0       # rx1 = rx4
addi rx3, rx3, 1       # Increment the counter
beq rx3, rx2, end      # Branch to last instruction
jal loop               # Branch to last instruction

end:
add rx4, rx0, rx1      # Store the 20th Fibonacci number in register rx4
```

---

# Appendix 3 — Sample Simulator Driver

```python
import sys
from simulator import TinyBASUSimulator as Simulator

def main():
    if len(sys.argv) != 6:
        print(
            "Usage: python sim.py [total_cycles] "
            "[prediction_method] [inst_file] [data_file] [report_file]"
        )
        return

    # Extract the command-line arguments
    timeout_cycles = int(sys.argv[1])
    prediction_method = sys.argv[2]
    inst_file = sys.argv[3]
    data_file = sys.argv[4]
    report_file = sys.argv[5]

    simulator = Simulator(prediction_method)
    simulator.parse_instruction(inst_file)
    simulator.init_memory(data_file)
    simulator.run(timeout_cycles)
    simulator.report(report_file)

if __name__ == "__main__":
    main()
```

---

# Appendix 4 — Sample Simulator Implementation

> The corresponding source file contains a more complete implementation. Use that version.

```python
class TinyBASU_Simulator:

    def __init__(self, prediction_method):
        self.regs = [0] * 8          # Initialize the registers
        self.memory = [0] * 512      # Initialize the memory
        self.pc = 0                  # Initialize the program counter
        self.num_cycles = 0
        self.num_instructions = 0
        self.num_stalls = 0
        self.prediction_method = prediction_method
        self.BPT = None              # Branch Prediction Table

    def parse_instruction(self, line):
        # Parse an assembly code instruction from a line
        line = line.strip()

        opcode = int(line[0:4], 2)
        rd = int(line[4:7], 2)
        ...

        return opcode, rd, ...

    def init_memory(self, inst_file, data_file):
        # Initialize the memory with content from files

        with open(data_file, "r") as file:
            data = file.readlines()

        for i, line in enumerate(data):
            self.memory[256 + i] = int(line.strip())

        with open(data_file, "r") as file:
            lines = file.readlines()

        for addr, line in enumerate(lines):
            instruction = self.parse_instruction(line)
            self.memory[addr] = instruction

    def fetch(self):
        instruction = self.memory[self.pc]
        self.pc += 1
        return instruction

    def decode(self, instruction):
        # Extract the opcode and operands from the instruction

        opcode = (instruction >> 12) & 0xF
        rd = (instruction >> 9) & ???
        ...

        return opcode, rd, rs, ...

    def execute(self, instruction):
        opcode, rd, ... = instruction

        if opcode == 0:
            if func == 1:
                self.regs[rd] = self.regs[rs] + self.regs[rt]
            elif func == 2:
                ...

    def branch_prediction(self, instruction):
        # Perform branch prediction based on the selected method

        if self.prediction_method == "ST":
            return True

        elif self.prediction_method == "SN":
            return False

        elif self.prediction_method == "D1":
            if instruction == ".....":
                return self.BPT["key"]
            else:
                ...

    def update_branch_prediction(self, opcode, rs, rt, actual_result):
        # Update the branch prediction table with the actual result

        if self.prediction_method == "dynamic ...":
            key = (opcode, rs, rt)
            self.BPT[key] = actual_result

    def simulate(self, timeout):

        while True:

            if self.num_cycles > timeout:
                print("timeout for executing program! Something has bug")
                exit()

            instruction = self.fetch()

            if instruction == 0:
                break

            opcode, rd, rs, rt, immediate = self.decode(instruction)

            if opcode == "?" or opcode == "?":
                predicted_result = self.branch_prediction(instruction)

                if predicted_result:
                    self.pc += immediate
                else:
                    pass

            self.execute(opcode, rd, rs, rt, immediate)

            self.num_cycles += 1
            self.num_instructions += 1

            if opcode == "?" or opcode == "?":
                actual_result = self.pc == (self.pc - 1) + immediate
                self.update_branch_prediction(
                    opcode,
                    rs,
                    rt,
                    actual_result,
                )

    def report(self, report_file):

        print("Performance Metrics:")
        print("Number of Cycles:", self.num_cycles)

        with open(report_file, "w") as file:
            # ... fill content
```