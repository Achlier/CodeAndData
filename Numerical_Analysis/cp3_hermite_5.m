function [Ans] = cp3_hermite_5(x,x0,x1,x2)
% input:
%     function fx
%     the target x
%     the point x0,x1,x2
L0=@(x) ((x-x1)*(x-x2))/((x0-x1)*(x0-x2));
L1=@(x) ((x-x0)*(x-x2))/((x1-x0)*(x1-x2));
L2=@(x) ((x-x0)*(x-x1))/((x2-x0)*(x2-x1));
dL0=@(x) ((x-x1)+(x-x2))/((x0-x1)*(x0-x2));
dL1=@(x) ((x-x0)+(x-x2))/((x1-x0)*(x1-x2));
dL2=@(x) ((x-x0)+(x-x1))/((x2-x0)*(x2-x1));
H0=@(x) (1-2*(x-x0)*dL0(x0))*L0(x)^(2);
H1=@(x) (1-2*(x-x1)*dL1(x1))*L1(x)^(2);
H2=@(x) (1-2*(x-x2)*dL2(x2))*L2(x)^(2);
dH0=@(x) (x-x0)*L0(x)^(2);
dH1=@(x) (x-x1)*L1(x)^(2);
dH2=@(x) (x-x2)*L2(x)^(2);
Ans=fx(x0)*H0(x)+fx(x1)*H1(x)+fx(x2)*H2(x)+dfx(x0)*dH0(x)+dfx(x1)*dH1(x)+dfx(x2)*dH2(x);
end

