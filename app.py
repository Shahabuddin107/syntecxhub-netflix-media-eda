import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Netflix Catalog EDA", layout="wide", page_icon="🎬")

# Title & Description
st.title("🎬 Netflix Catalog Interactive EDA Dashboard")
st.markdown("Exploratory Data Analysis covering catalog growth, genre distributions, and durations.")

@st.cache_data
def load_data():
    df = pd.read_csv('netflix_titles.csv')
    df['date_added'] = pd.to_datetime(df['date_added'].astype(str).str.strip(), errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['duration_num'] = df['duration'].astype(str).str.extract(r'(\d+)').astype(float)
    return df

df = load_data()

# ----------------- SIDEBAR FILTERS -----------------
st.sidebar.header("🔍 Filter Options")
types = st.sidebar.multiselect("Select Content Type:", ['Movie', 'TV Show'], default=['Movie', 'TV Show'])

min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
year_range = st.sidebar.slider("Release Year Range:", min_year, max_year, (min_year, max_year))

# Filter data
filtered_df = df[
    (df['type'].isin(types)) & 
    (df['release_year'] >= year_range[0]) & 
    (df['release_year'] <= year_range[1])
]

# ----------------- KEY METRICS -----------------
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Titles", f"{len(filtered_df):,}")
m2.metric("Movies", f"{len(filtered_df[filtered_df['type']=='Movie']):,}")
m3.metric("TV Shows", f"{len(filtered_df[filtered_df['type']=='TV Show']):,}")
median_movie = filtered_df[filtered_df['type']=='Movie']['duration_num'].median()
m4.metric("Avg Movie Duration", f"{median_movie:.0f} min" if not pd.isna(median_movie) else "N/A")

st.divider()

# ----------------- CHARTS ROW 1 -----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Top 10 Genres")
    top_genres = filtered_df['listed_in'].dropna().str.split(', ').explode().value_counts().head(10)
    fig1, ax1 = plt.subplots(figsize=(8, 4.5))
    sns.barplot(x=top_genres.values, y=top_genres.index, hue=top_genres.index, palette='Reds_r', legend=False, ax=ax1)
    ax1.set_xlabel("Count", fontweight='bold')
    st.pyplot(fig1)

with col2:
    st.subheader("📈 Content Growth Over Time")
    growth = filtered_df.groupby(['year_added', 'type']).size().unstack(fill_value=0)
    fig2, ax2 = plt.subplots(figsize=(8, 4.5))
    if 'Movie' in growth.columns:
        ax2.plot(growth.index, growth['Movie'], marker='o', color='#E50914', label='Movies', linewidth=2)
    if 'TV Show' in growth.columns:
        ax2.plot(growth.index, growth['TV Show'], marker='s', color='#221F1F', label='TV Shows', linewidth=2)
    ax2.set_xlabel("Year Added", fontweight='bold')
    ax2.set_ylabel("Titles Added", fontweight='bold')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig2)

# ----------------- CHARTS ROW 2 -----------------
st.subheader("⏱️ Runtime Distributions")
r1, r2 = st.columns(2)

with r1:
    movies_data = filtered_df[filtered_df['type'] == 'Movie']['duration_num'].dropna()
    fig3, ax3 = plt.subplots(figsize=(8, 3.5))
    sns.histplot(movies_data, kde=True, color='#E50914', bins=20, ax=ax3)
    ax3.set_title("Movie Durations (Minutes)", fontweight='bold')
    ax3.set_xlabel("Minutes")
    st.pyplot(fig3)

with r2:
    tv_data = filtered_df[filtered_df['type'] == 'TV Show']['duration_num'].value_counts().head(5)
    fig4, ax4 = plt.subplots(figsize=(8, 3.5))
    sns.barplot(x=tv_data.index.astype(int), y=tv_data.values, color='#221F1F', ax=ax4)
    ax4.set_title("TV Show Durations (Seasons)", fontweight='bold')
    ax4.set_xlabel("Seasons")
    st.pyplot(fig4)

# ----------------- DOWNLOAD REPORT SECTION -----------------
st.divider()
st.subheader("📄 Export Visual PDF Report")
if os.path.exists("netflix_final_report.pdf"):
    with open("netflix_final_report.pdf", "rb") as pdf_file:
        st.download_button(
            label="📥 Download Complete PDF Report",
            data=pdf_file,
            file_name="netflix_eda_report.pdf",
            mime="application/pdf"
        )
else:
    st.info("Run `python main.py` once to generate the PDF export.")