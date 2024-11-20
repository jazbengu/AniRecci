import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv('raw_anime_data_paged.csv')

# Function for EDA
def eda_page():
    st.title("Exploratory Data Analysis (EDA)")

    # Load the dataset
    anime_df = load_data()

    # Display the dataset
    if st.checkbox("Show raw data"):
        st.subheader("Raw Data")
        st.write(anime_df)

    # Show basic statistics
    st.subheader("Basic Statistics")
    st.write(anime_df.describe())

    # Plotting ratings distribution
    st.subheader("Distribution of Ratings")
    fig, ax = plt.subplots()
    sns.histplot(anime_df['rating'], bins=20, kde=True, ax=ax)
    ax.set_title('Distribution of Anime Ratings')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

    # Plotting popularity distribution
    st.subheader("Distribution of Popularity")
    fig2, ax2 = plt.subplots()
    sns.histplot(anime_df['popularity'], bins=20, kde=True, ax=ax2)
    ax2.set_title('Distribution of Anime Popularity')
    ax2.set_xlabel('Popularity')
    ax2.set_ylabel('Frequency')
    st.pyplot(fig2)

    # Genre analysis
    st.subheader("Top Genres")
    genre_counts = anime_df['genres'].explode().value_counts()
    top_genres = genre_counts.head(10)
    fig3, ax3 = plt.subplots()
    sns.barplot(x=top_genres.values, y=top_genres.index, ax=ax3)
    ax3.set_title('Top 10 Genres')
    ax3.set_xlabel('Count')
    ax3.set_ylabel('Genre')
    st.pyplot(fig3)

    # Filter by genre
    st.subheader("Filter by Genre")
    genre_options = anime_df['genres'].explode().unique()
    selected_genre = st.selectbox("Select a Genre", options=genre_options)

    # Show filtered results
    filtered_data = anime_df[anime_df['genres'].apply(lambda x: selected_genre in x)]
    st.write(f"Showing {len(filtered_data)} anime for genre: {selected_genre}")
    st.write(filtered_data[['title', 'rating', 'popularity']])

# Main app logic
if __name__ == "__main__":
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Recommendations", "EDA"])

    if page == "Recommendation":
        # Include your existing recommendation system code here
        pass  # Replace this with your recommendation system code
    elif page == "EDA":
        eda_page()