import streamlit as st
import pickle
import pandas as pd
import requests


def fetch(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=bc967c1024499a8bad280a219b251f01&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_poster.append(fetch(movie_id))
    return recommended_movies, recommended_poster


st.markdown("""
    <style>
    body {
        background-color: #e0f7fa;  /* Light cyan background color */
    }
    .main {
        background-color: #ffffff;  /* White background for the main container */
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        padding: 2rem;
    }
    h1 {
        color: #00796b;  /* Darker teal color for title */
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #00796b;  /* Teal color for buttons */
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        font-family: 'Arial', sans-serif;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #004d40;  /* Darker teal color on hover */
    }
    .stSelectbox>div {
        font-family: 'Arial', sans-serif;
    }
    .stText {
        color: #004d40;  /* Darker teal color for text */
        font-family: 'Arial', sans-serif;
    }
    .block-container {
        padding: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


movies_list = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

option = st.selectbox(
    'Select a movie',
movies['title'].values)

if st.button('Recommend'):
    name, poster = recommend(option)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(poster[0])

    with col2:
        st.text(name[1])
        st.image(poster[1])
    
    with col3:
        st.text(name[2])
        st.image(poster[2])

    with col4:
        st.text(name[3])
        st.image(poster[3])

    with col5:
        st.text(name[4])
        st.image(poster[4])
    