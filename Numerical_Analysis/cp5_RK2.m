function Ans = cp5_RK2(h,a0,b0,lam,y0)
t=a0:h:b0;
forcast=zeros(1,length(t));
forcast(1)=y0;
c1=lam;%change
c2=1-c1;
a=1/(2*c2);
b=1/(2*c2);

for i = 2:length(t)-1
    k1=h*fx(a0+step*(i-1),y(i));
    k2=h*fx(a0+(i-2)*h+a*h,forcast(i-1)+b*k1);
    forcast(i)=forcast(i-1)+c1*k1+c2*k2;
end

Ans=forcast;

end