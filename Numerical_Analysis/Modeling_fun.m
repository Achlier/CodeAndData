function Ans = Modeling_fun(t,h,yt,yt1)
% yt : value for y(t)
% p  : value fot y(t+1)

y0 = 250;
e = 0.0001;
Ans = yt + (1.3-e*t/2*y0) * h * yt1 + (-e*t/2-0.25) * h * yt1^(2);

end

