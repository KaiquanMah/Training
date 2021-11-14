function X_rec = recoverData(Z, U, K)
%RECOVERDATA Recovers an approximation of the original data when using the 
%projected data
%   X_rec = RECOVERDATA(Z, U, K) recovers an approximation the 
%   original data that has been reduced to K dimensions. It returns the
%   approximate reconstruction in X_rec.
%

% You need to return the following variables correctly.
% X_rec         # rows in dimension-reduced Z x # rows in eigenvector matrix U
X_rec = zeros(size(Z, 1), size(U, 1));

% =======================unit test data============================
% X = reshape(sin(1:165), 15, 11);
% Z = reshape(cos(1:121), 11, 11);
% C = Z(1:5, :);
% idx = (1 + mod(1:15, 3))';
% centroids = computeCentroids(X, idx, 3);
% [U, S] = pca(X);
% X_proj = projectData(X, Z, 5);
% X_rec = recoverData(X(:,1:5), Z, 5);
% =================================================================

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the approximation of the data by projecting back
%               onto the original space using the top K eigenvectors in U.
%
%               For the i-th example Z(i,:), the (approximate)
%               recovered data for dimension j is given as follows:
%                    v = Z(i, :)';
%                    recovered_j = v' * U(j, 1:K)';
%
%               Notice that U(j, 1:K) is a row vector.
%               

%Z  11x11
%U  11x11

% from the equations in the 'instructions' above
%v = Z' => v' = Z
X_rec = Z * U(:, 1:K)';

% =============================================================

end
