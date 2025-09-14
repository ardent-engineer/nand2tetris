# Nand2Tetris

Welcome to the **Nand2Tetris** repository! This project contains the complete set of 12 projects from the [Nand2Tetris](https://www.nand2tetris.org/) course, which guides you through building a modern computer system from the ground up, starting with basic logic gates and culminating in a fully functional computer capable of running programs written in a high-level language.

## Overview

The Nand2Tetris course, also known as "From Nand to Tetris," is a comprehensive journey through computer science, covering hardware and software design. This repository showcases my implementations of all 12 projects, each building on the previous one to create a fully operational computer system.

### Projects

1. **Boolean Logic**: Building basic logic gates (Nand, And, Or, Xor, Mux, etc.) using HDL (Hardware Description Language).
2. **Boolean Arithmetic**: Constructing arithmetic units like half-adders, full-adders, and ALUs.
3. **Sequential Logic**: Designing flip-flops, registers, and counters for memory storage.
4. **Machine Language**: Writing low-level programs in the Hack assembly language.
5. **Computer Architecture**: Building the Hack computer’s CPU, memory, and instruction set.
6. **Assembler**: Developing an assembler to translate Hack assembly code into machine code.
7. **Virtual Machine I**: Implementing the stack-based virtual machine (arithmetic and logical operations).
8. **Virtual Machine II**: Extending the VM with program flow and function-calling capabilities.
9. **High-Level Language**: Writing programs in the Jack programming language, a high-level language.
10. **Compiler I**: Building a syntax analyzer for the Jack language.
11. **Compiler II**: Completing the Jack compiler with code generation.
12. **Operating System**: Implementing a basic OS with memory management, I/O, and standard library functions.

Each project is implemented as per the specifications provided in the Nand2Tetris course, ensuring compatibility with the provided hardware simulator and testing tools.

## Repository Structure

- `/project_01` to `/project_12`: Each folder contains the source code and files for the respective project.
- `README.md`: This file, providing an overview of the repository.

## Getting Started

To explore or run the projects, you’ll need the Nand2Tetris software suite, which includes the hardware simulator, assembler, VM emulator, and Jack compiler. You can download it from the [official Nand2Tetris website](https://www.nand2tetris.org/software).

### Prerequisites

- Nand2Tetris software suite
- Basic understanding of computer architecture and programming

### Running the Projects

1. Clone this repository:
   ```bash
   git clone https://github.com/ardent-engineer/nand2tetris.git
   ```
2. Navigate to the desired project folder (e.g., `project_01` for Boolean Logic).
3. Use the Nand2Tetris tools to simulate or compile the code:
   - For hardware projects (1–5), use the Hardware Simulator to load `.hdl` files and run `.tst` scripts.
   - For the assembler (6), run the assembler on `.asm` files.
   - For VM projects (7–8), use the VM Emulator to test `.vm` files.
   - For Jack programs and compiler (9–12), use the Jack compiler and VM Emulator.

## Acknowledgments

- The Nand2Tetris course by Noam Nisan and Shimon Schocken for providing an incredible learning experience.
- The open-source community for inspiration and support.
