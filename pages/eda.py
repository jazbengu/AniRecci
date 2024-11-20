import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ast
from sklearn.preprocessing import MultiLabelBinarizer

# Title of the app
st.title("Deep Exploratory Data Analysis")

# Upload CSV file
uploaded_file = "raw_anime_data_paged.csv"

if uploaded_file is not None:
    # Read the data
    data = pd.read_csv(uploaded_file)
    for_Hm = data

    # Display the first few rows of the dataframe
    st.subheader("Data Preview")
    st.write(data.head())

    # Show basic statistics
    st.subheader("Basic Statistics")
    st.write(data.describe())

    # Show data types
    st.subheader("Data Types")
    st.write(data.dtypes)

    # Check for missing values
    st.subheader("Missing Values")
    st.write(data.isnull().sum())

    # Visualizations
    st.subheader("Visualizations")

    # Histogram
    if st.checkbox("Show Histogram"):
        column = st.selectbox("Select column for histogram", data.columns)
        fig, ax = plt.subplots()
        sns.histplot(data[column], ax=ax)
        st.pyplot(fig)

    # Correlation heatmap
    if st.checkbox("Show Correlation Heatmap"):
        for_Hm['genres'] = for_Hm['genres'].apply(ast.literal_eval)
        mlb = MultiLabelBinarizer()
        genres_encoded = pd.DataFrame(mlb.fit_transform(for_Hm['genres']), 
                                    columns=mlb.classes_, 
                                    index=for_Hm.index)
        for_Hm['rating'].fillna(for_Hm['rating'].median(), inplace=True)

        anime_features = pd.concat([genres_encoded, for_Hm[['popularity', 'rating']]], axis=1)

        correlation_matrix = anime_features.corr()
        plt.figure(figsize=(16, 12))

        # Plotting the heatmap
        sns.heatmap(correlation_matrix, annot=False, cmap="coolwarm", fmt=".2f", cbar=True)

        # Adding titles and labels
        plt.title("Heatmap of Anime Features (Genres, Popularity, and Ratings)", fontsize=16)
        plt.show(fig)

    # Pairplot
    if st.checkbox("Show Pairplot"):
        fig = sns.pairplot(data)
        st.pyplot(fig)

# Categorical plots
    if st.checkbox("Show Categorical Plot"):
        categorical_column = st.selectbox("Select categorical column", data.select_dtypes(include=['object']).columns)
        numerical_column = st.selectbox("Select numerical column", data.select_dtypes(include=['float64', 'int64']).columns)
        fig, ax = plt.subplots()
        sns.boxplot(x=categorical_column, y=numerical_column, data=data, ax=ax)
        st.pyplot(fig)

    # Distribution plot
    if st.checkbox("Show Distribution Plot"):
        column = st.selectbox("Select column for distribution plot", data.columns)
        fig, ax = plt.subplots()
        sns.kdeplot(data[column], ax=ax, fill=True)
        st.pyplot(fig)

    # Count plot for categorical data
    if st.checkbox("Show Count Plot"):
        categorical_column = st.selectbox("Select categorical column for count plot", data.select_dtypes(include=['object']).columns)
        fig, ax = plt.subplots()
        sns.countplot(x=categorical_column, data=data, ax=ax)
        st.pyplot(fig)

    # Add more analyses as needed
    if st.checkbox("Show Data Distribution"):
        st.subheader("Data Distribution")
        for column in data.select_dtypes(include=['float64', 'int64']).columns:
            st.write(f"Distribution for {column}")
            fig, ax = plt.subplots()
            sns.histplot(data[column], bins=30, kde=True, ax=ax)
            st.pyplot(fig)