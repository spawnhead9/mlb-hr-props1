import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="MLB HR Props", layout="wide")

st.title("🏟️ MLB Home Run Probability Model")
st.markdown("**Inspired by Rudebets** — Hitter Skill + Platoon + Pitcher + Park + Weather + Recent Form")

# Park Factors
park_factors = {
    "Coors Field": 1.25, "Chase Field": 1.08, "Great American Ball Park": 1.10,
    "Dodger Stadium": 1.05, "Fenway Park": 1.06, "Yankee Stadium": 1.12,
    "Oracle Park": 0.85, "T-Mobile Park": 0.90, "Petco Park": 0.92,
    "Citizen's Bank Park": 1.08, "Default": 1.00
}

# Sample players (you can add more later)
hitters_data = [
    {"Player": "Aaron Judge", "Team": "NYY", "HR/PA": 0.065, "Barrel%": 0.18, "HardHit%": 0.55, "Platoon": 1.15, "Recent_Mult": 1.10},
    {"Player": "Shohei Ohtani", "Team": "LAD", "HR/PA": 0.058, "Barrel%": 0.16, "HardHit%": 0.52, "Platoon": 1.20, "Recent_Mult": 1.05},
    {"Player": "Pete Alonso", "Team": "NYM", "HR/PA": 0.052, "Barrel%": 0.14, "HardHit%": 0.48, "Platoon": 1.10, "Recent_Mult": 1.00},
    {"Player": "Juan Soto", "Team": "NYY", "HR/PA": 0.048, "Barrel%": 0.13, "HardHit%": 0.50, "Platoon": 1.25, "Recent_Mult": 1.08},
    {"Player": "Kyle Schwarber", "Team": "PHI", "HR/PA": 0.055, "Barrel%": 0.15, "HardHit%": 0.49, "Platoon": 1.05, "Recent_Mult": 0.95},
]

df = pd.DataFrame(hitters_data)

def calculate_hr_prob(row, park_factor=1.0, weather_mult=1.0, pitcher_mult=1.0):
    base = row["HR/PA"] * 4.0
    adjusted = base * row["Platoon"] * row["Recent_Mult"] * park_factor * weather_mult * pitcher_mult
    prob = 1 - np.exp(-adjusted)
    return min(round(prob * 100, 1), 35.0)

st.sidebar.header("Adjust Settings")
selected_park = st.sidebar.selectbox("Select Ballpark", options=list(park_factors.keys()))
weather_boost = st.sidebar.slider("Weather Boost (Temp/Wind)", 0.85, 1.30, 1.05, 0.01)
pitcher_hr_mult = st.sidebar.slider("Pitcher HR Multiplier", 0.70, 1.50, 1.00, 0.01)

df["Park_Factor"] = park_factors.get(selected_park, 1.0)
df["Prob_%"] = df.apply(lambda row: calculate_hr_prob(row, df["Park_Factor"].iloc[0], weather_boost, pitcher_hr_mult), axis=1)

df_display = df.sort_values("Prob_%", ascending=False)
st.dataframe(df_display[["Player", "Team", "Prob_%"]], use_container_width=True, hide_index=True)

st.markdown("### Model Categories (Rudebets Style)")
st.write("- **Hitter Skill**: HR/PA, Barrel%, Hard Hit%  \n"
         "- **Platoon Matchup**  \n"
         "- **Pitcher Profile**  \n"
         "- **Park Factor**  \n"
         "- **Weather**  \n"
         "- **Recent Form**")

st.caption("Educational tool only. Expand with
