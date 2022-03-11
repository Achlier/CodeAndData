function ST=BSpath(S0,mu,sigma,T,n,N)
% S0 is the initial stock price, 
% K is strike price,  
% r is free interest rate, 
% T is time to maturity, 
% n is the number of time discretisation steps,
% N is the sample size
% mu is the asset's rate of return 
% sigma is the asset's volatility

nstep = power(2,n); % 步数
delt = T/nstep; % 每步时间间隔
const = ones(N,nstep+1)*(mu - 0.5*sigma*sigma)*delt; % 计算 s（t+1）时固定增长量
BMval = normrnd(0,1,[N,nstep+1]); % Brownian Motion Value/Matrix
BMval(1:N,1) = 0;
const(1:N,1) = 0;
incr = const + sigma*sqrt(delt)*BMval;
ST = S0*cumprod(exp(incr));
end
