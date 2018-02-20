* first we need regression *
xtreg ln_population ///
ktx_lead3 ktx_lead2 ktx_lead1 ktx ktx_lag1 ktx_lag2 ktx_lag3 ///
controls, fe robust

* then we use the coefficients from the regression result *
coefplot, keep(ktx_lead3 ktx_lead2 ktx_lead1 ktx ktx_lag1 ktx_lag2 ktx_lag3) ///
title(pre/post effect) yline(0) yscale(range(-0.1 0.1)) name(ln_population) vertical ///
coeflabels(ktx_lead3 = "t-3" ktx_lead2 = "t-2" ktx_lead1 = "t-1" ktx = "t" ktx_lag1 = "t+1" ktx_lag2 = "t+2" ktx_lag3 = "t+3")
