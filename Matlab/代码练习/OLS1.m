function [alphaHat, betaHat] = OLS1
load data;
N = length(x);
X = [ones(N,1) x];
b = X\y;
%b = (X'*X)n(X'*y);
%b = inv(X'*X)*(X'*y);
alphaHat = b(1);
betaHat = b(2);

