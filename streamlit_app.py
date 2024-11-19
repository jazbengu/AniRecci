# File: anime_recommendation_app.py

import streamlit as st
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def fetch_anime_data_paged(limit=4500):
    anime_list = []
    current_page = 1
    fetched_count = 0

    while fetched_count < limit:
        try:
            url = f"https://api.jikan.moe/v4/anime?page={current_page}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json().get('data', [])
                if not data:
                    print("No more anime data available.")
                    break

                for anime in data:
                    anime_data = {
                        'id': anime.get('mal_id'),
                        'title': anime.get('title'),
                        'genres': [genre['name'] for genre in anime.get('genres', [])],
                        'popularity': anime.get('popularity'),
                        'rating': anime.get('score'),
                        'description': anime.get('synopsis'),
                        'image_url': anime.get('images', {}).get('jpg', {}).get('image_url')  # Fetching image URL
                    }
                    anime_list.append(anime_data)
                    fetched_count += 1
                    if fetched_count >= limit:
                        break

                current_page += 1
            else:
                print(f"Error fetching page {current_page}: HTTP {response.status_code}")
                break
        except Exception as e:
            print(f"Error fetching page {current_page}: {e}")
            break

    return anime_list

    from sklearn.preprocessing import MinMaxScaler



def fetch_anime_details(title):
    try:
        url = f"https://api.jikan.moe/v4/anime?q={title}&limit=1"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get('data', [])
            if data:
                anime = data[0]
                return {
                    'id': anime.get('mal_id'),
                    'title': anime.get('title'),
                    'genres': [genre['name'] for genre in anime.get('genres', [])],
                    'description': anime.get('synopsis', ""),
                    'rating': anime.get('score', 0),
                    'image_url': anime.get('images', {}).get('jpg', {}).get('image_url')  # Fetching image URL
                }
        else:
            print(f"Error fetching details for '{title}': HTTP {response.status_code}")
    except Exception as e:
        print(f"Error fetching details for '{title}': {e}")
    return None



# Recommendation function with consistent TF-IDF usage
def recommend_less_popular(fetched_anime, tfidf_vectorizer, tfidf_matrix, less_popular_anime, num_recommendations=5):
    # Combine descriptions from fetched_anime
    fetched_descriptions = [anime['description'] for anime in fetched_anime if anime]

    if not fetched_descriptions:
        st.warning("No valid descriptions available for recommendations.")
        return []

    # Transform fetched descriptions using the pre-trained TF-IDF vectorizer
    fetched_features = tfidf_vectorizer.transform(fetched_descriptions).mean(axis=0).A1  # Use same vectorizer

    # Compute similarity scores
    similarity_scores = cosine_similarity(fetched_features.reshape(1, -1), tfidf_matrix)

    # Sort by similarity scores
    scores = [(i, similarity_scores[0, i]) for i in range(len(similarity_scores[0])) if i < len(less_popular_anime)]
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    # Limit the number of recommendations
    if len(scores) < num_recommendations:
        num_recommendations = len(scores)

    recommendations = []
    for i in scores[:num_recommendations]:
        try:
            recommendations.append(less_popular_anime.iloc[i[0]])
        except IndexError:
            continue

    return recommendations

if __name__ == "__main__":
    st.title("Anime Recommendation System")

    # Load and preprocess the dataset
    anime_df = pd.read_csv('less_popular_anime.csv')
    anime_df['description'] = anime_df['description'].fillna("No description available.")
    anime_df['genres'] = anime_df['genres'].apply(lambda x: [g.lower() for g in eval(x)] if pd.notna(x) else [])
    
    # Precompute TF-IDF and the similarity matrix using a single TfidfVectorizer object
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(anime_df['description'])

    # Filter less popular anime
    threshold = anime_df["popularity"].quantile(0.5)
    less_popular_anime = anime_df[anime_df["popularity"] > threshold]

    # User input
    user_input = st.text_input("Enter your favorite anime titles (comma-separated):", "")
    num_recommendations = st.slider("Number of recommendations:", 1, 10, 5)

    if st.button("Get Recommendations"):
        if user_input:
            titles = [title.strip() for title in user_input.split(',')]
            fetched_anime = []
            for title in titles:
                anime_details = fetch_anime_details(title)
                if anime_details:
                    fetched_anime.append(anime_details)

            if fetched_anime:
                # Pass the correct TF-IDF vectorizer
                recommendations = recommend_less_popular(fetched_anime, tfidf_vectorizer, tfidf_matrix, less_popular_anime, num_recommendations)
            if recommendations:
                st.write("### Recommended Lesser-Known Anime")

                # Create a row of columns for each recommendation
                cols = st.columns(len(recommendations))  # Create a number of columns equal to the number of recommendations

                for col, anime in zip(cols, recommendations):
                    with col:
                        # Safely get the image URL or use a placeholder
                        image_url = anime.get('image_url', "https://via.placeholder.com/120")
                        st.image(image_url, width=120)
                        st.markdown(f"**Title:** {anime['title']}")
                        st.markdown(f"**Genres:** {', '.join(anime['genres'])}")
                        st.markdown(f"**Rating:** {anime['rating']:.1f}")
                        st.markdown(f"**Description:** {anime['description'][:250]}...")

                else:
                    st.error("No recommendations could be generated.")
            else:
                st.warning("No anime details were fetched.")
        else:
            st.error("Please enter at least one anime title.")
