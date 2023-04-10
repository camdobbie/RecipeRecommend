clear all
close all
run data.m
ingredients = readtable('ingredients3');

%% Isolate meats into single table 'meatrows'
meat_index = strcmp(ingredients.section, "Meats and seafood");
meatrow = ingredients(meat_index,[3 5 7]);
meatrows = table2cell(meatrow);
meatrows(:,4) = {'-'}; % leftover column
meatrows(:,5) = {'-'};

%% Set up values
recip_ing = string((table2array(meatrow(:,3)))); % string needed to scan for letters in quantities
tesc_ing = string((table2array(meatrow(:,1)))); 
buying_quantities = cell2mat(meatrows(:,2)); % quantity needed for multiplying with tesc_ing


%% Apply Rules
for i = 1:length(meatrows)
    %% Rule 1
    if isempty(recip_ing{i}) == 1
        meatrows(i,4) = {0};
    end 
    %% Rule 2
    if contains(tesc_ing(i),"/") || contains(tesc_ing(i),"-")
        meatrows(i,4) = {0};
    
    %% Rule 3
    elseif contains(tesc_ing(i),"G") && contains(recip_ing(i),"g") 
        TescIng = split(extractBefore(tesc_ing(i),"G")); % words before G(rams)
        Tescgramsnumb = TescIng{end}; % number just before G(rams)
        Recgramsnumb = sscanf(recip_ing(i),'%d'); % extract g(rams) number from recipe 
        meatrows(i,4) = {str2num(Tescgramsnumb)*buying_quantities(i) - Recgramsnumb}; % tesco(g)*quantity-recipe(g)
        meatrows(i,5) = {'g'};
    %% Rule 4
    elseif contains(tesc_ing(i),"Kg") && contains(recip_ing(i),"kg")
        TescIng = split(extractBefore(tesc_ing(i),"Kg"));
        Tescgramsnumb = TescIng{end};
        Recgramsnumb = sscanf(recip_ing(i),'%d');
        meatrows(i,4) = {str2num(Tescgramsnumb)*buying_quantities(i) - Recgramsnumb};
        meatrows(i,5) = {'kg'};
    %% Rule 5  
    elseif ~isnan(str2double(recip_ing(i))) == 1 % if fails to convert to no. means it's not a unit quantity
        TescIng = split(tesc_ing(i)); % split tesc ing into separate words
        for j = 1:length(TescIng) 
            if ~isnan(str2double(TescIng(j))) % if a word fails to convert to no. means it's not a unit
                meatrows(i,4) = {str2num(TescIng(j))*buying_quantities(i) - str2num(recip_ing(i))};
                meatrows(i,5) = {'units'};
            end
        end
        
    %% Rule 6  
    if ~isnan(str2double(recip_ing(i))) == 1 && contains(string(meatrows(i,4)), "-") 
        meatrows(i,4) = {0};
    end   
end 
end 

%% Rules
% Rule 1: When Recipe = no units, assume all ingredient used
% Rule 2: When Tesc.Ing is sold as £/kg or has weight-range, leftover = 0 (all used)
% Rule 3: When Recipe = weight(g), Tesc.Ing = weight(g), do sum of leftover
% Rule 4: When Recipe = weight(kg), Tesc.Ing = weight(Kg), do sum of leftover
% Rule 5: When Recipe = unit, Tesc.Ing = unit, do sum of leftover 
% Rule 6: When recipe = unit, Tesc.Ing = NO unit, leftover = 0

%% Create Table Again

table1 = cell2table(meatrows(:,[1 2 3]));
table1.Properties.VariableNames = ["item","quantity", "quantities"];

leftovernum = cell2mat(meatrows(:,4));
table2 = array2table(leftovernum);
table2.Properties.VariableNames = ["leftover_amount"];

table3 = cell2table(meatrows(:,5));
table3.Properties.VariableNames = ["leftover_units"];
final_table = [table1 table2 table3];

writetable(final_table,'leftovers.csv')




