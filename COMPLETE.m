clear all
close all


table1 = readtable('ingredients_dietary.csv');

tablecell = table2cell(table1);



%% If they have dietry requirements, do this code - removes rows 
customer_preferences = "Vegan";

row = 1;
for i = 1:length(tablecell)
    ing_diet = split(tablecell(i,9));
    TF = contains(customer_preferences,ing_diet);
    if TF == 1
        tablec(row,:) = tablecell(i,:);
        row = row + 1;
    end
end
    
table = cell2table(tablec); % new table 

%% Userinput Savings
userinput = ["avocado", "lime juice", "onion", "tomato", "cheddar", "broccoli"]; 

% table setup
tablec = table2cell(table);
unique_ID = unique(cell2mat(tablec(:,1)));
non_unique_ID = cell2mat(tablec(:,1)); 
cust_savings = unique_ID;
custing_used = num2cell(unique_ID);


for i = 1:length(unique_ID)
    RecIngredients = string(tablec(non_unique_ID==unique_ID(i),8));
    Recleftovering = RecIngredients;
    Price = cell2mat(tablec(non_unique_ID==unique_ID(i),5));
    match_index = ismember(RecIngredients,userinput);
    
    cust_savings(i,2) = (sum(Price));
    cust_savings(i,3) = (sum(match_index));        % No. of cust ingredients                        
    cust_savings(i,4) = (sum(Price'*match_index));          % Savings
    cust_savings(i,5) = (sum(Price) - sum(Price'*match_index)); % New_Recipe_Cost
    custing_used(i,2) = {RecIngredients(match_index)}; % what customer used
    Recleftovering(match_index,:) = [];
    custing_used(i,3) = {Recleftovering}; % leftover ing to buy
end
    
% Take out cust ingredients from table 
for i = 1:length(userinput)
    input_2bremoved = userinput(i);
    table(table.tablec8 == [input_2bremoved], :) = [];
end 

T1 = array2table(cust_savings,'VariableNames',{'Recipe_ID','Recipe_Cost','No._of_Customer_ing', 'Savings', 'New_Recipe_Cost'}); %'Custing_recipe'});


%% Calculate leftovers from meal 1

leftover_m1 = leftover_func1(table2cell(table));


%% Leftovers from recipe 2 after considering leftover 1 recipes
leftover_ing_ID = cell2mat(leftover_m1(:,1));         % IDs of all the leftovers
unique_leftovering_ID = unique(leftover_ing_ID);      % unique IDs of all the leftovers
Table3 = [];
row = 0;
C = cell(1,9);
% scnd_rec_reduced_log = {};


for i = 1:length(unique_ID) % get specific meal 2 all ingredients
    scnd_rec_data = tablec(non_unique_ID==unique_ID(i),:);         %       
    scnd_rec_ings = string(tablec(non_unique_ID==unique_ID(i),8)); 
    scnd_rec_reduced = scnd_rec_data;
    
    scnd_rec_price = tablec(non_unique_ID==unique_ID(i),:);
  
    scnd_price = cell2mat(scnd_rec_price(:,5)); 
    new_price = scnd_price;
    % Get specific meal 2 ings
    
    for j = 1:length(unique_leftovering_ID) % get meal 1 all ingredients
        num_1lftover_used = [0];
        num_1lftover_unused = [0];
        ings_used = {0};
        
        first_meal_data = leftover_m1(leftover_ing_ID==unique_leftovering_ID(j),:); % could be 2+
        first_meal_unused = first_meal_data;
        first_meal_ings = first_meal_data(:,8);
        % Compare specific meal 2 all ings to specific meal 1 all ings (e.g ID 0 to ID 1)

   
        is_match = ismember(scnd_rec_ings, first_meal_ings);  
        % No correlation? Skip to next, ignore below
       
        if any(is_match)==1 % If matches, split meal 1 ings
            for k = 1:length(first_meal_ings)
                first_ing_data = first_meal_data(k,:);  
                first_ing = first_ing_data(:,8);
                is_match2 = ismember(string(scnd_rec_reduced(:,8)), first_ing); 
        % Compare first meal ing against 2nd meal reduced ing amount 
                
              
                if any(is_match2)==1 %
                    index = find(is_match2); % which index of second recipe does meal 1 ingredient correlate with 
                    matched_second_ing = scnd_rec_data(index,:); % isolate second recipe ing
                    
                    sec_ing = string(matched_second_ing(:,6)); 
                    sec_ing = erase(sec_ing,'g');  
                    sec_ing = str2num(sec_ing); % find amount of matched 2nd ing
                    
                    first_ingn = cell2mat(first_ing_data(:,10)); % find amount of 1st ing
           
                    try 
                    difference = sec_ing - first_ingn;     
                    
                    

                   % depending on value of difference
                    if difference < sec_ing*0.3
                        new_price(index) = 0;  
                        scnd_rec_reduced(index,:) = [];
                        first_ing_name = first_ing_data(:,8);
                        ings_used(num_1lftover_used + 1,1) = first_ing_name;
                        
                        
                        is_match3 = ismember(first_meal_unused(:,8),first_ing_name);
                        index1 = find(is_match3);
                        first_meal_unused(index1,:) = []; 
                      % final result will be added to m2 leftovers (number
                      % first_meal_unused - 1

                         
                        num_1lftover_used = num_1lftover_used + 1;
                        
 
                        
                    elseif difference > sec_ing*0.3
                        num_1lftover_unused = num_1lftover_unused +1;
                        % first_meal_unused the same 
                    end
                    
                    catch
                        fprintf("problem with" + i)
                        % num_1lftover_unused = num_1lftover_unused +1; ?
                    end
                else 
                    num_1lftover_unused = num_1lftover_unused + 1; 
                    % keep track of no.
                    % first_meal_unused unchanged (maybe use this to count?
                end  
            end % end of when ingredients matched

        Table3(row+1,1) = unique_leftovering_ID(j);          % meal 1 ID 
        % user unique_leftover_ID(j) to rill in 3 and 4!
        Table3(row+1,2) = unique_ID(i);                            % meal 2 ID 
        
        Table3(row+1,6) = sum(scnd_price);                     % original price 
        Table3(row+1,7) = sum(new_price);                 % new price
        Table3(row+1,8) = sum(scnd_price)-sum(new_price);      % savings from m2
     
        [nr,nc] = size(leftover_func1(scnd_rec_reduced));
        cust_leftover = cust_savings(unique_ID==unique_ID(i),3);
        Table3(row+1,11) = nr + num_1lftover_unused+cust_leftover; % leftover from 1&2&cust
        
                    else 
            Table3(row+1,1) = unique_leftovering_ID(j); % meal 1 ID
            Table3(row+1,2) = unique_ID(i);                   % meal 2 ID
            
            Table3(row+1,6) = sum(scnd_price);            % Cost meal 2
            Table3(row+1,7) = sum(scnd_price);            % Cost after meal 2
            
            [nr1,nc1] = size(first_meal_ings);              % leftover from meal 1 (all of it as 0 match)            
            [nr2,nc2] = size(leftover_func1(scnd_rec_data)); % leftover from meal 2
            cust_leftover = cust_savings(unique_ID==unique_ID(i),3);
            Table3(row+1,11) = nr1 + nr2+cust_leftover; % total leftovers
            % could add how much of meal 1 has gone into meal 2 here?
        
        end
        scnd_rec_reduced_log(row+1,2) = {unique_ID(i)};
        scnd_rec_reduced_log(row+1,1) = {unique_leftovering_ID(j)};
        scnd_rec_reduced_log(row+1,4) = {scnd_rec_reduced(:,[3 5])}; % what to get for second meal
        C = [C;scnd_rec_reduced];

        row = row + 1;
    end
end 


%% Add meal 1 cost etc values to table


for i = 1:length(unique_ID)
    ind = Table3(:,1)==unique_ID(i); % index of where meal i occurs  
    val = cust_savings(cust_savings(:,1)==unique_ID(i),2);
    val2 = cust_savings(cust_savings(:,1)==unique_ID(i),5);
    val3 = cust_savings(cust_savings(:,1)==unique_ID(i),3);
    Table3(ind,3) = (val); % original recipe cost 
    Table3(ind,4) = (val2); % new recipe cost
    Table3(ind,12) = val3; % no. of cust ings in M1
end    

%% Calculate total cost remaining table 
Table3(:,5) = Table3(:,3)-Table3(:,4); % m1 savings
Table3(:,9) = Table3(:,4)+Table3(:,7); % m2 savings
Table3(:,10) = Table3(:,5)+Table3(:,8);


T2 = array2table(Table3,'VariableNames',{'Meal1_ID','Meal2_ID','M1_cost', 'M1_newcost','M1_savings','M2_cost','M2_newcost','M2_savings','Total_cost','Total_Savings', 'Total leftovers','no.custinginm1'});

%% What customer needs to buy 

ingz = cell2mat(scnd_rec_reduced_log(:,1));

for i = 1:length(unique_ID)
    index = ingz==unique_ID(i);
    val = cell2mat(custing_used(:,1))==unique_ID(i);
    val2 = cell2mat(custing_used(:,1))==unique_ID(i);
    scnd_rec_reduced_log(index,5) = {custing_used(val,2)}; % what ing of cust went into m1
    scnd_rec_reduced_log(index,3) = {custing_used(val2,3)}; % what cust now needs to buy
end 

Table1 = cell2table(scnd_rec_reduced_log);
     
T3 = array2table(Table1,'VariableNames',{'Meal1_ID','Meal2_ID','M1_ings2buy','M2_ings2buy','Custingsin1'});




