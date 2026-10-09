import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
from fpdf.enums import XPos, YPos

print("1. Loading dataset...")
if not os.path.exists('netflix_titles.csv'):
    print("Error: 'netflix_titles.csv' file nahi mili! File ko usi folder me rakhein.")
    exit()

df = pd.read_csv('netflix_titles.csv')

print("2. Cleaning data...")
df['date_added'] = pd.to_datetime(df['date_added'].astype(str).str.strip(), errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['duration_num'] = df['duration'].astype(str).str.extract(r'(\d+)').astype(float)

movies = df[df['type'] == 'Movie'].copy()
tv_shows = df[df['type'] == 'TV Show'].copy()

# Calculations
type_counts = df['type'].value_counts()
top_10_genres = df['listed_in'].dropna().str.split(', ').explode().value_counts().head(10)
top_10_years = df['release_year'].value_counts().head(10)

print("3. Generating charts...")
# Chart 1: Growth Trend
plt.figure(figsize=(8, 4))
growth = df.groupby(['year_added', 'type']).size().unstack(fill_value=0)
if 'Movie' in growth.columns:
    plt.plot(growth.index, growth['Movie'], marker='o', color='#E50914', label='Movies', linewidth=2)
if 'TV Show' in growth.columns:
    plt.plot(growth.index, growth['TV Show'], marker='s', color='#221F1F', label='TV Shows', linewidth=2)
plt.title('Content Growth Over Time', fontweight='bold')
plt.xlabel('Year Added')
plt.ylabel('Count')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('growth_chart.png', dpi=150)
plt.close()

# Chart 2: Top 10 Genres
plt.figure(figsize=(8, 4))
sns.barplot(x=top_10_genres.values, y=top_10_genres.index, hue=top_10_genres.index, palette='Reds_r', legend=False)
plt.title('Top 10 Genres', fontweight='bold')
plt.xlabel('Titles Count')
plt.tight_layout()
plt.savefig('genres_chart.png', dpi=150)
plt.close()

# Chart 3: Runtime Distribution
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
sns.histplot(movies['duration_num'].dropna(), kde=True, ax=axes[0], color='#E50914', bins=20)
axes[0].set_title('Movie Durations (Minutes)', fontweight='bold')

tv_seasons = tv_shows['duration_num'].value_counts().head(5)
sns.barplot(x=tv_seasons.index.astype(int), y=tv_seasons.values, ax=axes[1], color='#221F1F')
axes[1].set_title('TV Show Durations (Seasons)', fontweight='bold')
plt.tight_layout()
plt.savefig('runtime_chart.png', dpi=150)
plt.close()

print("4. Building PDF report...")
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Page 1: Overview & Growth
pdf.add_page()
pdf.set_font('helvetica', 'B', 18)
pdf.set_text_color(229, 9, 20)
pdf.cell(0, 10, 'NETFLIX CATALOG EDA REPORT', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

pdf.set_font('helvetica', '', 11)
pdf.set_text_color(50, 50, 50)
pdf.cell(0, 8, f"Total Titles: {len(df):,} | Movies: {len(movies):,} | TV Shows: {len(tv_shows):,}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
pdf.ln(5)

pdf.set_font('helvetica', 'B', 12)
pdf.cell(0, 8, '1. Catalog Growth Over Time', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.image('growth_chart.png', x=15, y=pdf.get_y(), w=180)
pdf.ln(95)

pdf.cell(0, 8, '2. Top 10 Content Genres', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.image('genres_chart.png', x=15, y=pdf.get_y(), w=180)

# Page 2: Runtime & Tables
pdf.add_page()
pdf.set_font('helvetica', 'B', 12)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 8, '3. Runtime Distributions', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.image('runtime_chart.png', x=15, y=pdf.get_y(), w=180)
pdf.ln(85)

pdf.cell(0, 8, '4. Top 5 Genres & Production Years Summary', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('helvetica', '', 10)
for i in range(min(5, len(top_10_genres))):
    genre_name = top_10_genres.index[i]
    genre_cnt = top_10_genres.values[i]
    year_val = top_10_years.index[i]
    year_cnt = top_10_years.values[i]
    pdf.cell(0, 6, f"{i+1}. Genre: {genre_name} ({genre_cnt:,}) | Year: {year_val} ({year_cnt:,} titles)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.output('netflix_final_report.pdf')
print("\nSuccess! Report ban gayi: 'netflix_final_report.pdf'")