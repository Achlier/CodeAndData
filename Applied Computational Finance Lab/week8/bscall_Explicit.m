clear all
close all

J=1000;
S0=17;
% time steps to ensure numerical convergence
N = J^2;
K = 15;
logstrk = log(K);
T=0.3041;
r=0.03;
sigma = 0.25;
mu = r - 0.5*sigma^2;
xmin = log(10e-6);
xmax = log(2*K);
dx=(xmax-xmin)/J; 
x=[xmin:dx:xmax]'; %length = J+1
dt=T/N;

V=max(0,exp(x)-K);
Vold=V;
const1 = 1 - sigma^2*dt/dx^2;
const2 = 0.5*sigma^2*dt/dx^2;
const3 = 0.5*mu*dt/dx;

for n=1:N 
    %boundary condition at x = xmin  
    V(1)=0;  
        
    for j=2:J %in the interior
        V(j)= Vold(j)*const1 + Vold(j+1)*(const2+const3) + Vold(j-1)*(const2-const3) - r*dt*Vold(j);
    end
    
    %boundary condition at x = xmax
    V(J+1)= exp(xmax)-K;
    
    Vold=V;
end

V_Final = interp1(x, V, log(S0));

figure(1)
clf
plot(exp(x),V)
xlabel('asset price')
ylabel('call price')
