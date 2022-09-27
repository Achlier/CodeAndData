function Ans = cp4_five_point_end(x_box,fx_box,h)
% input:
%     function fx
%     all the x x_box
%     all the y y_box
% PS:
%    x_box 从小到大，x和fx二选一，h 正或者负
if isempty(fx_box)
    A=[-25 48 -36 16 -3];
    if h>0
        B=[fx(x_box(1));fx(x_box(2));fx(x_box(3));fx(x_box(4));fx(x_box(5))];
    else
        B=[fx(x_box(5));fx(x_box(4));fx(x_box(3));fx(x_box(2));fx(x_box(1))];
    end
    Ans=A*B/(12*h);
else
    A=[-25 48 -36 16 -3];
    if h>0
        B=[fx_box(1);fx_box(2);fx_box(3);fx_box(4);fx_box(5)];
    else
        B=[fx_box(5);fx_box(4);fx_box(3);fx_box(2);fx_box(1)];
    end
    Ans=A*B/(12*h);
end
end
