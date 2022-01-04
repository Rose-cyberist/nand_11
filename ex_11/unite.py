"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer

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
        self.jack_tokenizer = JackTokenizer(input_stream)
        self.current_token_line = self.jack_tokenizer.tokens[0]
        self.counter = 0
        self.compile_class()
        # self.current_token = self.get_token_from_line(self.current_token_line)

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.print_to_xml("<class>\n")
        self.print_to_xml(self.current_token_line)  # class
        self.print_to_xml(self.current_token_line)  # class name
        self.print_to_xml(self.current_token_line)  # {
        while self.is_class_var():
            self.compile_class_var_dec()
        while self.is_subroutine():
            self.compile_subroutine()
        # self.print_to_xml(self.current_token_line)  # }
        self.output_file.write("<symbol>" + self.current_token_line + "</symbol>\n")
        self.print_to_xml("</class>\n")

    def is_class_var(self):
        return 'static' == self.current_token_line or 'field' == self.current_token_line

    def is_subroutine(self):
        return 'constructor' == self.current_token_line or 'function' == self.current_token_line or \
               'method' == self.current_token_line

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.print_to_xml("<classVarDec>\n")
        self.print_to_xml(self.current_token_line)  # static/ field
        self.print_to_xml(self.current_token_line)  # type
        self.print_to_xml(self.current_token_line)  # vaName
        while ',' == self.current_token_line:
            self.print_to_xml(self.current_token_line)  # if we have multiple parameters
            self.print_to_xml(self.current_token_line)
        self.print_to_xml(self.current_token_line)  # ;
        self.print_to_xml("</classVarDec>\n")

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        self.print_to_xml("<subroutineDec>\n")
        self.print_to_xml(self.current_token_line)  # const, func, method..
        self.print_to_xml(self.current_token_line)  # type
        self.print_to_xml(self.current_token_line)  # name
        self.print_to_xml(self.current_token_line)  # (
        self.compile_parameter_list()
        self.print_to_xml(self.current_token_line)  # )
        self.print_to_xml("<subroutineBody>\n")
        self.print_to_xml(self.current_token_line)  # {
        while 'var' == self.current_token_line:
            self.compile_var_dec()
        self.compile_statements()
        self.print_to_xml(self.current_token_line)  # }
        self.print_to_xml("</subroutineBody>\n")
        self.print_to_xml("</subroutineDec>\n")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        self.print_to_xml("<parameterList>\n")
        if ')' != self.current_token_line:
            self.print_to_xml(self.current_token_line)  # type
            self.print_to_xml(self.current_token_line)  # name
        while ')' != self.current_token_line:
            self.print_to_xml(self.current_token_line)  # ,
            self.print_to_xml(self.current_token_line)  # type
            self.print_to_xml(self.current_token_line)  # name
        self.print_to_xml("</parameterList>\n")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.print_to_xml("<varDec>\n")  # type
        self.print_to_xml(self.current_token_line)  # var
        self.print_to_xml(self.current_token_line)  # type
        self.print_to_xml(self.current_token_line)  # name
        while ',' == self.current_token_line:
            self.print_to_xml(self.current_token_line)  # ,
            self.print_to_xml(self.current_token_line)  # name
        self.print_to_xml(self.current_token_line)  # ;
        self.print_to_xml("</varDec>\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        self.print_to_xml("<statements>\n")
        c = 0
        while self.is_statement(self.current_token_line):
            if 'let' == self.current_token_line:
                self.compile_let()
            if 'do' == self.current_token_line:
                self.compile_do()
            if 'while' == self.current_token_line:
                self.compile_while()
            if 'if' == self.current_token_line:
                self.compile_if()
            if 'return' == self.current_token_line:
                self.compile_return()
        self.print_to_xml("</statements>\n")

    def is_statement(self, cur_tok):
        b = 'let' == cur_tok or 'do' == cur_tok or 'while' == cur_tok or 'if' == cur_tok or 'return' == cur_tok
        return b

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.print_to_xml("<doStatement>\n")
        self.print_to_xml(self.current_token_line)  # do
        self.print_to_xml(self.current_token_line)  # name of sub/class/var
        if '.' == self.current_token_line:
            self.print_to_xml(self.current_token_line)  # .
            self.print_to_xml(self.current_token_line)  # name
        self.print_to_xml(self.current_token_line)  # (
        self.compile_expression_list()
        self.print_to_xml(self.current_token_line)  # )
        self.print_to_xml(self.current_token_line)  # ;
        self.print_to_xml("</doStatement>\n")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.print_to_xml("<letStatement>\n")
        self.print_to_xml(self.current_token_line)  # let
        self.print_to_xml(self.current_token_line)  # name
        if '[' == self.current_token_line:
            self.print_to_xml(self.current_token_line)  # [
            self.compile_expression()
            self.print_to_xml(self.current_token_line)  # ]
        self.print_to_xml(self.current_token_line)  # =
        self.compile_expression()
        self.print_to_xml(self.current_token_line)  # ;
        self.print_to_xml("</letStatement>\n")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.print_to_xml("<whileStatement>\n")
        self.print_to_xml(self.current_token_line)  # while
        self.print_to_xml(self.current_token_line)  # (
        self.compile_expression()
        self.print_to_xml(self.current_token_line)  # )
        self.print_to_xml(self.current_token_line)  # {
        self.compile_statements()
        self.print_to_xml(self.current_token_line)  # }
        self.print_to_xml("</whileStatement>\n")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.print_to_xml("<returnStatement>\n")
        self.print_to_xml(self.current_token_line)  # return
        if ';' != self.current_token_line:
            self.compile_expression()
        self.print_to_xml(self.current_token_line)  # ;
        self.print_to_xml("</returnStatement>\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.print_to_xml("<ifStatement>\n")
        self.print_to_xml(self.current_token_line)  # if
        self.print_to_xml(self.current_token_line)  # (
        self.compile_expression()
        self.print_to_xml(self.current_token_line)  # )
        self.print_to_xml(self.current_token_line)  # {
        self.compile_statements()
        self.print_to_xml(self.current_token_line)  # }
        if 'else' == self.current_token_line:
            self.print_to_xml(self.current_token_line)  # else
            self.print_to_xml(self.current_token_line)  # {
            self.compile_statements()
            self.print_to_xml(self.current_token_line)  # }
        self.print_to_xml("</ifStatement>\n")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.print_to_xml("<expression>\n")
        self.compile_term()
        while self.is_operation():
            self.print_to_xml(self.current_token_line)  # op
            self.compile_term()
        self.print_to_xml("</expression>\n")

    def is_operation(self):
        return '&lt;' == self.current_token_line or '&gt;' == self.current_token_line \
               or '=' in self.current_token_line or '&amp;' == self.current_token_line or \
               '+' == self.current_token_line or '-' == self.current_token_line or '*' == self.current_token_line \
               or '/' == self.current_token_line or "|" == self.current_token_line or '^' == self.current_token_line \
               or '#' == self.current_token_line

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
        self.print_to_xml("<term>\n")
        if self.is_unique():
            self.print_to_xml(self.current_token_line)  # the op
            self.compile_term()
        elif '(' == self.current_token_line:
            self.print_to_xml(self.current_token_line)  # (
            self.compile_expression()
            self.print_to_xml(self.current_token_line)  # )
        else:
            self.print_to_xml(self.current_token_line)  # id

        if '[' == self.current_token_line:
            self.print_to_xml(self.current_token_line)  # [
            self.compile_expression()
            self.print_to_xml(self.current_token_line)  # ]
        elif '.' == self.current_token_line:
            self.print_to_xml(self.current_token_line)  # .
            self.print_to_xml(self.current_token_line)  # name
            self.print_to_xml(self.current_token_line)  # (
            self.compile_expression_list()
            self.print_to_xml(self.current_token_line)  # )
        elif '(' == self.current_token_line:
            self.print_to_xml(self.current_token_line)  # (
            self.compile_expression_list()
            self.print_to_xml(self.current_token_line)  # )
        self.print_to_xml("</term>\n")

    def is_unique(self):
        return '~' == self.current_token_line or '-' == self.current_token_line

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.print_to_xml("<expressionList>\n")
        if ')' != self.current_token_line:
            self.compile_expression()
        while ')' != self.current_token_line:
            self.print_to_xml(self.current_token_line)  # ,
            self.compile_expression()
        self.print_to_xml("</expressionList>\n")

    def print_to_xml(self, s):
        if '<' in s and '>' in s:
            self.output_file.write(s)
        else:
            s = self.develop(s)
            self.output_file.write(s)
            self.advance_tokenizer()

    def develop(self, s):
        jt = self.jack_tokenizer
        jt.curr_token_idx = self.counter
        if jt.token_type() == "KEYWORD":
            return "<keyword>" + s + "</keyword>\n"
        elif jt.token_type() == "SYMBOL":
            return "<symbol>" + s + "</symbol>\n"
        elif jt.token_type() == "IDENTIFIER":
            return "<identifier>" + s + "</identifier>\n"
        elif jt.token_type() == "INT_CONST":
            return "<integerConstant>" + s + "</integerConstant>\n"
        elif jt.token_type() == "STRING_CONST":
            return "<stringConstant>" + s[1:-1] + "</stringConstant>\n"

    # def process(self, s):
    #     if self.current_token == s:
    #         self.print_to_xml(self.current_token_line)  # print the current token in tokenized file
    #     else:
    #         raise Exception("Syntax Error")
    #     self.advance_tokenizer()

    def advance_tokenizer(self):
        self.counter += 1
        self.current_token_line = self.jack_tokenizer.tokens[self.counter]
        # self.current_token = self.get_token_from_line(self.current_token_line)

    # def get_token_from_line(self, line):
    #     c1 = line.find(">") + 2
    #     line = line[c1:]
    #     c2 = line.find("<") + 1
    #     line = line[:c2]
    #     return line





    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.advance_tokenizer()  # let
        name = self.current_token_line
        self.advance_tokenizer()  # name
        if '[' in self.current_token_line:
            self.advance_tokenizer()  # [
            self.compile_expression()
            self.advance_tokenizer()  # ]
        self.advance_tokenizer()  # =
        self.compile_expression()
        if self.symbol_table.kind_of(name) == 'static' or self.symbol_table.kind_of(name) == "field":
            self.vmw.write_pop('this', self.symbol_table.index_of(name))
        else:
            self.vmw.write_pop('local', self.symbol_table.index_of(name))
        self.advance_tokenizer()  # ;





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
        term1 = self.current_token_line
        if term1 == '~':
            self.advance_tokenizer()
            self.compile_term()
            self.vmw.write_arithmetic("not")
        elif term1 == '-':
            self.advance_tokenizer()
            self.compile_term()
            self.vmw.write_arithmetic("neg")
        elif term1 == '(':
            self.advance_tokenizer()
            self.compile_expression()
            self.advance_tokenizer()
        elif term1 == 'true':
            self.vmw.write_push("constant", 1)
            self.vmw.write_arithmetic("neg")
            self.advance_tokenizer()
        elif term1.isdigit():
            self.vmw.write_push("constant", term1)
            self.advance_tokenizer()
        elif term1 == 'this':
            self.vmw.write_push("pointer", 0)
            self.advance_tokenizer()
        elif term1 == 'that':
            self.vmw.write_push("pointer", 1)
            self.advance_tokenizer()
        elif term1 == 'null' or term1 == 'false':
            self.vmw.write_push("constant", 0)
            self.advance_tokenizer()
        elif self.symbol_table.kind_of(term1):
            if self.symbol_table.kind_of(term1) == 'field' or self.symbol_table.kind_of(term1) == 'static':
                self.vmw.write_push('this', self.symbol_table.index_of(term1))
            else:
                self.vmw.write_push('local', self.symbol_table.index_of(term1))
            self.advance_tokenizer()
        elif self.token_type(self.current_token_line) == "stringConstant":
            self.vmw.write_push('constant', len(term1))
            self.vmw.write_call('String.new', 1)
            for char in term1:
                self.vmw.write_push('constant', ord(char))
                self.vmw.write_call('String.appendChar', 2)
                self.advance_tokenizer()
        else:
            self.advance_tokenizer()

        term2 = self.current_token_line
        if term2 == '(':
            self.advance_tokenizer()
            self.vmw.write_push('pointer', 0)
            num_of_args = self.compile_expression_list()
            self.vmw.write_call(self.class_name + '.' + term1,
                                1 + self.num_of_args)  # todo count somehow number of arguments
        if term2 == '[':
            self.advance_tokenizer()
            self.compile_expression()
            self.vmw.write_arithmetic('ADD')
            self.advance_tokenizer()
            self.vmw.write_pop('pointer', 1)
            self.vmw.write_push('that', 0)
        if term2 == '.':
            self.advance_tokenizer()
            func_name = self.current_token_line
            self.advance_tokenizer()
            self.advance_tokenizer()  # (
            if self.symbol_table.index_of(term1) != -1:
                self.num_of_args = 1
                self.compile_expression_list()
                self.vmw.write_call(term1 + '.' + func_name, self.num_of_args)
            else:
                self.num_of_args = 0
                self.compile_expression_list()
                self.vmw.write_call(term1 + '.' + func_name, self.num_of_args)
                # self.vmw.write_push('this', 0)
                # num_of_args = self.num_of_args + 1
                # self.vmw.write_call(self.symbol_table.type_of(term1) + '.' + func_name, num_of_args)
            self.advance_tokenizer()  # )