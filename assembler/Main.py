"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser_ex6 import Parser
from Code import Code


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    #
    # You should use the two-pass implementation suggested in the book:
    #
    # *Initialization*
    # Initialize the symbol table with all the predefined symbols and their
    # pre-allocated RAM addresses, according to section 6.2.3 of the book.
    #
    # *First Pass*
    # Go through the entire assembly program, line by line, and build the symbol
    # table without generating any code. As you march through the program lines,
    # keep a running number recording the ROM address into which the current
    # command will be eventually loaded.
    # This number starts at 0 and is incremented by 1 whenever a C-instruction
    # or an A-instruction is encountered, but does not change when a label
    # pseudo-command or a comment is encountered. Each time a pseudo-command
    # (Xxx) is encountered, add a new entry to the symbol table, associating
    # Xxx with the ROM address that will eventually store the next command in
    # the program.
    # This pass results in entering all the program’s labels along with their
    # ROM addresses into the symbol table.
    # The program’s variables are handled in the second pass.
    #
    # *Second Pass*
    # Now go again through the entire program, and parse each line.
    # Each time a symbolic A-instruction is encountered, namely, @Xxx where Xxx
    # is a symbol and not a number, look up Xxx in the symbol table.
    # If the symbol is found in the table, replace it with its numeric meaning
    # and complete the command’s translation.
    # If the symbol is not found in the table, then it must represent a new
    # variable. To handle it, add the pair (Xxx,n) to the symbol table, where n
    # is the next available RAM address, and complete the command’s translation.
    # The allocated RAM addresses are consecutive numbers, starting at address
    # 16 (just after the addresses allocated to the predefined symbols).
    # After the command is translated, write the translation to the output file.
    pass


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
