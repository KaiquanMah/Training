 function [J, grad] = costFunctionReg(theta, X, y, lambda)
%COSTFUNCTIONREG Compute cost and gradient for logistic regression with regularization
%   J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta


h=sigmoid(X*theta);


% set the first theta value as 0
% keep original theta values from row 2 until the last row
% keep "all cols" in theta
theta1 = [0 ; theta(2:size(theta), :)];

J = ((-y)' * log(h) - (1-y)' * log(1-h))/m + (theta1' * theta1)*lambda/2/m;


%for ALL thetas
grad = ((h-y)' * X)/m + (theta1)*lambda/m;
%update gradient0 for theta0
grad(1, :) = ((h-y)' * X)/m ;

% =============================================================

end
