# AniRecci

## Overview

AniRecci is a web application built with Streamlit that allows users to input their favorite anime titles and receive recommendations for lesser-known anime based on content similarity. The application utilizes the Jikan API to fetch anime data and employs machine learning techniques for recommendation.

## Features

- Input your favorite anime titles.
- Fetches and processes anime data from the Jikan API.
- Provides recommendations for lesser-known anime based on the input titles.
- Displays recommendations in a user-friendly interface.

## Technologies Used

- **Streamlit**: For building the web application.
- **Pandas**: For data manipulation and analysis.
- **Requests**: For making API calls to the Jikan API.
- **Scikit-learn**: For machine learning and similarity calculations.
- **Papermill**: For parameterizing and executing Jupyter Notebooks.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- Pip (Python package installer)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/anime-recommendation-app.git
   cd anime-recommendation-app

2. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```
   The requirements.txt file should include the following dependencies:
   ```
   streamlit
   pandas
   requests
   scikit-learn
   papermill
   ```

3. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

## Data Source
The application uses the Jikan API to fetch anime data, which is a RESTful API for the MyAnimeList website.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## Acknowledgments
Jikan API for providing anime data.
Streamlit for making it easy to create web applications.
The open-source community for their contributions and support.
