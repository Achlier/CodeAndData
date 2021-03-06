S0 = 100; %Starting price
r = 0.05; %interest rate
T = 1; %call option maturity
n = 10; %exponent in the number of time steps
N = 1000; %number of Monte Carlo sample paths
mu = 0.02; %asset return
sigma = 0.2; %volatility parameter
K = 80; %option strike
cprice = blsprice(S0,K,r,T,sigma); %Black-Scholes call price

nstep = power(2,n); %number of time steps
tstep = T/nstep; %time step size
tdisc = linspace(0,T,nstep+1);
dW = zeros(nstep+1,N); 
dW(2:nstep+1,1:N) = normrnd(0,1,[nstep,N])*sqrt(tstep); %Brownian motion increments
W = cumsum(dW,1); %Brownian motion paths
tgrid = (tdisc.').*ones(nstep+1,N); %discretised time grid
incr = sigma*W + (mu-0.5*sigma*sigma)*tgrid; %expression in the Black-Scholes price formula
ST = S0*exp(incr); %Black-Scholes price path
tt = ((T - tdisc).').*ones(nstep+1,N); %time to maturity
dfmat = exp(-r*tgrid); %discount factor

d1 = (log(ST(1:nstep,1:N)./(K*exp(-r*tt(1:nstep,1:N)))) + 0.5*sigma*sigma*tt(1:nstep,1:N))./(sigma*sqrt(tt(1:nstep,1:N)));
delta = normcdf(d1); %delta at different time steps excluding the final maturity time
pricediff = ST(2:nstep+1,1:N).*dfmat(2:nstep+1,1:N) - ST(1:nstep,1:N).*dfmat(1:nstep,1:N); %difference between two consecutive values of discounted asset price
sumholding = sum(delta.*pricediff,1); %final value of the holding in the underlying asset
X = exp(r*T)*(cprice + sumholding); %final value of the self-financing portfolio
upayoff = (ST(end,1:N)-K);
payoff = upayoff.*(upayoff>0); %payoff from option exercise
PNL = X - payoff; %Profit and loss over Monte Carlo sample paths