function [X,PNL]=deltahedge(S0,K,r,mu,sigma,T,n,N)
% S0 is the initial stock price, 
% K is strike price,  
% r is free interest rate, 
% T is time to maturity, 
% n is the number of time discretisation steps,
% N is the sample size
% mu is the asset's rate of return 
% sigma is the asset's volatility

strike = K;
nstep = power(2,n); % number of time steps
delt = T/nstep;% time step size
tstep = linspace(0,T,nstep+1);
const = ones(N,nstep+1)*(mu - 0.5*sigma*sigma)*delt;
BMval = normrnd(0,1,[N,nstep+1]); % Brownian motion increments
BMval(1:N,1) = 0;
const(1:N,1) = 0;
incr = const + sigma*sqrt(delt)*BMval;
ST = S0*cumprod(exp(incr),2);
% Compute delta at each readjustment time
tt = T-tstep(1:nstep); % 剩余时间
X = zeros(N,length(K)); % final value of the self-financing portfolio
PNL = zeros(N,length(K)); % Profit and loss over Monte Carlo sample paths

for i=1:N
    for j=1:length(K)
        price = blsprice(S0,strike(j),r,T,sigma); % Black-Scholes call price
        d1 = (log(ST(i,1:nstep)./(strike(j)*exp(-r*tt))) + 0.5*sigma*sigma*tt)./(sigma*sqrt(tt));
        delta = normcdf(d1); % 每时期对冲需要的股票数
        temp = ST(i,2:nstep+1).*exp(-r*tstep(2:nstep+1)) - ST(i,1:nstep).*exp(-r*tstep(1:nstep)); % 每时期持有一单位股票收益
        chng = delta.*temp;
        X(i,j) = exp(r*T)*(price +sum(chng));
        PNL(i,j) = exp(-r*T)*(X(i,j) - max(ST(i,nstep+1)-strike(j),0));
    end
end
end