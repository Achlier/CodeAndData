x = -pi:pi/100:pi;
y = cos(4*x).*sin(10*x).*exp(-abs(x));
plot(x,y,'k.-');
%%
time = 0:0.01:4*pi;
x = sin(time);
y = cos(time);
z = time;
plot3(x,y,z,"k--","LineWidth",2)
zlabel("Time");
%axis square,tight,equal
axis ij
%%
alpha = 0.5; beta = 2; N = 10;
x = (1:1:N)';
y = alpha + beta*x + randn(N,1);
%%
plot(x,y,"b");
hold on;
plot(x,alpha+x*beta,":r");
hold off;
legend("data","fitted data");
xlabel("x"); ylabel("y");
text(5, 1, "add text here");
title("Originary Least Square Regression");
%%
subplot(1,2,1);
plot(x,y,":m");
grid on 
subplot(1,2,2);
scatter(x,y,"r");
%%
x = -pi:0.1:pi;
y = -pi:0.1:pi;
[X,Y] = meshgrid(x,y);
Z = sin(X).*cos(Y);
%%
subplot(1,1,1);
surf(X,Y,Z);
%surf(x,y,Z);
%shading faceted,flat,interp
colormap('spring')
%%
mesh(X,Y,Z);
%%
contour(X,Y,Z);
colormap('winter');
colorbar
%%
phi = 3;
c = 0.1:0.1:5;
n = 0.0:0.1:1;
[C,N] = meshgrid(c,n);
U = log(C) - N.^(1+phi)/(1+phi);
figure(4)
subplot(1,2,1); surf(C,N,U);
colormap('HSV');
xlabel('consumption'); ylabel('labour'); zlabel('utility')
subplot(1,2,2)
contour(C,N,U,'ShowText','on'); xlabel('consumption');
ylabel('labour')
%%
for n=1:3
 x=-pi:0.1:pi;
 y=-pi:0.1:pi;
 [X,Y]=meshgrid(x,y);
 Z =sin(n*X).*cos(Y/n);
 subplot(1,3,n);
 surf(X,Y,Z);
end