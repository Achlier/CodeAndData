function impvol =  ImpVol(Price,Strike,Maturity,S0,r,MaxIter,MaxVolLevel) %function to find implied vol

volmin = zeros(size(Price));
volmax = MaxVolLevel*ones(size(Price));
vol = 0.5*MaxVolLevel*ones(size(Price));
counter = 0;
while counter < MaxIter
    CBSImp = CallBS(S0,Strike,vol,Maturity,r);
    temp1 = (CBSImp<=Price);
    temp2 = (CBSImp>Price);
    volmin = temp1.* vol + temp2.*volmin;
    volmax =  (CBSImp<Price).* volmax + (CBSImp>=Price).* vol;
    vol = (volmin + volmax)/2.0;
    counter = counter + 1;
end
impvol = vol;