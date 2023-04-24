%% Fruit n' Veg

clear all
close all
run data.m
ingredients = readtable('ingredients3');

%% Isolate meats into single table 'vegrows'
veg_index = strcmp(ingredients.section, "Fruits and vegetables");
vegrow = ingredients(veg_index,[3 5 7]);
vegrows = table2cell(vegrow);
vegrows(:,4) = {'00'}; % leftover column
vegrows(:,5) = {'-'};

%% Set up values
recip_ing = string((table2array(vegrow(:,3)))); % string needed to scan for letters in quantities
tesc_ing = string((table2array(vegrow(:,1)))); 
buying_quantities = cell2mat(vegrows(:,2)); % quantity needed for multiplying with tesc_ing

% %% Apply Rules
for i = 1:length(vegrows)
    %% Rule 1
    if isempty(recip_ing{i}) == 1
        vegrows(i,4) = {0};
        vegrows(i,5) = {"-"};
    end 
    
    %% Rule 2
    if contains(tesc_ing(i),"/") || contains(tesc_ing(i),"-")
        vegrows(i,4) = {0};
        vegrows(i,5) = {'£/Kg'};
    %% Rule 3
    elseif contains(tesc_ing(i),"G") && contains(recip_ing(i),"g") 
        Recgramsnumb = sscanf(recip_ing(i),'%d'); % number in grams 
        TescIng = split((tesc_ing(i))); % split words   
        for j = 1:length(TescIng)
            if contains(TescIng(j), "G") % isolate word containing G
                newTescIng = erase((TescIng(j)), "G");
                TF = isstrprop(newTescIng,'alpha','ForceCellOutput',true);
                if any(cat(2, TF{:}) == 0)
                    vegrows(i,4) = {str2num(newTescIng)*buying_quantities(i) - Recgramsnumb}; % tesco(g)*quantity-recipe(g)
                    vegrows(i,5) = {'g'};
                end
            end
        end                 
        
    elseif ~contains(tesc_ing(i),"G") && contains(recip_ing(i),"g")
        vegrows(i,4) = {0};
        vegrows(i,5) = {'g'};        
 

    
    %% Rule 4
    elseif ~isnan(str2double(recip_ing(i))) == 1 % if fails to convert to no. means it's not a unit quantity
        TescIng = split(tesc_ing(i)); % split tesc ing into separate words
        for j = 1:length(TescIng) 
            if ~isnan(str2double(TescIng(j))) % = if its NOT NaN if when trying to convert word to units = units 
                vegrows(i,4) = {str2num(TescIng(j))*buying_quantities(i) - str2num(recip_ing(i))};
                vegrows(i,5) = {'units'};
            end
        end
        
     %% Rule 5
    if ~isnan(str2double(recip_ing(i))) == 1 && contains(vegrows(i,5),'-')
        if contains(tesc_ing(i),"G") 
            vegrows(i,4) = {'0'};
            vegrows(i,5) = {'-'};
        else
            vegrows(i,4) = {buying_quantities(i) - str2num(recip_ing(i))};
            vegrows(i,5) = {'units'};
        end
    end

    end
    
end


leftover_string_version = string(vegrows(:,4));      
leftover_numbers = str2double(leftover_string_version);
rows = find(leftover_numbers > 0);
veg_leftovers = vegrows(rows, [1 4 5]);


        
