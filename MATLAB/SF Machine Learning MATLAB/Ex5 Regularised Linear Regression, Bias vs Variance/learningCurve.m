function [error_train, error_val] = ...
    learningCurve(X, y, Xval, yval, lambda)
%LEARNINGCURVE Generates the train and cross validation set errors needed 
%to plot a learning curve
%   [error_train, error_val] = ...
%       LEARNINGCURVE(X, y, Xval, yval, lambda) returns the train and
%       cross validation set errors for a learning curve. In particular, 
%       it returns two vectors of the same length - error_train and 
%       error_val. Then, error_train(i) contains the training error for
%       i examples (and similarly for error_val(i)).
%
%   In this function, you will compute the train and test errors for
%   dataset sizes from 1 up to m. In practice, when working with larger
%   datasets, you might want to do this in larger intervals.
%

% Number of training examples
% X 10x3
% m=10 rows
m = size(X, 1); 

% You need to return these values correctly
error_train = zeros(m, 1);
error_val   = zeros(m, 1);

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return training errors in 
%               error_train and the cross validation errors in error_val. 
%               i.e., error_train(i) and 
%               error_val(i) should give you the errors
%               obtained after training on i examples.
%
% Note: You should evaluate the training error on the first i training
%       examples (i.e., X(1:i, :) and y(1:i)).
%
%       For the cross-validation error, you should instead evaluate on
%       the _entire_ cross validation set (Xval and yval).
%
% Note: If you are using your cost function (linearRegCostFunction)
%       to compute the training and cross validation error, you should 
%       call the function with the lambda argument set to 0. 
%       Do note that you will still need to use lambda when running
%       the training to obtain the theta parameters.
%
% Hint: You can loop over the examples with the following:
%
%       for i = 1:m
%           % Compute train/cross validation errors using training examples 
%           % X(1:i, :) and y(1:i), storing the result in 
%           % error_train(i) and error_val(i)
%           ....
%           
%       end
% ---------------------- TRY ----------------------
% X 10x3
% y 10x1
% Xval 10x3
% yval 10x1
% lambda = 0; % for this exercise, BUT CANT ASSIGN HERE, we still need
% lambda for the 'trainLinearReg' fn
% assign lambda=0 in the 'linearRegCostFunction' fn instead, when computing
% the training and cross validation errors


% check the cost as we increase the # of data points in each batch of data 
% being used for training OR cross validation
for i = 1:m,
    % training set to evaluate
    % give me from row 1 down to the ith row of matrix X and col vector y
    X_train_subset = X(1:i, :);
    y_train_subset = y(1:i);
    % ALSO REMEMBER to compute theta => 1 set of theta for every iteration 
    % (since we would use a new subset of the original X matrix and y col vector)    
    [theta] = trainLinearReg(X_train_subset, y_train_subset, lambda);
    
    % cross validation 
    % use the full set of rows in Xval, yval
    
    % compute COST and assign to the error col vectors
    % ASSIGN lambda=0 here    
    [J_train, grad_train] = linearRegCostFunction(X_train_subset, y_train_subset, theta, 0);
    error_train(i) = J_train;
    
    % ASSIGN lambda=0 here    
    [J_validate, grad_validate] = linearRegCostFunction(Xval, yval, theta, 0);
    error_val(i) = J_validate;
    
end

% -------------------------------------------------------------
% =========================================================================
end
