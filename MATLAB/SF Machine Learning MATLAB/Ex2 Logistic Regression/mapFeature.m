function out = mapFeature(X1, X2)
% MAPFEATURE Feature mapping function to polynomial features
%
%   MAPFEATURE(X1, X2) maps the two input features
%   to quadratic features used in the regularization exercise.
%
%   Returns a new feature array with more features, comprising of 
%   X1, X2, X1.^2, X2.^2, X1*X2, X1*X2.^2, etc..
%
%   Inputs X1, X2 must be the same size
%

degree = 6;
out = ones(size(X1(:,1)));
for i = 1:degree
    for j = 0:i
        
        %using 'end' as an index
        %so in the next col position
        
        %1st iteration i=1, j=0 => (X1.^1).*(X2.^0) => (X1.^1).*1 =>
        %(X1.^1) => "X1"
        %2nd iteration i=1, j=1 => (X1.^0).*(X2.^1) => (X2.^1) => "X2"
        %then end the set of 'j' for loops when i=1
        out(:, end+1) = (X1.^(i-j)).*(X2.^j);
        
        %next iteration of i=2
        %1st i=2, j=0 => (X1.^2).*(X2.^0) => (X1.^2).*1 => (X1.^2) =>
        %"X1^2"
        %2nd i=2, j=1 => (X1.^1).*(X2.^1) => "X1X2"
        %3rd i=2, j=2 => (X1.^0).*(X2.^2) => "X2^2"
        %then end the set of 'j' for loops when i=2
        
        %then continue until we end the set of 'j' for loops when i=6
        
    end
end

end