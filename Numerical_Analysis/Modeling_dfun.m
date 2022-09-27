function Ans = Modeling_dfun(t,h,yt1)
% p  : value fot y(t+1)

y0 = 250;
e = 0.0001;
Ans = (1.3-e*t/2*y0) * h + 2 * (-e*t/2-0.25) * h * yt1;

end

