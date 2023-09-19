
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
@24575
D=A
@R3
M=D
(CHECK)
@R1
M=0
	@KBD
	D = M
	@BLACKSCREEN
	D;JNE
	@FULLWHITE
	D;JEQ
(BLACKSCREEN)
@R1
M=0
	@SCREEN
	D = A
	@R1
	M = D
(FULLYB)
	@R1
	D = M
	A = D
	M = -1
	A = A + 1
	D = A
	@R1
	M = D
	A = M
	@R3
	D=M-D
	@FULLYB
	D;JGE
	@CHECK
	0;JMP
(FULLWHITE)
@R1
M=0
	@SCREEN
	D = A
	@R1
	M = D
(FULLYW)
	@R1
	D = M
	A = D
	M = 0
	A = A + 1
	D = A
	@R1
	M = D
	A = M
	@R3	
	D = M - D
	@CHECK
	D;JLT
	@FULLYW
	D;JGE
