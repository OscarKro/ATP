import ANMtokens
import ANMCompilerTokens

checkNrParamDict = {"weide":0,"wim":0,"jet":0,"duif":1,"schaap":0,"lam":0,"aap":2,"noot":1,"mies":0,"vuur":0,"hok":1,"does":1,"teun":1,"bok":1}

interperterlambdaDict = {"weide": lambda w : ANMtokens.Weide_func(w), "wim":lambda w : ANMtokens.Wim(w),"jet":lambda w : ANMtokens.Jet(w),"duif":lambda w,a: ANMtokens.Duif(w,a),
"schaap":lambda w : ANMtokens.Schaap(w),"lam":lambda w : ANMtokens.Lam(w),"aap":lambda w,x,y,a: ANMtokens.Aap(w,x,y,a),"noot": lambda w,v: ANMtokens.Noot(w,v),"mies": lambda w: ANMtokens.Mies(w),
"vuur": lambda w : ANMtokens.Vuur(w), "does": lambda w, v : ANMtokens.Does(w,v), "hok": lambda w : ANMtokens.Hok(w), "teun" : lambda w,v : ANMtokens.Teun(w,v)}

compilerLambdaDict = {"weide" : lambda *args : ANMCompilerTokens.Weide(), "hok": lambda *args : ANMCompilerTokens.Hok(args[1]), "bok" : lambda *args : ANMCompilerTokens.Bok(args[1]),
 "wim": lambda *args : ANMCompilerTokens.Wim(), "jet": lambda *args : ANMCompilerTokens.Jet(),
"does" : lambda *args: ANMCompilerTokens.set_scratch_registers(args[1])+ANMCompilerTokens.Does(), "duif" : lambda *args: ANMCompilerTokens.Duif(args[1]), "schaap" : lambda *args : ANMCompilerTokens.Schaap(),
"lam" : lambda *args : ANMCompilerTokens.Lam(), "teun" : lambda *args : ANMCompilerTokens.set_scratch_registers(args[1])+ANMCompilerTokens.Teun()
,"aap" : lambda *args : ANMCompilerTokens.set_scratch_registers(args[1],args[2])+ANMCompilerTokens.Aap(args[3],args[4]), "noot" : lambda *args : ANMCompilerTokens.set_scratch_registers(args[1])+
ANMCompilerTokens.Noot(),"mies" : lambda *args : ANMCompilerTokens.Mies(),"vuur": lambda *args: ANMCompilerTokens.Vuur()} 