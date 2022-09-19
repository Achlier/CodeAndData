M = [3 7 5; 1 9 10; 30 -1 2];
find(M>5)
min(M)
%%
A = [1 2 -3;-3 -1 1;1 -1 1;];
b = [5;-8;0];
A\b 
% = inv(A)*b
% det() - determinant
% eig - eigenvalue
% svd - singular value
% qr - QR 
%%
pq = [1 0 -2];
r = roots(pq);
poly(r)
polyval(pq,5)
%%
X = [-1 0 2];
Y = [0 -1 3];
plot(X,Y,"o");
hold on;
pq = polyfit(X,Y,2)
plot(-3:0.1:3,polyval(pq,-3:0.1:3),"r--");
hold off;
%%
global tolerance maxits delta;
p=-3; q = 2; xmin = -1; xmax = +5;
vec = xmin:0.1:xmax;
y = feval(@(x) (x - p).*(x-q),vec);
plot(vec,y,vec,zeros(1,length(vec)),':');
x0=(p+q)/2 + 0.4;
z = fzero(@(x) (x - p).*(x-q),x0)
% use bisection method
tolerance = 1e-8; maxits = 2000;
[z_b1,err1] = bisect(@(x) (x - p).*(x-q),xmin,xmax)
%%
delta = 1e-4;
[answ, fz, iflag] = NewtonRaphson(@(x) (x - p).*(x-q),xmin)
%%
% fminbnd("myfun",1,3);
% fminsearch("myfun,0.5);
fminbnd(@(x) (cos(exp(x))+x^2-1),-1,2)
%%
a = [1 2 4 5 8];
diff(a);
x = 0:0.01:2*pi;
y = sin(x);
dydx = diff(y)./diff(x);
plot(x(1:end-1),dydx-cos(x(1:end-1)));
%%
mat=[1 3 5;4 8 6];
dm=diff(mat,1,2)
%first difference of mat along the 2nd dimension
%%
q = quad(@(x)(sin(x).*x),0,pi);
help quad
x=0:0.01:pi;
z=trapz(x,sin(x))s
z2=trapz(x,sqrt(exp(x))./x)
help trapz