function [Ans] = cp3_hermite_3(x,x0,x1)
% input:
%     function fx
%     the target x
%     the point x0,x1
L0=@(x) (x-x1)/(x0-x1);
L1=@(x) (x-x0)/(x1-x0);
dL0=@(x) 1/(x0-x1);
dL1=@(x) 1/(x1-x0);
H0=@(x) (1-2*(x-x0)*dL0(x0))*L0(x)^(2);
H1=@(x) (1-2*(x-x1)*dL1(x1))*L1(x)^(2);
dH0=@(x) (x-x0)*L0(x)^(2);
dH1=@(x) (x-x1)*L1(x)^(2);
Ans=fx(x0)*H0(x)+fx(x1)*H1(x)+dfx(x0)*dH0(x)+dfx(x1)*dH1(x);
end

