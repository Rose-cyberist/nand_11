@256
D = A
@SP
M = D
(SimpleFunction.test)
D = 0
@SP
A=M
M=D
@SP
M=M+1
D = 0
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
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
@SP
A = M-1
M = !M
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
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
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
