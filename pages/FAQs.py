import streamlit as st

def faqs_page():
    st.title("Frequently Asked Questions (FAQs) 📖")
    st.markdown("""
        Welcome to the FAQs page! Here, you'll find answers to common questions about **AniRecci**, 
        our anime recommendation system. If your question isn't listed here, feel free to reach out to us!
    """)
    
    # FAQ Sections
    st.header("1. General Questions")
    st.markdown("### What is AniRecci?")
    st.write("""
        AniRecci is an anime recommendation system designed to help you discover lesser-known anime titles 
        based on your preferences. By entering your favorite anime, AniRecci suggests similar anime that 
        might not be as mainstream but are worth exploring.
    """)

    st.markdown("### Who is AniRecci for?")
    st.write("""
        AniRecci is for anyone who loves anime and wants to explore underrated or hidden gems that they 
        might not find in popular lists. It's especially helpful for anime enthusiasts looking to expand 
        their watchlist beyond mainstream titles.
    """)

    st.header("2. Using the Application")
    st.markdown("### How do I use AniRecci?")
    st.write("""
        Using AniRecci is simple:
        1. Enter one or more of your favorite anime titles in the input box, separated by commas.
        2. Choose the number of recommendations you'd like to receive using the slider.
        3. Click the "Get Recommendations" button to see personalized suggestions!
    """)

    st.markdown("### Can I adjust the number of recommendations?")
    st.write("""
        Yes! You can use the slider to select how many recommendations you'd like to see, 
        ranging from 1 to 10 suggestions.
    """)

    st.markdown("### What kind of anime will AniRecci recommend?")
    st.write("""
        AniRecci focuses on lesser-known anime titles. These are anime that might not be as popular 
        as mainstream hits but have similar themes, genres, or styles to the titles you entered.
    """)

    st.header("3. Technical Questions")
    st.markdown("### How does AniRecci generate recommendations?")
    st.write("""
        AniRecci uses machine learning techniques, such as **TF-IDF vectorization** and **cosine similarity**, 
        to analyze anime descriptions and identify titles that are similar to the ones you like. It then ranks 
        these based on their relevance and presents you with the top recommendations.
    """)

    st.markdown("### What dataset does AniRecci use?")
    st.write("""
        AniRecci uses a custom dataset of anime titles, including metadata such as descriptions, genres, ratings, 
        and popularity scores. This dataset is sourced from **MyAnimeList** via the Jikan API.
    """)

    st.markdown("### Why are some anime missing or unavailable?")
    st.write("""
        AniRecci relies on the MyAnimeList API to fetch details about anime titles. If certain anime are missing, 
        it could be due to limitations in the API or the dataset being used. We're continuously updating the system 
        to include more titles.
    """)

    st.markdown("### How do you handle missing or incomplete data?")
    st.write("""
        If any data is missing (e.g., descriptions or genres), AniRecci fills those fields with default placeholders. 
        For example, missing descriptions are replaced with "No description available."
    """)

    st.header("4. Feedback and Support")
    st.markdown("### How can I provide feedback?")
    st.write("""
        After receiving recommendations, you can use the feedback dropdown to indicate whether you liked or disliked 
        the suggestions. This helps us improve the system for future users!
    """)

    st.markdown("### Can I report a bug or suggest a feature?")
    st.write("""
        Absolutely! If you encounter any issues or have ideas for new features, please reach out to us 
        via the feedback section or our support email at [support@anirecci.com](mailto:support@anirecci.com).
    """)

    st.header("5. Future Improvements")
    st.markdown("### Are there plans to improve AniRecci?")
    st.write("""
        Yes! We're constantly working to enhance AniRecci. Future plans include:
        - More advanced recommendation algorithms.
        - Support for multiple languages.
        - A mobile-friendly interface.
        - Personalized user profiles for even better suggestions.
    """)

    st.markdown("### Can I suggest new features?")
    st.write("""
        Of course! We're always open to suggestions. Let us know what features you'd like to see, 
        and we'll do our best to include them in future updates.
    """)

    st.markdown("---")
    st.write("""
        Still have questions? Feel free to contact us, and we'll be happy to help! 
        Thank you for using AniRecci 🌟.
    """)

# Call the FAQs page function
if __name__ == "__main__":
    faqs_page()
