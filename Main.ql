TestFunc(tf: bln): bln
{
	ltr tf = False
	ret tf
}

; Our program's entry point.
Entry(num: is32, val: ^^chr): is32
{
	ret (TestFunc(True)): is32
}

obj fp32vec2 { x: fp32
y: fp32 }