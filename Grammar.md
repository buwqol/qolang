lit => IU | FP | STR | CHR | TRUE | FALSE | NULL

prim => lit | grpng | IDENT

unry => (PLUS | DASH | EXCLAM | TIL | CARET | ATSGN) unry | prim

fact => unry ((ASTR | FSLSH | PRCNT) unry)*

term => fact ((PLUS | DASH) fact)*

btws => term ((AMP | PIPE | CARET) term)*

shft => btws ((LTLT | GTGT) btws)*

comp => shft ((LT | LTEQ | GT | GTEQ) shft)*

eqlt => comp ((EQEQ | EXCLAMEQ) comp)*

expr => eqlt

grpng => LPAREN expr RPAREN