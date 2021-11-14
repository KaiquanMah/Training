function idx = findClosestCentroids(X, centroids)
%FINDCLOSESTCENTROIDS computes the centroid memberships for every example
%   idx = FINDCLOSESTCENTROIDS (X, centroids) returns the closest centroids
%   in idx for a dataset X where each row is a single example. idx = m x 1 
%   vector of centroid assignments (i.e. each entry in range [1..K])
%


% ===============unit test data======================
% X 15x11
% X = reshape(sin(1:165), 15, 11);
% Z 11x11
% Z = reshape(cos(1:121), 11, 11);
% C 5x11 => 1st 5 rows of Z
% initial centroids C = Z(1:5, :);


% X =
%     0.8415   -0.2879   -0.4040    0.9018   -0.9661    0.5661    0.1060   -0.7271    0.9988   -0.7904    0.2021
%     0.9093   -0.9614    0.5514    0.1236   -0.7392    0.9995   -0.7795    0.1848    0.4987   -0.9425    0.9333
%     0.1411   -0.7510    0.9999   -0.7683    0.1674    0.5140   -0.9483    0.9268   -0.4599   -0.2281    0.8064
%    -0.7568    0.1499    0.5291   -0.9538    0.9200   -0.4441   -0.2453    0.8167   -0.9957    0.6961   -0.0619
%    -0.9589    0.9129   -0.4282   -0.2624    0.8268   -0.9939    0.6833   -0.0442   -0.6160    0.9802   -0.8733
%    -0.2794    0.8367   -0.9918    0.6702   -0.0266   -0.6299    0.9836   -0.8646    0.3300    0.3632   -0.8818
%     0.6570   -0.0089   -0.6435    0.9866   -0.8555    0.3132    0.3796   -0.8900    0.9726   -0.5878   -0.0795
%     0.9894   -0.8462    0.2964    0.3959   -0.8979    0.9684   -0.5734   -0.0972    0.7210   -0.9983    0.7958
%     0.4121   -0.9056    0.9638   -0.5588   -0.1148    0.7332   -0.9992    0.7850   -0.1935   -0.4910    0.9395
%    -0.5440   -0.1324    0.7451   -0.9998    0.7739   -0.1761   -0.5064    0.9454   -0.9301    0.4677    0.2194
%    -1.0000    0.7626   -0.1586   -0.5216    0.9511   -0.9235    0.4520    0.2367   -0.8116    0.9965   -0.7024
%    -0.5366    0.9564   -0.9165    0.4362    0.2538   -0.8218    0.9948   -0.6897    0.0531    0.6090   -0.9785
%     0.4202    0.2709   -0.8318    0.9929   -0.6768    0.0354    0.6230   -0.9820    0.8690   -0.3383   -0.3549
%     0.9906   -0.6636    0.0177    0.6367   -0.9851    0.8601   -0.3216   -0.3714    0.8859   -0.9746    0.5949
%     0.6503   -0.9880    0.8509   -0.3048   -0.3878    0.8940   -0.9705    0.5806    0.0884   -0.7149    0.9978
% 
% C =
%     0.5403    0.8439   -0.5328   -0.8486    0.5253    0.8532   -0.5178   -0.8578    0.5102    0.8623   -0.5025
%    -0.4161    0.9074    0.4242   -0.9037   -0.4322    0.8999    0.4401   -0.8960   -0.4481    0.8920    0.4560
%    -0.9900    0.1367    0.9912   -0.1280   -0.9923    0.1192    0.9934   -0.1104   -0.9944    0.1016    0.9953
%    -0.6536   -0.7597    0.6469    0.7654   -0.6401   -0.7711    0.6333    0.7767   -0.6264   -0.7822    0.6195
%     0.2837   -0.9577   -0.2921    0.9551    0.3006   -0.9524   -0.3090    0.9497    0.3174   -0.9469   -0.3258
% ===================================================






% Set K
% # rows in matrix C centroids
K = size(centroids, 1);

% You need to return the following variables correctly.
% X 15x11
% idx 15x1
idx = zeros(size(X,1), 1);

% ====================== YOUR CODE HERE ======================
% Instructions: Go over every example, find its closest centroid, and store
%               the index inside idx at the appropriate location.
%               Concretely, idx(i) should contain the index of the centroid
%               closest to example i. Hence, it should be a value in the 
%               range 1..K
%
% Note: You can use a for-loop over the examples to compute this.
%

% iterate across each X observation/row
for i = 1:size(X, 1),
    
    %instantiate the 'lowest_distance' variable 
    % which we would update as we
    % find the next lowest distance between each X point and centroid later
    lowest_distance = Inf;
    
    % iterate across each centroid
    for k = 1:K,
        
        % X 15x11, X(i, :) 1x11
        % C 5x11, C(k, :) 1x11
        difference = (X(i, :) - centroids(k, :));
        % difference 1x11
        % we want 1x1 => so difference 1x11 x difference' 11x1
        distance = difference*difference';
        
        
        % update the centroid # to assign to observation/row of X
        % if this centroid evaluated gives me a lower
        % minimum distance than all the other centroid evaluated so far
        % for this observation/row of X
        if distance < lowest_distance,
            
            lowest_distance = distance;
            % idx 15x1
            idx(i) = k;
            
        end
        
    end
    
end
% =============================================================

end

