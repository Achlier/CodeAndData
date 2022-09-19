% lecture1.m
% exercise for lecture 1
help clock
doc clock
%% 
start=clock;
disp(size(start));
disp(start);
startString = datestr(start);
disp(startString);
save startTime.mat start startString
%% 
a = [1 2 3+1i];
disp(a');
disp(a.');
a = [1 2 3;4 5 6;];
p = prod(a);
s = sum(a);
disp(p);
disp(s);
r = rand(2,2);
disp(r);
rg = linspace(0,10,5);% or 1:2:10
disp(rg);
%% 
m = rand(5);
disp(m);
disp(m(1:2,:));
disp(m([1 3 5],2));
test = [1 2;4 5;7 8];
size(test);
size(test,2);
%% 
v = [5 2 8 7];
[minval,minind]=min(v);
disp([minval minind]);
disp(find(v==8));
disp(find(v<=7 & v>2));
%% 
x = linspace(0,4*pi,10);
y = sin(x);
plot(y);
plot(x,y);
%% 
% function[output1,output2,output3,]=funName(input1,input2,)
x = 0.0:pi/10:pi;
y = x;
[X,Y] = meshgrid(x,y);
f = func(X,Y);
%contour(X,Y,f);
surf(X,Y,f);
axis([0 pi 0 pi]);
axis equal;
%% 
p = 1;
q = 3;
sol = fzero(@(x) (x - p).*(x-q),0);
disp(sol);