# 🎬 Netflix Media Content EDA & Visual Report Generator

An automated Exploratory Data Analysis (EDA) pipeline that analyzes catalog trends, genre representations, and content runtimes, exporting an executive-ready multi-page PDF report.

## 🚀 Features
- **Format Breakdown:** Compares distribution between standalone features (Movies) and episodic series (TV Shows).
- **Time Trend Analysis:** Evaluates content addition velocity and historical production release distribution.
- **Genre Clustering:** Extracts and ranks top multi-label genres.
- **Runtime Profiling:** Visualizes movie runtimes (minutes) vs TV show seasons.
- **Automated PDF Export:** Generates high-res vector/image PDF reports via `fpdf2`.

## 🛠️ Tech Stack
- **Python 3.10+**
- **Pandas & NumPy** (Data processing & extraction)
- **Matplotlib & Seaborn** (Data visualization)
- **FPDF2** (Automated PDF reporting)

## 📦 How to Run
1. Clone the repository and navigate to the directory:
   ```bash
   git clone <your-repo-link>
   cd netflix-eda-project