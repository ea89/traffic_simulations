function [pnot, pBn, pBd, pCn, pCd,pBtot] = pB3(lambda, mun, mud, p, Nt, L, d, Nv)
%PB2 Summary of this function goes here
%   Detailed explanation goes here

qLow = 0;
qHigh = 1;
qNum = 10;

q = linspace(qLow, qHigh, qNum);
q
pnot =   Nt/L * (1./ (1 + (p.*q)./...
           L*((1 - d)/mun + (d)/mud)))+ Nv/L;
       
pBnot = pnot - (Nv/L);

pBtot = zeros(L,qNum);

mu = 1 / (d * 1/mud + (1-d) * 1/mun); 

pBtot(1,:) =  (1./(2*lambda*p))* ...
  (lambda*(-mu + p*(pBnot + sqrt((1./(lambda^2*p^2))* ...
         (lambda.^2*(mu - p*pBnot).^2 - 2*lambda*mu*p*(mu + p.*pBnot).* ...
           (-1 + pnot) + mu.^2*p.^2*(-1 + pnot).^2)))) + mu.*p.*(-1 + pnot));
for i = 2:L 
pBtot(i,:) =  (1./(2*lambda*p))* ...
  (lambda*(-mu + p*(pBtot(i-1) + sqrt((1./(lambda^2*p^2))*...
         (lambda^2*(mu - p*pBtot(i-1))^2 - 2*lambda*mu*p*(mu + p*pBtot(i-1)).*...
           (-1 + pnot) + mu^2*p^2*(-1 + pnot).^2)))) + mu*p*(-1 + pnot));
end


pCtot = (lambda .* pBtot) ./ (repmat((1-pnot).*mu,L,1) + lambda .* pBtot);

pBn = (1-d)* pBtot;
pBd = d * pBtot;
pCn = ((1-d) * 1/mun) * mu * pCtot;
pCd = (d * (1/mud)) * pCtot;

plot(q,(pnot - pBtot(L))./pnot, q, q);


end

