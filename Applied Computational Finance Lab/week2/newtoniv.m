function vol=newtoniv(S,K,r,T,price,callput)
% S is stock price, 
% K is strike price,  
% r is free interest rate, 
% T is time to maturity, 
% price is market option price,
% callput is 1 if call 0 if put

vol     = 1.0; % initial value of implied volatility
sigma   = vol+0.1; % sigma is volatility in BS model
maxiter = 20;
tol     = 1e-4;
iter    = 0;
% newton-raphson method
while abs(sigma-vol)>tol || iter < maxiter % precision of result
    sigma = vol;
    d1    = (log(S/K)+(r+sigma^2/2)*T)/(sigma*sqrt(T));
    d2    = d1-sigma*sqrt(T);
    if callput == 1
        cp = S*normcdf(d1)-K*exp(-r*T)*normcdf(d2);   %European call option price under BS model
    else
        cp = K*exp(-r*T)*normcdf(-d2) - S*normcdf(-d1);   %European put option price under BS model
    end
    fsigma = cp-price; %function for computing implied volatility
    vega   = S*sqrt(T)*normpdf(d1);%call/put vega
    vol    = sigma-fsigma/vega;
    iter   = iter + 1;
end

    
    