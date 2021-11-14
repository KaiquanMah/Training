function p = predict(Theta1, Theta2, X)
%PREDICT Predict the label of an input given a trained neural network
%   p = PREDICT(Theta1, Theta2, X) outputs the predicted label of X given the
%   trained weights of a neural network (Theta1, Theta2)

% Useful values
m = size(X, 1);
num_labels = size(Theta2, 1);

% You need to return the following variables correctly 
p = zeros(size(X, 1), 1);

% ====================== YOUR CODE HERE ======================
% Instructions: Complete the following code to make predictions using
%               your learned neural network. You should set p to a 
%               vector containing labels between 1 to num_labels.
%
% Hint: The max function might come in useful. In particular, the max
%       function can also return the index of the max element, for more
%       information see 'help max'. If your examples are in rows, then, you
%       can use max(A, [], 2) to obtain the max for each row.
%



% Input layer
% X
% new X i.e. a1         m # rows x 401cols; m # observations x 401 pixels
% add a col of ones
a1 = [ones(m,1) X];



% Hidden layer - the 1 and only hidden layer
% Theta1            25 rows x 401 cols
% z2 = theta1 * a1'   (25 x 401) (401 x m) => 25 x m??
% => Theta1 * a1 => each row of
% Theta1 is a hidden unit AND cycles through all 401 'a1' observations 
% during each iteration
% 1. It seems that matrix X would have: m rows/observations and 400 pixels?
% 2. We essentially add 1 more pixel (all ones) to give us: m rows x 401 pixels.
% 3. Theta1 has: 25 rows x 401 cols. Each row corresponds to theta values for a particular hidden layer unit.
% 4. What I cant seem to wrap my head around is the intuition behind let's say the first row or first col of z2. Is there a resource which I can use to visualise this process better? 
% a1 m x 401 pixels
% Theta1 25 units x 401 param values for pixels
% Theta1' 401 param values x 25 units
% z2 m x 25 units => 1 col value per hidden layer unit
z2 = a1 * Theta1';
% s2    m x 25
s2 = sigmoid(z2);
% a2    m x 26 units (after adding 1 col of 'ones')
% DONT ADD 'ones' to theta
% ADD 'ones' to the output 'a' matrix at each layer
a2 = [ones(size(s2,1), 1) s2];




% Output layer
% output from hidden layer = 26 rows x (m+1) cols 
% a2 m x 26 'units from previous layer'
% Theta2    10 rows 'or units in the current layer' x 26 cols 'or param values for units from the previous layer'
% Theta2'   26 cols or param values x 10 rows or units in current layer
% z3        m observations x 10 units or 'classes, since this is the last/output layer'
% z3 => Theta2 (10,26) * a2 (26,m+1) => (m+1)x1??
z3 = a2 * Theta2';
a3 = sigmoid(z3);

% find across each row/observation
% the col/class/unit with the highest probability
% give me the probability value - p_max
% and the col position - p
[p_max, p] = max(a3, [], 2);
% =========================================================================


end













% 2021.08.10 Notes
% To summarise
% X => # observations x # parameters (x1, ..., xn)
% Theta1 => # units x # param values (for your parameters x1 to xn above)
% Theta2 => # units this layer x # param values (for your # units from the
% previous layer)
% DONT ADD 'ones' to theta
% ADD 'ones' to the output 'a' matrix at each layer
% find across each row/observation
% the col/class/unit with the highest probability
% give me the probability value - p_max
% and the col position - p








% data for unit testing
%   X = [ones(20,1) (exp(1) * sin(1:1:20))' (exp(0.5) * cos(1:1:20))'];
%   y = sin(X(:,1) + X(:,2)) > 0;
%   Xm = [ -1 -1 ; -1 -2 ; -2 -1 ; -2 -2 ; ...
%           1 1 ;  1 2 ;  2 1 ; 2 2 ; ...
%          -1 1 ;  -1 2 ;  -2 1 ; -2 2 ; ...
%           1 -1 ; 1 -2 ;  -2 -1 ; -2 -2 ];     %16x2 matrix
%   So Xm is a matrix of 16 observations across 2 variables/pixels

%   ym = [ 1 1 1 1 2 2 2 2 3 3 3 3 4 4 4 4 ]';
%   t1 = sin(reshape(1:2:24, 4, 3));    %give me #s from 1 to 24, in increments of 2
%   then reshape into a 4x3 matrix
%   then perform 'sine' computation on the numbers
%   t2 = cos(reshape(1:2:40, 4, 5));    %4x5 matrix
%   t1 and t2 both have 4 units in their respective layer?


% predict(t1, t2, Xm)
% m = size(Xm, 1);
% m=16

% num_labels = size(t2, 1);
% 4


% NOTE THAT ONES ARE ADDED AS A COL ACROSS EVERY ROW/OBSERVATION
% ONES ARE NOT ADDED AS JUST 1 NEW ROW/OBSERVATION => THIS IS DIFFERENT
% FROM ex3.pdf's understanding that gave us the inference that ONES are
% added as an extra row/observation!!!
% a1 = [ones(m,1) Xm];          %16 observations x 3 pixels
% a1 =
%      1    -1    -1
%      1    -1    -2
%      1    -2    -1
%      1    -2    -2
%      1     1     1
%      1     1     2
%      1     2     1
%      1     2     2
%      1    -1     1
%      1    -1     2
%      1    -2     1
%      1    -2     2
%      1     1    -1
%      1     1    -2
%      1    -2    -1
%      1    -2    -2

