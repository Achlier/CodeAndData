%In the data provided, there are non-zero call option prices for 0 maturity.
%In order to do the calculations, drop the values corresponding to 0 maturity. 
T = 0.9;
n = 8;
num_step = 2^n;
S0 = 100;
r = 0.0;
dt = T/num_step;
dK = 0.1;
MaxCounter = 100; %number of maximum iterations for implied vol inversion
MaxVolLevel = 6.0;
N = 1000; %number of Monte Carlo sample paths
        
strk = load('strikes.txt'); %strike vector length 401
mat = load('maturities.txt'); %maturity vector length 257
mat = mat(2:end); %remove the maturity 0 entry
pr = load('optionprices.txt'); %price is STRK * MAT 
pr = pr(:,2:end);%remove the prices corresponding to maturity 0
%     
pr_T = zeros(size(pr));
pr_T(1:end,2:end-1) = (pr(1:end,3:end)-pr(1:end,1:end-2))/(2*dt);
pr_T(1:end,1) = (pr(1:end,2)-pr(1:end,1))/dt;
pr_T(1:end,end) = (pr(1:end,end)-pr(1:end,end-1))/dt;
%
pr_K = zeros(size(pr));
pr_K(2:end-1,1:end) = (pr(3:end,1:end)-pr(1:end-2,1:end))/(2*dK);
pr_K(1,1:end) = (pr(2,1:end)-pr(1,1:end))/dK;
pr_K(end,1:end) = (pr(end,1:end)-pr(end-1,1:end))/dK;

pr_KK = zeros(size(pr));
pr_KK(2:end-1,1:end) = (pr_K(3:end,1:end)-pr_K(1:end-2,1:end))/(2*dK);
pr_KK(1,1:end) = (pr_K(2,1:end)-pr_K(1,1:end))/dK;
pr_KK(end,1:end) = (pr_K(end,1:end)-pr_K(end-1,1:end))/dK;

% %Question 1
volsq1 = 2.0*(pr_T./(strk.^2.*pr_KK)); %Vol estimate from Dupire formula
% 
% %Question 2 a
ivol = ImpVol(pr,strk,mat,S0,0,MaxCounter,MaxVolLevel); %Implied volatility surface
% 
%Question 2 b
ivol_T = zeros(size(ivol));
ivol_T(1:end,2:end-1) = (ivol(1:end,3:end)-ivol(1:end,1:end-2))/(2*dt);
ivol_T(1:end,1) = (ivol(1:end,2)-ivol(1:end,1))/dt;
ivol_T(1:end,end) = (ivol(1:end,end)-ivol(1:end,end-1))/dt;

ivol_K = zeros(size(ivol));
ivol_K(2:end-1,1:end) = (ivol(3:end,1:end)-ivol(1:end-2,1:end))/(2*dK);
ivol_K(1,1:end) = (ivol(2,1:end)-ivol(1,1:end))/dK;
ivol_K(end,1:end) = (ivol(end,1:end)-ivol(end-1,1:end))/dK;

ivol_KK = zeros(size(ivol));
ivol_KK(2:end-1,1:end) = (ivol_K(3:end,1:end)-ivol_K(1:end-2,1:end))/(2*dK);
ivol_KK(1,1:end) = (ivol_K(2,1:end)-ivol_K(1,1:end))/dK;
ivol_KK(end,1:end) = (ivol_K(end,1:end)-ivol_K(end-1,1:end))/dK;
% 
D1 = zeros(size(ivol));
D2 = zeros(size(ivol));
num = zeros(size(ivol));
den = zeros(size(ivol));
for i = 1:length(mat)
    D1(1:end,i) = (log(S0./strk) + (r+0.5*ivol(1:end,i).^2)*mat(i))./(ivol(1:end,i)*mat(i)^0.5);
    D2(1:end,i) = D1(1:end,i) - ivol(1:end,i)*mat(i)^0.5;
    num(1:end,i) = ivol(1:end,i)/mat(i) + 2.0*ivol_T(1:end,i) + 2*r*strk.*ivol_K(1:end,i);
    den(1:end,i) = strk.^2.*(1./(strk.^2.*ivol(1:end,i)*mat(i)) + 2.0*D1(1:end,i).*ivol_K(1:end,i)./(strk.*ivol(1:end,i)*mat(i)^0.5)... 
    + D1(1:end,i).*D2(1:end,i).*ivol_K(1:end,i).^2./ivol(1:end,i) + ivol_KK(1:end,i));
end
volsq2 = num./den;
% 
%Question 3 a
%[path_Euler1, path_Euler] = EulerPath(volsq1,volsq2,strk,mat,S0,dK, dt,N);