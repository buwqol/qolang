TestFunc(tf: bln): bln
{
	ltr tf = False
	ret tf
}

check1, check2, check3 : ^(is32, is32): non = Null

; Our program's entry point.
Entry(num: is32, val: ^^chr): is32
{
	ret (TestFunc(True)): is32
}

obj fp32vec2 { x,y: fp32 }

ord ut
{
	UT_IU32 = 0
	UT_IS32
	UT_FP32
}

uni uni32
{
	f_iu32: iu32
	f_is32: is32
	f_fp32: fp32
}