import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';

const AnimeRecommender = () => {
    const [selectedAnime, setSelectedAnime] = useState('');
    const [recommendations, setRecommendations] = useState([]);
    const [data, setData] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    const features = ['Score', 'Rank', 'Popularity', 'Members'];

    const normalizeData = (data, features) => {
        const normalizedData = [...data];

        features.forEach(feature => {
            const values = data.map(item => parseFloat(item[feature]));
            const min = Math.min(...values);
            const max = Math.max(...values);

            normalizedData.forEach(item => {
                item[`normalized_${feature}`] = (parseFloat(item[feature]) - min) / (max - min);
            });
        });

        return normalizedData;
    };

    const findSimilarAnime = (targetAnime, data, features) => {
        const normalizedFeatures = features.map(f => `normalized_${f}`);

        return data
            .filter(anime => anime.Name !== targetAnime.Name)
            .map(anime => {
                const distance = Math.sqrt(
                    normalizedFeatures.reduce((sum, feature) => {
                        const diff = targetAnime[feature] - anime[feature];
                        return sum + diff * diff;
                    }, 0)
                );
                return { ...anime, distance };
            })
            .sort((a, b) => a.distance - b.distance)
            .slice(0, 5);
    };

    useEffect(() => {
        const loadData = async () => {
            setIsLoading(true);
            try {
                const response = await fetch('/assets/processed_anime_dataset.csv');
                const text = await response.text();

                Papa.parse(text, {
                    header: true,
                    complete: (results) => {
                        const cleanData = results.data.filter(row =>
                            row.Name &&
                            !isNaN(row.Score) &&
                            !isNaN(row.Rank) &&
                            !isNaN(row.Popularity) &&
                            !isNaN(row.Members)
                        );
                        const normalizedData = normalizeData(cleanData, features);
                        setData(normalizedData);
                        setIsLoading(false);
                    },
                    error: (error) => {
                        console.error('Error parsing CSV:', error);
                        setIsLoading(false);
                    }
                });
            } catch (error) {
                console.error('Error loading CSV:', error);
                setIsLoading(false);
            }
        };

        loadData();
    }, []);

    const handleAnimeSelect = (animeName) => {
        setSelectedAnime(animeName);
        const targetAnime = data.find(anime => anime.Name === animeName);
        if (targetAnime) {
            const similar = findSimilarAnime(targetAnime, data, features);
            setRecommendations(similar);
        }
    };

    return (
        <div className="p-4 max-w-4xl mx-auto">
            <div className="bg-white shadow rounded-lg p-6 mb-6">
                <h1 className="text-2xl font-bold mb-6">Anime Recommendation System</h1>

                {isLoading ? (
                    <div className="text-center py-4">
                        <p>Loading anime data...</p>
                    </div>
                ) : (
                    <>
                        <div className="mb-4">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Select an Anime
                            </label>
                            <select
                                value={selectedAnime}
                                onChange={(e) => handleAnimeSelect(e.target.value)}
                                className="w-full p-2 border rounded-md"
                            >
                                <option value="">Choose an anime...</option>
                                {data.map((anime, index) => (
                                    <option key={index} value={anime.Name}>
                                        {anime.Name}
                                    </option>
                                ))}
                            </select>
                        </div>

                        {selectedAnime && (
                            <div className="mt-6">
                                <h3 className="text-lg font-semibold mb-4">Recommendations for {selectedAnime}</h3>
                                <div className="space-y-4">
                                    {recommendations.map((anime, index) => (
                                        <div
                                            key={index}
                                            className="bg-white border rounded-lg p-4 hover:bg-gray-50 transition-colors"
                                        >
                                            <img
                                                src={anime['Image URL']}
                                                alt={anime.Name}
                                                className="w-24 h-36 object-cover mr-4 rounded-lg"
                                            />
                                            <div className="flex justify-between items-start">
                                                <div className="flex-grow">
                                                    <h4 className="font-semibold text-lg text-blue-600">{anime.Name}</h4>
                                                    <div className="mt-2 grid grid-cols-2 gap-2">
                                                        <div className="text-sm"><strong>English
                                                            Name:</strong> {anime['English name']}</div>
                                                        <div className="text-sm"><strong>Other
                                                            Name:</strong> {anime['Other name']}</div>
                                                        <div className="text-sm">
                                                            <strong>Score:</strong> {parseFloat(anime.Score).toFixed(2)}
                                                        </div>
                                                        <div className="text-sm"><strong>Rank:</strong> #{anime.Rank}
                                                        </div>
                                                        <div className="text-sm">
                                                            <strong>Popularity:</strong> #{anime.Popularity}</div>
                                                        <div className="text-sm">
                                                            <strong>Members:</strong> {parseInt(anime.Members).toLocaleString()}
                                                        </div>
                                                        <div className="text-sm"><strong>Genres:</strong> {anime.Genres}
                                                        </div>
                                                        <div className="text-sm">
                                                            <strong>Synopsis:</strong> {anime.Synopsis}</div>
                                                        <div className="text-sm"><strong>Type:</strong> {anime.Type}
                                                        </div>
                                                        <div className="text-sm">
                                                            <strong>Episodes:</strong> {anime.Episodes}</div>
                                                        <div className="text-sm"><strong>Aired:</strong> {anime.Aired}
                                                        </div>
                                                        <div className="text-sm">
                                                            <strong>Studios:</strong> {anime.Studios}</div>
                                                        <div className="text-sm"><strong>Source:</strong> {anime.Source}
                                                        </div>
                                                        <div className="text-sm">
                                                            <strong>Duration:</strong> {anime.Duration}</div>
                                                        <div className="text-sm"><strong>Rating:</strong> {anime.Rating}
                                                        </div>
                                                    </div>
                                                </div>
                                                <div className="ml-4">
                                                    <span
                                                        className="inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                                                        {((1 - anime.distance) * 100).toFixed(1)}% Match
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
};

export default AnimeRecommender;
