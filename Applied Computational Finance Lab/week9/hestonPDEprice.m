function Un=hestonPDEprice(kappa,theta,delta,rho,T,dt,K,Y,I,J)
    %hestonPDEprice(1.15,0.10,0.2,-0.4,4/52,4/(52*4000),40,1.0,80,40)
    nt=ceil(T/dt);
    xmin = log(1e-2);
	xmax = log(2.0*K);
    ymin = 0;
    ymax = Y*1.2;
    dx = (xmax-xmin)/I; %step length of x
    dx2 = dx*dx;
    dy = Y/J; %step length of y
    dy2 = dy*dy;
    xvalue = xmin:dx:xmax; %grid of x values
    yvalue = ymin:dy:ymax; %grid of y values
    nx = length(xvalue)-1; %number of entries in x axis - 1
    ny = length(yvalue)-1; %number of entries in y axis - 1
    temp = max(exp(xvalue)-K,0); %European call payoff: terminal condition
    uinitial = temp'*ones(1,ny+1); %x in row i, vol in col j
    U = uinitial; % u in dimension of (nx+1)*(ny+1)
    for n=1:nt
        %interior elements in cross derivative
        Upp = U(3:nx+1,3:ny+1); %+1 in x, +1 in y
        Umm = U(1:nx-1,1:ny-1); %-1 in x, -1 in y
        Ump = U(1:nx-1,3:ny+1); %-1 in x, +1 in y
        Upm = U(3:nx+1,1:ny-1); %+1 in x, -1 in y
        Uxy = Upp+Umm-Ump-Upm;
        G0t = (rho*delta*dt/(4*dx*dy))*ones(1,nx+1)'*yvalue;
        G0 = G0t(2:nx,2:ny);        
        U1t = G0.*Uxy;
        U1 = [zeros(1,ny+1);zeros(nx-1,1) U1t zeros(nx-1,1);zeros(1,ny+1)];%pad with zeros at the edge of domain
        %
        % elements in X direction
        C1 = ones(1,nx-1)*(0.5/dx2 + 0.25/dx);
        C1 = [C1';0;0];
        A1 = -ones(1,nx-1)/dx2; 
        A1 = [0;A1';0];
        E1 = ones(1,nx-1)*(0.5/dx2 - 0.25/dx);
        E1 = [0;0;E1'];
        %sparse matrix with A1 on the diagonal, C1 one below & D1 one above
        B = spdiags([C1 A1 E1],[-1 0 1],nx+1,nx+1); 
        for j=2:ny
            A = U(:,j);
            G1 = dt*yvalue(j)*B;
            U2t = G1*A; % the interior elements along the j-th sub-vector.
            U2t(nx+1) = 0; 
            U2t(1) = 0;
            if j==2
                U2 = U2t;
            else
                U2 = [U2 U2t]; %arrange in columns
            end
        end
        U2 = [zeros(nx+1,1) U2 zeros(nx+1,1)]; %pad with zeros in the first and last columns
        %
        % elements in Y direction
        E1 = 0.5*delta^2*yvalue(2:ny)/dy2 - 0.5*kappa*(theta-yvalue(2:ny))/dy;
        E1 = [E1';0;0];
        A1 = -delta^2*yvalue(2:ny)/dy2;
        A1 = [0;A1';0];
        F1 = 0.5*delta^2*yvalue(2:ny)/dy2 + 0.5*kappa*(theta-yvalue(2:ny))/dy;
        F1 = [0;0;F1'];
        D = spdiags([E1 A1 F1],[-1 0 1],ny+1,ny+1);
        for i = 2:nx
            A = U(i,:)';
            U3t = dt*D*A;
            U3t(1) = 0;
            U3t(ny+1) = 0;
            if i==2
                U3 = U3t';
            else
                U3 = [U3; U3t'];
            end
        end
        U3 = [zeros(1,ny+1);U3;zeros(1,ny+1)];
        Uy = U(:,1); % the first column of the previous U
        U = U + U1 + U2 + U3 ;
        U(1,:) = zeros(1, ny+1); %when x = xmin
        U(:,ny+1) = exp(xvalue)'; %when y = ymax
        % elements where y=0
        for i=2:nx
            U(i,1)=(Uy(i)+kappa*theta*dt*U(i,2)/dy)/(1+kappa*theta*dt/dy);
        end
        U(nx+1,2:ny) = exp(xvalue(nx+1))- K;%when x = xmax
        %U(nx+1,2:ny) = (2*dx*exp(xvalue(nx+1))+4*U(nx,2:ny)-U(nx-1,2:ny))/3;
    end
    Un = U(1:I+1,1:J+1);
    
%     p0 = zeros(nx+1,ny+1);    
%     for i=1:nx+1
%         for j=1:ny+1            
%             p0(i,j) = HestonCallQuad(kappa,theta,delta,rho,yvalue(j),0,T,exp(xvalue(i)),K);
%         end
%     end
%     p = p0(1:I+1,1:J+1);
end