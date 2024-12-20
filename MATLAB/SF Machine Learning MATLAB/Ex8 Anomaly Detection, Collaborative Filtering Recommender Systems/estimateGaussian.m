function [mu sigma2] = estimateGaussian(X)
%ESTIMATEGAUSSIAN This function estimates the parameters of a 
%Gaussian distribution using the data in X
%   [mu sigma2] = estimateGaussian(X), 
%   The input X is the dataset with each n-dimensional data point in one row
%   The output is an n-dimensional vector mu, the mean of the data set
%   and the variances sigma^2, an n x 1 vector
% 

% Useful variables
[m, n] = size(X);

% You should return these values correctly
mu = zeros(n, 1);
sigma2 = zeros(n, 1);


%=======================unit test data==================
% n_u = 3; n_m = 4; n = 5;
% X = reshape(sin(1:n_m*n), n_m, n);
% Theta = reshape(cos(1:n_u*n), n_u, n);
% Y = reshape(sin(1:2:2*n_m*n_u), n_m, n_u);
% R = Y > 0.5;
% pval = [abs(Y(:)) ; 0.001; 1];
% Y = (Y .* double(R));  % set 'Y' values to 0 for movies not reviewed
% yval = [R(:) ; 1; 0];
% params = [X(:); Theta(:)];


% X =
%     0.8415   -0.9589    0.4121    0.4202   -0.9614
%     0.9093   -0.2794   -0.5440    0.9906   -0.7510
%     0.1411    0.6570   -1.0000    0.6503    0.1499
%    -0.7568    0.9894   -0.5366   -0.2879    0.9129
%=========================================================





% ====================== YOUR CODE HERE ======================
% Instructions: Compute the mean of the data and the variances
%               In particular, mu(i) should contain the mean of
%               the data for the i-th feature and sigma2(i)
%               should contain variance of the i-th feature.
%

%mean(A,2) => mean of values along each row
%mean(A,1) => mean of each col
mu = mean(X, 1)';
mu = mean(X)';
% https://www.mathworks.com/help/matlab/ref/std.html
% S = std(A,w,dim) returns the standard deviation along dimension dim. 
% To maintain the default normalization while specifying the 
% dimension of operation, 
% set w = 0 in the second argument.
% sd along rows => S = std(A,0,2)

% https://www.mathworks.com/help/matlab/ref/var.html
% V = var(A,w,dim)
% var(X, 0, 1) would return a row vector
% so to turn into a col vector, we have to transpose the result
% sigma2 = var(X, 0, 1)';
sigma2 = var(X, 1)';

% =============================================================


end



% [mu sigma2] = estimateGaussian(X)
% mu =
%     0.2838
%     0.1020
%    -0.4171
%     0.4433
%    -0.1624
% sigma2 =
%     0.6018
%     0.7888
%     0.3526
%     0.2925
%     0.7462
