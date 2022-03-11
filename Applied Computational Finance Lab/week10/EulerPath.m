function [pr_Euler1,pr_Euler2]= EulerPath(VolEst1,VolEst2,strk,mat,S0,dK,dt,N)
matlen = length(mat);
BM = normrnd(0.0,1.0,[N,matlen+1])*dt^0.5;
pr_Euler1 = ones(N,matlen+1)*S0;
pr_Euler2 = ones(N,matlen+1)*S0;
for i =1:matlen
    estvol1 = zeros(N);
    estvol2 = zeros(N);
    for j=1:N
        estvol1(j) = LinInter(pr_Euler1(j,i),strk,VolEst1,i,dK);
        estvol2(j) = LinInter(pr_Euler2(j,i),strk,VolEst2,i,dK);
    end
    pr_Euler1(1:end,i+1) = pr_Euler1(1:end,i).*(1+max(estvol1,0.0)^0.5*BM(1:end,i));
    pr_Euler2(1:end,i+1) = pr_Euler2(1:end,i).*(1+max(estvol2,0.0)^0.5*BM(1:end,i));        
end
   
