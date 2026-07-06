lit => LITIU | LITFP | LITSTR | LITCHR | KWTRUE | KWFALSE | KWNULL

<!-- typ => CARET typ | LBRACK expr? RBRACK typ | (TIU8 | TIS8 | TIU16 | TIS16 | TIU32 | TIS32 | TIU64 | TIS64 | TFP32 | TFP64 | TBLN | TNONE | TPTR | IDENT) -->

typ => TIU8 | TIS8 | TIU16 | TIS16 | TIU32 | TIS32 | TIU64 | TIS64 | TFP32 | TFP64 | TBLN | TNONE | TPTR | IDENT

tcst => prim COLON typ

prim => lit | IDENT | LPAREN expr RPAREN | tcst

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

cnd => KWIF expr cndbdy (NEWLINE* KWELIF expr cndbdy)\* (NEWLINE* KWELSE cndbdy)?

loop => KWWHILE expr cndbdy (NEWLINE* KWELSE cndbdy)?

assgn => IDENT EQ (assgn | expr)

stmnt => (assgn | expr | rtrn | blck | KWBRK | cnd | loop)

stlst => (stmnt (NEWLINE+ stmnt)*)?

blck => LBRACE NEWLINE\* stlst NEWLINE\* RBRACE

prog => NEWLINE\* stlst NEWLINE\*