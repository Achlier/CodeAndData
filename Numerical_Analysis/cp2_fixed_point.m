function [sol] = cp2_fixed_point(p0,tol,n0)
% input:
%     function fx,
%     initial approximation p0,
%     tolerance tol,
%     maximum number of iterations n0
% PS:
%    fx�����fx=x��������fx=0
i=1;
while i<=n0
%    fprintf("p"+(i-1)+":")
    fprintf('%f',p0)%�ɵ�һ��P��ʼ
    fprintf("\n")
    p=fx(p0);
%    fprintf("|p"+(i-1)+"-p"+i+"| :"+abs(p-p0)+"\n")
    if abs(p-p0)<tol
        fprintf('%9.9f',p)
        sol=p;
        break
    else
        i=i+1;
        p0=p;
    end
end