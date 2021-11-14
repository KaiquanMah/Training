function [bestEpsilon bestF1] = selectThreshold(yval, pval)
%SELECTTHRESHOLD Find the best threshold (epsilon) to use for selecting
%outliers
%   [bestEpsilon bestF1] = SELECTTHRESHOLD(yval, pval) finds the best
%   threshold to use for selecting outliers based on the results from a
%   validation set (pval) and the ground truth (yval).
%

bestEpsilon = 0;
bestF1 = 0;
F1 = 0;

stepsize = (max(pval) - min(pval)) / 1000;
for epsilon = min(pval):stepsize:max(pval)
    
    % ====================== YOUR CODE HERE ======================
    % Instructions: Compute the F1 score of choosing epsilon as the
    %               threshold and place the value in F1. The code at the
    %               end of the loop will compare the F1 score for this
    %               choice of epsilon and set it to be the best epsilon if
    %               it is better than the current choice of epsilon.
    %               
    % Note: You can use predictions = (pval < epsilon) to get a binary vector
    %       of 0's and 1's of the outlier predictions
    
    % 1 if pval has a probability which is much lower than threshold
    % i.e. 1 = anomalous, 0 = ok
    % get the binary vector based on the 'epsilon' threshold
    % values looped over during each iteration
    cvPredictions = (pval < epsilon);
    
    tp = sum((cvPredictions == 1) & (yval == 1));
    tn = sum((cvPredictions == 0) & (yval == 0));
    % falsely predicted as POS, actually is NEG
    fp = sum((cvPredictions == 1) & (yval == 0));
    % falsely predicted as NEG, actually is POS
    fn = sum((cvPredictions == 0) & (yval == 1));
    
    
    % compute precision, recall, F1 score
    prec = tp/(tp+fp);
    rec = tp/(tp+fn);
    F1 = (2*prec*rec)/(prec+rec);
    % =============================================================

    if F1 > bestF1
       bestF1 = F1;
       bestEpsilon = epsilon;
    end
end

end



% [bestEpsilon bestF1] = selectThreshold(yval, pval)
% bestEpsilon =
%     0.8422
% bestF1 =
%     0.7143
