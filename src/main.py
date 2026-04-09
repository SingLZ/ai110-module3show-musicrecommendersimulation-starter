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

    # Define diverse user profiles for evaluation
    user_profiles = {
        "Happy Pop Enthusiast": {
            "genre": "pop", 
            "mood": "happy", 
            "energy": 0.80,
            "likes_acoustic": False
        },
        "Chill Lofi Listener": {
            "genre": "lofi", 
            "mood": "chill", 
            "energy": 0.40,
            "likes_acoustic": True
        },
        "Intense Rock Fan": {
            "genre": "rock", 
            "mood": "intense", 
            "energy": 0.90,
            "likes_acoustic": False
        },
        "Workout Enthusiast": {
            "genre": "pop", 
            "mood": "intense", 
            "energy": 0.92,
            "likes_acoustic": False
        },
        "Acoustic Soul Seeker": {
            "genre": "acoustic", 
            "mood": "relaxed", 
            "energy": 0.32,
            "likes_acoustic": True
        },
        "Energetic EDM Dancer": {
            "genre": "electronic", 
            "mood": "happy", 
            "energy": 0.88,
            "likes_acoustic": False
        },
        "Jazz & Blues Lover": {
            "genre": "jazz", 
            "mood": "relaxed", 
            "energy": 0.37,
            "likes_acoustic": True
        },
        "Sad Contemplative Soul": {
            "genre": "pop", 
            "mood": "sad", 
            "energy": 0.38,
            "likes_acoustic": True
        }
    }

    print("\n" + "="*70)
    print("🎵 MUSIC RECOMMENDER EVALUATION - PHASE 4")
    print("="*70)
    
    # Test each profile
    for profile_name, user_prefs in user_profiles.items():
        print("\n" + "="*70)
        print(f"📊 PROFILE: {profile_name}")
        print("="*70)
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
        
        print("\n")
    
    print("="*70)
    print("✅ EVALUATION COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
