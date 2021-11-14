function [lambda_vec, error_train, error_val] = ...
    validationCurve(X, y, Xval, yval)
%VALIDATIONCURVE Generate the train and validation errors needed to
%plot a validation curve that we can use to select lambda
%   [lambda_vec, error_train, error_val] = ...
%       VALIDATIONCURVE(X, y, Xval, yval) returns the train
%       and validation errors (in error_train, error_val)
%       for different values of lambda. You are given the training set (X,
%       y) and validation set (Xval, yval).
%

% Selected values of lambda (you should not change this)
lambda_vec = [0 0.001 0.003 0.01 0.03 0.1 0.3 1 3 10]';
% lambda_vec    10x1

% You need to return these variables correctly.
error_train = zeros(length(lambda_vec), 1);
error_val = zeros(length(lambda_vec), 1);
% error_train   10x1
% error_val     10x1

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return training errors in 
%               error_train and the validation errors in error_val. The 
%               vector lambda_vec contains the different lambda parameters 
%               to use for each calculation of the errors, i.e, 
%               error_train(i), and error_val(i) should give 
%               you the errors obtained after training with 
%               lambda = lambda_vec(i)
%
% Note: You can loop over lambda_vec with the following:
%
%       for i = 1:length(lambda_vec)
%           lambda = lambda_vec(i);
%           % Compute train / val errors when training linear 
%           % regression with regularization parameter lambda
%           % You should store the result in error_train(i)
%           % and error_val(i)
%           ....
%           
%       end
%
%
for i = 1:length(lambda_vec),
    
    % get the lambda value from the lambda col vector
    lambda = lambda_vec(i);
    
    % perform linear regression (not the polynomial regression) on our
    % training set using the lambda value
    % to generate a set of theta param values
    [theta] = trainLinearReg(X, y, lambda);
    
    % then compute cost/errors
    % not sure why we are assigning lambda=0 here for these
    % linearRegCostFunctions again
    % like in the 'learningCurve.m' exercise
    % [J_train, grad_train] = linearRegCostFunction(X, y, theta, lambda);
    % [J_val, grad_val] = linearRegCostFunction(Xval, yval, theta, lambda);
    [J_train, grad_train] = linearRegCostFunction(X, y, theta, 0);
    [J_val, grad_val] = linearRegCostFunction(Xval, yval, theta, 0);
    
    % append cost/errors to the error_train/val col vector by replacing the
    % instantiated 'zero' entries
    error_train(i) = J_train;
    error_val(i) = J_val;
    
end
% =========================================================================

end






























% Iteration     1 | Cost: 7.114848e-02
% Iteration     2 | Cost: 7.260659e-04
% Iteration     3 | Cost: 6.879376e-09
% Iteration     4 | Cost: 1.645098e-09
% Iteration     5 | Cost: 1.489275e-10
% Iteration     6 | Cost: 3.192421e-15
% Iteration     7 | Cost: 3.207886e-16
% Iteration     8 | Cost: 1.241551e-16
% Iteration     9 | Cost: 2.740545e-17
% Iteration    10 | Cost: 9.383028e-20
% Iteration    11 | Cost: 3.548152e-34
% Iteration    12 | Cost: 1.999940e-35
% Iteration    13 | Cost: 1.151253e-37
% Iteration    14 | Cost: 1.399614e-61
% Iteration    15 | Cost: 1.415553e-62
% Iteration    16 | Cost: 1.301172e-63
% Iteration    17 | Cost: 2.270637e-64
% Iteration    18 | Cost: 0.000000e+00

% Iteration     1 | Cost: 1.758922e-01
% Iteration     2 | Cost: 1.695685e-01
% Iteration     3 | Cost: 1.665886e-01
% Iteration     4 | Cost: 1.655219e-01
% Iteration     5 | Cost: 1.655125e-01
% Iteration     6 | Cost: 1.655087e-01
% Iteration     8 | Cost: 1.655087e-01
% Iteration     1 | Cost: 1.726952e-01
% Iteration     2 | Cost: 1.610097e-01
% Iteration     3 | Cost: 1.608881e-01
% Iteration     5 | Cost: 1.608881e-01
% Iteration     6 | Cost: 1.608881e-01
% Iteration     7 | Cost: 1.608881e-01
% Iteration     8 | Cost: 1.608881e-01
% Iteration     9 | Cost: 1.608881e-01
% Iteration    11 | Cost: 1.608881e-01
% Iteration    13 | Cost: 1.608881e-01

