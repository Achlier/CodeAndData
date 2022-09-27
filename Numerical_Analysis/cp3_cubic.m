function [Ans,a_box,b_box,c_box,d_box] = cp3_cubic(x_box,y_box,x,inter)
% input:
%     function fx
%     all the x x_box
%     all the y y_box
%     the target x
%     the interval your target in
% PS:
%    x must between x0 and xn
%    fx or y_box

% if no y_box
% a_box=fx(x_box);

a_box=y_box;

n=length(x_box);
h_box=x_box(2:n)-x_box(1:n-1);

A=zeros(n,n);
A(1,1)=1;%change!!! 改变首尾两式子
A(n,n)=1;%change!!! 改变首尾两式子
for i=2:n-1
    A(i,i-1)=h_box(i-1);
    A(i,i)=2*(h_box(i-1)+h_box(i));
    A(i,i+1)=h_box(i);
end

b=zeros(n,1); %change!!! 改变首尾两式子
for i=2:n-1
    b(i)=3*((a_box(i+1)-a_box(i))/h_box(i)-(a_box(i)-a_box(i-1))/h_box(i-1));
end

c_box=inv(A)*b;

d_box=zeros(n,1);
d_box(1:n-1)=(c_box(2:n)-c_box(1:n-1))./(3*h_box(1:n-1)');
b_box=zeros(1,n);
b_box(1:n-1)=(a_box(2:n)-a_box(1:n-1))./h_box(1:n-1)-c_box(1:n-1)'.*h_box(1:n-1)-d_box(1:n-1)'.*h_box(1:n-1).*h_box(1:n-1);


Ans=a_box(1)+b_box(1)*(x-x_box(inter))+c_box(1)*(x-x_box(inter))^(2)+d_box(1)*(x-x_box(inter))^(3);
end

