%% Leftover function (cell/table? input)

function f = leftover_func1(t1)

% table = cell2table(vm_ingredients);
section = string(t1(:,2));

% Index all meat, veg, dairy rows
veg_index = strcmp(section, "Fruits and vegetables");
meat_index = strcmp(section, "Meats and seafood");
dairy_index = strcmp(section, "Dairy and eggs");
tot_index = logical(veg_index + meat_index + dairy_index);

vm_ingredients = t1(tot_index,:);


% Set up table and variables
vm_ingredients(:,10) = {'0'};
vm_ingredients(:,11) = {'-'};
recip_amount = string(vm_ingredients(:,6));
tesc_ing = string(vm_ingredients(:,3));
buying_quantities = cell2mat(vm_ingredients(:,4));
sz = size(vm_ingredients);


% Calculate leftovers
for i = 1:sz(1)
    
    % Rule 1
    if isempty(recip_amount{i}) == 1
        vm_ingredients(i,10) = {0};
        vm_ingredients(i,11) = {'r1'};
    end 

    % Rule 2
    if contains(tesc_ing(i),"/") || contains(tesc_ing(i),"-")
        vm_ingredients(i,10) = {0};
        vm_ingredients(i,11) = {'r2'};
        
    % Rule 3 (both recipe and tesc ing grams)
    elseif contains(tesc_ing(i),"G") && contains(recip_amount(i),"g")
        Recip_grams = sscanf(recip_amount(i),'%d'); % remove letter g (just number left)
        TescIngWords = split((tesc_ing(i))); 
        % For Tesc Ing, make sure 
        for j = 1:length(TescIngWords)
            if contains(TescIngWords(j), "G") % isolate word containing 'G'
                newTescIng = erase(TescIngWords(j), "G"); % remove G
                newTescIng = erase(newTescIng, "," ); %
                TF = isstrprop(newTescIng,'alpha','ForceCellOutput',true); % after removing, just letters left?
                if any(cat(2, TF{:}) == 0) % if false means numbers left, correct word
                    vm_ingredients(i,10) = {str2num(newTescIng)*buying_quantities(i) - Recip_grams}; 
                    vm_ingredients(i,11) = {'g'};
                else 
                    vm_ingredients(i,10) = {0};
                    vm_ingredients(i,11) = {'g'};                 
                end
            end
        end  
        
    % Rule 4 (recipe grams but tesc ing not grams)
     elseif ~contains(tesc_ing(i),"G") && contains(recip_amount(i),"g")
        vm_ingredients(i,10) = {'0'};
        vm_ingredients(i,11) = {'r4'};  
        
    % Rule 5 (units)
    elseif ~isnan(str2double(recip_amount(i))) == 1 % not NaN = just number so therefore unit
        TescIngWords = split(tesc_ing(i)); % split tesco ing words to search for no.
        for j = 1:length(TescIngWords) 
            if ~isnan(str2double(TescIngWords(j))) % if word not NaN, therefore = unit
                vm_ingredients(i,10) = {str2num(TescIngWords(j))*buying_quantities(i) - str2num(recip_amount(i))};
                vm_ingredients(i,11) = {'units'};
            end
        end
        
    % Rule 5 (rec is unit but previously tesc ing not unit so ignore)
    if ~isnan(str2double(recip_amount(i))) == 1 && contains(string(vm_ingredients(i,9)),'0') 
        if contains(tesc_ing(i),"G") 
            vm_ingredients(i,10) = {'0'};
            vm_ingredients(i,11) = {'-'};
        else
            vm_ingredients(i,10) = {buying_quantities(i) - str2num(recip_amount(i))};
            vm_ingredients(i,11) = {'units'};
        end        
        
        
    end
    end
    end
           
leftover = str2double(string(vm_ingredients(:,10)));
rows = find(leftover > 0);
f = vm_ingredients(rows,:); 
end