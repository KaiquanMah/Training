function [U, S] = pca(X)
%PCA Run principal component analysis on the dataset X
%   [U, S, X] = pca(X) computes eigenvectors of the covariance matrix of X
%   Returns the eigenvectors U,
%   the eigenvalues (on diagonal) in S
%

% Useful values
[m, n] = size(X);

% You need to return the following variables correctly.
U = zeros(n);
S = zeros(n);




% ====================== YOUR CODE HERE ======================
% Instructions: You should first compute the covariance matrix. Then, you
%               should use the "svd" function to compute the eigenvectors
%               and eigenvalues of the covariance matrix. 
%
% Note: When computing the covariance matrix, remember to divide by m (the
%       number of examples).
%

% X mxn 15x11
% covMatrix/Sigma is nxn 11x11 => covariance across each feature combo
Sigma = (X'*X)/m;


%https://www.mathworks.com/help/matlab/ref/double.svd.html
% singular value decomposition to retrieve
% U eigenvectors => principal components
% S eigenvalues on the diagonal
[U, S, V] = svd(Sigma);

% =========================================================================

end
