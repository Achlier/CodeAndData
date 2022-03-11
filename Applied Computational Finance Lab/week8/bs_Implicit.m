% S0= 17; K = 15; g = 0; T = 0.3041; r = 0.03; sigma = 0.25; M=100; N= 10000; theta= 0.5; 
% mex thomas.c
% bs_Implicit(17,0.25,0.3041,15,0.03,0,100,10000,0.5,1)
function V_Final = bs_Implicit(S0, sigma, T, K, r, g, M, N, theta, callPut)
	% numero de puntos considerando los extremos.
	nX = M + 2;
	nt = N + 2;
	
    X_min = log(10e-6);
	X_max = log(2*K);
    
	
	% space step
	AX = (X_max - X_min) / (M + 1);
	At = T / (N + 1);

	% Vector initialisation
	X = linspace(X_min,X_max,nX);
	t = linspace(0,T,nt); 
	
	aux = (T - t);
	aux1 = exp(-r .* aux);
	aux2 = exp(-g .* aux);

	if ~callPut % call
		V = max(exp(X)-K,0);
		V_0_t = zeros(1, nt); %boundary condition at xmin
		V_Xmax_t = exp(X_max) .* aux2 - K .* aux1; %boundary condition at xmax
	else % put
		V = max(K-exp(X),0);
		V_0_t = K .* aux1; 
		V_Xmax_t = zeros(1, nt);
    end


	% different constants used
	AX2 = AX.^2;
	sigma2 = sigma^2;

	cte1 = At.*r.*theta; 
	cte2 = At.*r.*(1-theta); 
	
	cte3 = At.*sigma2.*theta./AX2; 
	cte4 = At.*sigma2.*(1-theta)./AX2; 
	
	cte5 = cte3./2.0;
	cte6 = cte4./2.0; 
	
	cte7 = At.*theta.*(r-g-0.5*sigma2)./AX; 
	cte8 = At.*(1-theta).*(r-g-0.5*sigma2)./AX;

	%
	% diagonals in the tridiagonal system for finite differences
	%
	va = (1 + cte1 + cte3 + cte7)*ones(1,nX);
	vb = -cte5*ones(1,nX-1);
	vc = (-cte5 - cte7)*ones(1,nX-1);

	% 
	va(1) = 1; vc(1) = 0;	
	vb(nX-1) = 0; va(nX) = 1;

	% 
	vba = (1 - cte2 - cte4 - cte8)*ones(1,nX);	
	vbb = cte6*ones(1,nX-1);
	vbc = (cte6 + cte8)*ones(1,nX-1);

	b = zeros(1,nX);

	for j=nt-1:-1:1
		
		% 
		b(2:nX-1) = vba(2:nX-1).*V(2:nX-1) + vbb(1:nX-2).*V(1:nX-2) + vbc(2:nX-1).*V(3:nX);
		
		b(1) = V_0_t(j);
		b(nX) = V_Xmax_t(j);

		% 
		V = thomas(vb,va,vc,b);

	end

	V_Final = interp1(X, V, log(S0));
end