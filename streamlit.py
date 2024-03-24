import streamlit as st
from openai import OpenAI
import pandas as pd
import os

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

#api = os.environ.get("OPENAI_API_KEY")
#client = OpenAI(api_key=api)

#for vercel
#API_KEY = os.environ.get('API_URL')
#client = OpenAI(api_key=API_KEY)

def generator(selected_categories, budget, comment):
    
    # Load the items from the CSV file
    items_df = pd.read_csv('processedItemDetails.csv')

    # Filter items by selected categories
    filtered_items = items_df[items_df['Department'].isin(selected_categories)]

    # Constructing a detailed prompt with ingredient descriptions and their prices
    ingredients_list = [f"{row['Description']} ({row['Price']})" for index, row in filtered_items.iterrows()]
    ingredients_text = "; ".join(ingredients_list)
    
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You will act as a helpful assistant for a superstore provided with a strict budget, tasked with creating three budget-friendly meal plans for budget conscious customers. For each meal plan, please use the following structure: 1. Title: Provide a clear, big heading that names the Meal Plan. 2. Ingredients List: Under the heading, list all ingredients required for the meal plan along with their individual costs in a bullet-point format. Use sparsely - add (not listed) if you choose to recommend a few ingredients not liste 3. Total Cost: After the ingredients list, clearly state the total cost of the meal plan. 4. Recommendations: Conclude with a short section of notes that offer your practical recommendations tailored to budget constraints. These recommendations might include tips for cost-saving substitutions or how to make the most of the ingredients."},
            {"role": "user", "content": f"Given a very strict budget of ${budget} and focusing on the following ingredients with their prices: {ingredients_text}, generate three (3) meal prep recipe plans. Strongly consider the cost of ingredients to strictly stay within budget. Very important consideration - student's comments: {comment}."}
        ])
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        st.sidebar.error(f"An error occurred: {e}")
        return None

st.set_page_config(page_title="Meal Planner", page_icon="favicon.png", layout="centered", initial_sidebar_state="auto")

st.title("Meal Planner")
st.header("Get three tailored meal prep plans that fit your goals, budget, and taste")
st.subheader("Food categories / dietary allowance")

produce = st.checkbox("Produce", value=True)
meat = st.checkbox("Meat", value=True)
dairy = st.checkbox("Dairy", value=True)
seafood = st.checkbox("Seafood", value=True)
grocery = True

budget = st.number_input('Enter your budget', min_value=0.00, max_value=100.00, step=1.00, value=30.00, format="%.2f")
comment = st.text_area("Additional comments", value="High protein", max_chars=100)

if st.button('Generate Meals'):
    # edge case -  none selected
    if not (produce or meat or dairy or seafood):
        st.error('Error: At least one category must be selected.')

    else:
        selected_categories = [category for category, selected in 
                               [("Produce", produce), ("Meat", meat), ("Dairy", dairy), ("Seafood", seafood), ("Grocery", grocery)] if selected]
        #st.write(f'{selected_categories}')
        meal_plans = generator(selected_categories, budget, comment)
        st.write(meal_plans)