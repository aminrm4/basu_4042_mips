# 🖥️ TinyBASU — Processor Simulator & Branch Prediction Lab ⚡

<div align="center">

<h3>A general-purpose TinyBASU processor simulator with branch prediction analysis 🚀</h3>

![Python](https://img.shields.io/badge/Python-3-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Assembly](https://img.shields.io/badge/Assembly-TinyBASU_ISA-6E4C1E?style=for-the-badge&logo=assemblyscript&logoColor=white)
![CLI](https://img.shields.io/badge/CLI-Simulator-4B4B4B?style=for-the-badge)
![Branch Prediction](https://img.shields.io/badge/Branch-Prediction-9B59B6?style=for-the-badge)
![Pipeline](https://img.shields.io/badge/Pipeline-5--Stage-1ABC9C?style=for-the-badge)
![Build](https://img.shields.io/badge/Build-Manual-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

### 🧠 Team **`auf keinen fall`** 🇩🇪

</div>

---

## 📖 About The Project

This repository contains the final project for the **Computer Architecture** course 🎓 at **Bu-Ali Sina University**. It implements a **software simulator** for the fictional **TinyBASU** processor, and analyzes multiple **Branch Prediction** algorithms ⚡ on it.

> 💡 **Goal:** simulate the behavior of a pipelined processor when facing conditional branches, and compare the accuracy ⏱️ and speedup 🚀 of different branch prediction strategies.

---

## 🎯 Project Objectives

- 🔍 Study how static and dynamic branch prediction behave in MIPS-like and TinyBASU architectures
- 🛠️ Build a full **fetch → decode → execute** simulator from scratch
- 📊 Analyze and compare the accuracy of different branch prediction algorithms
- 📈 Evaluate the performance speedup gained from branch prediction

---

## 🏗️ TinyBASU Architecture

| Feature | Value |
|---|---|
| 📏 Bus & register width | 16-bit |
| 🗂️ Registers | 8 (`rx0` – `rx7`) |
| 💾 Instruction memory | addresses 0 – 255 |
| 💾 Data memory | addresses 256 – 511 |
| 🧩 Instruction formats | R-Format / I-Format / J-Format |

### 📋 Supported Instructions

| Category | Instructions |
|---|---|
| 🧮 Arithmetic / Logic | `ADD` `SUB` `SLT` `ADDI` `LI` `LUI` |
| 📥📤 Memory | `LW` `SW` |
| 🔀 Branch / Jump | `BEQ` `BNE` `JMP` `JAL` |

---

## 🔮 Branch Prediction Algorithms

| Code | Name | Type |
|:---:|---|---|
| 🟥 `ST` | Static Taken | Static |
| 🟦 `SN` | Static Not-Taken | Static |
| 🟨 `D1` | 1-bit Dynamic | Dynamic (2-state FSM) |
| 🟩 `D2` | 2-bit Dynamic | Dynamic (4-state FSM) |
| 🟪 `IQ` | Custom Heuristic | Dynamic (your own design) |

---

## 🧩 Project Modules

| Module | Title | Description |
|:---:|---|---|
| 1️⃣ | Assembly Programs | 30th Fibonacci (`beq` & `bne`) + Factorial(50) |
| 2️⃣ | Processor Simulator | Full fetch-decode-execute engine |
| 3️⃣ | Branch Prediction | `ST` `SN` `D1` `D2` `IQ` implementations |
| 4️⃣ | Execution & Reports | 15 report files (3 programs × 5 methods) |
| 5️⃣ | Final Report & Analysis | Performance comparison and analysis |

---

## 🌳 Repository Structure

```
📦 TinyBASU-Simulator
├── 📁 asm/           # 📝 Assembly & data files
│   ├── fibo_beq.txt
│   ├── fibo_bne.txt
│   └── factorial.txt
├── 📁 src/           # 🐍 Simulator source code
│   └── main.py
├── 📁 reports/       # 📊 Generated report files (15 total)
├── 📄 report.pdf     # 📑 Final analysis report
└── 📄 README.md      # 📘 You are here!
```

---

## ⚙️ Usage

```bash
# prediction_method: ST | SN | D1 | D2 | IQ
python main.py <timeout_cycles> <prediction_method> <inst_file> <data_file> <report_file>
```

### 🔸 Example

```bash
python src/main.py 10000 D2 asm/fibo_beq.txt asm/fibo_beq_data.txt reports/fibo_beq_d2.txt
```

---

## 📈 Report Output Includes

- ⏱️ Simulator execution time
- 🔢 Number of instructions executed & cycles consumed
- 📐 IPC (Instructions Per Cycle)
- 🗃️ Final register file & PC values
- ⛔ Number of stalls
- 🎯 Branch prediction accuracy
- 🚀 Speedup vs. no-prediction baseline

---

## 👥 Team Members

<div align="center">

| Avatar | Username | GitHub Profile |
|:---:|:---:|:---:|
| <img src="https://github.com/AbolfazlAsali.png" width="70" height="70" style="border-radius:50%"/> | **AbolfazlAsali** | [github.com/AbolfazlAsali](https://github.com/AbolfazlAsali) |
| <img src="https://github.com/imShahriar-klvd.png" width="70" height="70" style="border-radius:50%"/> | **imShahriar-klvd** | [github.com/imShahriar-klvd](https://github.com/imShahriar-klvd) |
| <img src="https://github.com/aminrm4.png" width="70" height="70" style="border-radius:50%"/> | **aminrm4** | [github.com/aminrm4](https://github.com/aminrm4) |

</div>



## 🏫 Course Info

- 📚 **Course:** Computer Architecture
- 🏛️ **University:** Bu-Ali Sina University
- 👨‍🏫 **Instructor:** Dr. Abbasi
- 📆 **Semester:** Second Semester 1404–1405

---

<div align="center">

### ⭐ Built with effort and coffee ☕ by Team `auf keinen fall` 🇩🇪

</div>
