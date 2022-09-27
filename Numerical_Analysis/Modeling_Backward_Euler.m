function Ans = Modeling_Backward_Euler(step,y0)
% step : ²½³¤

tol=10^(-10);
n0=50;
t=0:step:20;
y=zeros(1,length(t));
y(1)=y0;

for i = 1:length(t)-1
    p0 = y(i);
    y(i+1)=Modeling_newton(step,i*step,p0,p0,tol,n0);
end

Ans = y;

end