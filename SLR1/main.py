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
# print(parsed_rules)
# print(SLR.other_first(parsed_rules))
# print(SLR.other_follow(parsed_rules))
pretty_2d_table(SLR.other_slr_table(parsed_rules))
slr = SLR(RULES, show_slr=True, show_first=False, show_follow=False)
# slr.run("c $")
# print("//////////////////////////////////////////////////////////////////////////////")

#RULES = [
#    ["S", ["A B C $"]],
#    ["A", ["a A"]],
#    ["A", ["e"]],
#    ["B", ["b B"]],
#    ["B", ["b"]],
#    ["C", ["c C"]],
#    ["C", ["c"]]
#    ]
#
#Print_2D_Table(RULES)
#Print_2D_Table(SLR_Table(RULES))
#Runner(SLR_Table(RULES), "a a a b b c $", RULES)
#print()
#print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
#print()

#RULES = [
#    ["S", ["A B C $"]],
#    ["A", ["a A"]],
#    ["A", ["e"]],
#    ["B", ["b B"]],
#    ["B", ["e"]],
#    ["C", ["c C"]],
#    ["C", ["e"]]
#    ]
#
#Print_2D_Table(RULES)
#Runner(SLR_Table(RULES), "a a a b b c $", RULES)
#print()
#print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
#print()
#
#RULES = [
#    ["Z", ["A $"]],
#    ["A", ["A * B"]],
#    ["A", ["B"]],
#    ["B", ["( A )"]],
#    ["B", ["i"]]
#    ]
#
#Print_2D_Table(RULES)
#SLR_Table(RULES)
#print()
#print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
#print()
#
#RULES = [
#    ["Z", ["S $"]],
#    ["S", ["( S )"]],
#    ["S", ["( )"]]
#    ]
#
#Print_2D_Table(RULES)
#Runner(SLR_Table(RULES), "( ( ) ) $", RULES)
#print()
#print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
#print()
#
#RULES = [
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
#    ]
#
#Print_2D_Table(RULES)
#SLR_Table(RULES)
#print()
#print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
#print()
#
#RULES = [
#    ["F", ["function I ( I ) G end $"]],
#    ["G", ["I := E"]],
#    ["G", ["I := E ; G"]],
#    ["E", ["E * I"]],
#    ["E", ["E + I"]],
#    ["E", ["I"]],
#    ["I", ["a"]]
#    ]
#
#Print_2D_Table(RULES)
#Runner(SLR_Table(RULES), "function a ( a ) a := a ; a := a + a * a ; a := a + a end $", RULES)
#print()
#print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
#print()
#
#RULES = [
#    ["PROG", ["begin d ; X end $"]],
#    ["X", ["d ; X"]],
#    ["X", ["s Y"]],
#    ["Y", ["; s Y"]],
#    ["Y", ["e"]],
#    ]
#
#Print_2D_Table(RULES)
#Runner(SLR_Table(RULES), "begin d ; d ; s ; s end $", RULES)
#print()
#print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
#print()
#
#RULES = [
#    ["S", ["A $"]],
#    ["A", ["0 A"]],
#    ["A", ["1 A"]],
#    ["A", ["2 A"]],
#    ["A", ["e"]],
#    ]
#
#Print_2D_Table(RULES)
#Runner(SLR_Table(RULES), "0 1 2 0 1 2 $", RULES)
#print()
#print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
#print()
#
#RULES = [
#    ["Z", ["S $"]],
#    ["S", ["b B S"]],
#    ["S", ["e"]],
#    ["B", ["a B"]],
#    ["B", ["e"]]
#    ]
#
#Print_2D_Table(RULES)
#Runner(SLR_Table(RULES), "b b a a $", RULES)
#print()
#print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
#print()
#
#RULES = [
#    ["S", ["a A B $"]],
#    ["A", ["c A b"]],
#    ["A", ["e"]],
#    ["B", ["B a"]],
#    ["B", ["a"]]
#    ]
#
#Print_2D_Table(RULES)
#Runner(SLR_Table(RULES), "a c c b b a $", RULES)
#print()
#print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
#print()
#
#RULES = [
#    ["Z", ["S $"]],
#    ["S", ["a S b"]],
#    ["S", ["S c"]],
#    ["S", ["e"]]
#    ]
#
#Print_2D_Table(RULES)
#Runner(SLR_Table(RULES), "a a b c b $", RULES)
#print()
#print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
#print()
#
#RULES = [
#    ["S", ["A B C $"]],
#    ["A", ["A a"]],
#    ["A", ["e"]],
#    ["B", ["b B"]],
#    ["B", ["e"]],
#    ["C", ["c c"]],
#    ["C", ["e"]]
#    ]
#
#Print_2D_Table(RULES)
#SLR_Table(RULES)
##Runner(SLR_Table(RULES), "a a b c b $", RULES)
#print()
#print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
#print()

#RULES = [
#    ["S", ["A B C $"]],
#    ["A", ["A a"]],
#    ["A", ["e"]],
#    ["B", ["B b"]],
#    ["B", ["e"]],
#    ["C", ["c C"]],
#    ["C", ["e"]]
#    ]
#
#Print_2D_Table(RULES)
#print(First(RULES))
#Print_2D_Table(SLR_Table(RULES))
#Runner(SLR_Table(RULES), "a $", RULES)
#print()
#Runner(SLR_Table(RULES), "b $", RULES)
#print()
#Runner(SLR_Table(RULES), "c $", RULES)
#print()
#Runner(SLR_Table(RULES), "a b $", RULES)
#print()
#Runner(SLR_Table(RULES), "a c $", RULES)
#print()
#Runner(SLR_Table(RULES), "b c $", RULES)
#print()
#Runner(SLR_Table(RULES), "a b c c $", RULES)
#print()
#print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
#print()
#
#
#RULES = [
#
#    ["Z", ["E $"]],
#    ["E", ["E + T"]],
#    ["E", ["T"]],
#    ["T", ["T * F"]],
#    ["T", ["F"]],
#    ["F", ["( E )"]],
#    ["F", ["- F"]],
#    ["F", ["id"]],
#    ["F", ["num"]]
#    ]
#
#Print_2D_Table(RULES)
#Print_2D_Table(SLR_Table(RULES))
#Runner(SLR_Table(RULES), "- id + - ( id * num ) + id + id $", RULES)
#print()
#print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
#print()
