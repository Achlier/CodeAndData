function out = focs(in)
global x y
alphaHat = in(1);
betaHat = in(2);
out(1) = sum(y-alphaHat-betaHat.*x);
out(2) = sum((y-alphaHat-betaHat.*x).*x);
