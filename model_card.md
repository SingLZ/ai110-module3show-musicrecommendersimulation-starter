# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0** — A lightweight, interpretable music recommendation engine

---

## 2. Intended Use  

VibeFinder recommends 5 songs from a curated catalog of 20 songs based on a user's genre, mood, energy level, and acoustic preferences. It is designed for **classroom exploration and education** to understand how content-based recommender systems work, not for real-world deployment. The model assumes users have a clear primary genre preference and can articulate their preferred mood and energy level.

---

## 3. How the Model Works  

**The Core Idea:** VibeFinder scores each song by comparing it to what you like, then shows you the best matches.

**What it learns about you:**
- **Favorite Genre** (e.g., "pop", "rock", "lofi") — the music style you love most
- **Favorite Mood** (e.g., "happy", "chill", "intense") — the emotional vibe you want
- **Target Energy** (0.0 = relaxing, 1.0 = intense) — how energetic you want the music to be
- **Acoustic Preference** (Yes/No) — whether you prefer acoustic instruments or electronic sounds

**How it scores songs:**

VibeFinder uses a weighted scoring formula:
```
Final Score = (3.0 × genre_match) + (2.0 × mood_match) + (1.5 × energy_similarity) + (0.5 × acoustic_preference)
```

Each component works differently:

1. **Genre Match (Weight: 3.0)** — Most important. If the song's genre matches your favorite, you get +3.0 points. If not, you get +1.5 (partial credit for diversity). This is the heaviest weight because genre is the foundation of taste.

2. **Mood Match (Weight: 2.0)** — Very important. If the song's mood matches what you want, you get +2.0 points. If not, you get 0 points. Mood is all-or-nothing because it sets the emotional vibe; a "happy" pop song isn't helpful if you want "intense" energy.

3. **Energy Similarity (Weight: 1.5)** — Moderate importance. Instead of "high is good," this measures how close the song's energy is to your target. For example, if you want energy 0.50 and a song has 0.55, you get a high score because it's close (+1.42 points). This rewards songs that match your vibe, not just extreme values.

4. **Acoustic Preference (Weight: 0.5)** — Lowest priority. If you like acoustic sounds, the song's acousticness percentage becomes your score (0.0–1.0). If you prefer electronic sounds, it's the reverse (1.0 - acousticness). This is weighted lowest because it's a nice-to-have preference, not essential.

---

## 4. Data  

**Dataset:** 20 curated songs representing 12 genres and 8 moods

**Genres represented:** pop, rock, lofi, ambient, synthwave, jazz, hip-hop, electronic, acoustic, metal, country, blues, reggae, classical, folk

**Moods represented:** happy, chill, intense, relaxed, focused, moody, energetic, sad, inspired, contemplative

**Data characteristics:**
- All songs have numerical features (energy 0–1, valence, danceability, acousticness)
- Each song is manually tagged with genre and mood
- **No modifications** were made to the starter dataset; all 20 original songs are used as-is
- **Missing categories:** Limited representation of non-English music, one-off genres, and niche moods

**Imbalance identified:**
- Pop: 5 songs (25% of catalog)
- Lofi, rock, acoustic, jazz, blues, classical, folk, reggae, metal, ambient, hip-hop, synthwave, country, electronic: 1-2 songs each
- Some users (e.g., "Acoustic Soul Seeker") have only 1 perfect genre match in the entire catalog

---

## 5. Strengths  

**Where VibeFinder works well:**

1. **Multi-genre, same-mood users get good diversity** — E.g., "Workout Enthusiast" (pop/intense) with high energy gets "Gym Hero" (pop, close match) plus "Thunder in the Sky" (metal) and "Storm Runner" (rock). The algorithm rewards mood matching even when genre differs.

2. **Mood matching effectively filters vibe** — "Sad Contemplative Soul" (sad mood) and "Happy Pop Enthusiast" (happy mood) get completely different pop songs. "Midnight Sadness" scores 6.74/10 for the sad listener, but "Sunrise City" (a happy pop song) only scores 3.93. This shows mood is doing its job.

3. **Energy similarity formula captures the "target" concept** — Users wanting low energy (0.32) correctly get low-energy songs (lofi, ambient, acoustic ballads). Users wanting high energy (0.90+) correctly get high-energy songs (rock, metal, pop, electronic). The distance-based formula works better than "just maximize energy."

4. **Genre weight provides consistency** — Pop fans reliably get pop recommendations as their #1 match. This consistency is valuable for users who have a strong primary preference.

5. **Explanations are transparent** — Each recommendation includes a detailed breakdown (genre match, mood match, energy score, acoustic score), so users (and researchers) understand why a song was recommended.

---

## 6. Limitations and Bias 

**Key weaknesses discovered during evaluation:**

### 1. **Genre Weight is Too Strong (3.0) — Creates Homogeneous Playlists**

