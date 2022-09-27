function Ans = cp4_three_point_mid(x_box,fx_box,h)
% input:
%     function fx
%     all the x x_box
%     all the y y_box
% PS:
%    x_box 从小到大，x和fx二选一
if isempty(fx_box)
    A=[1 -1];
    B=[fx(x_box(3));fx(x_box(1))];
    Ans=A*B/(2*h);
else
    A=[1 -1];
    B=[fx_box(3);fx_box(1)];
    Ans=A*B/(2*h);
end
end
