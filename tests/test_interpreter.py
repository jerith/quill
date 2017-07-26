
from support import BaseTest

class TestInterpreterBasic(BaseTest):
    def test_interpret(self):
        w_res = self.interpret_expr('''
            var x;
            x = 1;
            ''')
        assert w_res is self.space.w_None

    def test_var_assign(self):
        w_res = self.interpret_expr('''
            var x;
            x = 3;
            return x;
        ''')
        assert self.space.int_w(w_res) == 3

    def test_while_loop(self):
        w_r = self.interpret_expr('''
            var i, s;
            i = 0;
            s = 0;
            while i < 10 {
                i = i + 1;
                s = s + i;
            }
            return s;
            ''')
        assert self.space.int_w(w_r) == 55

    def test_simple_if(self):
        w_r = self.interpret_expr('''
            if 0 < 3 {
                return 3;
            }
            ''')
        assert self.space.int_w(w_r) == 3

    def test_logical_or_and(self):
        w_r = self.interpret_expr('''
            return 0 or 1;
            ''')
        assert self.space.int_w(w_r) == 1
        w_r = self.interpret_expr('''
            var x;
            return 15 or x;
            ''')
        # unitialized x ignored (for now)
        assert self.space.int_w(w_r) == 15
        w_r = self.interpret_expr('''
            return 1 and 2;
            ''')
        assert self.space.int_w(w_r) == 2
        w_r = self.interpret_expr('''
            var x;
            return 0 and x;
            ''')
        assert self.space.int_w(w_r) == 0
        w_r = self.interpret_expr('''
            return 1 and true;
            ''')
        assert self.space.w_True is w_r

    def test_mul_div(self):
        assert self.space.int_w(self.interpret_expr('return 13 // 2;')) == 6
        assert self.space.int_w(self.interpret_expr('return 2 * 6;')) == 12

    def test_operator_precedence(self):
        assert self.space.int_w(self.interpret_expr('return 2 + 2 * 2;')) == 6
        assert self.space.int_w(self.interpret_expr('return 2 * 2 + 2;')) == 6
        assert self.space.int_w(self.interpret_expr('return 2 * 2 and 2;')) == 2
        assert self.space.int_w(self.interpret_expr('return 2 and 2 * 2;')) == 4
        assert self.space.int_w(self.interpret_expr('return (2 + 2) * 2;')) == 8
        assert self.space.int_w(self.interpret_expr('return 2 * (2 + 2);')) == 8

    def test_longer_blocks(self):
        code = '\n'.join(['if 0 < 3 {'] + ['    1;'] * 300 + ['}'])
        self.interpret_expr(code) # assert did not crash

class TestInterpreter(BaseTest):
    def test_basic(self):
        w_res = self.interpret('''
            def main() {
                return 3;
            }
            ''')
        assert self.space.int_w(w_res) == 3

    def test_function_declaration_and_call(self):
        w_res = self.interpret('''
            def foo() {
                return 3;
            }

            def main() {
                return foo() + 1;
            }
            ''')
        assert self.space.int_w(w_res) == 4

    def test_function_call_args(self):
        w_res = self.interpret('''
            def foo(a0, a1) {
                return a0 + a1;
            }
            def main() {
                return foo(1, 3);
            }
            ''')
        assert self.space.int_w(w_res) == 4

    def test_recursive_call(self):
        w_res = self.interpret('''
            def fib(n) {
                if (n == 0) or (n == 1) {
                    return 1;
                }
                return fib(n - 1) + fib(n - 2);
            }
            def main() {
                return fib(5);
            }
            ''')
        assert self.space.int_w(w_res) == 8
