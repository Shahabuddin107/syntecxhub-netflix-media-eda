import base64
import os
import webbrowser
import pandas as pd

df = pd.read_csv('netflix_titles.csv')
movies_cnt = len(df[df['type'] == 'Movie'])
tv_cnt = len(df[df['type'] == 'TV Show'])

def get_base64_img(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

g_b64 = get_base64_img("growth_chart.png")
j_b64 = get_base64_img("genres_chart.png")
r_b64 = get_base64_img("runtime_chart.png")

html = f"""
<!DOCTYPE html>
<html>
<head>
  <title>Netflix Catalog EDA Dashboard</title>
  <style>
    body {{ background-color: #141414; color: #fff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 30px; }}
    h1 {{ color: #E50914; margin: 0 0 10px 0; font-size: 28px; }}
    .subtitle {{ color: #aaa; margin-bottom: 25px; }}
    .cards {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }}
    .card {{ background: #1f1f1f; padding: 20px; border-radius: 8px; border-left: 4px solid #E50914; text-align: center; }}
    .card h2 {{ font-size: 30px; margin: 0; }}
    .card p {{ color: #888; text-transform: uppercase; font-size: 12px; margin: 5px 0 0; }}
    .chart-box {{ background: #1f1f1f; padding: 20px; border-radius: 8px; margin-bottom: 25px; text-align: center; }}
    .chart-box h3 {{ text-align: left; color: #E50914; margin: 0 0 15px; font-size: 16px; }}
    .chart-box img {{ max-width: 100%; border-radius: 6px; }}
  </style>
</head>
<body>
  <h1>Netflix Catalog EDA Dashboard</h1>
  <div class="subtitle">Exploratory Data Analysis • Trends, Formats & Content Distribution</div>
  <div class="cards">
    <div class="card"><h2>{len(df):,}</h2><p>Total Titles</p></div>
    <div class="card"><h2>{movies_cnt:,}</h2><p>Movies ({(movies_cnt/len(df))*100:.1f}%)</p></div>
    <div class="card"><h2>{tv_cnt:,}</h2><p>TV Shows ({(tv_cnt/len(df))*100:.1f}%)</p></div>
  </div>
  <div class="chart-box">
    <h3>1. Content Growth Trajectory</h3>
    <img src="data:image/png;base64,{g_b64}" />
  </div>
  <div class="chart-box">
    <h3>2. Top Content Genres</h3>
    <img src="data:image/png;base64,{j_b64}" />
  </div>
  <div class="chart-box">
    <h3>3. Runtime Distributions</h3>
    <img src="data:image/png;base64,{r_b64}" />
  </div>
</body>
</html>
"""

with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Opening dashboard in browser...")
webbrowser.open("dashboard.html")