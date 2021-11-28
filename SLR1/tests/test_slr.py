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
        print()
        assert self.slr.run("".split(" "), True) == SLRRunnerException(SLRErrId.NON_GRAMMAR_SYMBOL_TOKEN)
        assert self.slr.run("a".split(" "), True) == SLRRunnerException(SLRErrId.EMPTY_INPUT_STACK)
        assert self.slr.run("a b c".split(" "), True) == SLRRunnerException(SLRErrId.EMPTY_INPUT_STACK)

    def test_run_terminal_out_of_grammar(self):
        print()
        assert self.slr.run("d $".split(" "), True) == SLRRunnerException(SLRErrId.NON_GRAMMAR_SYMBOL_TOKEN)
        assert self.slr.run("a b d $".split(" "), True) == SLRRunnerException(SLRErrId.NON_GRAMMAR_SYMBOL_TOKEN)
        assert self.slr.run("a b d c $".split(" "), True) == SLRRunnerException(SLRErrId.NON_GRAMMAR_SYMBOL_TOKEN)

    def test_run_nonterminal_out_of_grammar(self):
        print()
        assert self.slr.run("A b $".split(" "), True) == SLRRunnerException(SLRErrId.NONTERMINAL_IN_INPUT_STACK)
        assert self.slr.run("a B c $".split(" "), True) == SLRRunnerException(SLRErrId.NONTERMINAL_IN_INPUT_STACK)
        assert self.slr.run("a b C c $".split(" "), True) == SLRRunnerException(SLRErrId.NONTERMINAL_IN_INPUT_STACK)

    def test_run_empty_symbols(self):
        print()
        assert self.slr.run("e $".split(" "), True) == SLRRunnerException(SLRErrId.NON_GRAMMAR_SYMBOL_TOKEN)
        assert self.slr.run("a e $".split(" "), True) == SLRRunnerException(SLRErrId.NON_GRAMMAR_SYMBOL_TOKEN)
        assert self.slr.run("a e c $".split(" "), True) == SLRRunnerException(SLRErrId.NON_GRAMMAR_SYMBOL_TOKEN)
        assert self.slr.run("a b e $".split(" "), True) == SLRRunnerException(SLRErrId.NON_GRAMMAR_SYMBOL_TOKEN)
