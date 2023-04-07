clear all
close all

run data.m % load ingredients3 data

ingredients = table2cell(ingredients3);                % convert table
recipeID = table2array(unique(ingredients3(2:end,1))); % unique recipe IDs
firstcolumn = table2array(ingredients3(:,1));          % non-unique recipe ID column
numbofingredients = recipeID; % 1st column = recipe ID

userinput = ["avocado", "lime juice"];    % ingredients I have

for i = 0:length(recipeID)-1
    rows = string(ingredients(firstcolumn==i,8));    % obtain ingredients for recipe ID
    price = cell2mat(ingredients(firstcolumn==i,6)); % price of each ingredient in recipe 
    total = ismember(rows, userinput);               % no. of customer's ingredients in recipe
    numbofingredients(i+1,2) = sum(price); % Recipe_Cost             
    numbofingredients(i+1,3) = sum(total); % No. of cust ingredients                        
    numbofingredients(i+1,4) = sum(price'*total); % Savings
    numbofingredients(i+1,5) = sum(price) - sum(price'*total); % New_Recipe_Cost
end

T = array2table(numbofingredients,'VariableNames',{'Recipe_ID','Recipe_Cost','No._of_Customer_ing', 'Savings', 'New_Recipe_Cost'});

%     A = string(join(rows((find(total)))));
%     numbofingredients(i+1,3) = str2double(A);