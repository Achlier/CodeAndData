clear;
global OptionData;
global NoOfOptions;
global NoOfIterations;
global PriceDifference;
NoOfIterations = 0;
load OptionData.m ;
%OptionData = [r,T,S0,K,Option Value,bid,offer]
Size = size(OptionData);
NoOfOptions = Size(1);
%input sequence in initial vectors [2*kappa*theta - sigma^2,theta,sigma,rho,v0]
%x0 = [0.05 0.05 0.5 -0.5 0.15];
x0 = [0.5 0.1 1.3 -0.75 0.2]; % 系数训练初始值
lb = [0 0 0 -1 0]; % 系数训练最小值
ub = [20 1 5 0 1]; % 系数训练最大值
options = optimset('MaxFunEvals',20000);
%sets the max no. of iteration to 20000 so that termination doesn't take place early.
tic;
Calibration = lsqnonlin(@HestonDifferences,x0,lb,ub);
toc;
Solution = [(Calibration(1)+Calibration(3)^2)/(2*Calibration(2)), Calibration(2:5)];
%output sequence in Solution = [kappa,theta,sigma,rho,v0]