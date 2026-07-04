lit => IU | FP | STR | CHR | TRUE | FALSE | NULL

prim => lit | IDENT | LPAREN expr RPAREN

pstfx => prim (LPAREN (expr (COMMA expr)\*)? RPAREN | LBRACK expr RBRACK | PERIOD IDENT)\*

unry => (PLUS | DASH | EXCLAM | TIL | CARET | ATSGN) unry | pstfx

fact => unry ((ASTR | FSLSH | PRCNT) unry)\*

term => fact ((PLUS | DASH) fact)\*

btws => term ((AMP | PIPE | CARET) term)\*

shft => btws ((LTLT | GTGT) btws)\*

comp => shft ((LT | LTEQ | GT | GTEQ) shft)\*

eqlt => comp ((EQEQ | EXCLAMEQ) comp)\*

expr => eqlt