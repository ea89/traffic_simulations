function [pnot, pBn, pBd, pCn, pCd,pBtot] = pB2(lambda, mun, mud, p, Nt, L, d, Nv)
%PB2 Summary of this function goes here
%   Detailed explanation goes here


numIter = 20;
initGuess = 0.5;
q = ones(1,numIter);

q(1) = initGuess;

for n = 1:(numIter-1)
   q(n+1) =   1 - exp( -1 * lambda * ...
       L * (1 + (Nt/L * (1/ (1 + (p*q(n))/L*((1 - d)/mun + (d)/mud)))) + ...
        Nv/L - Nt/L )/(p *(1 - (Nt/...
              L * (1/ (1 + (p*q(n))/L*((1 - d)/mun + (d)/mud))) + ...
            Nv/L))));
            
    
end
q(20) %right now, converges to either 1 or -inf 
%(-inf sorta makes sense since the approximation log(x) = x is used while deriving this equation
% now find the road density

pnot =   Nt/L * (1/ (1 + (p*q(numIter) )/...
           L*((1 - d)/mun + (d)/mud)))+ Nv/L;
       
pBnot = pnot - (Nv/L);

pBtot = zeros(1,L);

mu = 1 / (d * 1/mud + (1-d) * 1/mun); 

pBtot(1) =  (1/(2*lambda*p))* ...
  (lambda*(-mu + p*(pBnot + sqrt((1/(lambda^2*p^2))* ...
         (lambda^2*(mu - p*pBnot)^2 - 2*lambda*mu*p*(mu + p*pBnot)* ...
           (-1 + pnot) + mu^2*p^2*(-1 + pnot)^2)))) + mu*p*(-1 + pnot));
for i = 2:L 
pBtot(i) =  (1/(2*lambda*p))* ...
  (lambda*(-mu + p*(pBtot(i-1) + sqrt((1/(lambda^2*p^2))*...
         (lambda^2*(mu - p*pBtot(i-1))^2 - 2*lambda*mu*p*(mu + p*pBtot(i-1))*...
           (-1 + pnot) + mu^2*p^2*(-1 + pnot)^2)))) + mu*p*(-1 + pnot));
end

pCtot = (lambda .* pBtot) ./ ((1-pnot)*mu + lambda .* pBtot);

pBn = (1-d)* pBtot;
pBd = d * pBtot;
pCn = ((1-d) * 1/mun) * mu * pCtot;
pCd = (d * (1/mud)) * pCtot;

end

