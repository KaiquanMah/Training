function [all_theta] = oneVsAll(X, y, num_labels, lambda)
%ONEVSALL trains multiple logistic regression classifiers and returns all
%the classifiers in a matrix all_theta, where the i-th row of all_theta 
%corresponds to the classifier for label i
%   [all_theta] = ONEVSALL(X, y, num_labels, lambda) 
%   trains num_labels
%   logistic regression classifiers and 
%   returns each of these classifiers
%   in a matrix all_theta, where the i-th row of all_theta corresponds 
%   to the classifier for label i

% Some useful variables
%m = # rows/observations
m = size(X, 1);
%n = # cols/X features
n = size(X, 2);

% You need to return the following variables correctly 
all_theta = zeros(num_labels, n + 1);

% Add ones to the X data matrix
X = [ones(m, 1) X];

% ====================== YOUR CODE HERE ======================
% Instructions: You should complete the following code to train num_labels
%               logistic regression classifiers with regularization
%               parameter lambda. 
%
% Hint: theta(:) will return a column vector.
%
% Hint: You can use y == c to obtain a vector of 1's and 0's that tell you
%       whether the ground truth is true/false for this class.
%
% Note: For this assignment, we recommend using fmincg to optimize the cost
%       function. It is okay to use a for-loop (for c = 1:num_labels) to
%       loop over the different classes.
%
%       fmincg works similarly to fminunc, but is more efficient when we
%       are dealing with large number of parameters.
%
% Example Code for fmincg:
%
%     % Set Initial theta
%     initial_theta = zeros(n + 1, 1);
    initial_theta = zeros(n + 1, 1);
%     
%     % Set options for fminunc
%     options = optimset('GradObj', 'on', 'MaxIter', 50);
     options = optimset('GradObj', 'on', 'MaxIter', 50);
% 
%     % Run fmincg to obtain the optimal theta
%     % This function will return theta and the cost 
%     [theta] = ...
%         fmincg (@(t)(lrCostFunction(t, X, (y == c), lambda)), ...
%                 initial_theta, options);
%

%t is a set of theta values in the 'all_theta' matrix
%1 set per iteration
%extracted out as a set of 'theta'
for c=1:num_labels,
     [theta] = fmincg(@(t)(lrCostFunction(t, X, (y == c), lambda)), initial_theta, options);
     
     
     %fmincg gives us a col vector
     %so we need to transpose theta to obtain a row vector
     %then stored in all_theta
     all_theta(c,:) = theta';
end










% =========================================================================


end

















