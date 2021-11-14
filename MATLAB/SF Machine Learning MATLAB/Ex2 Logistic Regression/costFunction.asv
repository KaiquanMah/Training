%data = load('ex2data1.txt');
%X = data(:, [1, 2]); 
%y = data(:, 3);

%size(X)
%ans =
%   100     2
   
%size(y)
%ans =
%   100     1

%  Setup the data matrix appropriately
%[m, n] = size(X);

% Add intercept term to X
%X = [ones(m, 1) X];

%m is still 100
%n was 2 before adding col of 1s on the LHS
% Initialize the fitting parameters
%initial_theta = zeros(n + 1, 1);
%theta =
%     0
%     0
%     0






function [J, grad] = costFunction(theta, X, y)
%COSTFUNCTION Compute cost and gradient for logistic regression
%   J = COSTFUNCTION(theta, X, y) computes the cost of using theta as the
%   parameter for logistic regression and the gradient of the cost
%   w.r.t. to the parameters.

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
%
% Note: grad should have the same dimensions as theta
%


%X 100x3
%theta 3x1
%y 100x1
%h OR X * theta 100x1
h = sigmoid(X * theta);


%SUM method
%remember to transpose the 1st term of each matrix/vector multiplication
%which ex2.pdf did not mention
%J = (1/m) * sum((-y)' * log(h) - (1-y)' * log(1-h));
%grad = (1/m) * sum((h-y)' * X);



%no sum
%(-y)' * log(h)     1x100 * 100x1 => 1x1
%(1-y)' * log(1-h)  1x100 * 100x1 => 1x1
%single value cost (J)
J = ((-y)' * log(h) - (1-y)' * log(1-h))/m;


%X' 3x100
%h-y 100x1
%(X' * (h-y)) 3x1 => 1 gradient per theta parameter value
grad = (X' * (h-y))/m;

% =============================================================

end
