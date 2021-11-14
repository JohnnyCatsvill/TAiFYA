#
# @staticmethod
# def other_first(rules: list[Rule]):
#     nonterms = set([rule.left for rule in rules])
#     # e_nonterms, show if nonterm has empty symbol, S->AB$ A->e A->a B->b, there A could be skipped through rule 2
#     e_nonterms = {rules[i].left: i + 1 for i in range(len(rules)) if rules[i].right[0].type == WordType.EMPTY}
#     first_table: FirstTable = {i: [] for i in nonterms}
#
#     changed = True  # run while no changes left
#     while changed:
#         changed = False
#
#         for rule in rules:  # run through all rules
#             e_fold = 0
#             for right_word in rule.right:
#                 if right_word.type in [WordType.TERM, WordType.NONTERM, WordType.END]:
#                     changed += add_to_table(first_table[rule.left], right_word.add_e_fold(e_fold))
#
#                     if right_word.type == WordType.NONTERM and right_word.str in first_table:
#                         for i in first_table[right_word.str]:
#                             changed += add_to_table(first_table[rule.left], i)
#
#                     if right_word.str in e_nonterms:
#                         e_fold = e_nonterms[right_word.str]
#                     else:
#                         break
#
#             # step_on_e_nonterm = True
#             # while step_on_e_nonterm:
#             #     step_on_e_nonterm = False
#             #
#             #     if right_word.type in [WordType.TERM, WordType.NONTERM]:
#             #         changed = changed or add_to_table(first_table[rule.left], right_word.add_e_fold(e_fold))
#             #
#             #         if right_word.type == WordType.NONTERM and right_word.str in first_table:
#             #             for i in first_table[right_word.str]:
#             #                 changed = changed or add_to_table(first_table[rule.left], i)
#             #
#             #             if right_word.str in e_nonterms:
#             #                 step_on_e_nonterm = True
#             #                 e_fold = e_nonterms[right_word.str]
#             #                 right_word_index += 1
#             #                 right_word = deepcopy(rule.right[right_word_index])
#
#     return first_table

# @staticmethod
# def other_first(rules: list[Rule]):
#     nonterms = set([rule.left for rule in rules])
#     e_nonterms = {rules[i].left: str(i + 1) for i in range(len(rules)) if rules[i].right[0].type == WordType.EMPTY}
#
#     first_table: FirstTable = {i: [] for i in nonterms}
#     empty_table: FirstTable = {i: [] for i in nonterms}  # first через e символы
#     recurse_table: FirstTable = {i: [] for i in nonterms}  # first через собственный символ
#     # ПРИМЕР: H->S, S->(S), S->e; тут S имеет first )23 ,
#     # но H не может воспользоваться этим first
#
#     changed = True
#     while changed:
#         changed = False
#
#         for rule_index in range(len(rules)):
#             rule = rules[rule_index]
#             first_right = deepcopy(rule.right[0])
#             left = rule.left
#
#             there_are_empty_nonterminal = True
#             empty_nonterminal_entrance = 1
#             some_rule_adder = ""
#             while there_are_empty_nonterminal:
#                 there_are_empty_nonterminal = False
#                 if first_right.type in [WordType.TERM, WordType.NONTERM]:
#
#                     not_null_e_fold = some_rule_adder or "0"
#                     changed = changed or add_to_table(first_table[left],
#                                                       first_right.add_e_fold(int(not_null_e_fold.split(" ")[-1])))
#
#                     if first_right.type == WordType.NONTERM and first_right.str in first_table:
#                         for i in first_table[first_right.str]:
#                             changed = changed or add_to_table(first_table[left], i)
#
#                         if first_right.str in e_nonterms:
#                             there_are_empty_nonterminal = True
#                             some_rule_adder += " " + e_nonterms[first_right.str]
#                             first_right = deepcopy(rule.right[empty_nonterminal_entrance])
#                             empty_nonterminal_entrance += 1
#
#                 elif first_right.type == WordType.EMPTY:
#                     afterlooking_symbols = {left}
#                     afterlooking_symbols_changed = True
#
#                     while afterlooking_symbols_changed:
#                         afterlooking_symbols_changed = False
#
#                         for new_rule_index in range(len(rules)):
#                             new_rule = rules[new_rule_index]
#                             new_left = new_rule.left
#
#                             for word_index in range(len(new_rule.right)):
#                                 word = new_rule.right[word_index]
#
#                                 if word.str in afterlooking_symbols:
#                                     if word_index + 1 < len(new_rule.right):
#                                         next_word = new_rule.right[word_index + 1]
#
#                                         if new_left != left:
#                                             changed = changed or add_to_table(empty_table[left],
#                                                                               next_word.add_e_fold(rule_index + 1))
#
#                                         else:
#                                             changed = changed or add_to_table(recurse_table[left],
#                                                                               next_word.add_e_fold(rule_index + 1))
#
#                                         if next_word.str in first_table:
#                                             for i in first_table[next_word.str]:
#                                                 add_to_table(empty_table[left], i.add_e_fold(rule_index + 1))
#
#                                     else:
#                                         afterlooking_symbols_changed = new_rule.left not in afterlooking_symbols
#                                         afterlooking_symbols.add(new_rule.left)
#
#     return [first_table, empty_table, recurse_table]


