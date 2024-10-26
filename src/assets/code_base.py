import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

def get_anime_recommendations(filename, query_anime, k=10):
    """
    Get anime recommendations based on similar features using k-NN.
    
    Parameters:
    filename (str): Path to the CSV file containing anime data
    query_anime (str): Name of the anime to find recommendations for
    k (int): Number of recommendations to return (default: 10)
    
    Returns:
    list: List of recommended anime with their details
    """
    try:
        # Read the dataset
        df = pd.read_csv(filename)
        
        # Check if required columns exist
        required_features = ["Name", "Score", "Rank", "Popularity", "Members"]
        missing_columns = [col for col in required_features if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Prepare the feature matrix
        features = ["Score", "Rank", "Popularity", "Members"]
        X = df[features].astype(float)
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        # Normalize the features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Fit the k-NN model
        knn = NearestNeighbors(n_neighbors=k, metric='euclidean')
        knn.fit(X_scaled)
        
        # Find the index of the query anime
        if query_anime not in df['Name'].values:
            raise ValueError(f"Anime '{query_anime}' not found in the dataset.")
            
        query_index = df[df['Name'] == query_anime].index[0]
        
        # Find k-nearest neighbors
        distances, indices = knn.kneighbors([X_scaled[query_index]])
        
        # Prepare recommendations
        recommendations = []
        for i in range(k):
            idx = indices[0][i]
            anime_info = {
                'name': df.iloc[idx]['Name'],
                'score': df.iloc[idx]['Score'],
                'rank': df.iloc[idx]['Rank'],
                'popularity': df.iloc[idx]['Popularity'],
                'members': df.iloc[idx]['Members'],
                'distance': distances[0][i]
            }
            recommendations.append(anime_info)
        
        return recommendations
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    filename = "processed_anime_dataset.csv"
    query_anime = "Bouken Ou Beet"
    recommendations = get_anime_recommendations(filename, query_anime)
    
    if recommendations:
        print(f"\nSimilar anime to '{query_anime}':")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['name']}")
            print(f"   Score: {rec['score']:.2f}")
            print(f"   Rank: {rec['rank']}")
            print(f"   Popularity: {rec['popularity']}")
            print(f"   Members: {rec['members']}")
            print(f"   Similarity Distance: {rec['distance']:.4f}\n")