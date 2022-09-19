function [answer, fz, iflag] = NewtonRaphson(func,x0)
global tolerance maxits delta;
iterations = 0 ; x = x0;
while (iterations<maxits) && (abs(func(x))>tolerance)
f0 = func(x);
f1 = func(x+delta);
x = x-f0*delta/(f1-f0);
iterations = iterations + 1;
end
answer = x; fz = func(x);
if iterations>maxits
iflag = 0;disp('No root found')
else
iflag = 1;disp(['Root = ' num2str(x) ' found in ' num2str(iterations) ' iterations.'])
end