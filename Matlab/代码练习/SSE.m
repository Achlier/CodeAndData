function out = SSE(in)
global x y
alphaHat = in(1);
betaHat = in(2);
out = sum( ( y- alphaHat - betaHat .* x ).^2); 
