"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs
import os


def main() -> None:
    # Navigate to data directory relative to project root
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "songs.csv")
    songs = load_songs(csv_path) 

    if not songs:
        print("No songs loaded. Exiting.")
        return

    # Starter example profile: Pop/Happy listener
    user_prefs = {
        "genre": "pop", 
        "mood": "happy", 
        "energy": 0.8,
        "likes_acoustic": False
    }

    print("\n" + "="*70)
    print("🎵 MUSIC RECOMMENDER SIMULATION")
    print("="*70)
    print("\n📊 USER PROFILE:")
    print(f"  • Favorite Genre: {user_prefs['genre'].title()}")
    print(f"  • Favorite Mood: {user_prefs['mood'].title()}")
    print(f"  • Target Energy: {user_prefs['energy']:.1f}/1.0")
    print(f"  • Prefers Acoustic: {'Yes' if user_prefs['likes_acoustic'] else 'No (Electronic)'}")
    
    print("\n" + "-"*70)
    print("🎧 TOP 5 RECOMMENDATIONS:")
    print("-"*70)
    
    recommendations = recommend_songs(user_prefs, songs, k=5)

    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"\n{i}. {song['title']}")
        print(f"   🎤 Artist: {song['artist']}")
        print(f"   📈 Score: {score:.2f}/10.0")
        print(f"   💭 Why:")
        for line in explanation.split("\n"):
            print(f"      • {line}")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
