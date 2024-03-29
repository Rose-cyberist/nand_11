"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from Parser import Parser
from CodeWriter import CodeWriter


def translate_file(
        input_file: typing.TextIO, output_file: typing.TextIO, cw) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # Note: you can get the input file's name using:
    # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
    input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
    cw.set_file_name(input_filename)
    p = Parser(input_file)
    while p.has_more_commands():
        p.advance()
        if p.has_more_commands():
            cmd = p.current_comment.strip()
            output_file.write("//" + cmd + "\n")
            ct = p.command_type()
            if ct == "C_ARITHMETIC":
                cw.write_arithmetic(cmd)
            elif ct == "C_POP" or ct == "C_PUSH":
                cw.write_push_pop(ct, cmd.split()[1], p.arg2())
            elif ct == "C_LABEL":
                cw.writeLabel(cmd)
            elif ct == "C_GOTO":
                cw.writeGoto(cmd.split()[1])
            elif ct == "C_IF":
                cw.writeIf(cmd.split()[1])
            elif ct == "C_CALL":
                lst = cmd.split()
                cw.writeCall(lst[1], int(lst[2]))
            elif ct == "C_RETURN":
                cw.writeReturn()
            elif ct == "C_FUNCTION":
                lst = cmd.split()
                cw.writeFunction(lst[1], int(lst[2]))
    # cw.close()


if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    with open(output_path, 'w') as output_file:
        cw = CodeWriter(output_file)
        cw.writeInit()
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file, cw)