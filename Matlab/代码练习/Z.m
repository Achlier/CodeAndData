function [z] = Z(x,y)
z = exp(x).*cos(y)+sin(x.^2-y);
end

