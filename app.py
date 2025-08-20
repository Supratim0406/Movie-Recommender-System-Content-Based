# Author: Supratim Saha
# Email: supratimsaha.ds@gmail.com
# Date: 2025-Aug-10

import requests
import streamlit as st
import pickle
from PIL import Image
import base64

# Set page configuration
st.set_page_config(
    page_title="Movie Buddy - Your Personal Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
        color: #FF4B4B;
        text-align: center;
    }
    .subtitle {
        font-size:25px;
        color: #0483d7;
        text-align: center;
        margin-bottom: 30px;
    }
    .movie-title {
        font-size:16px;
        color: #0483d7;
        text-align: center;
        padding: 10px;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)


def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
            movie_id)
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except:
        return "https://path-to-your-default-image.jpg"  # Add a default image path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters


# Main UI
st.markdown('<p class="big-font">🎬 Movie Recommender</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your Personal Movie Recommender</p>', unsafe_allow_html=True)

# Load data
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

# Create three columns for layout
left_col, middle_col, right_col = st.columns([1, 2, 1])

with middle_col:
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "🔍 Search for a movie you like",
        movie_list
    )

    if st.button('🎯 Get Recommendations'):
        with st.spinner('Finding movies you might like...'):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

            st.markdown("### 🌟 Based on your selection, you might like:")

            # Create five columns for movies
            cols = st.columns(5)
            for idx, (col, name, poster) in enumerate(zip(cols, recommended_movie_names, recommended_movie_posters)):
                with col:
                    # Changed use_column_width to use_container_width
                    st.image(poster, use_container_width=True)
                    st.markdown(f'<p class="movie-title">{name}</p>', unsafe_allow_html=True)

                    # Add rating or additional info if available
                    st.markdown(f"""
                        <div style='text-align: center'>
                            ⭐ {round(float(similarity[movies[movies['title'] == name].index[0]][0]), 2)}
                        </div>
                    """, unsafe_allow_html=True)

# Footer
st.markdown("""---""")
st.markdown("""
<div style='text-align: center'>
    <p>Created with ❤️ by Supratim Saha</p>
    <p>Data source: TMDb API</p>
</div>
""", unsafe_allow_html=True)
