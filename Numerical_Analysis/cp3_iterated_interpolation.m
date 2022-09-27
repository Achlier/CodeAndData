function [Ans] = cp3_iterated_interpolation(x_box,y_box,x)
% input:
%     function fx
%     all the x x_box
%     all the y y_box
%     the target x
n=length(x_box)-1;
Q=zeros(n,n);
if isempty(y_box)
    for i=1:n
        Q(i,1)=cp3_lagrange_interpolation([x_box(i),x_box(i+1)],[fx(x_box(i)),fx(x_box(i+1))],x);
    end
else
    for i=1:n
        Q(i,1)=cp3_lagrange_interpolation([x_box(i),x_box(i+1)],[y_box(i),y_box(i+1)],x);
    end
end
% Q     j1     j2     j3
%  [    p12,   p123,  p1234 ;i1
%              1-3    1-4
%       p23,   p234,  0     ;i2
%              2-4
%       p34,   0,     0     ;i3]
for j=2:n
    for i=1:n-j+1
        Q(i,j)=((x-x_box(i))*Q(i+1,j-1)-(x-x_box(i+j))*Q(i,j-1))/(x_box(i+j)-x_box(i));
    end
end
Ans=Q(1,n);
end

