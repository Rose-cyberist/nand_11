@256
D = A
@SP
M = D
@returnAddress0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(returnAddress0)
//function Main.fibonacci 0
(Main.fibonacci)
//push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//lt
@SP
M = M-1
A = M
D = M
@a
M = D
@a_is_neg1
D;JGT
@b_is_pos1
@SP
A = M-1
M;JLT
@SP
A = M-1
M = 0
@end1
0;JMP
(a_is_neg1)
@SP
A = M-1
D = M
@b
M = D
@b_is_pos1
D;JGT
@SP
A = M-1
M = -1
@end1
0;JMP
(b_is_pos1)
@a
D = M
@b
D = M-D
@is_lt1
D;JLT
@SP
A = M-1
M = 0
@end1
0;JMP
(is_lt1)
@SP
A = M-1
M = -1
(end1)
//if-goto IF_TRUE
@SP
M = M-1
A = M
D = M
@end2
D;JEQ
@IF_TRUE
0;JMP
(end2)
//goto IF_FALSE
@IF_FALSE
0;JMP
//label IF_TRUE
(IF_TRUE)
//push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//return
@LCL
D=M
@endFrame
M=D
A=D
A=A-1
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@retAddr
M=D
@ARG
D=M
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@ARG
D=M+1
@SP
M=D
@endFrame
D=M-1
A=D
D=M
@THAT
M=D
@endFrame
D=M-1
D=D-1
A=D
D=M
@THIS
M=D
@endFrame
D=M-1
D=D-1
D=D-1
A=D
D=M
@ARG
M=D
@endFrame
D=M-1
D=D-1
D=D-1
D=D-1
A=D
D=M
@LCL
M=D
@retAddr
A=M
0;JMP
//label IF_FALSE
(IF_FALSE)
//push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
@SP
M = M-1
A = M
D = M
@SP
M = M-1
A = M
M = M-D
@SP
M = M+1
A = M
//call Main.fibonacci 1
@returnAddress3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
D = D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(returnAddress3)
//push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
@SP
M = M-1
A = M
D = M
@SP
M = M-1
A = M
M = M-D
@SP
M = M+1
A = M
//call Main.fibonacci 1
@returnAddress4
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
D = D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(returnAddress4)
//add
@SP
M = M-1
A = M
D = M
@SP
M = M-1
A = M
M = M+D
@SP
M = M+1
A = M
//return
@LCL
D=M
@endFrame
M=D
A=D
A=A-1
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@retAddr
M=D
@ARG
D=M
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@ARG
D=M+1
@SP
M=D
@endFrame
D=M-1
A=D
D=M
@THAT
M=D
@endFrame
D=M-1
D=D-1
A=D
D=M
@THIS
M=D
@endFrame
D=M-1
D=D-1
D=D-1
A=D
D=M
@ARG
M=D
@endFrame
D=M-1
D=D-1
D=D-1
D=D-1
A=D
D=M
@LCL
M=D
@retAddr
A=M
0;JMP
//function Sys.init 0
(Sys.init)
//push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
//call Main.fibonacci 1
@returnAddress5
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
D = D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(returnAddress5)
//label WHILE
(WHILE)
//goto WHILE
@WHILE
0;JMP
