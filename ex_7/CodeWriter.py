"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.current_label = 0
        self.output_file = output_stream
        self.static_var_filename = ""

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.

        Args:
            filename (str): The name of the VM file.
        """
        self.static_var_filename = filename

    def pop_assembly(self, assembly_command: str):
        assembly_command += '@SP\n'
        assembly_command += 'M = M-1\n'
        assembly_command += 'A = M\n'
        return assembly_command

    def push_assembly(self, assembly_command: str):
        assembly_command += '@SP\n'
        assembly_command += 'M = M+1\n'
        assembly_command += 'A = M\n'
        return assembly_command

    def top_assembly(self, assembly_command: str):
        assembly_command += '@SP\n'
        assembly_command += 'A = M-1\n'
        return assembly_command

    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given
        arithmetic command.

        Args:
            command (str): an arithmetic command.
        """
        assembly_command = ""
        if command == 'add':
            assembly_command = self.pop_assembly(assembly_command)
            assembly_command += 'D = M\n'
            assembly_command = self.pop_assembly(assembly_command)
            assembly_command += 'M = M+D\n'
            assembly_command = self.push_assembly(assembly_command)
        elif command == 'sub':
            assembly_command = self.pop_assembly(assembly_command)
            assembly_command += 'D = M\n'
            assembly_command = self.pop_assembly(assembly_command)
            assembly_command += 'M = M-D\n'
            assembly_command = self.push_assembly(assembly_command)
        elif command == 'neg':
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M = -M\n'
        elif command == 'not':
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M = !M\n'
        elif command == 'and':
            assembly_command = self.pop_assembly(assembly_command)
            assembly_command += 'D = M\n'
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M = M&D\n'
        elif command == 'or':
            assembly_command = self.pop_assembly(assembly_command)
            assembly_command += 'D = M\n'
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M = M|D\n'

        elif command == 'shiftleft':
            assembly_command += self.top_assembly(assembly_command)
            assembly_command += 'M = M<<'

        elif command == 'shiftright':
            assembly_command += self.top_assembly(assembly_command)
            assembly_command += 'M = M>>'
        elif command == 'eq':
            assembly_command = self.pop_assembly(assembly_command)
            assembly_command += 'D = M\n'

            assembly_command += '@a\n'
            assembly_command += 'M = D\n'
            assembly_command += '@a_is_neg' + str(self.current_label) + '\n'
            assembly_command += 'D;JGT\n'
            assembly_command += '@b_is_pos' + str(self.current_label) + '\n'

            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M;JLT\n'
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M = 0\n'
            assembly_command += '@end' + str(self.current_label) + '\n'
            assembly_command += '0;JMP\n'
            assembly_command += '(a_is_neg' + str(self.current_label) + ')\n' # here a is bigger then 0
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'D = M\n'
            assembly_command += '@b\n'
            assembly_command += 'M = D\n'
            assembly_command += '@b_is_pos' + str(self.current_label) + '\n'
            assembly_command += 'D;JGT\n'
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M = 0\n'
            assembly_command += '@end' + str(self.current_label) + '\n'
            assembly_command += '0;JMP\n'
            assembly_command += '(b_is_pos' + str(self.current_label) + ')' + '\n'

            assembly_command += '@a\n'
            assembly_command += 'D = M\n'
            assembly_command += '@b\n'
            assembly_command += 'D = M-D\n'
            assembly_command += '@is_eq' + str(self.current_label) + '\n'
            assembly_command += 'D;JEQ\n'
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M = 0\n'
            assembly_command += '@end' + str(self.current_label) + '\n'
            assembly_command += '0;JMP\n'
            assembly_command += '(is_eq' + str(self.current_label) + ')\n'
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M = -1\n'
            assembly_command += '(end' + str(self.current_label) + ')\n'
            self.current_label += 1

        elif command == 'gt':
            assembly_command = self.pop_assembly(assembly_command)
            assembly_command += 'D = M\n'

            assembly_command += '@a\n'
            assembly_command += 'M = D\n'
            assembly_command += '@a_is_neg' + str(self.current_label) + '\n'
            assembly_command += 'D;JGT\n'
            assembly_command += '@b_is_pos' + str(self.current_label) + '\n'
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M;JLT\n'
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M = -1\n'
            assembly_command += '@end' + str(self.current_label) + '\n'
            assembly_command += '0;JMP\n'
            assembly_command += '(a_is_neg' + str(self.current_label) + ')\n' # here a is bigger then 0
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'D = M\n'
            assembly_command += '@b\n'
            assembly_command += 'M = D\n'
            assembly_command += '@b_is_pos' + str(self.current_label) + '\n'
            assembly_command += 'D;JGT\n'
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M = 0\n'
            assembly_command += '@end' + str(self.current_label) + '\n'
            assembly_command += '0;JMP\n'
            assembly_command += '(b_is_pos' + str(self.current_label) + ')' + '\n'

            assembly_command += '@a\n'
            assembly_command += 'D = M\n'
            assembly_command += '@b\n'
            assembly_command += 'D = M-D\n'
            assembly_command += '@is_gt' + str(self.current_label) + '\n'
            assembly_command += 'D;JGT\n'
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M = 0\n'
            assembly_command += '@end' + str(self.current_label) + '\n'
            assembly_command += '0;JMP\n'
            assembly_command += '(is_gt' + str(self.current_label) + ')\n'
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M = -1\n'
            assembly_command += '(end' + str(self.current_label) + ')\n'
            self.current_label += 1

        elif command == 'lt':
            assembly_command = self.pop_assembly(assembly_command)
            assembly_command += 'D = M\n'

            assembly_command += '@a\n'
            assembly_command += 'M = D\n'
            assembly_command += '@a_is_neg' + str(self.current_label) + '\n'
            assembly_command += 'D;JGT\n'
            assembly_command += '@b_is_pos' + str(self.current_label) + '\n'
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M;JLT\n'
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M = 0\n'
            assembly_command += '@end' + str(self.current_label) + '\n'
            assembly_command += '0;JMP\n'
            assembly_command += '(a_is_neg' + str(self.current_label) + ')\n' # here a is bigger then 0
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'D = M\n'
            assembly_command += '@b\n'
            assembly_command += 'M = D\n'
            assembly_command += '@b_is_pos' + str(self.current_label) + '\n'
            assembly_command += 'D;JGT\n'
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M = -1\n'
            assembly_command += '@end' + str(self.current_label) + '\n'
            assembly_command += '0;JMP\n'
            assembly_command += '(b_is_pos' + str(self.current_label) + ')' + '\n'

            assembly_command += '@a\n'
            assembly_command += 'D = M\n'
            assembly_command += '@b\n'
            assembly_command += 'D = M-D\n'
            assembly_command += '@is_lt' + str(self.current_label) + '\n'
            assembly_command += 'D;JLT\n'
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M = 0\n'
            assembly_command += '@end' + str(self.current_label) + '\n'
            assembly_command += '0;JMP\n'
            assembly_command += '(is_lt' + str(self.current_label) + ')\n'
            assembly_command = self.top_assembly(assembly_command)
            assembly_command += 'M = -1\n'
            assembly_command += '(end' + str(self.current_label) + ')\n'
            self.current_label += 1

        self.output_file.write(assembly_command)

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes the assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        if command == "C_PUSH":
            ret_str = ''
            if segment == "static":
                ret_str = "@" + self.static_var_filename + "." + str(index) + "\n"
                ret_str += "D=M\n"
            elif segment == "that":
                ret_str += "@" + str(index) + "\n"
                ret_str += "D=A\n"
                ret_str += "@THAT\n"
                ret_str += "A=M+D\n"
                ret_str += "D=M\n"
            elif segment == "this":
                ret_str += "@" + str(index) + "\n"
                ret_str += "D=A\n"
                ret_str += "@THIS\n"
                ret_str += "A=M+D\n"
                ret_str += "D=M\n"
            elif segment == "constant":
                ret_str = "@" + str(index) + "\n"
                ret_str += "D=A\n"
            elif segment == "temp":
                ret_str = "@" + str(index) + "\n"
                ret_str += "D=A\n"
                ret_str += "@5\n"
                ret_str += "A=A+D\n"
                ret_str += "D=M\n"
            elif segment == "local":
                ret_str = "@" + str(index) + "\n"
                ret_str += "D=A\n"
                ret_str += "@LCL\n"
                ret_str += "A=M+D\n"
                ret_str += "D=M\n"
            elif segment == "pointer":
                ret_str = "@" + str(index) + "\n"
                ret_str += "D=A\n"
                ret_str += "@3\n"
                ret_str += "A=A+D\n"
                ret_str += "D=M\n"
            elif segment == "argument":
                ret_str = "@" + str(index) + "\n"
                ret_str += "D=A\n"
                ret_str += "@ARG\n"
                ret_str += "A=M+D\n"
                ret_str += "D=M\n"
            ret_str += self.push_template()
        elif command == "C_POP":
            ret_str = ''
            if segment == "static":
                ret_str = "@SP\n"
                ret_str += "AM=M-1\n"
                ret_str += "D=M\n"
                ret_str += "@" + self.static_var_filename + "." + str(index) + "\n"
                ret_str += "M=D\n"
            elif segment == "that":
                ret_str = "@" + str(index) + "\n"
                ret_str += "D=A\n"
                ret_str += "@THAT\n"
                ret_str += "D=M+D\n"
                ret_str += self.pop_template()
            elif segment == "this":
                ret_str = "@" + str(index) + "\n"
                ret_str += "D=A\n"
                ret_str += "@THIS\n"
                ret_str += "D=M+D\n"
                ret_str += self.pop_template()
            elif segment == "temp":
                ret_str = "@" + str(index) + "\n"
                ret_str += "D=A\n"
                ret_str += "@5\n"
                ret_str += "D=A+D\n"
                ret_str += self.pop_template()
            elif segment == "local":
                ret_str += "@" + str(index) + "\n"
                ret_str += "D=A\n"
                ret_str += "@LCL\n"
                ret_str += "D=M+D\n"
                ret_str += self.pop_template()
            elif segment == "pointer":
                ret_str = "@" + str(index) + "\n"
                ret_str += "D=A\n"
                ret_str += "@3\n"
                ret_str += "D=A+D\n"
                ret_str += self.pop_template()
            elif segment == "argument":
                ret_str = "@" + str(index) + "\n"
                ret_str += "D=A\n"
                ret_str += "@ARG\n"
                ret_str += "D=M+D\n"
                ret_str += self.pop_template()
        self.output_file.write(ret_str)

    def push_template(self):
        push_str = "@SP\n"
        push_str += "A=M\n"
        push_str += "M=D\n"
        push_str += "@SP\n"
        push_str += "M=M+1\n"
        return push_str

    def pop_template(self):
        pop_str = "@R13\n"
        pop_str += "M=D\n"
        pop_str += "@SP\n"
        pop_str += "AM=M-1\n"
        pop_str += "D=M\n"
        pop_str += "@R13\n"
        pop_str += "A=M\n"
        pop_str += "M=D\n"
        return pop_str

    def close(self) -> None:
        """Closes the output file."""
        self.output_file.close()

    def writeReturn(self):
        ret_str = ''
        ret_str += "@LCL\n"
        ret_str += "D=M\n"
        ret_str += "@endFrame\n"
        ret_str += "M=D\n"

        ret_str += "A=D\n"
        for i in range(5):
            ret_str += "A=A-1\n"
        ret_str += "D=M\n"
        ret_str += "@retAddr\n"
        ret_str += "M=D\n"

        ret_str += "@ARG\n"
        ret_str += "D=M\n"
        ret_str += self.pop_template()

        ret_str += "@ARG\n"
        ret_str += "D=M+1\n"
        ret_str += "@SP\n"
        ret_str += "M=D\n"

        ret_str += "@endFrame\n"
        ret_str += "D=M-1\n"
        ret_str += "A=D\n"
        ret_str += "D=M\n"
        ret_str += "@THAT\n"
        ret_str += "M=D\n"

        ret_str += "@endFrame\n"
        ret_str += "D=M-1\n"
        ret_str += "D=D-1\n"
        ret_str += "A=D\n"
        ret_str += "D=M\n"
        ret_str += "@THIS\n"
        ret_str += "M=D\n"

        ret_str += "@endFrame\n"
        ret_str += "D=M-1\n"
        for i in range(2):
            ret_str += "D=D-1\n"
        ret_str += "A=D\n"
        ret_str += "D=M\n"
        ret_str += "@ARG\n"
        ret_str += "M=D\n"

        ret_str += "@endFrame\n"
        ret_str += "D=M-1\n"
        for i in range(3):
            ret_str += "D=D-1\n"
        ret_str += "A=D\n"
        ret_str += "D=M\n"
        ret_str += "@LCL\n"
        ret_str += "M=D\n"
        ret_str += "@retAddr\n"
        ret_str += "A=M\n"
        ret_str += "0;JMP\n"

        self.output_file.write(ret_str)

    def writeInit(self):
        assembly_command = '@256\n'
        assembly_command += 'D = A\n'
        assembly_command += '@SP\n'
        assembly_command += 'M = D\n'
        self.output_file.write(assembly_command)
        self.writeCall('Sys.init', 0)
        # return

    def writeLabel(self, label: str):
        label = label.split()[1]
        assembly_command = "(" + label + ")\n"
        self.output_file.write(assembly_command)

    def writeGoto(self, label: str):
        assembly_command = "@" + label + "\n"
        assembly_command += "0;JMP\n"
        self.output_file.write(assembly_command)

    def writeIf(self, label: str):
        assembly_command = ""
        assembly_command += self.pop_assembly(assembly_command)
        assembly_command += "D = M\n"
        assembly_command += "@end" + str(self.current_label) + "\n"
        assembly_command += "D;JEQ\n"
        assembly_command += "@" + label + "\n"
        assembly_command += "0;JMP\n"
        assembly_command += "(end" + str(self.current_label) + ")\n"
        self.current_label += 1
        self.output_file.write(assembly_command)

    def writeCall(self, functionName: str, numArgs: int):
        ret_str = "@returnAddress" + str(self.current_label) + "\n"
        ret_str += "D=A\n"
        ret_str += self.push_template()

        ret_str += "@LCL\n"
        ret_str += "D=M\n"
        ret_str += self.push_template()

        ret_str += "@ARG\n"
        ret_str += "D=M\n"
        ret_str += self.push_template()

        ret_str += "@THIS\n"
        ret_str += "D=M\n"
        ret_str += self.push_template()

        ret_str += "@THAT\n"
        ret_str += "D=M\n"
        ret_str += self.push_template()

        ret_str += "@SP\n"
        ret_str += "D=M\n"
        for i in range(5):
            ret_str += "D=D-1\n"
        for i in range(numArgs):
            ret_str += "D = D-1\n"
        ret_str += "@ARG\n"
        ret_str += "M=D\n"

        ret_str += "@SP\n"
        ret_str += "D=M\n"
        ret_str += "@LCL\n"
        ret_str += "M=D\n"

        ret_str += "@" + functionName + "\n"
        ret_str += "0;JMP\n"

        ret_str += "(returnAddress" + str(self.current_label) + ")\n"
        self.current_label += 1

        self.output_file.write(ret_str)

    def writeFunction(self, functionName: str, numLocals: int):
        assembly_command = "(" + functionName + ")\n"
        for i in range(numLocals):
            assembly_command += "D = 0\n"
            assembly_command += self.push_template()
        self.output_file.write(assembly_command)