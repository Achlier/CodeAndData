function Ans = cp3_lagrange_interpolation(x_box,y_box,x)
% input:
%     function fx
%     all the x x_box
%     all the y y_box
%     the target x
% PS:
%    x must between x0 and xn
%    fx or y_box
Ans=0;
if isempty(y_box)
    for i=1:length(x_box)
        Ans=Ans+cp3_lagrange(x_box,i,x)*fx(x_box(i));
    end
else
    for i=1:length(x_box)
        Ans=Ans+cp3_lagrange(x_box,i,x)*y_box(i);
    end
end
end

