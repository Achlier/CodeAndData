function ret = HestonDifferences(input)
global NoOfOptions;
global OptionData;
global NoOfIterations;
global PriceDifference;
NoOfIterations = NoOfIterations + 1;
%counts the no of iterations run to calibrate model
for i = 1:NoOfOptions
PriceDifference(i) = (OptionData(i,5)-HestonCallQuad( ...
(input(1)+input(3)^2)/(2*input(2)),input(2),input(3),input(4),input(5), ...
OptionData(i,1),OptionData(i,2),OptionData(i,3),OptionData(i,4)))...
/sqrt((abs(OptionData(i,6)- OptionData(i,7))));
%Option Value-Estimated Value(4个系数，4个已知)
%kappa=(?+sigma^2)/2theta,theta,sigma,rho,v0,r,T,s0,K
%sqrt((abs(OptionData(i,6)-OptionData(i,7))))-> w_ij (weight)
end
ret = PriceDifference';