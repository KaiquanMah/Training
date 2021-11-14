function [X_norm, mu, sigma] = featureNormalize(X)
%FEATURENORMALIZE Normalizes the features in X 
%   FEATURENORMALIZE(X) returns a normalized version of X where
%   the mean value of each feature is 0 and the standard deviation
%   is 1. This is often a good preprocessing step to do when
%   working with learning algorithms.

% You need to set these values correctly
%instantiate first
X_norm = X;
%zero vector with 1 row and # cols according to 2nd dimension of incoming matrix X
mu = zeros(1, size(X, 2));
sigma = zeros(1, size(X, 2));

numRows = size(X,1);
numCols = size(X,2); 

%find the mean, sd outside and before the for loop
mu = mean(X);
sigma = std(X);



% ====================== YOUR CODE HERE ======================
% Instructions: First, for each feature dimension, compute the mean
%               of the feature and subtract it from the dataset,
%               storing the mean value in mu. 
% 


% j is the counter for each col
j = 1;


%iterate col by col
for j=1:numCols,
    
    % instantiate i at the start of iterating through each col
    % i is the counter for each row
    i = 1;
    
    %within each col, iterate row by row
    for i=1:numRows,
        
%               Next, compute the 
%               standard deviation of each feature and divide
%               each feature by it's standard deviation, storing
%               the standard deviation in sigma. 
%
        
        %then standardise by subtracting the col mean
        %from the Xij element value,
        %then dividing by col SD
        
        
        X_norm(i,j) = (X(i,j) - mu(1,j))/sigma(1,j);
        
        i = i+1;

%               Note that X is a matrix where each column is a 
%               feature and each row is an example. You need 
%               to perform the normalization separately for 
%               each feature. 
%
% Hint: You might find the 'mean' and 'std' functions useful.
%       

    end

    j = j+1;
    
end    
% ============================================================

end






%X=magic(5)
%X =
%    17    24     1     8    15
%    23     5     7    14    16
%     4     6    13    20    22
%    10    12    19    21     3
%    11    18    25     2     9

%featureNormalize(X)
%ans =
%    0.5521    1.3644   -1.2649   -0.6202    0.2760
%    1.3801   -0.9923   -0.6325    0.1240    0.4140
%   -1.2421   -0.8682         0    0.8682    1.2421
%   -0.4140   -0.1240    0.6325    0.9923   -1.3801
%   -0.2760    0.6202    1.2649   -1.3644   -0.5521

