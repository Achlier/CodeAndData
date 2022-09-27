function Ans = cp7_Jacobi(A,B,x)
n= length(B);
x_n=zeros(n,1);
for i = 1:n
    x_n(i)=1/A(i,i)*(-sum(A(i,:)*x)+B(i)+A(i,i)*x(i));
end
Ans=x_n;
end

%if 使用x_n则另一种方法