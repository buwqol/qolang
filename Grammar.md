lit => LITIU | LITFP | LITSTR | LITCHR | KWTRUE | KWFALSE | KWNULL

typ => TIU8 | TIS8 | TIU16 | TIS16 | TIU32 | TIS32 | TIU64 | TIS64 | TFP32 | TFP64 | TBLN | TUSZ | TSSZ | TNONE | TPTR | IDENT

ftyp => LPAREN (mtyp (COMMA mtyp)*)? RPAREN COLON mtyp

mtyp => CARET mtyp | LBRACK expr RBRACK mtyp | ftyp | typ

cst => COLON mtyp

prim => (lit | IDENT | LPAREN expr RPAREN) cst?

pstfx => prim (LPAREN (expr (COMMA expr)\*)? RPAREN | LBRACK expr RBRACK | PERIOD IDENT)\*

unry => (PLUS | DASH | EXCLAM | TIL | CARET | ATSGN) unry | pstfx

fact => unry ((ASTR | FSLSH | PRCNT) unry)\*

term => fact ((PLUS | DASH) fact)\*

btws => term ((AMP | PIPE | CARET) term)\*

shft => btws ((LTLT | GTGT) btws)\*

cmp => shft ((LT | LTEQ | GT | GTEQ) shft)\*

eqlt => cmp ((EQEQ | EXCLAMEQ) cmp)\*

lgca => eqlt (KWAND eqlt)\*

lgco => lgca (KWOR lgca)\*

expr => lgco

rtrn => KWRET expr?

cndbdy => NEWLINE\* (stmnt | blck)

cnd => KWIF expr cndbdy (NEWLINE* KWELIF expr cndbdy)\* (NEWLINE* KWELSE cndbdy)?

loop => KWWHILE expr cndbdy (NEWLINE* KWELSE cndbdy)?

assgn => unry EQ (assgn | expr)

cssgn => unry (PLUSEQ | DASHEQ | ASTREQ | FSLSHEQ | PRCNTEQ | AMPEQ | PIPEEQ | CARETEQ | TILEQ) (assgn | expr)

var => IDENT (COMMA NEWLINE* IDENT)\* COLON ((mtyp (EQ expr)?) | (EQ expr))

cntrl => KWBRK | KWCONT

stmnt => (var | cssgn | assgn | expr | rtrn | blck | cntrl | cnd | loop)

stlst => (stmnt (NEWLINE+ stmnt)\*)?

blck => LBRACE NEWLINE\* stlst NEWLINE\* RBRACE

arg => IDENT COLON mtyp

fnc => IDENT LPAREN (NEWLINE\* arg (COMMA NEWLINE\* arg)\*)? RPAREN COLON mtyp NEWLINE\* blck?

dobja => IDENT (COMMA NEWLINE\* IDENT)\* COLON mtyp

dobj => KWOBJ IDENT NEWLINE\* (LBRACE NEWLINE\* dobja (NEWLINE+ dobja)\* NEWLINE\* RBRACE)?

dunia => IDENT COLON mtyp

duni => KWUNI IDENT NEWLINE\* (LBRACE NEWLINE\* dunia (NEWLINE+ dunia)\* NEWLINE\* RBRACE)?

dorda => IDENT (EQ expr)?

dord => KWORD IDENT NEWLINE\* (LBRACE NEWLINE\* dorda (NEWLINE+ dorda)\* NEWLINE\* RBRACE)?

prog => NEWLINE\* ((fnc | var | dobj | duni | dord) NEWLINE+)\* EOF