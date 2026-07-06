lit => LITIU | LITFP | LITSTR | LITCHR | KWTRUE | KWFALSE | KWNULL

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

rtrn => KWRET expr

cndbdy => NEWLINE\* (stmnt | blck)

cnd => KWIF expr cndbdy (NEWLINE+ KWELIF expr cndbdy)\* (NEWLINE+ KWELSE cndbdy)?

assgn => IDENT EQ (assgn | expr)

stmnt => (assgn | expr | rtrn | blck | KWBRK | cnd)

stlst => (stmnt (NEWLINE+ stmnt)*)?

blck => LBRACE NEWLINE\* stlst NEWLINE\* RBRACE

prog => NEWLINE\* stlst NEWLINE\*