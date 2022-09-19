r = 0; u = 4/3; d = 3/4; 
strike = 1; S0 = 1; T = 4; N = T;
SS = zeros(N,T);
SS(1,1) = S0;
for t = 2:T
    for n = 1:t
        SS(n,t) = S0*u^(t-n)*d^(n-1);
    end
end
payoff = max((strike-SS(:,T)),0);
rnp = (1+r-d)/(u-d);
PayOffMatr = zeros(N,T);
PayOffMatr(:,T) = payoff;
for j=T-1:-1:1
    for k = 1:N-1
        % PayOffMatr(k,j) = max(((PayOffMatr(k,j+1)*rnp+ PayOffMatr(k+1,j+1)*(1-rnp))/(1+r)),(strike-SS(k,j)));
        PayOffMatr(k,j) = (PayOffMatr(k,j+1)*rnp + PayOffMatr(k+1,j+1)*(1-rnp))/(1+r);
    end
end
% call	s-k
% put	k-s
%%
% Alternatively
% for j=T-1:-1:1
% for k = 1:N-1
% PayOff0 = (PayOffMatr(k,j+1)*rnp ...
% + PayOffMatr(k+1,j+1)*(1-rnp))/(1+r);
% if PayOff0 > (strike-SS(k,j))
% PayOffMatr(k,j) = PayOff0; IndWait(k,j) = 1;
% else
% PayOffMatr(k,j) = (strike-SS(k,j)); IndWait(k,j) = 0;
% end
% end
% end
% ctrl+R/T