% z2 = a1 * t1';          %16 observations x 4
% from a1 16x3, t1 4x3, t1' 3x4
% z2 =
%     1.3907    0.9912   -2.2157    0.8529
%     2.3521    0.8414   -3.0524    1.6991
%     0.9786    1.9912   -2.6359    0.2026
%     1.9400    1.8413   -3.4726    1.0489
%     0.2922   -0.7090    0.2979    0.4611
%    -0.6692   -0.5591    1.1346   -0.3852
%     0.7043   -1.7090    0.7181    1.1113
%    -0.2571   -1.5591    1.5547    0.2651
%    -0.5320    1.2910   -0.5424   -0.8395
%    -1.4934    1.4409    0.2942   -1.6857
%    -0.9442    2.2910   -0.9626   -1.4898
%    -1.9056    2.4409   -0.1259   -2.3360
%     2.2150   -1.0087   -1.3754    2.1535
%     3.1764   -1.1586   -2.2121    2.9997
%     0.9786    1.9912   -2.6359    0.2026
%     1.9400    1.8413   -3.4726    1.0489
    
% s2 = sigmoid(z2);          %16x4
% s2 =
%     0.8007    0.7293    0.0983    0.7012
%     0.9131    0.6988    0.0451    0.8454
%     0.7268    0.8799    0.0669    0.5505
%     0.8744    0.8631    0.0301    0.7406
%     0.5725    0.3298    0.5739    0.6133
%     0.3387    0.3638    0.7567    0.4049
%     0.6691    0.1533    0.6722    0.7524
%     0.4361    0.1738    0.8256    0.5659
%     0.3700    0.7843    0.3676    0.3016
%     0.1834    0.8086    0.5730    0.1563
%     0.2801    0.9081    0.2764    0.1840
%     0.1295    0.9199    0.4686    0.0882
%     0.9016    0.2672    0.2017    0.8960
%     0.9599    0.2389    0.0987    0.9526
%     0.7268    0.8799    0.0669    0.5505
%     0.8744    0.8631    0.0301    0.7406


% a2 = [ones(size(s2,1), 1) s2];          %16 observations x 5
% a2 =
%     1.0000    0.8007    0.7293    0.0983    0.7012
%     1.0000    0.9131    0.6988    0.0451    0.8454
%     1.0000    0.7268    0.8799    0.0669    0.5505
%     1.0000    0.8744    0.8631    0.0301    0.7406
%     1.0000    0.5725    0.3298    0.5739    0.6133
%     1.0000    0.3387    0.3638    0.7567    0.4049
%     1.0000    0.6691    0.1533    0.6722    0.7524
%     1.0000    0.4361    0.1738    0.8256    0.5659
%     1.0000    0.3700    0.7843    0.3676    0.3016
%     1.0000    0.1834    0.8086    0.5730    0.1563
%     1.0000    0.2801    0.9081    0.2764    0.1840
%     1.0000    0.1295    0.9199    0.4686    0.0882
%     1.0000    0.9016    0.2672    0.2017    0.8960
%     1.0000    0.9599    0.2389    0.0987    0.9526
%     1.0000    0.7268    0.8799    0.0669    0.5505
%     1.0000    0.8744    0.8631    0.0301    0.7406
    
    

% z3 = a2 * t2';          %16x4
% from a2 16x5, t2 4x5, t2' 5x4
% z3 =
%    -0.3018   -0.9277    1.0739    0.0339
%    -0.4504   -1.0723    1.3429   -0.0454
%    -0.3051   -0.6338    0.8326   -0.0591
%    -0.4738   -0.8108    1.1487   -0.1452
%     0.4886   -1.3832    0.6626    0.8317
%     0.8763   -1.2158    0.1356    1.1029
%     0.5447   -1.7118    0.8800    0.9794
%     0.9060   -1.5688    0.3998    1.2361
%     0.3477   -0.5929    0.1457    0.4716
%     0.7166   -0.4984   -0.3018    0.7496
%     0.3067   -0.3379   -0.0255    0.3591
%     0.6325   -0.2965   -0.3857    0.6175
%    -0.1666   -1.5904    1.4903    0.3500
%    -0.3149   -1.6392    1.6792    0.2416
%    -0.3051   -0.6338    0.8326   -0.0591
%    -0.4738   -0.8108    1.1487   -0.1452

   
% a3 = sigmoid(z3);          %16x4
% a3 =
%     0.4251    0.2834    0.7453    0.5085
%     0.3893    0.2550    0.7930    0.4887
%     0.4243    0.3466    0.6969    0.4852
%     0.3837    0.3077    0.7593    0.4638
%     0.6198    0.2005    0.6598    0.6967
%     0.7061    0.2287    0.5339    0.7508
%     0.6329    0.1529    0.7068    0.7270
%     0.7122    0.1724    0.5986    0.7749
%     0.5861    0.3560    0.5364    0.6158
%     0.6719    0.3779    0.4251    0.6791
%     0.5761    0.4163    0.4936    0.5888
%     0.6530    0.4264    0.4048    0.6497
%     0.4584    0.1693    0.8161    0.5866
%     0.4219    0.1626    0.8428    0.5601
%     0.4243    0.3466    0.6969    0.4852
%     0.3837    0.3077    0.7593    0.4638



% seems to be finding the max of each row in a3
% to identify which class from theta2/t2 had the highest probability
% for each observation
% [p_max, p] = max(a3, [], 2);          %16x1
% p_max =
%     0.7453
%     0.7930
%     0.6969
%     0.7593
%     0.6967
%     0.7508
%     0.7270
%     0.7749
%     0.6158
%     0.6791
%     0.5888
%     0.6530
%     0.8161
%     0.8428
%     0.6969
%     0.7593
% 
% 
% 
% retrieve the position of the theta2/t2 class
% which had the highest probability
% p =          %16x1
%      3
%      3
%      3
%      3
%      4
%      4
%      4
%      4
%      4
%      4
%      4
%      1
%      3
%      3
%      3
%      3

