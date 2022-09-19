function [matrix] = portfolio_optimization_c(mean,beta,sigma,sigma_m,rf)
% mean|excess return|beta|excess return over beta|sigma_i|sigma_ei|(ri-rf)beta/sigma_ei^2|sum(8)|betai/sigma_ei^2|betai^2/sigma_ei^2|sum(11)|C*|Z|X
n = length(mean);
matrix = zeros(n,15);
matrix(:,1) = 1:1:n;
matrix(:,2) = mean;
matrix(:,3) = mean-rf;
matrix(:,4) = beta;
matrix(:,5) = matrix(:,3)./matrix(:,4);
matrix(:,6) = sigma;
matrix(:,7) = sqrt(matrix(:,6).^2-sigma_m^2*matrix(:,4).^2);
matrix(:,8) = matrix(:,3).*matrix(:,4)./matrix(:,7).^2;
matrix(:,10) = matrix(:,4)./matrix(:,7).^2;
matrix(:,11) = matrix(:,4).^2./matrix(:,7).^2;
matrix = sortrows(matrix,5,'descend');
for i = 1:1:n
    matrix(i,9) = sum(matrix(1:i,8));
    matrix(i,12) = sum(matrix(1:i,11));
end
matrix(:,13) = sigma_m^2*matrix(:,9)./(1+sigma_m^2*matrix(:,12));
C = matrix(1,13);
for i = 1:1:n
    if matrix(i,13) > matrix(i,5)
        break;
    else
        C = matrix(i,13);
    end
end
matrix(:,14) = matrix(:,10).*(matrix(:,5)-C);
matrix(:,15) = matrix(:,14)/sum(matrix(:,14));
name = {'index','mean','excess_return','beta','excess_return_over_beta','sigma','sigma_e','excess_return_time_beta_by_sigma_e2','sum_of_8','beta_by_sigma_e2','beta2_by_sigma_e2','sum_of_11','C','Z','X'};
matrix = array2table(matrix, 'VariableNames', name);
end

