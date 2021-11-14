function [J, grad] = linearRegCostFunction(X, y, theta, lambda)
%LINEARREGCOSTFUNCTION Compute cost and gradient for regularized linear 
%regression with multiple variables
%   [J, grad] = LINEARREGCOSTFUNCTION(X, y, theta, lambda) computes the 
%   cost of using theta as the parameter for linear regression to fit the 
%   data points in X and y. Returns the cost in J and the gradient in grad

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost and gradient of regularized linear 
%               regression for a particular choice of theta.
%
%               You should set J to the cost and grad to the gradient.
%


% ===========visualise dimensions===========
% 1 col of 'ones'
% 1:2 => 1 2
% 1:1.5:15 => from 1 to 15 in increments of 1.5 => 1.0000    2.5000    4.0000    5.5000    7.0000    8.5000   10.0000   11.5000   13.0000   14.5000
% sin/cos(1:1.5:15)' => sin/cos on each # generated, then turn into col vector
% 2nd col for sine
% 3rd col for cosine
% X is 10x3
% y is 10x1
% X = [ones(10,1) sin(1:1.5:15)' cos(1:1.5:15)'];
% y = sin(1:3:30)';

% Xval = [ones(10,1) sin(0:1.5:14)' cos(0:1.5:14)'];
% yval = sin(1:10)';

% theta is 3x1
% theta = [0.1 0.2 0.3]';
% theta =
%     0.1000
%     0.2000
%     0.3000
% lambda = 0.5;
% ============================================




% =============compute expected 'y'==========
% in linear regression, we multiply 'X' with the 'theta' parameter values
% to get 'h'
% as 'y' is 10x1, we also need 'h' to be 10x1 => X 10x3 x theta 3x1 => 10x1
h = X*theta;

% ====compute the full regularised cost function 'J'==========
JUnreg = sum((h-y).^2)/2/m;
% JReg => 1x2 x 2x1 => 1x1
JReg = (theta(2:end)' * theta(2:end))*lambda/2/m;
J = JUnreg + JReg;



% ====compute the regularised gradient 'grad'==========
% (h-y) 10x1
% X 10x3
% gradUnreg => X' 3x10 x (h-y) 10x1 => 3x1
gradUnreg = X'*(h-y) /m;
% for gradReg, we need same # dimensions as gradUnreg => 3x1
% BUT we SHOULD NOT REGULARISE theta(1) which corresponds to the '1' bias term
% so to maintain theta's dimension, we replace theta(1)'s value 
% by adding a row of '0'
gradReg = ([0; theta(2:end)]) * lambda/m;
grad = gradUnreg + gradReg;

% grad =
%     0.0707
%     0.1009
%     0.1192


% =========================================================================
% not sure why the original base code contained this 'unroll grad' line
% when 'grad' is still a 3x1 col vector
grad = grad(:);

% grad =
%     0.0707
%     0.1009
%     0.1192


end
