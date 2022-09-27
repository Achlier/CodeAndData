function Ans = cp4_trapezoidal(interval)
% input:
%     function fx,
%     interval [a, b],
Ans=(interval(2)-interval(1))*(fx(interval(2))+fx(interval(1)))/2;
end