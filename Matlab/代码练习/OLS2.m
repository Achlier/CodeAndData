function [alphaHat, betaHat] = OLS2
load data;
N = length(x);
meanX = sum(x)/N;
meanY = sum(y)/N;
betaHat = sum((x-meanX).*(y-meanY))./sum((x-meanX).^2);
alphaHat = mean(y) - betaHat * mean(x);
