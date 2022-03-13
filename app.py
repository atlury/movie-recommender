import requests
import streamlit as st
import pickle
import os
API_KEY=os.getenv('SECRET_KEY')
IMAGE_FULL_PATH = "https://image.tmdb.org/t/p/w500"
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}')
    data = response.json()
    return IMAGE_FULL_PATH+data['poster_path']

movies_df = pickle.load(open('models/movies.pkl','rb'))
similarity = pickle.load(open('models/similarity.pkl','rb'))
movies_titles = movies_df['title'].values

def recommend(movie):
    movie_index = movies_df[movies_df['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x : x[1])[1:6]
    recommended_movies = list() 
    posters = list()
    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movies.append(movies_df.iloc[i[0]].title) 
        posters.append(fetch_poster(movie_id)) 
    return recommended_movies,posters

st.title('Basic Movie Recommender System')
st.subheader("Recommends top 5 movies of similar content across 5000 movies")

option = st.selectbox('Movies',movies_titles)

if st.button('Recommend',key=option):
    if option is not None:
        names,posters = recommend(option)
        col1, col2, col3,col4,col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])

        with col2:
            st.text(names[1])
            st.image(posters[1])

        with col3:
            st.text(names[2])
            st.image(posters[2])

        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])