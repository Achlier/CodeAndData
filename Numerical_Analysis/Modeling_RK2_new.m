function Ans = Modeling_RK2_new(lam,h,y0)
t=0:h:20;
e=0.0001;
forcast=zeros(1,length(t));
forcast(1)=y0;
c1=lam;%change
c2=1-c1;
a=1/(2*c2);
b=1/(2*c2);
forcast(2)=y0+h*(1.3*y0-0.25*y0^(2));

tol=10^(-10);
n0=50;

for i = 2:length(t)
    k1=Modeling_newton(h,(i-1)*h,forcast(i-1),forcast(i-1),tol,n0)-forcast(i-1);
    k2=h*(1.5*(forcast(i-1)+b*k1)-0.25*(forcast(i-1)+b*k1)^(2)-e*(forcast(i-1)+b*k1)*(y0+(forcast(i-1)+b*k1))*(i-1+b)*h/2);
    forcast(i)=forcast(i-1)+c1*k1+c2*k2;
end

Ans=forcast;

end