% Iteration     1 | Cost: 2.464694e-01
% Iteration     2 | Cost: 2.462441e-01
% Iteration     3 | Cost: 2.461110e-01
% Iteration     4 | Cost: 2.461099e-01
% Iteration     5 | Cost: 2.461099e-01
% Iteration     6 | Cost: 2.461099e-01
% Iteration     7 | Cost: 2.461099e-01
% Iteration     8 | Cost: 2.461099e-01
% Iteration     9 | Cost: 2.461099e-01
% Iteration    10 | Cost: 2.461099e-01
% Iteration    12 | Cost: 2.461099e-01

% Iteration     1 | Cost: 2.017319e-01
% Iteration     2 | Cost: 2.012966e-01
% Iteration     3 | Cost: 2.012940e-01
% Iteration     4 | Cost: 2.012939e-01
% Iteration     5 | Cost: 2.012938e-01
% Iteration     6 | Cost: 2.012938e-01
% Iteration     7 | Cost: 2.012938e-01
% Iteration     8 | Cost: 2.012938e-01
% Iteration     9 | Cost: 2.012938e-01
% Iteration    10 | Cost: 2.012938e-01
% Iteration    11 | Cost: 2.012938e-01
% Iteration    13 | Cost: 2.012938e-01
% 
% Iteration     1 | Cost: 1.769857e-01
% Iteration     2 | Cost: 1.757778e-01
% Iteration     3 | Cost: 1.752241e-01
% Iteration     4 | Cost: 1.752179e-01
% Iteration     5 | Cost: 1.752179e-01
% Iteration     6 | Cost: 1.752179e-01
% Iteration     7 | Cost: 1.752179e-01
% Iteration     9 | Cost: 1.752179e-01

% Iteration     1 | Cost: 1.554306e-01
% Iteration     2 | Cost: 1.542656e-01
% Iteration     3 | Cost: 1.538759e-01
% Iteration     4 | Cost: 1.538717e-01
% Iteration     5 | Cost: 1.538717e-01
% Iteration     6 | Cost: 1.538717e-01
% Iteration     7 | Cost: 1.538717e-01
% Iteration     8 | Cost: 1.538717e-01

% Iteration     1 | Cost: 1.370406e-01
% Iteration     2 | Cost: 1.362668e-01
% Iteration     3 | Cost: 1.360040e-01
% Iteration     4 | Cost: 1.360020e-01
% Iteration     5 | Cost: 1.360020e-01
% Iteration     6 | Cost: 1.360020e-01
% Iteration     7 | Cost: 1.360020e-01
% Iteration     8 | Cost: 1.360020e-01
% Iteration    10 | Cost: 1.360020e-01

% Iteration     1 | Cost: 1.256075e-01
% Iteration     2 | Cost: 1.253832e-01
% Iteration     3 | Cost: 1.253144e-01
% Iteration     4 | Cost: 1.253141e-01
% Iteration     5 | Cost: 1.253141e-01
% Iteration     6 | Cost: 1.253141e-01
% Iteration     7 | Cost: 1.253141e-01
% Iteration     8 | Cost: 1.253141e-01
% Iteration     9 | Cost: 1.253141e-01
% Iteration    10 | Cost: 1.253141e-01
% Iteration    11 | Cost: 1.253141e-01
% Iteration    12 | Cost: 1.253141e-01
% Iteration    13 | Cost: 1.253141e-01
% Iteration    14 | Cost: 1.253141e-01

% Iteration     1 | Cost: 1.157593e-01
% Iteration     2 | Cost: 1.155587e-01
% Iteration     3 | Cost: 1.155521e-01
% Iteration     4 | Cost: 1.155236e-01
% Iteration     5 | Cost: 1.155152e-01
% Iteration     6 | Cost: 1.155151e-01
% Iteration     7 | Cost: 1.155151e-01
% Iteration     8 | Cost: 1.155151e-01
% Iteration     9 | Cost: 1.155151e-01
% Iteration    10 | Cost: 1.155151e-01
% Iteration    11 | Cost: 1.155151e-01
% Iteration    13 | Cost: 1.155151e-01

