import streamlit as st
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load external CSS
st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

# Function to fetch anime details
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
                    'image_url': anime.get('images', {}).get('jpg', {}).get('image_url')
                }
        else:
            print(f"Error fetching details for '{title}': HTTP {response.status_code}")
    except Exception as e:
        print(f"Error fetching details for '{title}': {e}")
    return None

# Function to recommend lesser-known anime
def recommend_less_popular(fetched_anime, tfidf_vectorizer, tfidf_matrix, less_popular_anime, num_recommendations=5):
    fetched_descriptions = [anime['description'] for anime in fetched_anime if anime]

    if not fetched_descriptions:
        st.warning("No valid descriptions available for recommendations.")
        return []

    fetched_features = tfidf_vectorizer.transform(fetched_descriptions).mean(axis=0).A1
    similarity_scores = cosine_similarity(fetched_features.reshape(1, -1), tfidf_matrix)

    scores = [(i, similarity_scores[0, i]) for i in range(len(similarity_scores[0])) if i < len(less_popular_anime)]
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    if len(scores) < num_recommendations:
        num_recommendations = len(scores)

    recommendations = []
    for i in scores[:num_recommendations]:
        try:
            recommendations.append(less_popular_anime.iloc[i[0]])
        except IndexError:
            continue

    return recommendations

# Function for user feedback
def get_user_feedback():
    feedback = st.selectbox("Rate your overall recommendations experience:", options=["Select", "👍", "👎"])
    return feedback

# Main application
if __name__ == "__main__":
    st.title("AniRecci - Discover Lesser-Known Anime 🌟")

    # Load and preprocess the dataset
    anime_df = pd.read_csv('less_popular_anime.csv')
    anime_df['description'] = anime_df['description'].fillna("No description available.")
    anime_df['genres'] = anime_df['genres'].apply(lambda x: [g.lower() for g in eval(x)] if pd.notna(x) else [])
    
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(anime_df['description'])

    threshold = anime_df["popularity"].quantile(0.5)
    less_popular_anime = anime_df[anime_df["popularity"] > threshold]

    # Initialize session state for recommendations and user input
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
    if 'num_recommendations' not in st.session_state:
        st.session_state.num_recommendations = 5
    if 'feedback' not in st.session_state:
        st.session_state.feedback = ""

    # User input section
    st.session_state.user_input = st.text_input("Enter your favorite anime titles (comma-separated):", st.session_state.user_input)
    st.session_state.num_recommendations = st.slider("Number of recommendations:", 1, 10, st.session_state.num_recommendations)

    # Colorful "Get Recommendations" Button
    if st.button("Get Recommendations"):
        if st.session_state.user_input:
            titles = [title.strip() for title in st.session_state.user_input.split(',')]
            fetched_anime = []
            for title in titles:
                anime_details = fetch_anime_details(title)
                if anime_details:
                    fetched_anime.append(anime_details)

            if fetched_anime:
                st.session_state.recommendations = recommend_less_popular(fetched_anime, tfidf_vectorizer, tfidf_matrix, less_popular_anime, st.session_state.num_recommendations)
                if st.session_state.recommendations:
                    st.write("### Here Are Some Lesser-Known Anime 🌸")

                    # Display recommendations with colorful borders and hover effects
                    cols = st.columns(len(st.session_state.recommendations))

                    for col, anime in zip(cols, st.session_state.recommendations):
                        with col:
                            # If an image URL is not available, use a placeholder
                            image_url = anime.get('image_url', "https://via.placeholder.com/120")

                            # Display the recommendation card with detailed information
                            st.image(image_url, width=120)
                            
                            # Use the 'recommendation-card' class for styling
                            st.markdown(f"""
                            <div class='recommendation-card'>
                                <h4>{anime['title']}</h4>
                                <p><strong>Genres:</strong> {', '.join(anime['genres'])}</p>
                                <p><strong>Rating:</strong> {anime['rating']:.1f}</p>
                                <p><strong>Description:</strong> {anime['description'][:250]}...</p>
                            </div>
                            """, unsafe_allow_html=True)

                    feedback = get_user_feedback()
                    if feedback != "Select":
                        st.session_state.feedback = feedback
                        st.success(f"Thank you for your feedback: {st.session_state.feedback}")
                else:
                    st.error("No recommendations could be generated.")
            else:
                st.warning("No anime details were fetched.")
        else:
            st.error("Please enter at least one anime title.")

    # Display feedback section
    if st.session_state.feedback:
        st.write(f"### Thank You for Your Feedback! 🙏")
        st.markdown(f"Your feedback: {st.session_state.feedback}")
