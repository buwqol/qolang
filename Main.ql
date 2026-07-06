if ^^^^(someVariable:^[1]^[2]tFP32) == 0.0
{
	^(a.field) = 1
}
else
{
	^a = 3
}
; Our program's entry point.
; Entry(num: tIS32, val: ^^tChr): tIS32
; {
; 	var: tBln = True
; 	if var == True
; 	{
; 		ret 0
; 	}
; 	else
; 	{
; 		ret 1
; 	}
; }