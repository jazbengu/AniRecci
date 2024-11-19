import streamlit as st
import papermill as pm
import pandas as pd
import json

def main():
    st.title("AniRecci")
    user_anime_titles = st.text_input("Enter your favorite anime titles separated by commas:")
    
    if st.button("Submit"):
        # Split the titles and prepare them for passing
        titles = user_anime_titles.split(',')

        # Run the Jupyter notebook with parameters using papermill
        pm.execute_notebook(
            'anime_processing.ipynb',  # Path to your notebook
            parameters={'user_anime_titles': json.dumps(titles)}  # Pass the titles as a JSON string
        )

        # Read the recommendations from the CSV file
        recommendations_df = pd.read_csv('anime_recommendations.csv')
        st.dataframe(recommendations_df)

if __name__ == "__main__":
    main()