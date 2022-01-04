
    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.advance_tokenizer()
        var1 = self.distract_word(self.current_token_line)
        self.advance_tokenizer()
        if self.distract_word(self.current_token_line) == '[':
            self.advance_tokenizer()
            self.term_helper_push(var1)
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
            else:
                self.compile_expression()
                self.term_helper_pop(var1)
        else:
            self.advance_tokenizer()  # =
            self.compile_expression()
            self.term_helper_pop(var1)

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
            if self.symbol_table.index_of(self.current_token_line) != -1:
                self.num_of_args = 1
                self.compile_expression_list()
                self.vmw.write_call(term1 + '.' + func_name, self.num_of_args)
            else:
                self.num_of_args = 0
                self.compile_expression_list()
                self.vmw.write_call(term1 + '.' + func_name, self.num_of_args)
            self.advance_tokenizer()  # )

    def term_helper_pop(self, term):
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
            self.vmw.write_pop("constant", 1)
            self.vmw.write_arithmetic("neg")
            self.advance_tokenizer()
        elif term.isdigit():
            self.vmw.write_pop("constant", term)
            self.advance_tokenizer()
        elif term == 'this':
            self.vmw.write_pop("pointer", 0)
            self.advance_tokenizer()
        elif term == 'that':
            self.vmw.write_pop("pointer", 1)
            self.advance_tokenizer()
        elif term == 'null' or term == 'false':
            self.vmw.write_pop("constant", 0)
            self.advance_tokenizer()
        elif term == self.symbol_table.kind_of(term):
            self.vmw.write_pop(self.symbol_table.kind_of(term), self.symbol_table.index_of(term))
            self.advance_tokenizer()
        elif self.token_type(self.current_token_line) == "stringConstant":
            self.vmw.write_pop('constant', len(term))
            self.vmw.write_call('String.new', 1)
            for char in term:
                self.vmw.write_pop('constant', ord(char))
                self.vmw.write_call('String.appendChar', 2)
                self.advance_tokenizer()
        else:
            self.advance_tokenizer()

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
        elif term == self.symbol_table.kind_of(term):
            self.vmw.write_push(self.symbol_table.kind_of(term), self.symbol_table.index_of(term))
            self.advance_tokenizer()
        elif self.token_type(self.current_token_line) == "stringConstant":
            self.vmw.write_push('constant', len(term))
            self.vmw.write_call('String.new', 1)
            for char in term:
                self.vmw.write_push('constant', ord(char))
                self.vmw.write_call('String.appendChar', 2)
                self.advance_tokenizer()
        else:
            self.advance_tokenizer()

