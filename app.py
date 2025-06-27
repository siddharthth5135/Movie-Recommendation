import streamlit as st
import pickle
import pandas as pd
import requests

# --- Apply Custom CSS ---
st.markdown("""
    <style>
    body {
        background-color: #1e1e1e;
        color: white;
        font-family: 'Arial', sans-serif;
    }
    .title {
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        color: #EB566C;
        text-shadow: 3px 3px 8px rgba(0,0,0,0.5);
        margin-top: 40px;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 1.5em;
        font-weight: 500;
        text-align: center;
        color: #EB566C;
    }
    .movie-card {
        padding: 15px;
        border-radius: 20px;
        background-color: #2a2a2a;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
        height: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .movie-card:hover {
        transform: scale(1.05);
        box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.7);
    }
    .movie-poster {
        border-radius: 15px;
        width: 100%;
        height: auto;
        max-height: 400px;
        object-fit: cover;
    }
    .movie-title {
        color: #EB566C;
        font-size: 1.2em;
        font-weight: 600;
        margin-top: 10px;
    }
    .movie-info {
        font-size: 1em;
        color: #cccccc;
    }
    .movie-info strong {
        color: #EB566C;
    }
    .selectbox, .search-bar, .button {
        margin-top: 20px;
        width: 100%;
        font-size: 1.1em;
        padding: 10px;
        border-radius: 10px;
        background-color: #333;
        color: #fff;
        border: none;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .selectbox:hover, .search-bar:hover, .button:hover {
        background-color: #EB566C;
        cursor: pointer;
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.5);
    }
    .selectbox:focus, .search-bar:focus {
        outline: none;
        border: 2px solid #EB566C;
    }
    </style>
""", unsafe_allow_html=True)

# --- OMDb Fetch ---
def fetch_movie_details(title):
    try:
        url = f"http://www.omdbapi.com/?t={title}&apikey=3a810a39"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            "poster": data.get("Poster") if data.get("Poster") != "N/A" else "https://via.placeholder.com/300x450?text=No+Poster",
            "year": data.get("Year", "N/A"),
            "rating": data.get("imdbRating", "N/A"),
        }
    except:
        return {
            "poster": "https://via.placeholder.com/300x450?text=Error",
            "year": "N/A",
            "rating": "N/A"
        }

# --- Recommend Logic ---
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    results = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        cast = movies.iloc[i[0]].cast
        director = movies.iloc[i[0]].crew
        details = fetch_movie_details(title)

        results.append({
            "title": title,
            "cast": cast,
            "director": director,
            "poster": details["poster"],
            "year": details["year"],
            "rating": details["rating"]
        })

    return results

# --- Load Data ---
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Streamlit UI ---
st.markdown('<div class="title">🎬 Ultimate Movie Recommender</div>', unsafe_allow_html=True)

# Subtitle for better UI
st.markdown('<div class="subtitle">Find your next favorite movie!</div>', unsafe_allow_html=True)

st.markdown("### 📽️ Select a movie you like:")

# Search bar and select box with better styling
selected_movie_name = st.selectbox('', movies['title'].values, key="select_movie", index=0, help="Search for your favorite movie", format_func=lambda x: f"{x}")
st.markdown('<br>', unsafe_allow_html=True)

# Add recommend button with enhanced style
if st.button('🎯 Recommend', key="recommend", help="Get recommendations based on your movie choice"):
    results = recommend(selected_movie_name)

    st.markdown("## 🔍 Your Top 5 Recommendations:")

    for i in range(0, len(results), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(results):
                movie = results[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="movie-card">
                            <img src="{movie['poster']}" class="movie-poster"/>
                            <h4 class="movie-title">{movie['title']}</h4>
                            <p class="movie-info">🎬 <strong>Director:</strong> {movie['director']}</p>
                            <p class="movie-info">👥 <strong>Cast:</strong> {movie['cast']}</p>
                            <p class="movie-info">⭐ <strong>Rating:</strong> {movie['rating']} / 10</p>
                            <p class="movie-info">📅 <strong>Year:</strong> {movie['year']}</p>
                        </div>
                    """, unsafe_allow_html=True)
