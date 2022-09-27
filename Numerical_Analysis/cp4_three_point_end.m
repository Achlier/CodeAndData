function Ans = cp4_three_point_end(x_box,fx_box,h)
% input:
%     function fx
%     all the x x_box
%     all the y y_box
% PS:
%    x_box 从小到大，x和fx二选一，h 正或者负
if isempty(fx_box)
    A=[-3 4 -1];
    if h>0
        B=[fx(x_box(1));fx(x_box(2));fx(x_box(3))];
    else
        B=[fx(x_box(3));fx(x_box(2));fx(x_box(1))];
    end
    Ans=A*B/(2*h);
else
    A=[-3 4 -1];
    if h>0
        B=[fx_box(1);fx_box(2);fx_box(3)];
    else
        B=[fx_box(3);fx_box(2);fx_box(1)];
    end
    Ans=A*B/(2*h);
end
end

