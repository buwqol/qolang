lit -> IU | FP | STR | CHR | TRUE | FALSE | NULL

prim -> lit

unry -> (POS | NEG | NOT | INV) unry | prim

fact -> unry ((MUL | DIV | MOD) fact)*