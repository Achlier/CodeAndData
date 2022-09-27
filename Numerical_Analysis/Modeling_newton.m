function [sol] = Modeling_newton(step,t,yt,p0,tol,n0)
% input:
%     i time
%     yt value for y(t)
%     function fx,
%     initial approximation p0,
%     tolerance tol,
%     maximum number of iterations n0
i=1;
while i<=n0
    p=p0-Modeling_fun(t,step,yt,p0)/Modeling_dfun(t,step,p0);
    if abs(p-p0)<tol
        sol=p;
        break
    else
        i=i+1;
        p0=p;
    end
end