function Ans = cp4_simpson(interval)
% input:
%     function fx,
%     interval [a, b],
Ans=(interval(2)-interval(1))*(fx(interval(1))+4*fx((interval(1)+interval(2))/2)+fx(interval(2)))/6;
end