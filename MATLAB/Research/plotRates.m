%%Plot the rate to town and rate to city for ranging values of Nt
clear;
clc;

lambda = 0.5;
mun = 0.1;
mud = 0.001;
p = 0.4;
L = 50;
d = 0.1;
N = [5, 30, 50]; 


for j= 1:length(N)
    Nt = 1:N(j);
Nv = N(j) - Nt;
for i=1:N(j)

 [pnot, pBn, pBd, pCn, pCd] = pB2(lambda, mun, mud, p, Nt(i), L, d, Nv(i));

 rateTown(j,i) = sum((pBn + pBd) .* lambda .* (1 - pCn));
 rateVillage(j,i) = sum(Nv(i)/L * p * (1 - pnot));
 
 
end

end

figure(1)
plot(rateTown(1,:), rateVillage(1,:), rateTown(2,:), rateVillage(2,:), rateTown(3, :), rateVillage(3, :))
title('Rate regions for various N values')
xlabel('Rate to Town')
ylabel('Rate to Village')
legend('N = 5', 'N = 30', ' N = 50')
