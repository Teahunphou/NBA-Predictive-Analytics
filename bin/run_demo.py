import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression


# Load stored game data
df = pd.read_csv("nba_games.csv")

# Features
X = df[
    [
        "home_team",
        "away_team"
    ]
]

# Target
y = df["total_points"]

# Split into training/testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)

# Convert team names into numerical features
preprocessor = ColumnTransformer(
    transformers=[
        (
            "teams",
            OneHotEncoder(handle_unknown="ignore"),
            ["home_team", "away_team"]
        )
    ]
)

# Create model pipeline
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regression", LinearRegression())
    ]
)

# Train model
model.fit(
    X_train,
    y_train
)

# Example matchup
example_game = pd.DataFrame(
    {
        "home_team": ["Boston Celtics"],
        "away_team": ["Los Angeles Lakers"]
    }
)

# Make prediction
prediction = model.predict(
    example_game
)[0]

print(
    "Predicted Total Points:",
    round(prediction, 1)
)