# @staticmethod
#     def other_follow(rules, norm_rules: list[Rule]):
#         _first_tables_ = SLR.First(rules)
#         first_table = _first_tables_[0]
#
#         nonterms = set([rule.left for rule in norm_rules])
#         e_nonterms = {norm_rules[i].left: i + 1 for i in range(len(norm_rules)) if
#                       norm_rules[i].right[0].type == WordType.EMPTY}
#         set_of_control_symbols = {EMPTY_SYMBOL}
#         terms = set([letter for rule_pack in rules for letter in parse_rule(rule_pack[1][0]) if
#                                 letter not in nonterms and letter not in set_of_control_symbols])
#
#         typed_first_table = SLR.other_first(norm_rules)
#         typed_follow_table: FollowTable = dict()
#         follow_table = dict()
#
#         for rule_index in range(len(norm_rules)):
#             rule = norm_rules[rule_index]
#             for word_index in range(len(rule.right)):
#                 word = rule.right[word_index]
#                 follow_table[word.str + " " + str(rule_index + 1) + " " + str(word_index + 1)] = []
#
#                 typed_follow_table[word] = []  # new
#
#         last_table = {"why": "i don't understand!!!, <sobs>"}  # yea.. it just to set a non empty dict
#         follow_table[norm_rules[0].left + ' 0 0'] = []
#         typed_follow_table[Word(Word.get_type(norm_rules[0].left, nonterms, terms), norm_rules[0].left, 0, 0)] = []
#
#         while follow_table != last_table:
#             last_table = deepcopy(follow_table)
#
#             first_nonterm = norm_rules[0].left
#             follow_word = follow_table[first_nonterm + ' 0 0']
#             typed_follow_word = typed_follow_table[Word(Word.get_type(norm_rules[0].left, nonterms, terms), norm_rules[0].left, 0, 0)]
#
#             parsed_rule = norm_rules[0].right
#             next_letter = parsed_rule[0]
#
#             # first_first_symbol = ParseRule(rules[0][1][0])[0]
#
#             if next_letter.type in [WordType.TERM, WordType.END]:
#                 add_to_table(follow_word, next_letter.str + " 1 1")
#                 add_to_table(typed_follow_word, next_letter)  # new
#             elif next_letter.type == WordType.NONTERM:
#                 add_to_table(follow_word, next_letter.str + " 1 1")
#                 add_to_table(typed_follow_word, next_letter)  #new
#                 for i in first_table[next_letter.str]:
#                     add_to_table(follow_word, i)
#
#                 for i in typed_first_table[next_letter.str]:
#                     add_to_table(typed_follow_word, i)
#
#                 if next_letter in typed_follow_table:
#                     if next_letter.str in e_nonterms:
#                         for i in follow_table[str(next_letter)]:
#                             add_to_table(follow_word, i + " " + str(e_nonterms[next_letter.str]))
#
#                         for i in typed_follow_table[next_letter]:
#                             add_to_table(typed_follow_word, i.add_e_fold(e_nonterms[next_letter.str]))
#
#             for rule_index in range(len(norm_rules)):
#                 rule = norm_rules[rule_index]
#                 cur_nonterm = rule.left
#                 parsed_rule = deepcopy(rule.right)
#
#                 for word_index in range(len(parsed_rule)):
#                     word = parsed_rule[word_index]
#                     follow_word = follow_table[word.str + " " + str(rule_index + 1) + " " + str(word_index + 1)]
#                     typed_follow_word = typed_follow_table[word]
#
#                     if word_index + 1 < len(parsed_rule):
#                         next_letter = parsed_rule[word_index + 1]
#
#                         if next_letter.type in [WordType.TERM, WordType.END]:
#                             add_to_table(follow_word,
#                                          next_letter.str + " " + str(rule_index + 1) + " " + str(word_index + 2))
#                             add_to_table(typed_follow_word, next_letter)
#
#                         elif next_letter.type == WordType.NONTERM:
#                             add_to_table(follow_word,
#                                          next_letter.str + " " + str(rule_index + 1) + " " + str(word_index + 2))
#                             add_to_table(typed_follow_word, next_letter)
#
#                             for i in first_table[next_letter.str]:
#                                 add_to_table(follow_word, i)
#
#                             for i in typed_first_table[next_letter.str]:
#                                 add_to_table(typed_follow_word, i)
#
#                             if next_letter.str + " " + str(rule_index + 1) + " " + str(word_index + 2) in follow_table:
#                                 if next_letter.str in e_nonterms:
#                                     for i in follow_table[
#                                         next_letter.str + " " + str(rule_index + 1) + " " + str(word_index + 2)]:
#                                         add_to_table(follow_word, i + " " + str(e_nonterms[next_letter.str]))
#
#                             if next_letter in typed_follow_table:
#                                 if next_letter.str in e_nonterms:
#                                     for i in typed_follow_table[next_letter]:
#                                         add_to_table(typed_follow_word, i.add_e_fold(e_nonterms[next_letter.str]))
#
#                     elif word.type != WordType.EMPTY:
#                         for i in typed_follow_table:
#                             if i.str == cur_nonterm:
#                                 for j in follow_table[i.str + ' ' + str(i.row) + ' ' + str(i.col)]:
#                                     add_to_table(follow_word, j)
#
#                                 for j in typed_follow_table[i]:
#                                     add_to_table(typed_follow_word, j)
#
#         items_to_delete = []
#         for i, j in typed_follow_table.items():
#             if i.type in [WordType.EMPTY, WordType.END]:
#                 items_to_delete.append(i)
#
#         for i in items_to_delete:
#             follow_table.pop(str(i))
#             typed_follow_table.pop(i)
#
#         print(typed_follow_table)
#         return follow_table