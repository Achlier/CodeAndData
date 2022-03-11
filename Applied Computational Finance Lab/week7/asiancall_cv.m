function [Pasian_cv,CIasian_cv,Pasian,CIasian,Pgm,CIgm,Pgeo] = asiancall_cv(S0,K,r,sigma,T,n,N,b)
dt= T/n;
R = exp(-r*T);
m = (r - sigma^2/2)*dt;
s = sigma*sqrt(dt);
Vcall = zeros(1,N);
Vgmcall = zeros(1,N);
for j = 1:N
    Z= m+s*randn(1,n);
    S = cumsum([log(S0), Z],2);
    Vcall(j) = max(mean(exp(S))-K,0); % Arithmetic average
    Vgmcall(j) = max(exp(mean(S))-K,0); % Geometric average
end
Pasian = mean(R*Vcall); 
CIasian = std(R*Vcall)/sqrt(N);
Pgm = mean(R*Vgmcall);
CIgm = std(R*Vgmcall)/sqrt(N);

sigmaG = sigma*sqrt(dt*(2*n+1)*(n+1)/(6*n));
muG = log(S0) + 1/2*(r-sigma^2/2)*(T+dt);
d1 = (muG -log(K) + sigmaG^2)/sigmaG;
d2 = d1 - sigmaG;
Pgeo = R*(exp(muG+0.5*sigmaG^2)*normcdf(d1) - K*normcdf(d2)); % the price of Geometric Asian option

Pasian_cv = R*Vcall - b*(R*Vgmcall-Pgeo);
CIasian_cv = std(Pasian_cv)/sqrt(N);
Pasian_cv = mean(Pasian_cv);
