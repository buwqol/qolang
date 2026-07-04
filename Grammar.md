lit => IU | FP | STR | CHR | TRUE | FALSE | NULL

prim => lit

unry => (PLUS | DASH | EXCLAM | TIL) unry | prim

fact => unry ((ASTR | FSLSH | PRCNT) fact)*

term => fact ((PLUS | DASH) term)*

btws => term ((AMP | PIPE | CARET) btws)*

shft => btws ((LTLT | GTGT) shft)*

comp => shft ((LT | LTEQ | GT | GTEQ) comp)*

eqlt => comp ((EQEQ | EXCLAMEQ) eqlt)*

expr => eqlt

grpng => LPAREN expr RPAREN