**The problem:** With genre weighted at 3.0 (vs mood at 2.0), genre dominates all other factors. This means:
- Users only get recommendations from genres they select, even if other genres have better mood/energy matches
- "Gym Hero" (pop, intense) appears in the top 5 for both "Happy Pop Enthusiast" and "Workout Enthusiast," showing the same genre repeats even when mood differs
- There's no "cross-genre discovery" — a pop fan will never see a rock song, even if there's a rock song that perfectly matches their mood and energy

**Why it matters:** Real recommenders (Spotify, Apple Music) introduce cross-genre recommendations to prevent filter bubbles. Users get "surprised" with similar vibes from different genres. VibeFinder's heavy genre weighting prevents this.

**Evidence:** In the weight sensitivity experiment, reducing genre weight from 3.0 to 1.5 and increasing mood weight from 2.0 to 3.5 caused:
- "Workout Enthusiast": Storm Runner and Thunder in the Sky moved up to #2–3 (tied with Gym Hero score), vs #2–3 much lower in baseline
- This shows different genre/same mood songs can be competitive when mood weights higher

### 2. **Mood is Binary, Not Spectrum — Ignores Similar Emotions**

**The problem:** Mood must match exactly or you get 0 points. This means:
- "Contemplative" ≠ "Relaxed" — but they're emotionally similar moods
- "Energetic" ≠ "Intense" — but both describe high-energy vibes
- "Acoustic Soul Seeker" (relaxed mood) doesn't reward "Desert Soul" (contemplative mood) at all, even though folklore/acoustic music with contemplative energy is a natural recommendation

**Why it matters:** In the real world, mood is a spectrum. Spotify's mood estimations use continuous warmth/energy scales, not binary buckets. Our system is too rigid.

### 3. **Tiny Dataset Creates Artificial Scarcity**

**The problem:** Only 20 songs means:
- "Acoustic Soul Seeker" has only 1 song in their **exact** genre match (Acoustic Breeze)
- "Jazz & Blues Lover" has only 1 jazz song (Coffee Shop Stories) and 1 blues song (Blue Note Blues)
- Users with niche genre preferences quickly exhaust options

**Why it matters:** Real recommenders have millions of songs. A user preferring "acoustic" shouldn't see the same 3 songs repeated. Our dataset is pedagogically useful but extremely limiting.

### 4. **Acoustic Preference Weight is Weak (0.5) — Barely Influences Results**

**The problem:** With weight 0.5 (vs genre 3.0), acoustic/electronic preference is ~6x less important than genre. Even users who prefer acoustic heavily get electronic songs if the genre and mood match.

**Evidence:** "Chill Lofi Listener" (likes_acoustic=True) gets "Irie Vibes" (reggae, only 0.65 acousticness) as a top-5 pick because lofi + chill mood dominate. The acoustic preference would need to be 3+ times heavier to shift this.

### 5. **Energy Similarity Doesn't Account for Outliers**

**The problem:** A user wanting calm music (energy=0.32) might get recommended an acoustic classical piece AND an acoustic reggae song. Both are low-energy, but reggae has upbeat vibes despite low technical "energy." The energy metric alone doesn't capture this nuance.

**Why it matters:** Energy (0–1) and valence (positivity, 0–1) are related but different. A sad, low-energy song isn't the same as a chill, low-energy song, even if energy scores match.

### 6. **Dataset Has Genre Misclassifications** — Electronic ≠ Synthwave

**The problem:** "Energetic EDM Dancer" prefers "electronic" but gets "Neon Dreams" (synthwave). Are these the same? The dataset groups them together, but synthwave has a retro aesthetic that electronic dance listeners might not want. Genre is too broad.

---

## 7. Evaluation  

### **Profiles Tested (8 Diverse User Types)**

| Profile | Genre | Mood | Energy | Result |
|---------|-------|------|--------|--------|
| Happy Pop Enthusiast | pop | happy | 0.80 | Excellent — "Sunrise City" perfectly matches all factors |
| Chill Lofi Listener | lofi | chill | 0.40 | Excellent — "Library Rain" and "Midnight Coding" both perfect |
| Intense Rock Fan | rock | intense | 0.90 | Good, but gets pop alternatives for mood (not rock) |
| Workout Enthusiast | pop | intense | 0.92 | Excellent — "Gym Hero" is a perfect match |
| Acoustic Soul Seeker | acoustic | relaxed | 0.32 | Limited — only 1 perfect match, then forced to similar genres |
| Energetic EDM Dancer | electronic | happy | 0.88 | Good — "Neon Dreams" matches, but limited electronic songs |
| Jazz & Blues Lover | jazz | relaxed | 0.37 | Adequate — "Coffee Shop Stories" matches, but limited diversity |
| Sad Contemplative Soul | pop | sad | 0.40 | Good match on "Midnight Sadness," but pop dominance limits mood diversity |


