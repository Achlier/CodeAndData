function [sol] = cp2_bisection(a,b,tol,n0)
% input:
%     function fx,
%     interval [a, b],
%     tolerance tol,
%     maximum number of iterations n0
i=1;
fa=fx(a);
if fa*fx(b)>0
    fprintf("Please change the interval [a, b].")
else
    while i<=n0
        p=a+(b-a)/2;
        fp=fx(p);
        fprintf('%9.9f',p)%由第一个P开始
        fprintf("\n")
        fprintf("a:"+a+" b:"+b+" p:"+p+"\n")
        fprintf("fa:"+fa+" fb:"+fx(b)+" fp:"+fp+"\n")
        if fp==0 || (b-a)/2<tol
            sol=p;
            break
        else
            i=i+1;
            if fa*fp>0
                a=p;
                fa=fp;
            else
                b=p;
            end
        end
    end
end

