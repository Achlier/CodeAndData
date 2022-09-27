function Ans = cp4_secondly_three_point_mid(x_box,fx_box,h)
% input:
%     function fx
%     all the x x_box
%     all the y y_box
% PS:
%    x_box 从小到大，x和fx二选一
if isempty(fx_box)
    A=[1 -2 1];
    B=[fx(x_box(1));fx(x_box(2));fx(x_box(3))];
    Ans=A*B/(h*h);
else
    A=[1 -2 1];
    B=[fx_box(1);fx_box(2);fx_box(3)];
    Ans=A*B/(h*h);
end
end