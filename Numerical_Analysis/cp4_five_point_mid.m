function Ans = cp4_five_point_mid(x_box,fx_box,h)
% input:
%     function fx
%     all the x x_box
%     all the y y_box
% PS:
%    x_box 从小到大，x和fx二选一
if isempty(fx_box)
    A=[1 -8 8 -1];
    B=[fx(x_box(1));fx(x_box(2));fx(x_box(4));fx(x_box(5))];
    Ans=A*B/(12*h);
else
    A=[1 -8 8 -1];
    B=[fx_box(1);fx_box(2);fx_box(4);fx_box(5)];
    Ans=A*B/(12*h);
end
end

