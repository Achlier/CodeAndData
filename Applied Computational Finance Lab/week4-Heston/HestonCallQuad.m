function call = HestonCallQuad(kappa,theta,sigma,rho,v0,r,T,s0,K)
warning off;
call = s0*HestonP(kappa,theta,sigma,rho,v0,r,T,s0,K,1) - ...
K*exp(-r*T)*HestonP(kappa,theta,sigma,rho,v0,r,T,s0,K,2);

function ret = HestonP(kappa,theta,sigma,rho,v0,r,T,s0,K,type)
ret = 0.5 + 1/pi*quadl(@HestonPIntegrand,0,100,[],[],kappa, ...
theta,sigma,rho,v0,r,T,s0,K,type);

function ret = HestonPIntegrand(phi,kappa,theta,sigma,rho, ...
v0,r,T,s0,K,type)
ret = real(exp(-1i*phi*log(K)).*Hestf(phi,kappa,theta,sigma, ...
rho,v0,r,T,s0,type)./(1i*phi));

function f = Hestf(phi,kappa,theta,sigma,rho,v0,r,T,s0,type)
if type == 1
u = 0.5;
b = kappa - rho*sigma;
else
u = -0.5;
b = kappa;
end
a = kappa*theta; x = log(s0);
d = sqrt((rho*sigma*phi.*1i-b).^2-sigma^2*(2*u*phi.*1i-phi.^2));
g = (b-rho*sigma*phi*1i + d)./(b-rho*sigma*phi*1i - d);
C = r*phi.*1i*T + a/sigma^2.*((b- rho*sigma*phi*1i + d)*T - ...
2*log((1-g.*exp(d*T))./(1-g)));
D = (b-rho*sigma*phi*1i + d)./sigma^2.*((1-exp(d*T))./ ...
(1-g.*exp(d*T)));
f = exp(C + D*v0 + 1i*phi*x);