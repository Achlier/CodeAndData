%prime
primes(10)
%prime factor
factor(123)
%%
syms x y;
f = x^2-y^2
fff = factor(f);
fff
%%
exp(sym(pi))
%%
syms a b c d
f = a*x^2+b*x+c;
factor(f)
%%
syms a b c
A = [a b c; c a b; b c a]
det(A)
sum(A(1,:))
diag(A)
%%
syms x
f = sin(x)^2
diff(f)
syms x y
f = x^3*y^3
diff(f)
diff(f,y)
diff(f,y,2)
int(3*x^3*y^2,y)
%%
syms a b c x
eqn = a*x^2 + b*x + c
solve(eqn)
%%
syms x a b c
simplify(sin(x)^2 + cos(x)^2)
f = exp(c*log(sqrt(a+b)))
simplify(f)
syms x
M = [(x^2 + 5*x + 6)/(x + 2), sin(x)*sin(2*x) + cos(x)*cos(2*x);
    (exp(-x*i)*i)/2 - (exp(x*i)*i)/2, sqrt(16)]
simplify(M)
syms x
f = ((exp(-x*i)*i)/2 - (exp(x*i)*i)/2)/(exp(-x*i)/2 + ...
exp(x*i)/2)
simplify(f,50)
%%
syms x
expand((x+1)^3)
expand(sin(x+y))
%%
syms x
g = x^3 + 6*x^2 + 11*x + 6;
factor(g)
simplify(g)
horner(g)
%%
syms x y
f = x^2*y + 5*x*sqrt(y)
subs(f, x, 3)
syms x y
f = x^2*y + 5*x*sqrt(y)
subs(f, y, x)
%%
syms a b n t x
g = sin(a*t + b)
symvar(g) % symvar(g,1)
%%
syms x
f = x^3 - 6*x^2 + 11*x - 6
ezplot(f)
syms t
x = t*sin(5*t);
y = t*cos(5*t); 
ezplot(x,y)
%%
syms x y
f = x^2*y + 5*x*sqrt(y)
ezsurf(f)
f=real(5*tan(x+i*y));
ezsurf(f)
f=real(5*atan(x+i*y));
ezsurf(f)
%%
syms s t
r = 2 + sin(7*s + 5*t);
x = r*cos(s)*sin(t);
y = r*sin(s)*sin(t);
z = r*cos(t);
ezsurf(x,y,z)
%%
syms x y x0 y0;
f =y*exp(x-x0)-x*log(y);
ft=taylor(f,[x,y],[x0,y0],'order',3)
%%
syms x y x0 y0 u v;
f = y*exp(x - x0) - x*log(y);
ft = taylor(f, [x, y], [x0, y0], 'order', 3)
g = subs(f,[x, y],[x0*exp(u),y0*exp(v)]);
gt = taylor(g, [u, v], [0, 0], 'order', 3)
%%
syms x y x0 y0 u v;
f = y*exp(x - x0) - x*log(y);
df = jacobian(f,[x, y]);
d2f =jacobian(df, [x, y]);
ft =subs(f,[x, y],[x0, y0]) ...
+ subs(df,[x, y],[x0, y0])*[x-x0;y-y0] ...
+ 1/2*[x-x0,y-y0]*subs(d2f,[x, y],...
[x0, y0])*[x-x0;y-y0];