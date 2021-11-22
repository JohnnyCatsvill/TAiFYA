from SLR1 import *


class TestABC:
    RULES = [
       ["S", ["A B C $"]],
       ["A", ["a A"]],
       ["A", ["e"]],
       ["B", ["b B"]],
       ["B", ["e"]],
       ["C", ["c C"]],
       ["C", ["e"]],
    ]

    slr = SLR(RULES)

    def test_run_normal(self):
        assert self.slr.run("a b c $".split(" ")) == RUNNER_OK
        assert self.slr.run("a a b b c c $".split(" ")) == RUNNER_OK

    def test_run_with_e(self):
        assert self.slr.run("$".split(" ")) == RUNNER_OK
        assert self.slr.run("a $".split(" ")) == RUNNER_OK
        assert self.slr.run("b $".split(" ")) == RUNNER_OK
        assert self.slr.run("c $".split(" ")) == RUNNER_OK
        assert self.slr.run("a c $".split(" ")) == RUNNER_OK
        assert self.slr.run("b c $".split(" ")) == RUNNER_OK

    def test_run_lost_end(self):
        assert self.slr.run("".split(" "), True) == RUNNER_FAIL
        assert self.slr.run("a".split(" "), True) == RUNNER_FAIL
        assert self.slr.run("a b c".split(" "), True) == RUNNER_FAIL

    def test_run_terminal_out_of_grammar(self):
        assert self.slr.run("d $".split(" "), True) == RUNNER_FAIL
        assert self.slr.run("a b d $".split(" "), True) == RUNNER_FAIL
        assert self.slr.run("a b d c $".split(" "), True) == RUNNER_FAIL

    def test_run_nonterminal_out_of_grammar(self):
        assert self.slr.run("A b $".split(" "), True) == RUNNER_FAIL
        assert self.slr.run("a B c $".split(" "), True) == RUNNER_FAIL
        assert self.slr.run("a b C c $".split(" "), True) == RUNNER_FAIL

    def test_run_empty_symbols(self):
        assert self.slr.run("e $".split(" "), True) == RUNNER_FAIL
        assert self.slr.run("a e $".split(" "), True) == RUNNER_FAIL
        assert self.slr.run("a e c $".split(" "), True) == RUNNER_FAIL
        assert self.slr.run("a b e $".split(" "), True) == RUNNER_FAIL
