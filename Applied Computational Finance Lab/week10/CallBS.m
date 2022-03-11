function callprice = CallBS(S0,K,vol,T,r) %Black-Scholes call price formula
matlen = length(T);
callprice = zeros(size(vol));
for i = 1:matlen
    d1 = (log(S0./K) + (r+0.5*vol(1:end,i).^2)*T(i))./(vol(1:end,i)*T(i)^0.5);
    d2 = d1 - vol(1:end,i)*T(i)^0.5;
    callprice(1:end,i) = S0*normcdf(d1)-K*exp(-r*T(i)).*normcdf(d2);
end
