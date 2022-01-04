"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter


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
        self.jack_tokenizer = JackTokenizer(input_stream)
        self.current_token_line = self.jack_tokenizer.tokens[0]
        self.token_counter = 0
        self.vmw = VMWriter(output_stream)
        self.if_counter = 0
        self.while_counter = 0
        self.symbol_table = SymbolTable()
        self.class_name = ""
        self.is_void = False
        self.num_of_vars = 0
        self.num_of_args = 0
        self.in_method = False

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.advance_tokenizer()  # class
        self.class_name = self.current_token_line  # class name
        self.advance_tokenizer()
        self.advance_tokenizer()  # {
        while self.is_class_var():
            self.compile_class_var_dec()
        while self.is_subroutine():
            self.compile_subroutine()
        # }

    def is_class_var(self):
        return 'static' in self.current_token_line or 'field' in self.current_token_line

    def is_subroutine(self):
        return 'constructor' in self.current_token_line or 'function' in self.current_token_line or \
               'method' in self.current_token_line

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        kind = self.current_token_line  # static/ field
        self.advance_tokenizer()
        n_type = self.current_token_line  # type
        self.advance_tokenizer()
        name = self.current_token_line  # name
        self.advance_tokenizer()
        self.symbol_table.define(name, n_type, kind)
        while ',' in self.current_token_line:
            self.advance_tokenizer()
            name = self.current_token_line  # name
            self.advance_tokenizer()
            self.symbol_table.define(name, n_type, kind)
        self.advance_tokenizer()  # ;

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        self.is_void = False
        self.in_method = False
        cfm = self.current_token_line
        self.advance_tokenizer()  # const, func, method..
        n_type = self.current_token_line
        self.advance_tokenizer()  # type
        if n_type == 'void':
            self.is_void = True
        if cfm == 'method' or 'constructor':
            self.in_method = True
        name = self.current_token_line  # name
        self.advance_tokenizer()
        self.advance_tokenizer()  # (
        self.compile_parameter_list()  # todo: check
        self.advance_tokenizer()  # )
        self.advance_tokenizer()  # {
        while 'var' == self.current_token_line:
            self.compile_var_dec()
        self.vmw.write_function(self.class_name + '.' + name, self.num_of_vars)
        if cfm == 'method':
            self.vmw.write_push('argument', 0)
            self.vmw.write_pop('pointer', 0)
        elif cfm == 'constructor':
            self.vmw.write_push('constant', self.symbol_table.var_count('field'))
            self.vmw.write_call('Memory.alloc', 1)
            self.vmw.write_pop('pointer', 0)
        self.compile_statements()  # todo: check
        self.advance_tokenizer()  # }

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        if ')' not in self.current_token_line:
            n_type = self.current_token_line  # type
            self.advance_tokenizer()
            name = self.current_token_line  # name
            self.advance_tokenizer()
            self.symbol_table.define(name, n_type, 'arg')
        while ')' not in self.current_token_line:
            self.advance_tokenizer()  # ,
            n_type = self.current_token_line  # type
            self.advance_tokenizer()
            name = self.current_token_line  # name
            self.advance_tokenizer()
            self.symbol_table.define(name, n_type, 'arg')

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.advance_tokenizer()  # var
        n_type = self.current_token_line  # type
        self.advance_tokenizer()
        name = self.current_token_line  # name
        self.advance_tokenizer()
        self.symbol_table.define(name, n_type, 'var')
        self.num_of_vars += 1
        while ',' in self.current_token_line:
            self.advance_tokenizer()  # ,
            name = self.current_token_line  # name
            self.advance_tokenizer()
            self.num_of_vars += 1
            self.symbol_table.define(name, n_type, 'var')
        self.advance_tokenizer()  # ;

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        while self.is_statement(self.current_token_line):
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

    def is_statement(self, cur_tok):
        return 'let' == cur_tok or 'do' == cur_tok or 'while' == cur_tok or 'if' == cur_tok or 'return' == cur_tok

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.advance_tokenizer()  # do
        class_name = self.current_token_line  # name of sub/class/var
        self.advance_tokenizer()
        is_dot = False
        func = ""
        if '.' in self.current_token_line:
            self.advance_tokenizer()  # .
            func = self.current_token_line  # name
            self.advance_tokenizer()
            is_dot = True
        self.advance_tokenizer()  # (
        if is_dot and self.symbol_table.index_of(class_name) != -1:
            self.vmw.write_push('this', self.symbol_table.index_of(class_name))
        self.num_of_args = 0
        self.compile_expression_list()
        if is_dot:  # p1.draw() or Output.blah() or Mall.buy()
            if self.symbol_table.index_of(class_name) != -1:  # p1.draw()
                self.num_of_args += 1  # for self
                # self.vmw.write_push('local', 0)  todo: ask why not ok
                class_name = self.symbol_table.type_of(class_name)  # Point for example
            self.vmw.write_call(class_name + "." + func, self.num_of_args)
        else:  # if its a method i guess
            if self.in_method:
                self.vmw.write_push('pointer', 0)
                self.num_of_args += 1
                self.vmw.write_call(self.class_name + "." + class_name, self.num_of_args)
            else:
                self.vmw.write_call(self.class_name + "." + class_name, self.num_of_args)
        self.vmw.write_pop('temp', 0)
        self.advance_tokenizer()  # )
        self.advance_tokenizer()  # ;

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.advance_tokenizer()  # let
        var1 = self.current_token_line  # name
        self.advance_tokenizer()
        if self.current_token_line == '[':
            self.advance_tokenizer()
            self.term_helper_push(var1)
            self.reverse_tokenizer()
            self.compile_expression()
            self.advance_tokenizer()
            self.vmw.write_arithmetic('add')
            self.advance_tokenizer()  # =
            var2 = self.distract_word(self.current_token_line)
            self.advance_tokenizer()
            if self.current_token_line == '[':
                self.advance_tokenizer()
                self.term_helper_push(var2)
                self.compile_expression()
                self.advance_tokenizer()
                self.vmw.write_arithmetic('add')
                self.vmw.write_pop('pointer', 1)
                self.vmw.write_push('that', 0)
                self.vmw.write_pop('temp', 0)
                self.vmw.write_pop('pointer', 1)
                self.vmw.write_push('temp', 0)
                self.vmw.write_pop('that', 0)
            else:  # just left is array
                self.vmw.write_pop('pointer', 1)
                self.compile_expression()
                self.vmw.write_pop('that', 0)
                # self.term_helper_pop(var1)
        else:
            self.advance_tokenizer()  # =
            var2 = self.current_token_line
            test = self.jack_tokenizer.return_cur_token(self.token_counter + 1)
            if test == '[':  # just right is array
                self.advance_tokenizer()
                self.term_helper_push(var2)
                self.compile_expression()
                self.advance_tokenizer()
                self.vmw.write_arithmetic('add')
                self.vmw.write_pop('pointer', 1)
                self.vmw.write_push('that', 0)
            else:
                self.compile_expression()
            if self.symbol_table.kind_of(var1) == "field":
                self.vmw.write_pop('this', self.symbol_table.index_of(var1))
            elif self.symbol_table.kind_of(var1) == 'static':
                self.vmw.write_pop('static', self.symbol_table.index_of(var1))
            elif self.symbol_table.kind_of(var1) == 'arg':
                self.vmw.write_pop('argument', self.symbol_table.index_of(var1))
            else:
                self.vmw.write_pop('local', self.symbol_table.index_of(var1))
        self.advance_tokenizer()  # ;

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.advance_tokenizer()  # while
        self.advance_tokenizer()  # (
        self.vmw.write_label("WHILE_LABEL " + str(self.while_counter))
        self.while_counter += 1
        self.compile_expression()
        self.advance_tokenizer()  # )
        self.advance_tokenizer()  # {
        self.vmw.write_arithmetic("not")  # todo: changed
        self.vmw.write_if("WHILE_LABEL " + str(self.while_counter))
        self.compile_statements()
        self.vmw.write_goto("WHILE_LABEL " + str(self.while_counter-1))
        self.vmw.write_label("WHILE_LABEL " + str(self.while_counter))
        self.while_counter += 1
        self.advance_tokenizer()  # }

    def compile_return(self) -> None:
        """Compiles a return statement."""
        if self.is_void:
            self.vmw.write_push('constant', 0)
        self.advance_tokenizer()  # return
        if self.current_token_line != ';':
            self.compile_expression()
        self.vmw.write_return()
        self.advance_tokenizer()  # ;

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.advance_tokenizer()  # if
        self.advance_tokenizer()  # (
        self.compile_expression()
        self.advance_tokenizer()  # )
        self.vmw.write_arithmetic("not")
        # self.advance_tokenizer()
        self.advance_tokenizer()  # {
        self.vmw.write_if("IF_LABEL " + str(self.if_counter))
        self.compile_statements()
        self.if_counter += 1
        self.advance_tokenizer()  # }
        if self.current_token_line == 'else':
            self.vmw.write_goto("IF_LABEL " + str(self.if_counter))
            self.vmw.write_label("IF_LABEL " + str(self.if_counter - 1))
            self.advance_tokenizer()  # else
            self.advance_tokenizer()  # {
            self.compile_statements()
            self.vmw.write_label("IF_LABEL " + str(self.if_counter))
            self.advance_tokenizer()  # }
        else:
            self.vmw.write_label("IF_LABEL " + str(self.if_counter - 1))
        self.if_counter += 1


    def compile_expression(self) -> None:
        """Compiles an expression."""
        op_dict = {"+": "add", "-": "sub", "&amp;": "and", "|": "or", "&lt;": "lt", "&gt;": "gt", "=": "eq"}
        self.compile_term()
        while self.is_operation():
            op = self.current_token_line  # op
            self.advance_tokenizer()
            self.compile_term()
            if op in op_dict:
                self.vmw.write_arithmetic(op_dict[op])
            else:
                if op == "*":
                    self.vmw.write_call("Math.multiply", 2)
                elif op == "/":
                    self.vmw.write_call("Math.divide", 2)

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
        term1 = self.current_token_line
        self.term_helper_push(term1)
        term2 = self.current_token_line
        if term2 == '(':
            self.advance_tokenizer()
            self.vmw.write_push('pointer', 0)
            self.num_of_args = 0
            self.compile_expression_list()
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
            self.advance_tokenizer()  # )

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        if ')' not in self.current_token_line:
            self.num_of_args += 1
            self.compile_expression()
        while ')' not in self.current_token_line:
            self.num_of_args += 1
            self.advance_tokenizer()  # ,
            self.compile_expression()

    def advance_tokenizer(self):
        self.token_counter += 1
        self.current_token_line = self.jack_tokenizer.tokens[self.token_counter]

    def distract_word(self, line):
        c1 = line.find(">") + 2
        line = line[c1:]
        c2 = line.find("<") - 1
        line = line[:c2]
        return line

    def token_type(self, line):
        jt = self.jack_tokenizer
        jt.curr_token_idx = self.token_counter
        if jt.token_type() == "KEYWORD":
            return "keyword"
        elif jt.token_type() == "SYMBOL":
            return "symbol"
        elif jt.token_type() == "IDENTIFIER":
            return "identifier"
        elif jt.token_type() == "INT_CONST":
            return "integerConstant"
        elif jt.token_type() == "STRING_CONST":
            return "stringConstant"



    def term_helper_push(self, term):
        if term == '~':
            self.advance_tokenizer()
            self.compile_term()
            self.vmw.write_arithmetic("not")
        elif term == '-':
            self.advance_tokenizer()
            self.compile_term()
            self.vmw.write_arithmetic("neg")
        elif term == '(':
            self.advance_tokenizer()
            self.compile_expression()
            self.advance_tokenizer()
        elif term == 'true':
            self.vmw.write_push("constant", 1)
            self.vmw.write_arithmetic("neg")
            self.advance_tokenizer()
        elif term.isdigit():
            self.vmw.write_push("constant", term)
            self.advance_tokenizer()
        elif term == 'this':
            self.vmw.write_push("pointer", 0)
            self.advance_tokenizer()
        elif term == 'that':
            self.vmw.write_push("pointer", 1)
            self.advance_tokenizer()
        elif term == 'null' or term == 'false':
            self.vmw.write_push("constant", 0)
            self.advance_tokenizer()
        elif self.symbol_table.kind_of(term):
            kind = self.symbol_table.kind_of(term)
            if self.symbol_table.kind_of(term) == 'field':
                self.vmw.write_push('this', self.symbol_table.index_of(term))
            elif self.symbol_table.kind_of(term) == 'static':
                self.vmw.write_push('static', self.symbol_table.index_of(term))
            elif self.symbol_table.kind_of(term) == 'arg':
                self.vmw.write_push('argument', self.symbol_table.index_of(term))
            else:
                self.vmw.write_push('local', self.symbol_table.index_of(term))
            self.advance_tokenizer()
        elif self.token_type(self.current_token_line) == "stringConstant":
            self.current_token_line = self.current_token_line[1:-1]
            term = term[1:-1]
            self.vmw.write_push('constant', len(term))
            self.vmw.write_call('String.new', 1)
            for char in term:
                self.vmw.write_push('constant', ord(char))
                self.vmw.write_call('String.appendChar', 2)
                # self.advance_tokenizer()
            self.advance_tokenizer()
        else:
            self.advance_tokenizer()

    def reverse_tokenizer(self):
        self.token_counter -= 1
        self.current_token_line = self.jack_tokenizer.tokens[self.token_counter]

