function Ans = cp4_composite_simpson(a,b,n)
% input:
%     function fx,
%     interval [a, b],
%     the patch n
h=(b-a)/n;
sum1=0;
sum2=fx(a+(n-1)*h);% change fx
for i=1:(n/2-1)
    sum1=sum1+fx(a+2*i*h);% change fx
    sum2=sum2+fx(a+(2*i-1)*h);% change fx
end
Ans=h/3*(fx(a)+fx(b)+2*sum1+4*sum2);% change fx
end

