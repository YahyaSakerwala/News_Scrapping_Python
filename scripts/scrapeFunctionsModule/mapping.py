def map_categories(original_category):
        # Define a mapping dictionary
        category_mapping = {
        'Business': ['financial','business'],
        'Economy': ['economy', 'economic news'],
        'Politics': ['politics', 'government', 'political'],
        'Opinion': ['opinion'],
        'Stocks':['stock markets','stocks','stock market'],
        'Sports':['sports','sport'],
        'Education':['eductaion'],
        'World':['national report','asia & world','u.s. news']
        # Add more mappings as needed
        }
        # Convert the original category to lowercase for case-insensitive matching
        original_category_lower = original_category.strip().lower()

        # Iterate through the mapping dictionary to find a match
        for standard_category, aliases in category_mapping.items():
            if any(alias in original_category_lower for alias in aliases):
             return standard_category
            
        return "Others"