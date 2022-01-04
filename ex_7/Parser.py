
"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient
    access to their components.
    In addition, it removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is:
        # input_lines = input_file.read().splitlines()
        self.input_lines = input_file.read().splitlines()
        self.line_ind = 0
        self.line_num = len(self.input_lines)
        self.current_comment = self.input_lines[self.line_ind]


    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.line_ind < self.line_num

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        self.line_ind += 1
        if self.has_more_commands():
            self.current_comment = self.input_lines[self.line_ind]
            self.current_comment.strip()
            c = self.current_comment.find('//')
            if c != -1:
                self.current_comment = self.current_comment[:c]
        while self.current_comment == '':
            self.advance()

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        self.current_comment = self.current_comment.strip()
        if 'function' in self.current_comment:
            return 'C_FUNCTION'
        elif 'call' in self.current_comment:
            return 'C_CALL'
        elif 'pop' in self.current_comment:
            return 'C_POP'
        elif 'push' in self.current_comment:
            return 'C_PUSH'
        elif 'add' == self.current_comment or 'sub' == self.current_comment or 'neg' == self.current_comment or \
                'eq' == self.current_comment or 'gt' == self.current_comment or 'lt' == self.current_comment or \
                'and' == self.current_comment or 'or' == self.current_comment or 'not' == self.current_comment:
            return 'C_ARITHMETIC'
        elif 'if-goto' in self.current_comment:
            return 'C_IF'
        elif 'goto' in self.current_comment:
            return 'C_GOTO'
        elif 'return' in self.current_comment:
            return 'C_RETURN'
        return 'C_LABEL'


    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned.
            Should not be called if the current command is "C_RETURN".
        """
        if self.command_type == 'C_ARITHMETIC':
            return self.current_comment
        c = self.current_comment.find(" ")
        return self.current_comment[0:c]


    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP",
            "C_FUNCTION" or "C_CALL".
        """
        lst = self.current_comment.split()
        return int(lst[-1])
