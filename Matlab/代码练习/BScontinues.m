function out = BScontinues(S,K,sig,r,b,T)
tmp = sig * sqrt(T);
d1 = (log(S/K) + (b + (sig*sig)*0.5)*T)/tmp;
d2 = d1 - tmp;
out=S*exp((b-r)*T)*normcdf(d1) - K * exp(-r*T)*normcdf(d2);

