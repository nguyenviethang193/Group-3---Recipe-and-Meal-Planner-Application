from pickle import load
with open('clean_data.pkl', 'rb') as f:
    user_search_list = load(f)
    final_recipes_data = load(f)
    cuisine_region_list = load(f)
    dessert_list = load(f)
    maindish_list = load(f)
    sidedish_list = load(f)
    drink_list = load(f)
    appetizer_snack_list = load(f)