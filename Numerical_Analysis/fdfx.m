function Ans = fdfx(time)
% Find the dfx function
% input:
%       function fx
%       time to derivation
syms x
if length(time)<=1
    Ans=diff(fx(x),time);
else
    Ans=table;
    Ans.time=time';
    Ans.fun=strings(length(time),1);
    for i=1:length(time)
        Ans.fun(i)=diff(fx(x),time(i));
    end
end
end