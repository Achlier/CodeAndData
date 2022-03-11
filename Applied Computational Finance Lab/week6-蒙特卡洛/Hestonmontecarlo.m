% European call option under Heston model with Euler-Maruyama-Method and Milstein method
clear all;
M = 50000; % number of paths
N = 100;% number of time steps
T = 1;% maturity
h = T/N;%delta t
S0 = 100; 
sigma20 = 0.0625; %variance at t=0
K=100; % strike
kappa = 2;
theta = 0.4;
nu = 0.2;
rho = -0.7;
r=0.02;

% two dimensional Brownian motion
dW1 = randn(M,N+1)*sqrt(h);
dW2 = rho*dW1 + sqrt(1-rho^2)*randn(M,N+1)*sqrt(h);

% Initialisation of stock price and volatility for Euler Maruyama method
S = S0*ones(M,N+1);
sigma2 = sigma20*ones(M,N+1);

% Solution of the SDE-System with Euler-Maruyama-Method
% NOTE: we don't need to store the entire simulation path to compute the 
%European option payoff!
for i = 1:N
    sigma2(:,i+1) = sigma2(:,i) + kappa*(theta-sigma2(:,i))*h ...
        + nu*sqrt(abs(sigma2(:,i))).*dW2(:,i);
    S(:,i+1) = S(:,i).*(1 + r*h + sqrt(abs(sigma2(:,i))).*dW1(:,i));
end

payoff = exp(-r*T)*max(0,S(:,end)-K);
stdpayoff = std(payoff);
V = mean(payoff)
Vleft = V - 1.96*stdpayoff/sqrt(M)
Vright = V + 1.96*stdpayoff/sqrt(M)

% Initialisation of stock price and volatility for Milstein method
S1 = S0*ones(M,N+1);
sigma3 = sigma20*ones(M,N+1);
% Solution of the Milstein method

for i = 1:N
    sigma3(:,i+1) = sigma3(:,i) + kappa*(theta-sigma3(:,i))*h ...
        + nu*sqrt(abs(sigma3(:,i))).*dW2(:,i)+1/4*nu.*(dW2(:,i).^2-h);
    S1(:,i+1) = S1(:,i).*(1 + r*h + sqrt(abs(sigma3(:,i))).*dW1(:,i))+1/2*sigma3(:,i).*S1(:,i).*(dW1(:,i).^2-h);
end

payoff1 = exp(-r*T)*max(0,S1(:,end)-K);
stdpayoff1 = std(payoff1);
V1 = mean(payoff1)
V1left = V1 - 1.96*stdpayoff1/sqrt(M)
V1right = V1 + 1.96*stdpayoff1/sqrt(M)