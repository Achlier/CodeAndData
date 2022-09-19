function F = func11(x)
F(1) = exp(-exp(-x(1)+x(2)))-x(2)^2*(1+x(1)^2);
F(2) = x(1)*tan(x(2))+x(2)*sin(x(1))-0.5;
end

