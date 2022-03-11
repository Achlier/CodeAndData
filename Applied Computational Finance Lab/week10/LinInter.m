function interpvol = LinInter(price,strk,VolEst,ixt,dK) %linear interpolation for the volatility
    strk_cls = find(price <= strk);
    if isempty(strk_cls)% no value of vol estimate exists
        tempx = length(strk);
        temp = VolEst(tempx,ixt);
    elseif strk_cls(1) == 80 %this is the minimum entry in the strike array
        tempx = 1;
        temp = VolEst(tempx,ixt);
    else %linearly interpolate
        strk1 = strk(strk_cls(1));
        strk2 = strk(strk_cls(1)-1);        
        temp = (VolEst(strk_cls(1)-1,ixt)*(price-strk1)+VolEst(strk_cls(1),ixt)*(strk2 - price))/dK;
    end
 interpvol = temp;
