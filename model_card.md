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

### My Biggest Learning Moment

The turning point came when I tested the "Sad Pop Listener" profile and saw that "Sunrise City" (a happy pop song) scored only 3.93/10.0, while "Midnight Sadness" (a sad pop song) scored 6.74/10.0. Same genre, same artist style, completely different recommendations because of one attribute: **mood**.

This revealed something profound: **mood is a stronger dividing line than genre**. I had designed the system thinking genre would be the primary separator (pop fans follow pop, rock fans follow rock), but the evaluation showed that a "happy pop fan" and "sad pop fan" have practically zero recommendation overlap. They're different users entirely.

That moment changed how I think about music taste: **it's not "what type of music do you like" — it's "what emotional state are you trying to achieve?"** A playlist for studying (focused mood, low-medium energy) looks nothing like a playlist for a road trip (happy/energetic mood, high energy), even if both users like the same genre. The algorithm was right; I was thinking about it wrong. Mood is the primary filter; genre is secondary.

**Why this matters:** Real platforms like Spotify organize by mood-based playlists precisely because of this insight. The algorithm's behavior taught me something that would have taken years to learn through user research alone.

---

### How I Used AI Tools (And When I Had to Verify Them)

**How AI helped:**

1. **Rapid prototyping** — When I needed to create 8 diverse user profiles, I used AI to brainstorm persona names and characteristics (Happy Pop Enthusiast, Workout Enthusiast, etc.). This saved hours of creative thinking.

2. **Testing strategy design** — AI suggested "weight sensitivity experiments" as a way to understand feature importance. This led to `main_experiment.py`, which revealed that reducing genre weight from 3.0 to 1.5 dramatically changes recommendations.

3. **Diversity logic implementation** — I asked AI: "How would you design a fairness penalty for repeated artists in recommendations?" The response outlined a clean approach: deduct points if an artist already appears in the top recommendations. This became `main_diversity.py`.

4. **Explanation clarity** — AI helped rewrite vague sentences into clear, non-technical language for the model card. For example, turning "the distance-based energy similarity formula captures target-seeking behavior" into "This rewards songs that match your vibe, not just extreme values."

**When I had to double-check:**

1. **The explanation format bug** — AI generated code that returned explanations as a list in one place and a string in another. The initial `main_diversity.py` crashed because of this type inconsistency. I had to manually fix it and add type checking with `isinstance()`.

2. **Weight values** — AI suggested various weight combinations, but I had to verify by running actual tests. When AI suggested "make mood weight 5.0 for mood-focused mode," I tested it and saw that it actually suppressed genre diversity too much. I settled on 3.5 instead after manual experimentation.

3. **The comparative analysis logic** — AI's initial suggestion for profile comparison focused on raw scores, but I realized the comparative insight should focus on **why** scores differ, not just how different they are. I rewrote PROFILE_COMPARISON_ANALYSIS.md to include deeper causal analysis.

4. **Energy similarity formula** — AI suggested various formulas. I had to manually verify that `1.0 - abs(target - song)` was correct by testing edge cases: if target=0.5 and song energy=0.5, result should be 1.0 (perfect match). ✓ If target=0.5 and song=1.0, result should be 0.5 (50% match). ✓

**Key lesson:** AI is excellent for generating structure and options, but **human judgment is required for validation**. I used AI to build faster, but I tested everything before trusting it.

---

### What Surprised Me About Simple Algorithms

I expected the recommender to feel "mechanical" or "obviously flawed"—that users would immediately say "this isn't how real recommendations work." Instead, I was shocked by how **human** it feels.

**The surprise:**

When I ran the evaluation, "Chill Lofi Listener" got recommendations that perfectly matched:
1. "Library Rain" (lofi, chill, 0.35 energy, 0.86 acoustic)
2. "Midnight Coding" (lofi, chill, 0.42 energy, 0.71 acoustic)
3. "Spacewalk Thoughts" (ambient, chill, 0.28 energy, 0.92 acoustic)

These *feel* right. Not because the algorithm is magical, but because the system is capturing something real: **that people want consistency in emotional tone and intensity level**.

The reason it works is that I encoded real knowledge into the weights. By setting mood weight to 2.0 and energy weight to 1.5, I'm encoding the knowledge that "people care more about how you *feel* listening to a song than they care about extreme values." This wisdom didn't come from data science—it came from understanding humans.

