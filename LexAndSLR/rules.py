RULES = [
    ["PROGRAM", ["function_type entry_point ( ) { LIST_OF_COMMANDS } $"]],

    ["LIST_OF_COMMANDS", ["COMMAND LIST_OF_COMMANDS"]],
    ["LIST_OF_COMMANDS", ["COMMAND"]],

    ["COMMAND", ["type ID divider"]],  # [["add", "remove"], ["print"], []]
    ["COMMAND", ["reader ( ID ) divider"]],
    ["COMMAND", ["printer ( ID ) divider"]],
    ["COMMAND", ["ID assign EXPRESSION divider"]],
    ["COMMAND", ["ID assign CONDITION divider"]],
    ["COMMAND", ["ID assign LIST_OF_ELEMENTS divider"]],
    ["COMMAND", ["condition_start ( CONDITION ) { LIST_OF_COMMANDS }"]],
    ["COMMAND", ["condition_start ( CONDITION ) { LIST_OF_COMMANDS } condition_else { LIST_OF_COMMANDS }"]],
    ["COMMAND", ["cycle ( CONDITION ) { LIST_OF_COMMANDS }"]],

    ["ANY_NUMBER", ["OCT"]],
    ["ANY_NUMBER", ["HEX"]],
    ["ANY_NUMBER", ["BIN"]],
    ["ANY_NUMBER", ["FLOAT"], [["pass"]] ],
    ["ANY_NUMBER", ["ID"]],
    ["ANY_NUMBER", ["INT"], [["pass"]] ],


    ["LIST_OF_ELEMENTS", ["[ LIST_OF_ELEMENTS2 ]"]],
    ["LIST_OF_ELEMENTS", ["STRING"]],
    ["LIST_OF_ELEMENTS2", ["ANY_NUMBER comma LIST_OF_ELEMENTS2"]],
    ["LIST_OF_ELEMENTS2", ["ANY_NUMBER"]],


    ["BOOL_NUMBER", ["boolean_true"]],
    ["BOOL_NUMBER", ["boolean_false"]],

    ["EXPRESSION", ["EXPRESSION plus_symbol EXPRESSION2"]],
    ["EXPRESSION", ["EXPRESSION minus_symbol EXPRESSION2"]],
    ["EXPRESSION", ["EXPRESSION2"], [["pass"]] ],

    ["EXPRESSION2", ["EXPRESSION2 multiply_symbol EXPRESSION3"]],
    ["EXPRESSION2", ["EXPRESSION2 divide_symbol EXPRESSION3"]],
    ["EXPRESSION2", ["EXPRESSION3"], [["pass"]] ],

    ["EXPRESSION3", ["( EXPRESSION )"]],
    ["EXPRESSION3", ["minus_symbol EXPRESSION3"]],
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
