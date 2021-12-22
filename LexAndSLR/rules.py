from constants.constants_lex import OCT_NAME, DEC_NAME, FLOAT_NAME, BIN_NAME, HEX_NAME, STRING_NAME

RULES = [
    ["PROGRAM", ["function_type entry_point ( ) { LIST_OF_COMMANDS } $"], [],
     [[], [], [], [], ["block"], [], ["end_block"]]],

    ["LIST_OF_COMMANDS", ["COMMAND LIST_OF_COMMANDS"]],
    ["LIST_OF_COMMANDS", ["COMMAND"]],

    ["COMMAND", ["type ID divider"], [["init"], ["init"]]],  # [["add", "remove"], ["print"], []]
    ["COMMAND", ["reader ( ID ) divider"]],
    ["COMMAND", ["printer ( ID ) divider"]],
    ["COMMAND", ["ID assign EXPRESSION divider"], [["assign"], [], ["assign"]]],
    ["COMMAND", ["ID assign CONDITION divider"]],
    ["COMMAND", ["ID assign LIST_OF_ELEMENTS divider"]],
    ["COMMAND", ["condition_start ( CONDITION ) { LIST_OF_COMMANDS }"], [],
     [[], [], [], [], ["block"], [], ["end_block"]]],
    ["COMMAND", ["condition_start ( CONDITION ) { LIST_OF_COMMANDS } condition_else { LIST_OF_COMMANDS }"], [],
     [[], [], [], [], ["block"], [], ["end_block"], [], ["block"], [], ["end_block"]]],
    ["COMMAND", ["cycle ( CONDITION ) { LIST_OF_COMMANDS }"], [],
     [[], [], [], [], ["block"], [], ["end_block"]]],
    ["COMMAND", ["{ LIST_OF_COMMANDS }"], [], [["block"], [], ["end_block"]]],

    ["ANY_NUMBER", [OCT_NAME], [["pass"]]],
    ["ANY_NUMBER", [HEX_NAME], [["pass"]]],
    ["ANY_NUMBER", [BIN_NAME], [["pass"]]],
    ["ANY_NUMBER", [FLOAT_NAME], [["pass"]]],
    ["ANY_NUMBER", ["ID"], [["get_id_val"]]],
    ["ANY_NUMBER", [DEC_NAME], [["pass"]]],


    ["LIST_OF_ELEMENTS", ["[ LIST_OF_ELEMENTS2 ]"], [[], ["pass"]]],
    ["LIST_OF_ELEMENTS", [STRING_NAME], [["pass"]]],
    ["LIST_OF_ELEMENTS2", ["ANY_NUMBER comma LIST_OF_ELEMENTS2"], [["add_to_list"], [], ["add_to_list"]]],
    ["LIST_OF_ELEMENTS2", ["ANY_NUMBER"], [["init_list"]]],


    ["BOOL_NUMBER", ["boolean_true"]],
    ["BOOL_NUMBER", ["boolean_false"]],

    ["EXPRESSION", ["EXPRESSION plus_symbol EXPRESSION2"], [["add"], [], ["add"]]],
    ["EXPRESSION", ["EXPRESSION minus_symbol EXPRESSION2"], [["sub"], [], ["sub"]]],
    ["EXPRESSION", ["EXPRESSION2"], [["pass"]] ],

    ["EXPRESSION2", ["EXPRESSION2 multiply_symbol EXPRESSION3"]],
    ["EXPRESSION2", ["EXPRESSION2 divide_symbol EXPRESSION3"]],
    ["EXPRESSION2", ["EXPRESSION3"], [["pass"]] ],

    ["EXPRESSION3", ["( EXPRESSION )"], [[], ["pass"]]],
    ["EXPRESSION3", ["minus_symbol EXPRESSION3"], [[], ["negate"]]],
    ["EXPRESSION3", ["ANY_NUMBER"], [["pass"]] ],

    ["CONDITION", ["CONDITION binary_or CONDITION2"]],
    ["CONDITION", ["CONDITION2"]],

    ["CONDITION2", ["CONDITION2 binary_and CONDITION3"]],
    ["CONDITION2", ["CONDITION3"]],

    ["CONDITION3", ["( CONDITION )"]],
    ["CONDITION3", ["unary_not CONDITION3"]],
    ["CONDITION3", ["BOOL_NUMBER"]],
    # ["CONDITION3", ["ANY_NUMBER"]],
    ["CONDITION3", ["ANY_NUMBER binary_compare ANY_NUMBER"]],
]
