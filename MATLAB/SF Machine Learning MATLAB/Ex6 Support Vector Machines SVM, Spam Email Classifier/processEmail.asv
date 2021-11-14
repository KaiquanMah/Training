function word_indices = processEmail(email_contents)
%PROCESSEMAIL preprocesses a the body of an email and
%returns a list of word_indices 
%   word_indices = PROCESSEMAIL(email_contents) preprocesses 
%   the body of an email and returns a list of indices of the 
%   words contained in the email. 
%

% Load Vocabulary
vocabList = getVocabList();

% Init return value
word_indices = [];

% ========================== Preprocess Email ===========================

% Find the Headers ( \n\n and remove )
% Uncomment the following lines if you are working with raw emails with the
% full headers

% hdrstart = strfind(email_contents, ([char(10) char(10)]));
% email_contents = email_contents(hdrstart(1):end);

% Lower case
email_contents = lower(email_contents);

% Strip all HTML
% Looks for any expression that starts with < and ends with > and replace
% and does not have any < or > in the tag it with a space
email_contents = regexprep(email_contents, '<[^<>]+>', ' ');

% Handle Numbers
% Look for one or more characters between 0-9
email_contents = regexprep(email_contents, '[0-9]+', 'number');

% Handle URLS
% Look for strings starting with http:// or https://
email_contents = regexprep(email_contents, ...
                           '(http|https)://[^\s]*', 'httpaddr');

% Handle Email Addresses
% Look for strings with @ in the middle
email_contents = regexprep(email_contents, '[^\s]+@[^\s]+', 'emailaddr');

% Handle $ sign
email_contents = regexprep(email_contents, '[$]+', 'dollar');


% ========================== Tokenize Email ===========================

% Output the email to screen as well
fprintf('\n==== Processed Email ====\n\n');

% Process file
l = 0;

while ~isempty(email_contents)

    % Tokenize and also get rid of any punctuation
    % https://www.mathworks.com/help/matlab/ref/strtok.html
    % strtok(stringVariable, list of delimiters)
    % https://www.mathworks.com/help/matlab/ref/newline.html
    % newline is equivalent to char(10) or sprintf('\n')
    % https://stackoverflow.com/questions/10059142/reading-r-carriage-return-vs-n-newline-from-console-with-getc
    % carriage return '\r' => char(13)
    [str, email_contents] = ...
       strtok(email_contents, ...
              [' @$/#.-:&*+=[]?!(){},''">_<;%' char(10) char(13)]);
   
    
    % https://www.mathworks.com/help/matlab/ref/regexprep.html
    % regexprep => replace text using regex
    % newStr = regexprep(str, expression, replace with)
    % https://regexr.com/
    % ^ => match chars NOT IN THIS SET
    % Remove any non alphanumeric characters
    str = regexprep(str, '[^a-zA-Z0-9]', '');

    
    % Stem the word 
    % (the porterStemmer sometimes has issues, so we use a try catch block)
    % https://www.mathworks.com/help/matlab/ref/strtrim.html
    % strtrim removes leading and trailing whitespace from strings
    % then run the 'porterStemmer.m' script
    try str = porterStemmer(strtrim(str)); 
    % if the 'try' statement doesnt work
    % assign '' blank to the string 'str'
    catch str = ''; continue;
    end;

    
    
    % Skip the word if it is too short
    if length(str) < 1
       continue;
    end

    
    
    % Look up the word in the dictionary and add to word_indices if
    % found
    % ====================== YOUR CODE HERE ======================
    % Instructions: Fill in this function to add the index of str to
    %               word_indices if it is in the vocabulary. 
    % 
    %               At this point
    %               of the code, you have a stemmed word from the email in
    %               the variable str. 
    % 
    %               You should look up str in the
    %               vocabulary list (vocabList). If a match exists, you
    %               should add the index of the word to the word_indices
    %               vector. 
    % 
    %               Concretely, if str = 'action', then you should
    %               look up the vocabulary list to find where in vocabList
    %               'action' appears. 
    %
    %               For example, if vocabList{18} =
    %               'action', then, you should add 18 to the word_indices 
    %               vector (e.g., word_indices = [word_indices ; 18]; ).
    % 
    % Note: vocabList{idx} returns a the word with index idx in the
    %       vocabulary list.
    % 
    %https://www.mathworks.com/help/matlab/ref/strcmp.html
    %strcmp = string compare => TRUE/1 means strings are the same 
    % Note: You can use strcmp(str1, str2) to compare two strings (str1 and
    %       str2). It will return 1 only if the two strings are equivalent.
    %

    for i= 1:length(vocabList),
        
        % if vocablist{i} = str,
        if strcmp(vocabList{i}, str),
            word_indices = [word_indices; i];
        end
        
    end


    % =============================================================


    % Print to screen, ensuring that the output lines are not too long
    if (l + length(str) + 1) > 78
        fprintf('\n');
        l = 0;
    end
    fprintf('%s ', str);
    l = l + length(str) + 1;

end

% Print footer
fprintf('\n\n=========================\n');

end




% ====================================================
% spam email public corpus
% http://spamassassin.apache.org/old/publiccorpus/





% vocabList =
%   1899×1 cell array
%     {'aa'                                      }
%     {'ab'                                      }
%     {'abil'                                    }
%     {'abl'                                     }
%     {'about'                                   }
%     {'abov'                                    }
%     {'absolut'                                 }
%     ...
%     {'yahoo'                                   }
%     {'ye'                                      }
%     {'yeah'                                    }
%     {'year'                                    }
%     {'yesterdai'                               }
%     {'yet'                                     }
%     {'york'                                    }
%     {'you'                                     }
%     {'young'                                   }
%     {'your'                                    }
%     {'yourself'                                }
%     {'zdnet'                                   }
%     {'zero'                                    }
%     {'zip'                                     }
    