More details on [**Profile analysis**](PROFILE_COMPARISON_ANALYSIS.md)

### **Key Findings**

**What Surprised Me:**
1. **Genre weight dominance** — I expected mood to matter more. The 3.0 vs 2.0 split is surprisingly genre-heavy. Swapping a pop-sad user with pop-happy gives completely different recommendations, but a rock-intense user and pop-intense user don't share much even though they want the same mood and energy.

2. **Mood binary is too harsh** — "Desert Soul" (folk, contemplative) would be a perfect recommendation for "Acoustic Soul Seeker" (acoustic, relaxed), but the system gives 0 points because contemplative ≠ relaxed. In real systems, these are on the same emotional spectrum.

3. **Energy similarity works great** — This was the surprise success. The distance formula (1.0 - |target - song|) perfectly captures "want something close to my target, not extreme." Low-energy users consistently got low-energy songs, high-energy users got high-energy songs.

4. **Pop dominance is real** — With 5 pop songs in 20 total, pop users get the most varied recommendations. Jazz, blues, acoustic users hit a wall fast. This wasn't intentional but reveals how dataset composition affects recommendation fairness.

5. **The "Gym Hero" effect** — This pop/intense song appears in top-5 recommendations for "Happy Pop Enthusiast" (#5), "Intense Rock Fan" (#2), and "Workout Enthusiast" (#1). High energy + pop genre + electronic preference makes it universally appealing, which is realistic but also shows the algorithm can converge on a few "safe" recommendations.

### **Experiment: Weight Sensitivity**

**Hypothesis:** Reducing genre weight from 3.0 → 1.5 and increasing mood weight from 2.0 → 3.5 creates cross-genre recommendations while keeping mood matching strict.

**Results:** ✅ Hypothesis confirmed
- "Workout Enthusiast" in baseline: "Gym Hero" (#1, 6.96), "Thunder in the Sky" (#2, 5.44), "Storm Runner" (#3, 5.43)
- "Workout Enthusiast" with new weights: "Gym Hero" (#1, 6.96), "Thunder in the Sky" (#2, 6.19), "Storm Runner" (#3, 6.18)
- Thunder and Storm moved much closer in score, suggesting people wanting intense-mood music would get better recommendations across genres

**Conclusion:** Genre weight of 3.0 is probably too high for a system that should encourage discovery. A weight of 1.5–2.0 might be more balanced.

---

## 8. Future Work  

1. **Make mood continuous, not binary** — Replace mood categories with X/Y coordinates (e.g., "happy-sad" axis, "energetic-calm" axis). Then calculate mood similarity as distance, not exact match.

2. **Add a "mood family" concept** — Group moods into families (happy/excited/energetic, sad/melancholic/contemplative, chill/relaxed/focused) and reward partial matches (0.5 points for same family).

3. **Reduce genre weight** — Test weight of 1.5–2.0 for genre to enable more cross-genre discovery while preserving preference for primary genre.

4. **Expand acoustic categorization** — Instead of binary acoustic vs electronic, use the continuous acousticness metric (0–1) and let users express preference on a scale, not yes/no.

5. **Add diversity bonus** — Penalize recommendations if the same song/artist appears too often in top-5. Encourage algorithmic serendipity.

6. **Dataset expansion** — Add 50–100 more songs, ensuring genre representation is more balanced. Include real streaming data frequencies so the algorithm reflects actual music consumption patterns.

7. **Temporal/contextual signals** — Consider time-of-day (morning music ≠ night music) and activity (workout, studying, relaxing) to provide situation-aware recommendations.

---

## 9. Personal Reflection  

**What I learned:**

Building this recommender revealed how **weight distribution is the real art** of recommender design. The math is simple — just multiply features by weights and add them up—but deciding those weights changes everything. A genre weight of 3.0 vs 1.5 shifts the entire personality of the system from "stay in your lane" to "explore similar vibes."

**Surprising insight:**

I expected mood to be the strongest signal, but the baseline weights (genre=3.0, mood=2.0) show that real recommenders still rely heavily on genre as the primary filter. This makes sense for discovery (people search by genre) but creates filter bubbles. The weight sensitivity experiment proved that different weight distributions lead to fundamentally different user experiences — the same algorithm can be either conservative or adventurous depending on one number.

**How it changed my thinking:**

Using Spotify and TikTok, I always assumed the recommendations were driven by "what I actually listened to" (collaborative filtering). This project showed me that even simple content-based rules (genre + mood + energy) can feel surprisingly accurate. But I also learned the danger: with only 20 songs and biased genre distribution, the system quickly becomes predictable and exhausts its catalog. Real platforms solve this with millions of songs, different weight distributions, and continuous model updates based on what users actually click. The simplicity of our model made the limitations obvious — that's both the weakness and the educational value.  
