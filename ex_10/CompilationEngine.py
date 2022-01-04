"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: typing.TextIO,
                 output_stream: typing.TextIO) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.output_file = output_stream
        self.input_file = input_stream
        self.current_token_line = self.input_file.readline()
        # self.current_token = self.get_token_from_line(self.current_token_line)

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.print_to_xml("<class>")
        self.print_to_xml(self.current_token_line)  # class
        self.print_to_xml(self.current_token_line)  # class name
        self.print_to_xml(self.current_token_line)  # {
        while self.is_class_var():
            self.compile_class_var_dec()
        while self.is_subroutine():
            self.compile_subroutine()
        self.print_to_xml(self.current_token_line)  # }
        self.print_to_xml("</class>")

    def is_class_var(self):
        return 'static' in self.current_token_line or 'field' in self.current_token_line

    def is_subroutine(self):
        return 'constructor' in self.current_token_line or 'function' in self.current_token_line or \
               'method' in self.current_token_line

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.print_to_xml("<classVarDec>")
        self.print_to_xml(self.current_token_line)  # static/ field
        self.print_to_xml(self.current_token_line)  # type
        while ',' in self.current_token_line or 'identifier' in self.current_token_line:
            self.print_to_xml(self.current_token_line)  # if we have multiple parameters
        self.print_to_xml(self.current_token_line)  # ;
        self.print_to_xml("</classVarDec")

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        self.print_to_xml("<subroutineDec>")
        self.print_to_xml(self.current_token_line)  # const, func, method..
        self.print_to_xml(self.current_token_line)  # type
        self.print_to_xml(self.current_token_line)  # name
        self.print_to_xml(self.current_token_line)  # (
        self.compile_parameter_list()
        self.print_to_xml(self.current_token_line)  # )
        self.print_to_xml("<subroutineBody>")
        self.print_to_xml(self.current_token_line)  # {
        while 'var' in self.current_token_line:
            self.compile_var_dec()
        self.compile_statements()
        self.print_to_xml(self.current_token_line)  # }
        self.print_to_xml("</subroutineBody")
        self.print_to_xml("</subroutineDec>")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self.print_to_xml("<parameterList>")
        if ')' not in self.current_token_line:
            self.print_to_xml(self.current_token_line)  # type
            self.print_to_xml(self.current_token_line)  # name
        while ')' not in self.current_token_line:
            self.print_to_xml(self.current_token_line)  # ,
            self.print_to_xml(self.current_token_line)  # type
            self.print_to_xml(self.current_token_line)  # name
        self.print_to_xml("</parameterList>")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.print_to_xml("<varDec>")  # type
        self.print_to_xml(self.current_token_line)  # var
        self.print_to_xml(self.current_token_line)  # type
        self.print_to_xml(self.current_token_line)  # name
        while ',' in self.current_token_line:
            self.print_to_xml(self.current_token_line)  # ,
            self.print_to_xml(self.current_token_line)  # name
        self.print_to_xml(self.current_token_line)  # ;
        self.print_to_xml("</varDec>")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        self.print_to_xml("<statements>")
        if 'let' in self.current_token_line:
            self.compile_let()
        if 'do' in self.current_token_line:
            self.compile_do()
        if 'while' in self.current_token_line:
            self.compile_while()
        if 'if' in self.current_token_line:
            self.compile_if()
        if 'return' in self.current_token_line:
            self.compile_return()
        self.print_to_xml("</statements>")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.print_to_xml("<doStatement>")
        self.print_to_xml(self.current_token_line)  # do
        self.print_to_xml(self.current_token_line)  # name of sub/class/var
        if '.' in self.current_token_line:
            self.print_to_xml(self.current_token_line)  # .
            self.print_to_xml(self.current_token_line)  # name
        self.print_to_xml(self.current_token_line)  # (
        self.compile_expression_list()
        self.print_to_xml(self.current_token_line)  # )
        self.print_to_xml(self.current_token_line)  # ;
        self.print_to_xml("</doStatement>")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.print_to_xml("<letStatement>")
        self.print_to_xml(self.current_token_line)  # let
        self.print_to_xml(self.current_token_line)  # name
        if '[' in self.current_token_line:
            self.print_to_xml(self.current_token_line)  # [
            self.compile_expression()
            self.print_to_xml(self.current_token_line)  # ]
        self.print_to_xml(self.current_token_line)  # =
        self.compile_expression()
        self.print_to_xml(self.current_token_line)  # ;
        self.print_to_xml("</letStatement>")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.print_to_xml("<whileStatement>")
        self.print_to_xml(self.current_token_line)  # while
        self.print_to_xml(self.current_token_line)  # (
        self.compile_expression()
        self.print_to_xml(self.current_token_line)  # )
        self.print_to_xml(self.current_token_line)  # {
        self.compile_statements()
        self.print_to_xml(self.current_token_line)  # }
        self.print_to_xml("</whileStatement>")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.print_to_xml("<returnStatement>")
        self.print_to_xml(self.current_token_line)  # return
        self.print_to_xml(self.current_token_line)  # ;
        self.print_to_xml("</returnStatement>")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.print_to_xml("<ifStatement>")
        self.print_to_xml(self.current_token_line)  # if
        self.print_to_xml(self.current_token_line)  # (
        self.compile_expression()
        self.print_to_xml(self.current_token_line)  # )
        self.print_to_xml(self.current_token_line)  # {
        self.compile_statements()
        self.print_to_xml(self.current_token_line)  # }
        if 'else' in self.current_token_line:
            self.print_to_xml(self.current_token_line)  # else
            self.print_to_xml(self.current_token_line)  # {
            self.compile_statements()
            self.print_to_xml(self.current_token_line)  # }
        self.print_to_xml("</ifStatement>")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.print_to_xml("<expression>")
        self.compile_term()
        while self.is_operation():
            self.print_to_xml(self.current_token_line)  # op
            self.compile_term()
        self.print_to_xml(self.current_token_line)  # ;
        self.print_to_xml("</expression>")

    def is_operation(self):
        return '&lt;' in self.current_token_line or '&gt;' in self.current_token_line \
               or '=' in self.current_token_line or '&amp;' in self.current_token_line or \
               '+' in self.current_token_line or '-' in self.current_token_line or '*' in self.current_token_line \
               or '/' in self.current_token_line or "|" in self.current_token_line

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        self.print_to_xml("<term>")
        if self.is_unique():
            self.print_to_xml(self.current_token_line)  # the op
            self.compile_term()
        elif ' ( ' in self.current_token_line:
            self.print_to_xml(self.current_token_line)  # (
            self.compile_expression()
            self.print_to_xml(self.current_token_line)  # )
        else:
            self.print_to_xml(self.current_token_line)  # id

        if ' [ ' in self.current_token_line:
            self.print_to_xml(self.current_token_line)  # [
            self.compile_expression()
            self.print_to_xml(self.current_token_line)  # ]
        elif ' . ' in self.current_token_line:
            self.print_to_xml(self.current_token_line)  # .
            self.print_to_xml(self.current_token_line)  # name
            self.print_to_xml(self.current_token_line)  # (
            self.compile_expression_list()
            self.print_to_xml(self.current_token_line)  # )
        elif ' ( ' in self.current_token_line:
            self.print_to_xml(self.current_token_line)  # (
            self.compile_expression_list()
            self.print_to_xml(self.current_token_line)  # )
        self.print_to_xml("</term")

    def is_unique(self):
        return '~' in self.current_token_line or '-' in self.current_token_line

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.print_to_xml("<expressionList>")
        if ')' not in self.current_token_line:
            self.compile_expression()
        while ')' not in self.current_token_line:
            self.print_to_xml(self.current_token_line)  # ,
            self.compile_expression()
        self.print_to_xml("</expressionList>")

    def print_to_xml(self, s):
        self.output_file.write(s)
        self.advance_tokenizer()

    # def process(self, s):
    #     if self.current_token == s:
    #         self.print_to_xml(self.current_token_line)  # print the current token in tokenized file
    #     else:
    #         raise Exception("Syntax Error")
    #     self.advance_tokenizer()

    def advance_tokenizer(self):
        self.current_token_line = self.input_file.readline()
        # self.current_token = self.get_token_from_line(self.current_token_line) #todo: regard the case where no more lines in the file

    # def get_token_from_line(self, line):
    #     c1 = line.find(">") + 2
    #     line = line[c1:]
    #     c2 = line.find("<") + 1
    #     line = line[:c2]
    #     return line
