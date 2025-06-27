# 🎬 Movie Recommendation System

A visually rich and interactive **Movie Recommender Web App** built with **Streamlit** and **Python**, using content-based filtering and OMDb API integration for live movie data like posters, ratings, year, etc.

---

## 🔧 Features

- 🔍 **Searchable dropdown** to pick your favorite movie  
- 🤖 **Top 5 movie recommendations** based on similarity  
- 🖼️ **Live posters, cast, director, rating, and release year** via [OMDb API](https://www.omdbapi.com)  
- 🎨 Fully customized dark-themed UI with hover animations  
- 🧠 Uses a **precomputed similarity matrix** for fast results

---

## Set Up Virtual Environment (Optional but Recommended)
python -m venv venv
venv\Scripts\activate  # On Windows

## Install Dependencies
pip install -r requirements.txt

## Run the APP
streamlit run app.py

⚠️ Notes
.pkl files like similarity.pkl are large and not tracked in GitHub due to size limits.
Keep them stored locally or load from external storage if needed.

You’ll need a valid OMDb API Key to fetch movie posters and info. One is already included for demo use.
