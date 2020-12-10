import ANMtokens
import ANMCompilerTokens

checkNrParamDict = {"weide":0,"wim":0,"jet":0,"duif":1,"schaap":0,"lam":0,"aap":3,"noot":1,"mies":0,"vuur":0,"hok":0,"does":1,"teun":1}

lambdaDict = {"weide": lambda w : ANMtokens.Weide_func(w), "wim":lambda w : ANMtokens.Wim(w),"jet":lambda w : ANMtokens.Jet(w),"duif":lambda w,a: ANMtokens.Duif(w,a),
"schaap":lambda w : ANMtokens.Schaap(w),"lam":lambda w : ANMtokens.Lam(w),"aap":lambda w,x,y,a: ANMtokens.Aap(w,x,y,a),"noot": lambda w,v: ANMtokens.Noot(w,v),"mies": lambda w: ANMtokens.Mies(w),
"vuur": lambda w : ANMtokens.Vuur(w), "does": lambda w, v : ANMtokens.Does(w,v), "hok": lambda w : ANMtokens.Hok(w), "teun" : lambda w,v : ANMtokens.Teun(w,v)}

compilerLambdaDict = {"weide" : lambda *args : ANMCompilerTokens.Weide(), "hok": lambda *args : ANMCompilerTokens.Hok(), "wim": lambda *args : ANMCompilerTokens.branch_to(args[0]), "jet": lambda *args : ANMCompilerTokens.branch_to(args[0]),
"does" : lambda *args: ANMCompilerTokens.set_scratch_registers(args[1])+ANMCompilerTokens.branch_to(args[0]), "duif" : lambda *args: ANMCompilerTokens.Duif(args[0]), "schaap" : lambda *args : ANMCompilerTokens.branch_to(args[0]),
"lam" : lambda *args : ANMCompilerTokens.branch_to(args[0]), "teun" : lambda *args : ANMCompilerTokens.set_scratch_registers(args[1])+ANMCompilerTokens.branch_to(args[0])
,"aap" : lambda *args : ANMCompilerTokens.set_scratch_registers(args[1],args[2],args[3])+ANMCompilerTokens.branch_to(args[0]), "noot" : lambda *args : ANMCompilerTokens.set_scratch_registers(args[1])+
ANMCompilerTokens.branch_to(args[0]),"mies" : lambda *args : ANMCompilerTokens.branch_to(args[0]),"vuur": lambda *args: ANMCompilerTokens.branch_to(args[0])} 