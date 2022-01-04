"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads and assembly language 
    command, parses it, and provides convenient access to the commands 
    components (fields and symbols). In addition, removes all white space and 
    comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is:
        self.input_lines = input_file.read().splitlines()
        self.line_idx = 0
        self.line_num = len(self.input_lines)
        self.current_comment = self.input_lines[0]
        self.shifted = 0

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.line_idx < self.line_num


    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        while self.input_lines[self.line_idx] == '' or self.input_lines[self.line_idx][0] == '/':
            self.input_lines.remove(self.input_lines[self.line_idx])
            self.line_num -= 1


        if self.has_more_commands():
            self.current_comment = self.input_lines[self.line_idx]
            self.remove_slash()
        self.line_idx += 1


    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if self.current_comment[0] == '@':
            self.shifted = 0
            return "A_COMMAND"
        if ';' in self.current_comment or '=' in self.current_comment or '>>' in self.current_comment or '<<' in self.current_comment:
            if '<<' in self.current_comment or '>>' in self.current_comment:
                self.shifted = 1
            return "C_COMMAND"
        if '(' == self.current_comment[0] and ')' == self.current_comment[-1]:
            self.shifted = 0
            return "L_COMMAND"


    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or
            "L_COMMAND".
        """
        if self.command_type() == "A_COMMAND":
            self.current_comment.lstrip()
            self.current_comment = self.current_comment[1:]
            return self.current_comment
        if self.command_type() == "L_COMMAND":
            return self.current_comment[1:-1]


    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        if self.command_type() == "C_COMMAND":
            if '=' in self.current_comment:
                eql_idx = self.current_comment.find('=')
                return self.current_comment[:eql_idx]
        return "null"

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        if self.command_type() == "C_COMMAND":
            if ';' in self.current_comment and '=' in self.current_comment:
                sc_idx = self.current_comment.find(';')
                eql_idx = self.current_comment.find('=')
                return self.current_comment[eql_idx+1:sc_idx]
            elif ';' in self.current_comment:
                sc_idx = self.current_comment.find(';')
                return self.current_comment[:sc_idx]
            elif '=' in self.current_comment:
                eql_idx = self.current_comment.find('=')
                return self.current_comment[eql_idx+1:]
            else:
                return 'null'
        else:
            return 'null'

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        if self.command_type() == "C_COMMAND" and ';' in self.current_comment:
            sc_idx = self.current_comment.find(';')
            return self.current_comment[sc_idx+1:]
        return 'null'

    def remove_slash(self):
        if '//' in self.current_comment:
            s_ind = self.current_comment.find('/')
            self.current_comment = self.current_comment[:s_ind].rstrip()

        self.current_comment = self.current_comment.lstrip()
        self.current_comment = self.current_comment.rstrip()