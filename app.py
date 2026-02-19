import pickle
import streamlit as st
import requests
import io

# ---------------- Google Drive links ----------------
MOVIE_LIST_URL = "https://drive.google.com/uc?export=download&id=1SCLlIPw5Pf0QZg4Am5riKd5wCk5dVThu"
SIMILARITY_URL = "https://drive.google.com/uc?export=download&id=1m5m2SD3tKa1tta2tUSvqzf5bBOA_qoPA"

# ---------------- Load .pkl from URL ----------------
@st.cache_data
def load_pickle_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return pickle.load(io.BytesIO(response.content))

movies = load_pickle_from_url(MOVIE_LIST_URL)
similarity = load_pickle_from_url(SIMILARITY_URL)

# ---------------- TMDB poster fetch ----------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/200x300?text=No+Image"

# ---------------- Recommendation ----------------
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

# ---------------- Streamlit UI ----------------
st.header('Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx])
