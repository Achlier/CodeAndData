function [alphaHat, betaHat] = OLS4
global x y
load data;
[sol, fval] = fminsearch('SSE',[1 .5],optimset('TolFun',1.e-15,'display','final'));
alphaHat = sol(1);
betaHat = sol(2);
