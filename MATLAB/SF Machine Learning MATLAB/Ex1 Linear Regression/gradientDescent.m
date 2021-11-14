function [theta, J_history] = gradientDescent(X, y, theta, alpha, num_iters)
%GRADIENTDESCENT Performs gradient descent to learn theta
%   theta = GRADIENTDESCENT(X, y, theta, alpha, num_iters) updates theta by 
%   taking num_iters gradient steps with learning rate alpha

% Initialize some useful values
% number of training examples, used to refine our theta value during each
% iteration
m = length(y); 
% initialise empty vector
J_history = zeros(num_iters, 1);
theta_len = length(theta);



for iter = 1:num_iters

    % ====================== YOUR CODE HERE ======================
    % Instructions: Perform a single gradient step on the parameter vector
    %               theta.  
    %
    % Hint: While debugging, it can be useful to print out the values
    %       of the cost function (computeCost) and gradient here.
    %
	
    
    %instantiate temp_theta using the input theta vector as a starting
    %point
	temp_theta = theta;
    
    
	for j = 1:theta_len		
		
        %instantiate SUM of errors
        sumErrors = 0;
        
        %following eqn on PDF pg 6
        %iterate through every row in X and y
        %sum ALL the errors
        %JUST DONT GET why we need to multiply with X(i,j)
		for i = 1:m
            sumErrors = sumErrors + (X(i,:) * theta - y(i,:)) * X(i,j);
            
            %the shorter "+=" approach below gave an error
            %Using sumErrors as both a variable and command is not
            %supported.
            % %sumErrors += (X(i,:) * theta - y(i,:)) * X(i,j);
		end

        %following eqn, update theta j for ALL j
        % maybe because we DONT want to co-mingle the FULL difference
        % between prediction vs 'y' 
        % for both theta1 and theta2 when we adjust it after every round

        % so we multiply (prediction-y) * the specific X col
        % get the SSE
        % then adjust the corresponding theta, e.g. theta1/2 (corresponding to the specific X col)
		temp_theta(j,:) = temp_theta(j,:) - ((alpha/m)*sumErrors);
	end
    
    %so from the SUM of errors
    %and adjusted theta value
	theta = temp_theta;

    % ============================================================
    
    %use the theta value to compute the cost during every iteration
    % Save the cost J in every iteration
    J_history(iter) = computeCost(X, y, theta);

end

end