% Execution results
% Iteration     1 | Cost: 4.749342e-01
% Iteration     2 | Cost: 3.951798e-01
% Iteration     3 | Cost: 3.410009e-01
% Iteration     4 | Cost: 3.408546e-01
% Iteration     5 | Cost: 3.402400e-01
% Iteration     6 | Cost: 3.397496e-01
% Iteration     7 | Cost: 3.395172e-01
% Iteration     8 | Cost: 3.391977e-01
% Iteration     9 | Cost: 3.391811e-01
% Iteration    10 | Cost: 3.391637e-01
% Iteration    11 | Cost: 3.391498e-01
% Iteration    12 | Cost: 3.391382e-01
% Iteration    13 | Cost: 3.391350e-01
% Iteration    14 | Cost: 3.391343e-01
% Iteration    15 | Cost: 3.391340e-01
% Iteration    16 | Cost: 3.391340e-01
% Iteration    17 | Cost: 3.391340e-01
% Iteration    18 | Cost: 3.391340e-01
% Iteration    19 | Cost: 3.391340e-01
% Iteration    20 | Cost: 3.391340e-01
% Iteration    21 | Cost: 3.391340e-01
% Iteration    22 | Cost: 3.391340e-01
% Iteration    23 | Cost: 3.391340e-01
% Iteration    24 | Cost: 3.391340e-01
% Iteration    25 | Cost: 3.391340e-01
% 
% Iteration     1 | Cost: 1.934937e-01
% Iteration     2 | Cost: 1.557194e-01
% Iteration     3 | Cost: 1.037875e-01
% Iteration     4 | Cost: 7.802805e-02
% Iteration     5 | Cost: 6.676458e-02
% Iteration     6 | Cost: 6.647775e-02
% Iteration     7 | Cost: 6.637033e-02
% Iteration     8 | Cost: 6.631655e-02
% Iteration     9 | Cost: 6.631456e-02
% Iteration    10 | Cost: 6.631440e-02
% Iteration    11 | Cost: 6.631439e-02
% Iteration    12 | Cost: 6.631438e-02
% Iteration    13 | Cost: 6.631438e-02
% Iteration    14 | Cost: 6.631438e-02
% Iteration    15 | Cost: 6.631438e-02
% Iteration    16 | Cost: 6.631438e-02
% Iteration    17 | Cost: 6.631438e-02
% Iteration    18 | Cost: 6.631438e-02
% Iteration    19 | Cost: 6.631438e-02
% 
% Iteration     1 | Cost: 3.899941e-01
% Iteration     2 | Cost: 3.371335e-01
% Iteration     3 | Cost: 2.080753e-01
% Iteration     4 | Cost: 1.142276e-01
% Iteration     5 | Cost: 1.139130e-01
% Iteration     6 | Cost: 1.095794e-01
% Iteration     7 | Cost: 1.012910e-01
% Iteration     8 | Cost: 1.003343e-01
% Iteration     9 | Cost: 1.002875e-01
% Iteration    10 | Cost: 1.002708e-01
% Iteration    11 | Cost: 1.002660e-01
% Iteration    12 | Cost: 1.002639e-01
% Iteration    13 | Cost: 1.002636e-01
% Iteration    14 | Cost: 1.002636e-01
% Iteration    15 | Cost: 1.002636e-01
% Iteration    16 | Cost: 1.002636e-01
% Iteration    17 | Cost: 1.002636e-01
% Iteration    18 | Cost: 1.002636e-01
% Iteration    19 | Cost: 1.002636e-01
% Iteration    20 | Cost: 1.002636e-01
% Iteration    21 | Cost: 1.002636e-01
% Iteration    22 | Cost: 1.002636e-01
% Iteration    23 | Cost: 1.002636e-01
% Iteration    24 | Cost: 1.002636e-01
% Iteration    25 | Cost: 1.002636e-01
% Iteration    26 | Cost: 1.002636e-01
% Iteration    27 | Cost: 1.002636e-01
% Iteration    29 | Cost: 1.002636e-01
% Iteration    30 | Cost: 1.002636e-01
% Iteration    31 | Cost: 1.002636e-01
% Iteration    32 | Cost: 1.002636e-01
% 
% Iteration     1 | Cost: 4.202132e-01
% Iteration     2 | Cost: 3.970889e-01
% Iteration     3 | Cost: 3.673914e-01
% Iteration     4 | Cost: 3.642254e-01
% Iteration     5 | Cost: 3.611087e-01
% Iteration     6 | Cost: 3.598573e-01
% Iteration     7 | Cost: 3.598359e-01
% Iteration     8 | Cost: 3.598130e-01
% Iteration     9 | Cost: 3.598122e-01
% Iteration    10 | Cost: 3.598119e-01
% Iteration    11 | Cost: 3.598119e-01
% Iteration    12 | Cost: 3.598119e-01
% Iteration    13 | Cost: 3.598119e-01
% Iteration    14 | Cost: 3.598119e-01
% Iteration    15 | Cost: 3.598119e-01
% Iteration    16 | Cost: 3.598119e-01
% Iteration    17 | Cost: 3.598119e-01
% Iteration    18 | Cost: 3.598119e-01
% Iteration    19 | Cost: 3.598119e-01
% Iteration    20 | Cost: 3.598119e-01
% Iteration    21 | Cost: 3.598119e-01
% Iteration    22 | Cost: 3.598119e-01
% Iteration    23 | Cost: 3.598119e-01
% Iteration    24 | Cost: 3.598119e-01
% 
% 
