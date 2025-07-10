import sqlite3
import pandas as pd
from datetime import datetime

DATABASE_PATH = "C:/Users/thisr/source/repos/CISTAC2/CistacApp/CistacApp.db"

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# Reviews tablosundan verileri al
df = pd.read_sql_query("SELECT UserID, RoomID, Rating FROM Reviews", conn)

# Pivot: user x room matrix
ratings_matrix = df.pivot_table(index="UserID", columns="RoomID", values="Rating")

# Kullanıcı benzerliklerini hesapla (Pearson)
user_similarity = ratings_matrix.T.corr()

def recommend_rooms(user_id, top_n=10):
    if user_id not in ratings_matrix.index:
        return []

    user_ratings = ratings_matrix.loc[user_id]
    similar_users = user_similarity[user_id].drop(user_id).dropna()
    similar_users = similar_users[similar_users > 0]

    scores, sim_sums = {}, {}
    for other_user, similarity in similar_users.items():
        for room_id, rating in ratings_matrix.loc[other_user].dropna().items():
            if pd.isna(user_ratings.get(room_id)):
                scores[room_id] = scores.get(room_id, 0) + rating * similarity
                sim_sums[room_id] = sim_sums.get(room_id, 0) + similarity

    predicted_scores = {
        room_id: scores[room_id] / sim_sums[room_id]
        for room_id in scores if sim_sums[room_id] != 0
    }

    return sorted(predicted_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

# Mevcut önerileri temizle
cursor.execute("DELETE FROM Recommendations")

# Her kullanıcı için önerileri hesapla ve Recommendations tablosuna yaz
for user_id in df['UserID'].unique():
    recommendations = recommend_rooms(user_id, top_n=10)
    for room_id, score in recommendations:
        if score >= 4.0:  # Sadece 4.0 ve üstü önerileri kaydet
            cursor.execute(
                "INSERT INTO Recommendations (user_id, recommended_room_id, predicted_score, Created_At) VALUES (?, ?, ?, ?)",
                (int(user_id), int(room_id), float(score), datetime.now().isoformat())
            )

conn.commit()
conn.close()

print("✔ Recommendations başarıyla güncellendi.")
