function [C, sigma] = dataset3Params(X, y, Xval, yval)
%DATASET3PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = DATASET3PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
C = 1;
sigma = 0.3;


%X 211x2
% y 211x1
% Xval 200x2
% yval 200x1


% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%
% define the C and sigma values to test out
C_params = [0.01 0.03 0.1 0.3 1 3 10 30];
sigma_params = [0.01 0.03 0.1 0.3 1 3 10 30];

% instantiate the max amount of error
maxError = Inf;

% loop through every C value
% C_i is our C counter
for Ci = 1:length(C_params),
    CInner = C_params(Ci);
    
    % loop through every sigma value   
    % sigma_i is our sigma counter
    for sigmai = 1:length(sigma_params),
        sigmaInner = sigma_params(sigmai);
        
        % from the CInner and sigmaInner combo obtained
        % train on the training set
        % to obtain a trained model => 1 for every C + sigma combo
        % svmTrain(X, Y, C, kernelFunction, tol tolerance value, max_passes)
        % tol and max_passes values can be defaulted in the 'svmTrain' function
        model = svmTrain(X, y, CInner, @(x1, x2) gaussianKernel(x1, x2, sigmaInner));
        
        % use trained model to predict 'y' values using Xval/cross
        % validation set
        predictions = svmPredict(model, Xval);
        
        % find the errors where predicted 'y' is different from actual 'y'
        % in 'yval'
        predictionError = mean(double(predictions ~= yval));
        
        % as we loop through each of the C + sigma combos
        % only assign the value to the 'resulting' variables
        % if the predictionError from this iteration is lower than 
        % what we have obtained so far
        
        if predictionError < maxError,
            % assign the latest predictionError to our 'maxError', which
            % should ideally be decreasing
            % on average, as we increase the # of iterations
            % through the C + sigma combos
            maxError = predictionError;
            
            % assign the optimal C and sigma param values
            % and return as output in this function
            C = CInner;
            sigma = sigmaInner;
        end
        
    end
end

% =========================================================================

end



% C =
%      1
% sigma =
%     0.3000
