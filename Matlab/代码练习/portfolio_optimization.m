function [X] = portfolio_optimization(R,H,rf)
% Z = H^(-1)(R-rf)
n = length(R);
X = zeros(n,1);
Z = inv(H)*(R-rf);
Z_sum = sum(Z);
for i = 1:1:n
    X(i)=Z(i)/Z_sum;
end
end

