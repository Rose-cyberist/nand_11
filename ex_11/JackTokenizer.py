"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        self.curr_token_idx = 0
        self.input_lines = input_stream.read().splitlines()
        self.clean_lines()
        self.tokens = []
        self.convert_to_tokens()
        self.token_num = len(self.tokens)

    def return_cur_token(self, ind):
        return self.tokens[ind]

    def clean_lines(self) -> None:
        """
        Cleans lines from comments end trash
        """
        clean_file = []
        in_comment = False
        for line in self.input_lines:
            line = line.strip()
            if line[:3] == '/**' or line[:2] == '/*':
                in_comment = True
            if not in_comment:
                if "//" not in line[:2] and "//" in line:
                    s = line.split("//")[0].strip()
                    clean_file.append(s)
                elif "/*" not in line[:2] and "/*" in line:
                    s = line.split("//")[0].strip()
                    clean_file.append(s)
                elif "//" not in line and line != "":
                    clean_file.append(line)
            if line[-3:] == '**/' or line[-2:] == '*/':
                in_comment = False
        self.input_lines = clean_file

    def convert_to_tokens(self) -> None:
        for line in self.input_lines:
            token_lst = self.tokens_line(line)
            for i in range(len(token_lst)):
                if token_lst[i] != '':
                    if token_lst[i] == "&":
                        token_lst[i] = "&amp;"
                    if token_lst[i] == "<":
                        token_lst[i] = "&lt;"
                    if token_lst[i] == ">":
                        token_lst[i] = "&gt;"
                    if token_lst[i] == "\"":
                        token_lst[i] = "&quot;"
                    self.tokens.append(token_lst[i])

    def tokens_line(self, line):
        line = line.strip()
        new_line = []
        if '"' in line:
            match = re.search(r"\"[^\"]*\"", line)
            new_line.extend(self.tokens_line(match.string[:match.start()]))
            end = match.end()
            new_line.append(match.string[match.start():end])
            new_line.extend(self.tokens_line(match.string[match.end():]))
        else:
            split_line = line.split()
            for inner_line in split_line:
                new_line.extend(self.inner_line_tokens(inner_line))
        return new_line

    def inner_line_tokens(self, inner_line):
        new_inner_line = []
        if inner_line is None:
            return new_inner_line
        inner_line = inner_line.strip()
        match = re.search(r"([\&\|\)\(<=\+\-\*>\\/.;,\]\[}{~])", inner_line)
        if match:
            new_inner_line.extend(self.inner_line_tokens(match.string[:match.start()]))
            new_inner_line.append(match.string[match.start()])
            new_inner_line.extend(self.inner_line_tokens(match.string[match.end():]))
        else:
            new_inner_line.append(inner_line)
        return new_inner_line

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        # Your code goes here!
        return self.curr_token_idx <= self.token_num

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token.
        This method should be called if has_more_tokens() is true.
        Initially there is no current token.
        """
        # Your code goes here!
        self.curr_token_idx += 1

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        # Your code goes here!
        keyword_dict = {'class': 'CLASS', 'method': 'METHOD', 'function': 'FUNCTION', 'constructor': 'CONSTRUCTOR',
                        'int': 'INT', 'boolean': 'BOOLEAN', 'char': 'CHAR', 'void': 'VOID',
                        'var': 'VAR', 'static': 'STATIC', 'field': 'FIELD', 'let': 'LET', 'do': 'DO', 'if': 'IF',
                        'else': 'ELSE', 'while': 'WHILE', 'return': 'RETURN', 'true': 'TRUE', 'false': 'FALSE',
                        'null': 'NULL', 'this': 'THIS'}
        symbol_lst = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;',
                      '^', '#', '&quot;', '=', '~']
        if self.tokens[self.curr_token_idx] in keyword_dict:
            return "KEYWORD"
        elif self.tokens[self.curr_token_idx] in symbol_lst:
            return "SYMBOL"
        elif self.tokens[self.curr_token_idx].isdigit():
            return "INT_CONST"
        elif self.tokens[self.curr_token_idx].startswith('"') and self.tokens[self.curr_token_idx].endswith('"'):
            return 'STRING_CONST'
        elif not self.tokens[self.curr_token_idx][0].isdigit():
            return "IDENTIFIER"

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT",
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO",
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        # Your code goes here!
        keyword_dict = {'class': 'CLASS', 'method': 'METHOD', 'function': 'FUNCTION', 'constructor': 'CONSTRUCTOR',
                        'int': 'INT', 'boolean': 'BOOLEAN', 'char': 'CHAR', 'void': 'VOID',
                        'var': 'VAR', 'static': 'STATIC', 'field': 'FIELD', 'let': 'LET', 'do': 'DO', 'if': 'IF',
                        'else': 'ELSE', 'while': 'WHILE', 'return': 'RETURN', 'true': 'TRUE', 'false': 'FALSE',
                        'null': 'NULL', 'this': 'THIS'}
        return keyword_dict[self.tokens[self.curr_token_idx]]

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
        """
        # Your code goes here!
        return self.tokens[self.curr_token_idx]
        pass

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
        """
        # Your code goes here!
        return self.tokens[self.curr_token_idx]
        pass

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
        """
        # Your code goes here!
        return self.tokens[self.curr_token_idx]
        pass

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double
            quotes. Should be called only when token_type() is "STRING_CONST".
        """
        # Your code goes here!
        return self.tokens[self.curr_token_idx][1:-1]
        pass
