function [alphaHat, betaHat] = OLS3
global x y
load data;
[sol, fval] = fsolve('focs',[2 1], optimset('TolFun',1.e-10));
error = sum(fval.^2);
if (error > sqrt(1.e-10))
disp('sol is not a zero!');
end
alphaHat = sol(1);
betaHat = sol(2);
