%data = load('ex2data1.txt');
%X=data(:,1:2);
%y=data(:,3);


function plotData(X, y)
%PLOTDATA Plots the data points X and y into a new figure 
%   PLOTDATA(x,y) plots the data points with + for the positive examples
%   and o for the negative examples. X is assumed to be a Mx2 matrix.

% Create New Figure
figure; hold on;

% ====================== YOUR CODE HERE ======================
% Instructions: Plot the positive and negative examples on a
%               2D plot, using the option 'k+' for the positive
%               examples and 'ko' for the negative examples.
%


% Find Indices of Positive and Negative Examples
%'find' retrieves positions
% pos for those admitted
pos = find(y==1); 
%neg for those not admitted
neg = find(y==0);


% Plot Examples
%plot X col 2 on the y axis, X col 1 on the x axis
%separate into 2 plots, 1 for those positive/admitted
%plot using '+'s
plot(X(pos, 1), X(pos, 2), 'k+','LineWidth', 2, 'MarkerSize', 7);
%1 plot for those negative/not admitted
%plot using circles 'o'
plot(X(neg, 1), X(neg, 2), 'ko', 'MarkerFaceColor', 'y', 'MarkerSize', 7);





% =========================================================================



hold off;

end
