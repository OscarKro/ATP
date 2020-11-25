from ANMtokens import *
checkNrParamDict = {"weide":0,"wim":0,"jet":0,"duif":1,"schaap":0,"lam":0,"aap":3,"noot":1,"mies":0,"vuur":0}
lambdaDict = {"weide":lambda w,pc: Weide(w,pc),"wim":lambda w : Wim(w),"jet":lambda w : Jet(w),"duif":lambda w,a: Duif(w,a),
"schaap":lambda w : Schaap(w),"lam":lambda w : Lam(w),"aap":lambda w,x,y,a: Aap(w,x,y,a),"noot": lambda w,v: Noot(w,v),"mies": lambda w: Mies(w),
"vuur": lambda w : Vuur(w)}