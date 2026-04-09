from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Recommends top k songs for a user.
        Returns list of Song objects sorted by score (best first).
        """
        if not self.songs:
            return []
        
        # Score all songs
        scored_songs = []
        for song in self.songs:
            score = self._score_song_oop(user, song)
            scored_songs.append((song, score))
        
        # Sort by score (highest first) and return top k
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return [song for song, score in scored_songs[:k]]
    
    def _score_song_oop(self, user: UserProfile, song: Song) -> float:
        """
        Scores a single song against user profile (OOP version).
        Returns numeric score only.
        """
        score = 0.0
        
        # Weights
        w_genre = 3.0
        w_mood = 2.0
        w_energy = 1.5
        w_acoustic = 0.5
        
        # Genre match
        genre_score = 1.0 if song.genre.lower() == user.favorite_genre.lower() else 0.5
        score += w_genre * genre_score
        
        # Mood match
        mood_score = 1.0 if song.mood.lower() == user.favorite_mood.lower() else 0.0
        score += w_mood * mood_score
        
        # Energy similarity
        energy_similarity = 1.0 - abs(user.target_energy - song.energy)
        score += w_energy * energy_similarity
        
        # Acoustic preference
        acoustic_score = song.acousticness if user.likes_acoustic else (1.0 - song.acousticness)
        score += w_acoustic * acoustic_score
        
        return score

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Generates an explanation for why a song was recommended.
        Returns a readable explanation string.
        """
        explanations = []
        
        # Genre match
        if song.genre.lower() == user.favorite_genre.lower():
            explanations.append(f"✓ Genre matches: {song.genre}")
        else:
            explanations.append(f"~ Genre: {song.genre} (you prefer {user.favorite_genre})")
        
        # Mood match
        if song.mood.lower() == user.favorite_mood.lower():
            explanations.append(f"✓ Mood matches: {song.mood}")
        else:
            explanations.append(f"~ Mood: {song.mood} (you prefer {user.favorite_mood})")
        
        # Energy
        energy_diff = abs(user.target_energy - song.energy)
        if energy_diff < 0.2:
            explanations.append(f"✓ Energy matches: {song.energy:.2f}")
        else:
            explanations.append(f"~ Energy: {song.energy:.2f} (you prefer {user.target_energy:.2f})")
        
        # Acoustic
        if user.likes_acoustic:
            if song.acousticness > 0.7:
                explanations.append(f"✓ Acoustic sound: {song.acousticness:.2f}")
            else:
                explanations.append(f"~ Less acoustic than preferred: {song.acousticness:.2f}")
        else:
            if song.acousticness < 0.3:
                explanations.append(f"✓ Electronic sound: {song.acousticness:.2f}")
            else:
                explanations.append(f"~ More acoustic than preferred: {song.acousticness:.2f}")
        
        return " | ".join(explanations)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and converts numerical values to floats/ints.
    Returns a list of dictionaries representing songs.
    """
    songs = []
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numerical columns to appropriate types
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': int(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness']),
                }
                songs.append(song)
    except FileNotFoundError:
        print(f"Error: Could not find {csv_path}")
        return []
    
    print(f"✓ Loaded {len(songs)} songs from {csv_path}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using weighted formula.
    Returns: (total_score, list_of_reasons)
    
    Formula:
    Score = (3.0 × genre_match) + 
            (2.0 × mood_match) + 
            (1.5 × energy_similarity) + 
            (0.5 × acoustic_preference)
    """
    score = 0.0
    reasons = []
    
    # Weights
    w_genre = 3.0
    w_mood = 2.0
    w_energy = 1.5
    w_acoustic = 0.5
    
    # 1. Genre Match (3.0 weight)
    if song['genre'].lower() == user_prefs['genre'].lower():
        genre_score = 1.0
        reasons.append(f"Genre match: {song['genre']} (+{w_genre:.1f})")
    else:
        # Partial credit for different genre
        genre_score = 0.5
        reasons.append(f"Genre mismatch: {song['genre']} (expected {user_prefs['genre']}) (+{w_genre * genre_score:.1f})")
    
    score += w_genre * genre_score
    
    # 2. Mood Match (2.0 weight)
    if song['mood'].lower() == user_prefs['mood'].lower():
        mood_score = 1.0
        reasons.append(f"Mood match: {song['mood']} (+{w_mood:.1f})")
    else:
        mood_score = 0.0
        reasons.append(f"Mood mismatch: {song['mood']} (expected {user_prefs['mood']}) (+0.0)")
    
    score += w_mood * mood_score
    
    # 3. Energy Similarity (1.5 weight) - distance-based
    # Similarity = 1.0 - |user_target_energy - song_energy|
    user_target_energy = user_prefs['energy']
    energy_diff = abs(user_target_energy - song['energy'])
    energy_similarity = 1.0 - energy_diff
    energy_contribution = w_energy * energy_similarity
    score += energy_contribution
    
    reasons.append(f"Energy match: {song['energy']:.2f} (target {user_target_energy:.2f}) (+{energy_contribution:.2f})")
    
    # 4. Acoustic Preference (0.5 weight)
    if user_prefs.get('likes_acoustic', False):
        # User likes acoustic, so high acousticness is good
        acoustic_score = song['acousticness']
        reasons.append(f"Acoustic preference: {song['acousticness']:.2f} (+{w_acoustic * acoustic_score:.2f})")
    else:
        # User prefers electronic, so low acousticness is good
        acoustic_score = 1.0 - song['acousticness']
        reasons.append(f"Electronic preference: {song['acousticness']:.2f} (+{w_acoustic * acoustic_score:.2f})")
    
    score += w_acoustic * acoustic_score
    
    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Recommends top k songs by scoring all songs and returning highest-scoring ones.
    Returns: list of (song_dict, score, explanation_string) tuples
    """
    if not songs:
        return []
    
    # Score all songs
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "\n  ".join(reasons)
        scored_songs.append((song, score, explanation))
    
    # Sort by score (highest first)
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    # Return top k
    return scored_songs[:k]
