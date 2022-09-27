function Ans = Modeling_midfun(t,y,midnum)
%Modeling_midfun(t,h,yh,yh2)
% yh : value for y(t-step)
% yh2  : value fot y(t-step/2)

e = 0.0001;
Ans = 1.3*y-0.25*y^(2)-e*y*midnum;

end

