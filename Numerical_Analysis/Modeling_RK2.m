function Ans = Modeling_RK2(lam,h,y0)
t=0:h:20;
forcast=zeros(1,length(t));
forcast(1)=y0;
c1=lam;%change
c2=1-c1;
a=1/(2*c2);
b=1/(2*c2);
forcast(2)=y0+h*(1.3*y0-0.25*y0^(2));
midlist=zeros(1,length(t));
midlist(1)=0;%从0积分到0
midlist(2)=h/2*forcast(2);%从0积分到1*h
midlist(3)=2*h*forcast(2);%从0积分到2*h


for i = 3:length(t)
    midlist(i)=2*h*forcast(i-1)+midlist(i-2);
    k1=h*Modeling_midfun((i-2)*h,forcast(i-1),midlist(i-1));
    k2=h*Modeling_midfun((i-2)*h+a*h,forcast(i-1)+b*k1,midlist(i-2)+a*h*(midlist(i-1)-midlist(i-2)));
    forcast(i)=forcast(i-1)+c1*k1+c2*k2;
end

Ans=forcast;

end