% Iteration     1 | Cost: 1.156362e-01
% Iteration     2 | Cost: 1.152010e-01
% Iteration     3 | Cost: 1.151656e-01
% Iteration     4 | Cost: 1.151643e-01
% Iteration     5 | Cost: 1.151643e-01
% Iteration     6 | Cost: 1.151643e-01

% Iteration     1 | Cost: 1.156364e-01
% Iteration     2 | Cost: 1.152014e-01
% Iteration     3 | Cost: 1.151661e-01
% Iteration     4 | Cost: 1.151648e-01
% Iteration     5 | Cost: 1.151647e-01
% Iteration     6 | Cost: 1.151647e-01
% Iteration     7 | Cost: 1.151647e-01

% Iteration     1 | Cost: 1.156366e-01
% Iteration     2 | Cost: 1.152022e-01
% Iteration     3 | Cost: 1.151669e-01
% Iteration     4 | Cost: 1.151656e-01
% Iteration     5 | Cost: 1.151656e-01
% Iteration     6 | Cost: 1.151656e-01
% Iteration     7 | Cost: 1.151656e-01
% Iteration     8 | Cost: 1.151656e-01
% Iteration     9 | Cost: 1.151656e-01
% Iteration    10 | Cost: 1.151656e-01

% Iteration     1 | Cost: 1.156375e-01
% Iteration     2 | Cost: 1.152050e-01
% Iteration     3 | Cost: 1.151699e-01
% Iteration     4 | Cost: 1.151686e-01
% Iteration     5 | Cost: 1.151685e-01
% Iteration     6 | Cost: 1.151685e-01
% Iteration     8 | Cost: 1.151685e-01
% Iteration     1 | Cost: 1.156399e-01
% Iteration     2 | Cost: 1.152129e-01
% Iteration     3 | Cost: 1.151783e-01
% Iteration     4 | Cost: 1.151770e-01
% Iteration     5 | Cost: 1.151769e-01
% Iteration     6 | Cost: 1.151769e-01
% Iteration     7 | Cost: 1.151769e-01
% Iteration     8 | Cost: 1.151769e-01
% Iteration    10 | Cost: 1.151769e-01

% Iteration     1 | Cost: 1.156485e-01
% Iteration     2 | Cost: 1.152401e-01
% Iteration     3 | Cost: 1.152071e-01
% Iteration     4 | Cost: 1.152058e-01
% Iteration     5 | Cost: 1.152058e-01
% Iteration     6 | Cost: 1.152058e-01

% Iteration     1 | Cost: 1.156732e-01
% Iteration     2 | Cost: 1.153135e-01
% Iteration     3 | Cost: 1.152854e-01
% Iteration     4 | Cost: 1.152840e-01
% Iteration     5 | Cost: 1.152840e-01
% Iteration     6 | Cost: 1.152840e-01
% Iteration     7 | Cost: 1.152840e-01
% Iteration     1 | Cost: 1.157593e-01
% Iteration     2 | Cost: 1.155587e-01
% Iteration     3 | Cost: 1.155521e-01
% Iteration     4 | Cost: 1.155236e-01
% Iteration     5 | Cost: 1.155152e-01
% Iteration     6 | Cost: 1.155151e-01
% Iteration     7 | Cost: 1.155151e-01
% Iteration     8 | Cost: 1.155151e-01
% Iteration     9 | Cost: 1.155151e-01
% Iteration    10 | Cost: 1.155151e-01
% Iteration    11 | Cost: 1.155151e-01
% Iteration    13 | Cost: 1.155151e-01
% Iteration     1 | Cost: 1.160054e-01
% Iteration     2 | Cost: 1.159478e-01
% Iteration     3 | Cost: 1.159476e-01
% Iteration     4 | Cost: 1.159475e-01
% Iteration     5 | Cost: 1.159475e-01
% Iteration     6 | Cost: 1.159475e-01
% Iteration     8 | Cost: 1.159475e-01
% Iteration    10 | Cost: 1.159475e-01

% Iteration     1 | Cost: 1.168667e-01
% Iteration     2 | Cost: 1.168361e-01
% Iteration     3 | Cost: 1.165444e-01
% Iteration     4 | Cost: 1.165428e-01
% Iteration     5 | Cost: 1.165421e-01
% Iteration     6 | Cost: 1.165421e-01
% Iteration     7 | Cost: 1.165421e-01
% Iteration     8 | Cost: 1.165421e-01
% Iteration     9 | Cost: 1.165421e-01
% Iteration    10 | Cost: 1.165421e-01




