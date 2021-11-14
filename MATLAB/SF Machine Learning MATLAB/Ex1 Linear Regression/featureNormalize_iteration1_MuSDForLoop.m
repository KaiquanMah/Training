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
    % instantiate colMean, colSD
    colMean = 0;
    colSD = 0;
    
    %within each col, iterate row by row
    for i=1:numRows,
        
%               Next, compute the 
%               standard deviation of each feature and divide
%               each feature by it's standard deviation, storing
%               the standard deviation in sigma. 
%
        
        %find the mean, sd, then standardise by subtracting the col mean
        %from the Xij element value,
        %then dividing by col SD
        
        colMean = mean(X,1);
        mu(1,j) = colMean;
        colSD = std(X);
        sigma(1,j) = colSD;
        
        X_norm(i,j) = (X(i,j) - colMean)/colSD;
        
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
