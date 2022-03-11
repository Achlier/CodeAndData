S=260.05;% stock price
r=0.02; % interest rate
T=[4/365,11/365,18/365,25/365,32/365]; % time maturity
K=[250,252.5,255,257.5,260,262.5,265,267.5,270];%strike price
C=[ 10.4 7.73 5.8 3.8 2.3 1.19 0.55 0.25 0.12;
    10.24 8.69 6.6 4.85 3.3 2.2 1.29 0.81 0.46;
    10.9 8.23 6.4 4.65 3.42 2.45 1.72 1.11 0.75;
    12 9.89 7.95 6.4 4.9 3.84 2.52 1.8 1.4;
    11.57 10.83	8.02 7.26 5.7 4.1 3.55 2.54 1.97;];%prices for different maturities in rows
volatility=zeros(5,9);
% plot implied volatility surface
[x,y]=meshgrid(K,T);
for i=1:5  
   for  j=1:9
     % volatility(i,j)=blsimpv(S,K(j),r,T(i),C(i,j));
     volatility(i,j)=newtoniv(S,K(j),r,T(i),C(i,j),1);
   end
end
surf(x,y,volatility)


