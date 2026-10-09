import numpy as np
import pandas as pd

np.random.seed(42)
n = 8000

types = np.random.choice(['Movie', 'TV Show'], size=n, p=[0.7, 0.3])
years = np.random.choice(range(2010, 2022), size=n)
added_years = np.random.choice(range(2015, 2022), size=n)

movie_genres = ['Dramas', 'Comedies', 'Action & Adventure', 'Documentaries', 'International Movies']
tv_genres = ['TV Dramas', 'TV Comedies', 'Crime TV Shows', 'Kids\' TV', 'International TV Shows']

genres = [
    np.random.choice(movie_genres) if t == 'Movie' else np.random.choice(tv_genres)
    for t in types
]

durations = [
    f"{np.random.randint(60, 160)} min" if t == 'Movie' else f"{np.random.choice([1, 2, 3])} Season"
    for t in types
]

dates = [f"September {np.random.randint(1, 28)}, {y}" for y in added_years]

df = pd.DataFrame({
    'show_id': [f"s{i+1}" for i in range(n)],
    'type': types,
    'title': [f"Sample Title {i+1}" for i in range(n)],
    'date_added': dates,
    'release_year': years,
    'duration': durations,
    'listed_in': genres
})

df.to_csv('netflix_titles.csv', index=False)
print("Success: 'netflix_titles.csv' generate ho gayi hai!")