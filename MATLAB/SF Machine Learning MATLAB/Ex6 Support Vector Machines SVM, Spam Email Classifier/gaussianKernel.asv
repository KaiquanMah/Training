function sim = gaussianKernel(x1, x2, sigma)
%RBFKERNEL returns a radial basis function kernel between x1 and x2
%   sim = gaussianKernel(x1, x2) returns a gaussian kernel between x1 and x2
%   and returns the value in sim

% Ensure that x1 and x2 are column vectors
x1 = x1(:); x2 = x2(:);

% You need to return the following variables correctly.
sim = 0;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the similarity between x1
%               and x2 computed using a Gaussian kernel with bandwidth
%               sigma
%
%

%===========unit test dataset========================
% x1, x2 10x1
% x1 = sin(1:10)';
% x2 = cos(1:10)';
% wi 10x1
% wi = 1 + abs(round(x1 * 1863));
% wi is now 20x1
% wi = [wi ; wi];
% ec = 'the quick brown fox jumped over the lazy dog';
% ========================================================


% sim = exp((-sum((x1-x2).^2))/2/sigma^2);
norm_squared = sum((x2 - x1).^2);
sim = exp(-norm_squared/(2*sigma^2));
    
% =============================================================
end
