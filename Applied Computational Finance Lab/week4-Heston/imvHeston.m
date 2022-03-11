% initialization of parameters for Heston model
s0=100;% stock price
r=0.02; % interest rate
kappa=5; % speed of mean reversion
theta=0.04;% long term mean
sigma=0.5; % volatility of volatility
rho=-0.7;
v0=0.5;% initial variance
T=[0.2,0.4,0.6,0.8,1]; % time maturity
K=[80,90,100,110,120]; % strike price

C=zeros(5,5);
for i=1:5
    for j=1:5
        C(i,j)=HestonCallQuad(kappa,theta,sigma,rho,v0,r,T(i),s0,K(j)); % European call option price under Heston model
    end
end

volatility=zeros(5,5);
% plot implied volatility surface
[x,y]=meshgrid(T,K);
for i=1:5
   for  j=1:5
     volatility(i,j)=blsimpv(s0,K(j),r,T(i),C(i,j));
   end
end
surf(x,y,volatility)
