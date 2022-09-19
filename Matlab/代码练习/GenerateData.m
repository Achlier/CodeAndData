function GenerateData(alpha,beta,N)
x=[1:1:N]';
y=alpha + beta * x + randn(N,1);
save data x y;
figure(1);
plot(x,y,'b',x,alpha+x*beta,':r')

