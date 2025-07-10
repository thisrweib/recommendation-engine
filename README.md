🧠 Recommendation Engine Overview
* This project implements a User-Based Collaborative Filtering recommendation system.
* It analyzes users’ past rating behavior to recommend rooms favored by other users with similar preferences.

⚙️ Technologies & Methods Used
* SQLite – A lightweight, local relational database used for storing user reviews and recommendation results.
* pandas (Python) – Used for data processing, building the user–item rating matrix, and performing matrix operations efficiently.
* Pearson Correlation – Measures the similarity between users based on their rating patterns, compensating for individual rating biases.

🔍 How It Works
* Calculates user-to-user similarity using Pearson correlation on a user–room rating matrix.
* For each user, finds other users with similar preferences and selects rooms that those similar users rated highly.
* Each recommended room receives a predicted score, calculated as a weighted average based on similarity strength and rating values.
* Filters recommendations: only rooms with a predicted score ≥ 4.0 are stored.
* Stores final results in a separate Recommendations table in the SQLite database.
* The script runs in batch mode, generating updated recommendations for all users at once.

▶️ How to Run the Code
To generate fresh recommendations and populate the `Recommendations` table, simply execute the Python script from your terminal or IDE:

```bash
python recommendation_generator.py
```

Ensure that:
- Python is installed on your system
- The `pandas` library is available (`pip install pandas` if not)
- The database path in the script (`DATABASE_PATH`) points to your actual SQLite file
- The `Reviews` table contains meaningful rating data
After successful execution, the `Recommendations` table will be updated with the latest predicted suggestions.
