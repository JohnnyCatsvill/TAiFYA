from SLR1 import *


class F:
    a1: callable = lambda x: print(x)
    a2: callable = lambda x: x
    a3: callable = lambda x, y: x+y


RULES = [
    ["S", ["A B C $"], [None, None, F.a1, None]],
    ["A", ["A a"]],
    ["A", ["e"]],
    ["B", ["B b"]],
    ["B", ["e"]],
    ["C", ["C c"]],
    ["C", ["e"]],
]

parsed_rules = parse_all_rules(RULES)
slr = SLR(parsed_rules, show_slr=False, show_first=False, show_follow=False)
slr.run("c $".split(" "))
#
# RULES = [
#    ["S", ["A B C $"]],
#    ["A", ["a A"]],
#    ["A", ["e"]],
#    ["B", ["b B"]],
#    ["B", ["b"]],
#    ["C", ["c C"]],
#    ["C", ["c"]]
# ]
#
# parsed_rules = parse_all_rules(RULES)
# slr = SLR(parsed_rules, show_slr=False, show_first=False, show_follow=False)
# slr.run("a a a b b c $".split(" "))
#
# RULES = [
#    ["Z", ["A $"]],
#    ["A", ["A * B"]],
#    ["A", ["B"]],
#    ["B", ["( A )"]],
#    ["B", ["i"]]
# ]
#
# parsed_rules = parse_all_rules(RULES)
# slr = SLR(parsed_rules, show_slr=False, show_first=False, show_follow=False)
#
# RULES = [
#    ["Z", ["S $"]],
#    ["S", ["( S )"]],
#    ["S", ["( )"]]
# ]
#
# parsed_rules = parse_all_rules(RULES)
# slr = SLR(parsed_rules, show_slr=False, show_first=False, show_follow=False)
# slr.run("( ( ) ) $".split(" "))
#
# RULES = [
#    ["S", ["type F $"]],
#    ["F", ["I = T"]],
#    ["F", ["I = T ; F"]],
#    ["T", ["int"]],
#    ["T", ["record G end"]],
#    ["G", ["I : T"]],
#    ["G", ["I : T ; G"]],
#    ["I", ["a"]],
#    ["I", ["b"]],
#    ["I", ["c"]]
# ]
#
# parsed_rules = parse_all_rules(RULES)
# slr = SLR(parsed_rules, show_slr=False, show_first=False, show_follow=False)
#
# RULES = [
#    ["F", ["function I ( I ) G end $"]],
#    ["G", ["I := E"]],
#    ["G", ["I := E ; G"]],
#    ["E", ["E * I"]],
#    ["E", ["E + I"]],
#    ["E", ["I"]],
#    ["I", ["a"]]
# ]
# parsed_rules = parse_all_rules(RULES)
# slr = SLR(parsed_rules, show_slr=False, show_first=False, show_follow=False)
# slr.run("function a ( a ) a := a ; a := a + a * a ; a := a + a end $".split(" "))
#
# RULES = [
#    ["PROG", ["begin d ; X end $"]],
#    ["X", ["d ; X"]],
#    ["X", ["s Y"]],
#    ["Y", ["; s Y"]],
#    ["Y", ["e"]],
# ]
#
# parsed_rules = parse_all_rules(RULES)
# slr = SLR(parsed_rules, show_slr=False, show_first=False, show_follow=False)
# slr.run("begin d ; d ; s ; s end $".split(" "))
#
# #
# RULES = [
#    ["S", ["A $"]],
#    ["A", ["0 A"]],
#    ["A", ["1 A"]],
#    ["A", ["2 A"]],
#    ["A", ["e"]],
# ]
# parsed_rules = parse_all_rules(RULES)
# slr = SLR(parsed_rules, show_slr=False, show_first=False, show_follow=False)
# slr.run("0 1 2 0 1 2 $".split(" "))
#
# RULES = [
#    ["Z", ["S $"]],
#    ["S", ["b B S"]],
#    ["S", ["e"]],
#    ["B", ["a B"]],
#    ["B", ["e"]]
# ]
#
# parsed_rules = parse_all_rules(RULES)
# slr = SLR(parsed_rules, show_slr=False, show_first=False, show_follow=False)
# slr.run("b b a a $".split(" "))
#
#
# RULES = [
#    ["S", ["a A B $"]],
#    ["A", ["c A b"]],
#    ["A", ["e"]],
#    ["B", ["B a"]],
#    ["B", ["a"]]
# ]
# parsed_rules = parse_all_rules(RULES)
# slr = SLR(parsed_rules, show_slr=False, show_first=False, show_follow=False)
# slr.run("a c c b b a $".split(" "))
#
# RULES = [
#    ["Z", ["S $"]],
#    ["S", ["a S b"]],
#    ["S", ["S c"]],
#    ["S", ["e"]]
# ]
# parsed_rules = parse_all_rules(RULES)
# slr = SLR(parsed_rules, show_slr=False, show_first=False, show_follow=False)
# slr.run("a a b c b $".split(" "))

RULES = [
   ["S", ["A B C $"]],
   ["A", ["A a"]],
   ["A", ["e"]],
   ["B", ["B b"]],
   ["B", ["e"]],
   ["C", ["C c"]],
   ["C", ["e"]]
]
parsed_rules = parse_all_rules(RULES)
slr = SLR(parsed_rules, show_slr=False, show_first=False, show_follow=False)
slr.run("a a b b b $".split(" "))
#
# RULES = [
#    ["S", ["A B C $"]],
#    ["A", ["A a"]],
#    ["A", ["e"]],
#    ["B", ["B b"]],
#    ["B", ["e"]],
#    ["C", ["c C"]],
#    ["C", ["e"]]
# ]
# parsed_rules = parse_all_rules(RULES)
# slr = SLR(parsed_rules, show_slr=False, show_first=False, show_follow=False)
# slr.run("a $".split(" "))
# slr.run("b $".split(" "))
# slr.run("c $".split(" "))
# slr.run("a b $".split(" "))
# slr.run("a c $".split(" "))
# slr.run("b c $".split(" "))
# slr.run("a b c c $".split(" "))
#
#
# RULES = [
#    ["Z", ["E $"]],
#    ["E", ["E + T"]],
#    ["E", ["T"]],
#    ["T", ["T * F"]],
#    ["T", ["F"]],
#    ["F", ["( E )"]],
#    ["F", ["- F"]],
#    ["F", ["id"]],
#    ["F", ["num"]]
# ]
# parsed_rules = parse_all_rules(RULES)
# slr = SLR(parsed_rules, show_slr=False, show_first=False, show_follow=False)
# slr.run("- id + - ( id * num ) + id + id $".split(" "))