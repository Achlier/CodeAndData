function [answer,errr] = bisect(fun,a,b)
global tolerance maxits;
iterations = 0 ;
f_a = feval(fun,a);
f_b = feval(fun,b);
while ((f_a*f_b<0) && iterations<maxits) && (b-a)>tolerance
iterations = iterations + 1 ;
c = (b+a)/2;
f_c = feval(fun,c);
if f_c*f_a<0
b=c; f_b = f_c;
else
a=c; f_a = f_c;
end
errr = (b-a); answer = c;
end
