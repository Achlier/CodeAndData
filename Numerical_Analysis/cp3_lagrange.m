function Ans = cp3_lagrange(x_box,k,x)
% input:
%     all the x x_box
%     all the y y_box
%     the index of special x k
%     the target x
upper=1;
lower=1;
for i=1:length(x_box)
    if i ~= k
        upper=upper*(x-x_box(i));
        lower=lower*(x_box(k)-x_box(i));
    end
end
Ans=upper/lower;
end

