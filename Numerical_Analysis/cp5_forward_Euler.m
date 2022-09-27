function Ans = cp5_forward_Euler(step,a,b,y0)
% step : ²½³¤
t=a:step:b;
y=zeros(1,length(t));
y(1)=y0;

for i = 1:length(t)-1
    y(i+1)=y(i)+step*fx(a+step*(i-1),y(i));
end

Ans = y;

end