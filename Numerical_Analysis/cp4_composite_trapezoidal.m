function Ans = cp4_composite_trapezoidal(a,b,n)
% input:
%     function fx,
%     interval [a, b],
%     the patch n
h=(b-a)/n;
sum1=0;
for i=1:(n-1)
    sum1=sum1+fx(a+i*h);% change fx
end
Ans=h/2*(fx(a)+fx(b)+2*sum1);% change fx
end

