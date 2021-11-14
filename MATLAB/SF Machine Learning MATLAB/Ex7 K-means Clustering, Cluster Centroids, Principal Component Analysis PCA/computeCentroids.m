function centroids = computeCentroids(X, idx, K)
%COMPUTECENTROIDS returns the new centroids by computing the means of the 
%data points assigned to each centroid.
%   centroids = COMPUTECENTROIDS(X, idx, K) returns the new centroids by 
%   computing the means of the data points assigned to each centroid. 
% 
% It is
%   given a dataset X where each row is a single data point, 
% 
% a vector
%   idx of centroid assignments (i.e. each entry in range [1..K]) for each
%   example, and 
% 
% K, the number of centroids. 
% 
% You should return a matrix
%   centroids, where each row of centroids is the mean of the data points
%   assigned to it.
%

% Useful variables
[m n] = size(X);

% You need to return the following variables correctly.
centroids = zeros(K, n);


% ====================== YOUR CODE HERE ======================
% Instructions: Go over every centroid and compute mean of all points that
%               belong to it. Concretely, the row vector centroids(i, :)
%               should contain the mean of the data points assigned to
%               centroid i.
%
% Note: You can use a for-loop over the centroids to compute this.
%

%X 15x11
%idx 15x1
%centroids 5x11
% loop through every centroid
for k = 1:K,
    
    % instantiate # X observations with an index asigned to this centroid
    countsThisCentroid = 0;
    % instantiate a sum across all X observations asigned to this centroid
    sum = zeros(1, n);
    
    
    % loop through every row/observation in X
    % m = # observations
    for i = 1:m,
        
        if idx(i) == k,
            
            % sum 1xn
            % X(i, :) 1xn
            sum = sum + X(i, :);
            
            % add the count of X observations assigned to this centroid
            countsThisCentroid = countsThisCentroid + 1;
        
        end
        
    end    
    
    % at each centroid level
    % compute the new centroid mean values
    % centroids Kxn
    % denote centroids(k, :) => kth row, ALL cols
    % otherwise, centroids(k) returns only the kth row, 1st col value
    centroids(k, :) = sum/countsThisCentroid;    
    
end
% =============================================================
end
