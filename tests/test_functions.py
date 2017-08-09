import py
from support import BaseTest


class TestFunctions(BaseTest):
    def test_simple_function(self):
        w_res = self.interpret('''
            def foo() {
                return 13
            }

            def main() {
                return foo()
            }
        ''')
        assert self.space.int_w(w_res) == 13

    def test_simple_args(self):
        w_res = self.interpret('''
            def foo(a, b) {
                return a + b
            }

            def main() {
                return foo(10, 3)
            }
        ''')
        assert self.space.int_w(w_res) == 13

    def test_named_args(self):
        py.test.skip("implement named args properly")
        w_res = self.interpret('''
            def foo(a, b) {
                return a * 10 + b
            }

            def main() {
                return foo(a=2, b=3)
            }
        ''')
        assert self.space.int_w(w_res) == 23

        w_res = self.interpret('''
            def foo(a, b) {
                return a * 10 + b
            }

            def main() {
                return foo(b=3, a=2)
            }
        ''')
        assert self.space.int_w(w_res) == 23

    def test_named_args_illegal(self):
        py.test.skip("implement named args properly")
        self.assert_parse_error('''
            def foo(a, b) {
                return a + b
            }

            def main() {
                return foo(a=10, 3)
            }
        ''')
