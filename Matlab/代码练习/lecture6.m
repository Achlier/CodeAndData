rand(2,3)
randi(100)
%rng(3)
rand('seed',3);
rand('seed')
%%
scores = 100*rand(1,100);
mean(scores)
median(scores)
mode(scores)
size(scores)
hist(scores,5:10:95); 
N=histc(scores,0:10:100);
bar(0:10:100,N,'r');
%%
x=zeros(10000,1);
for n=2:10000
 if rand<0.5
 x(n)=x(n-1)-1;
 else
 x(n)=x(n-1)+1;
 end
end
figure;
hist(x,50);
%%
normpdf(1,0,1)%pdf(norm,1,0,1)
normcdf(1,0,1)
norminv(0.841,0,1)
tpdf(3,15)
%%
left_tail = -exprnd(1,10,1);
right_tail = exprnd(5,10,1);
center = randn(80,1);
data = [left_tail;center;right_tail];
figure;
probplot(data);
p = mle(data,'dist','tlo');
t = @(data,mu,sig,df)cdf('tlocationscale',data,mu,sig,df);
h = probplot(gca,t,p); %gca µ±Ç°×ø±êÍ¼
h.Color = 'r';
h.LineStyle = '-';
title('{\bf Probability Plot}')
legend('Normal','Data','t','Location','NW')
%%
%randn('seed',1) % specify a seed (optional)
n=50; % number of observations
x=linspace(0,1,n); % linearly spaced vector a length n
y= 10*x + 3 + randn(1,n);
plot(x,y,'.')
xlabel('x')
ylabel('y')
mx=mean(x);
my=mean(y);
hold on;
plot(mx,my, 'ro', 'markerfacecolor','r')
legend('data', 'point of averages')
c= mean((x-mx).*(y-my)) % covariance (biased)
n=length(x);
cs= c*n/(n-1) % sample covariance(unbiased) 
zx=zscore(x,1);
zy=zscore(y,1);
r=mean(zx.*zy)
sx=std(x,1);
sy=std(y,1);
r=c/(sx*sy)
%%
ncoin = [1 3 5 10 20 50];
nroll=10000; % number of rolls
for i=1:length(ncoin),
ni=ncoin(i);
x=randi([0,1],ni,nroll) ; % coin flip: Head = 1 Tail =0
y=sum(x,1); % sample sum.
edges=min(y):max(y);
af=histc(y,edges); %absolute
rf=af/nroll; % relative
% plot figure
subplot(3,2,i)
stem(edges,rf,'filled')
title(['Number of Coins: n = ',num2str(ni)]);
xlabel('sample sum');
ylabel('rel. freq.');
end
%%
alpha = 0.5;
beta = 1.3;
N = 100;
GenerateData(alpha,beta,N);
[alphaHat1, betaHat1] = OLS1
[alphaHat2, betaHat2] = OLS2
[alphaHat3, betaHat3] = OLS3
[alphaHat4, betaHat4] = OLS4
%%
alpha = 0.5; beta = 2; N = 10;
x=[1:1:N]';
y=alpha + beta * x + randn(N,1);
save data x y;
figure(1);
%plot(x,y,'b',x,alpha+x*beta,':r')
plot(x,y,'b',x,alpha+x*beta,':r','LineWidth',3) % width of line
%%

plot(x,y,'b','LineWidth',2)
hold on;
plot(x,alpha+x*beta,':r','LineWidth',1)
hold on;
legend('data','fitted data');
xlabel('x'); ylabel('y');
text(5, 1,'add text here')
title('Ordinary Least Square Regression')
%%
figure(2)
subplot(1,2,1); plot(x,y,'b',x,alpha+x*beta,':r','LineWidth',3)
subplot(1,2,2); plot(x,y,'b',x,alpha+x*beta,':r')
figure(3)
subplot(2,2,1); plot(x,y,'b',x,alpha+x*beta,':r','LineWidth',3)
subplot(2,2,2); plot(x,y,'b',x,alpha+x*beta,':r')
subplot(2,2,3); plot(x,y,'b-',x,alpha+x*beta,':m')
subplot(2,2,4); plot(x,y,'g:',x,alpha+x*beta,'y-.','LineWidth',6)
%%
phi = 3;
c = [0.1:0.1:5];
n = [0.0:0.1:1];
[C,N] = meshgrid(c,n);
U = log(C) - N.^(1+phi)/(1+phi);
figure(3)
subplot(1,2,1); surf(C,N,U);
colormap('hsv');
xlabel('consumption'); ylabel('labour'); zlabel('utility')
subplot(1,2,2)
contour(C,N,U,'ShowText','on'); xlabel('consumption');
ylabel('labour');