**What surprised me most:** The algorithm is effective *because it's built on correct assumptions about human taste*, not because it's complex. It's as if I wrote:
- Assumption 1: Genre is foundational to taste (weight 3.0)
- Assumption 2: Mood is deal-breaker (weight 2.0, binary)
- Assumption 3: People want targeted intensity, not extremes (distance-based energy)
- Assumption 4: Acoustic vs electronic is peripheral (weight 0.5)

And all four assumptions hold up in practice! The algorithm "feels" like recommendations because **I designed it to match how people actually think about music, not how a computer would naturally optimize it.**

**The dark side of this simplicity:** Once I realized how well simple rules work, I also realized how insidious algorithmic bias becomes. If a 3.0 weight on genre creates meaningful filter bubbles, then Spotify engineers, knowing this, are *deliberately choosing* to accept that tradeoff because it improves user satisfaction on some metric (probably click-through rate). The algorithm isn't wrong; the engineers just decided different consequences were acceptable. That's when "simple" becomes "dangerous"—when the design is intentional and the bias is a feature, not a bug.

---

### What I'd Try Next (If Extending This Project)

**Short-term improvements (could implement in a hackathon):**

1. **Continuous mood space** — Instead of discrete moods (happy, sad, chill, intense), map every mood to 2D coordinates: "happiness axis" (-sad to +happy) and "energy axis" (-calm to +energetic). Then use Euclidean distance for mood similarity instead of binary matching. This would let "contemplative" (low happiness, low energy) partially match "relaxed" (low happiness, mid energy).

   Implementation: Represent moods as (happiness, energy) tuples, calculate similarity as `1.0 - distance/max_distance`.

2. **Popularity/cultural moment signal** — Add a feature that considers whether a song is trending or culturally relevant. Some users want "timeless classics," others want "what everyone's talking about right now." This would require historical data but would make recommendations feel more current.

3. **Explicit "diversity injection"** — Implement the diversity penalty I prototyped, but smarter: instead of a flat -0.5 penalty, use a *diversity multiplier* that increases as your top 5 becomes more homogeneous. If you have 5 pop songs, artist 6 (non-pop) gets a +1.5 boost. This is how Spotify likely works.

**Medium-term research (would need more data):**

4. **Collaborative filtering hybrid** — Add a component that says "users like you also liked songs from [artist X]" without explicit song-to-song similarity. Combine content-based (genre/mood/energy) with collaborative (what similar users clicked) weighting at maybe 30% collaborative, 70% content.

5. **Contextual recommendations** — Gather metadata: "What time of day does this user listen? What activity? What weather?" Morning commute music ≠ evening relaxation music. A small context input could be a multiplier on various weights.

6. **Attention vs. completion metrics** — Instead of assuming all clicks are equal, track whether users skip 5% into a song (didn't like it) vs listening to 95% (loved it). This would reveal "songs that feel right on paper but users bounce off." This requires real user interaction data.

**Long-term ambitious ideas:**

7. **Cross-domain recommendation** — Instead of just music, recommend activities with the mood: "You want 'chill' mood? Here's a song, a podcast, a recommended location to study, a recipe to cook." Music taste becomes a window into lifestyle preference. This is what Netflix/Spotify are doing now by expanding beyond their core service.

8. **Emotional prediction model** — What if the recommender predicted emotional arcs? "You want happy music, but my model predicts you'll appreciate a moment of poignancy in the 4th song." This would require understanding emotional trajectories, probably through neural networks trained on listening patterns.

9. **Generate playlists, not just songs** — Instead of top 5 recommendations, generate a full 60-minute playlist with arc, pacing, and narrative. Maybe 20% genre A, 40% genre B, with energy that builds/falls strategically. This is where artificial orchestration becomes valuable; single songs are too granular.

10. **Domain transfer learning** — Train on 1 million songs and 100,000 music fans to learn the "taste landscape," then apply to book recommendations, movie recommendations, etc. If someone likes "intense pop," what books/movies do they like? Taste isn't music-specific; it's a fundamental preference dimension.

**The one I'd prioritize:** Continuous mood space (#1). It's a small change (maybe 2 hours of work) that would dramatically improve recommendations for users with nuanced mood preferences. The binary mood matching is the #1 limitation, so fixing it has the highest return on investment.

---

