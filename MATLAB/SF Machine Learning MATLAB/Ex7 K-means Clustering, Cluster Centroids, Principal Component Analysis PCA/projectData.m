function Z = projectData(X, U, K)
%PROJECTDATA Computes the reduced data representation when projecting only 
%on to the top k eigenvectors
%   Z = projectData(X, U, K) computes the projection of 
%   the normalized inputs X into the reduced dimensional space spanned by
%   the first K columns of U. It returns the projected examples in Z.
%

% You need to return the following variables correctly.
Z = zeros(size(X, 1), K);



% =======================unit test data============================
% U 11x11
% S 11x11

% U =
%    -0.3792   -0.1534   -0.6603   -0.2212    0.0702    0.2122    0.3725   -0.1409   -0.1815   -0.3251   -0.0233
%     0.3703   -0.1650   -0.2031    0.4572    0.5570   -0.0490   -0.0848   -0.3566   -0.2114   -0.0108    0.3059
%    -0.1834    0.4042   -0.1238    0.3539   -0.0123    0.3442    0.3113   -0.0981    0.0119    0.6549   -0.0902
%    -0.0916   -0.4491    0.0471    0.1552    0.0116    0.1111    0.0305   -0.3769    0.7361   -0.0015   -0.2576
%     0.3226    0.2781   -0.5130    0.0952   -0.4832   -0.1011   -0.4100   -0.2590    0.0429   -0.0645   -0.2480
%    -0.3986    0.0265    0.1640    0.5907    0.0431   -0.0730   -0.1466    0.1070   -0.2657   -0.3525   -0.4792
%     0.2830   -0.3184   -0.1449   -0.2108    0.2417   -0.2041    0.0974    0.1912   -0.2118    0.3706   -0.6518
%    -0.0314    0.4573   -0.1965   -0.1449    0.5897    0.1044   -0.2689    0.3014    0.4130   -0.1459   -0.1294
%    -0.2353   -0.3763   -0.1046   -0.0513   -0.0249    0.4778   -0.6467    0.1635   -0.1594    0.2743    0.1218
%     0.3889    0.1146    0.3158   -0.1556    0.0237    0.6876    0.0797   -0.2177   -0.1822   -0.2829   -0.2672
%    -0.3556    0.2023    0.2118   -0.3775    0.2046   -0.2293   -0.2454   -0.6491   -0.1843    0.1514   -0.1116
% 
% 
% S =
%     3.2794         0         0         0         0         0         0         0         0         0         0
%          0    2.2552         0         0         0         0         0         0         0         0         0
%          0         0    0.0000         0         0         0         0         0         0         0         0
%          0         0         0    0.0000         0         0         0         0         0         0         0
%          0         0         0         0    0.0000         0         0         0         0         0         0
%          0         0         0         0         0    0.0000         0         0         0         0         0
%          0         0         0         0         0         0    0.0000         0         0         0         0
%          0         0         0         0         0         0         0    0.0000         0         0         0
%          0         0         0         0         0         0         0         0    0.0000         0         0
%          0         0         0         0         0         0         0         0         0    0.0000         0
%          0         0         0         0         0         0         0         0         0         0    0.0000
% =================================================================






% ====================== YOUR CODE HERE ======================
% Instructions: Compute the projection of the data using only the top K 
%               eigenvectors in U (first K columns). 
%               For the i-th example X(i,:), the projection on to the k-th 
%               eigenvector is given as follows:
%                    x = X(i, :)';
%                    projection_k = x' * U(:, k);
%

%X 15x11
%x, i.e. X' 11x15 => now each row corresponds to each feature; each col corresponds
%to each observation

U_reduce = U(:, 1:K);

for i = 1:size(X, 1),
    
    x = X(i, :)';
    %method 1
    % (U_reduce' * x)  (11xK)' i.e. Kx11 x 1x15 => Kx15
    % (U_reduce' * x)' => 15x11 => 15 rows/observations with K updated col/feature values
    % Z(i, :) = (U_reduce' * x)';
    
    %method 2 following equation in the 'instructions' section above
    % or x 1x15, x' 15x1 x U_reduce 11xK => 15xK
    % so now we have scaled down to just K # features for each observation
    Z(i, :) = (x' * U_reduce);
  
end
% =============================================================

end








% X_proj = projectData(X, Z, 5);
% X_proj =
%     0.5943    0.4674   -0.5902   -0.4726    0.5860
%     0.7408   -0.2363   -0.7429    0.2297    0.7449
%     0.2062   -0.7227   -0.2126    0.7208    0.2190
%    -0.5180   -0.5447    0.5131    0.5492   -0.5083
%    -0.7659    0.1341    0.7671   -0.1273   -0.7682
%    -0.3097    0.6896    0.3158   -0.6868   -0.3219
%     0.4313    0.6111   -0.4259   -0.6149    0.4204
%     0.7757   -0.0293   -0.7760    0.0224    0.7762
%     0.4070   -0.6427   -0.4127    0.6390    0.4183
%    -0.3359   -0.6652    0.3300    0.6682   -0.3241
%    -0.7700   -0.0762    0.7693    0.0830   -0.7686
%    -0.4961    0.5829    0.5013   -0.5785   -0.5064
%     0.2339    0.7061   -0.2276   -0.7081    0.2214
%     0.7488    0.1801   -0.7473   -0.1867    0.7456
%     0.5753   -0.5115   -0.5799    0.5064    0.5843



% because only the 1st 2 eigenvalues in 'S' are significant
% let us try using only 2 PCA components
% instead of 5, which the original assignment used above
% X_proj = projectData(X, Z, 2);
% X_proj =
%     0.5943    0.4674
%     0.7408   -0.2363
%     0.2062   -0.7227
%    -0.5180   -0.5447
%    -0.7659    0.1341
%    -0.3097    0.6896
%     0.4313    0.6111
%     0.7757   -0.0293
%     0.4070   -0.6427
%    -0.3359   -0.6652
%    -0.7700   -0.0762
%    -0.4961    0.5829
%     0.2339    0.7061
%     0.7488    0.1801
%     0.5753   -0.5115
