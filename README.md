# NBA Predictive Analytics Project

## Overview

This project is an NBA predictive analytics tool created for **DTSC 3601: Data Science Studio 3 – Predictive Analysis & Their Impacts**.

The current version of the project retrieves NBA data from **TheSportsDB API**, stores the data in CSV files, performs basic feature engineering, and trains a regression model to predict the total number of points scored in an NBA game.

The long-term goal of the project is to expand from game-level predictions to individual player predictions such as:

- Points
- Rebounds
- Assists
- Steals
- Blocks

The final version is intended to use recent player performance, matchup information, minutes played, home/away status, and other contextual features.

---

## Group Members

- Aiden Phillips
- Teahun Phou
- Ethan Whitesell
- Will Self

---

## Project Motivation

NBA performance prediction is useful for fantasy basketball players, sports analysts, bettors, and fans who want a data-driven estimate of future performance.

Rather than relying only on intuition or basic season averages, this project is designed to build a pipeline that can collect NBA data, process it, generate features, train a machine-learning model, and produce predictions.

The current demo focuses on proving that this full pipeline works from beginning to end.

---

## Current Project Pipeline

The current workflow is:

```text
TheSportsDB API
        ↓
Python API Requests
        ↓
JSON Data
        ↓
Pandas DataFrames
        ↓
Feature Engineering
        ↓
CSV Storage
        ↓
Train/Test Split
        ↓
Linear Regression
        ↓
Prediction
```

---

## Data Source

The current project uses **TheSportsDB V1 API**.

The notebook retrieves:

- NBA league information
- NBA team information
- NBA game information
- Game dates
- Home teams
- Away teams
- Home scores
- Away scores
- Venues
- Game status
- League information

The notebook currently uses the public V1 API key:

```python
API_KEY = "123"
```

---

## Installation

### Requirements

The project requires Python 3 and the following Python libraries:

- `requests`
- `pandas`
- `scikit-learn`

### Install Required Libraries

Run:

```bash
pip install requests pandas scikit-learn
```

If your computer uses `pip3`, run:

```bash
pip3 install requests pandas scikit-learn
```

For Jupyter Notebook or Google Colab, you can use:

```python
!pip install requests pandas scikit-learn
```

---

## Getting Started

### 1. Clone or Download the Repository

Clone the repository using Git:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Then enter the project folder:

```bash
cd YOUR_REPOSITORY_NAME
```

You can also download the repository as a ZIP file from GitHub.

---

### 2. Run the Data Ingestion Code

The ingestion portion connects to TheSportsDB API and retrieves NBA data.

Run the notebook:

```text
nba_data_ingestion.ipynb
```

or open it in Jupyter Notebook or Google Colab.

The ingestion process:

1. Connects to TheSportsDB API
2. Finds the NBA league
3. Downloads NBA team data
4. Downloads NBA game data
5. Creates additional features
6. Saves the results as CSV files

---

## Output Files

The data ingestion process creates two CSV files:

```text
nba_teams.csv
nba_games.csv
```

### `nba_teams.csv`

This file stores team-level information such as:

- Team ID
- Team name
- Location
- League
- Sport
- Stadium
- Country
- Year formed

### `nba_games.csv`

This file stores game-level information such as:

- Event ID
- Game date
- Home team
- Away team
- Home score
- Away score
- Venue
- Game status
- League
- Total points
- Score difference
- Home win indicator

---

## Feature Engineering

The notebook creates several additional values from the original game data.

### `total_points`

The total number of points scored by both teams.

```python
df["total_points"] = (
    df["home_score"] +
    df["away_score"]
)
```

Example:

```text
Home Score = 111
Away Score = 103

Total Points = 214
```

---

### `score_difference`

The difference between the home team's score and the away team's score.

```python
df["score_difference"] = (
    df["home_score"] -
    df["away_score"]
)
```

Example:

```text
Home Score = 111
Away Score = 103

Score Difference = 8
```

---

### `home_win`

Indicates whether the home team won the game.

```text
1 = Home team won
0 = Home team lost
```

The code is:

```python
df["home_win"] = (
    df["home_score"] >
    df["away_score"]
).astype("Int64")
```

---

## Machine-Learning Model

The current demonstration uses a **Linear Regression** model.

Regression is used because the model predicts a numerical value rather than a category.

The current target is:

```text
total_points
```

This means that the model attempts to predict the combined number of points scored by the two NBA teams.

---

## Model Features

The current input features are:

```python
X = df[
    [
        "home_team",
        "away_team"
    ]
]
```

The prediction target is:

```python
y = df["total_points"]
```

A simple way to think about this is:

```text
X = information given to the model

y = value we want the model to predict
```

For the current demo:

```text
Home Team
+
Away Team
      ↓
Regression Model
      ↓
Predicted Total Points
```

---

## Data Preprocessing

The home and away team names are text values.

Machine-learning models cannot directly use strings such as:

```text
Boston Celtics
Los Angeles Lakers
```

The notebook therefore uses:

```python
OneHotEncoder
```

This converts team names into numerical features that can be used by the regression model.

The preprocessing is handled using:

```python
ColumnTransformer
```

and the preprocessing and model are combined using:

```python
Pipeline
```

---

## Training the Model

The data is divided into training and testing sets using:

```python
train_test_split
```

The current code uses:

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)
```

The training data is used to teach the model.

The testing data is used to evaluate how well the trained model performs on games it did not train on.

The model is trained using:

```python
model.fit(
    X_train,
    y_train
)
```

---

## Quick Training Example

A simplified version of the model training process is:

```python
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression

df = pd.read_csv("nba_games.csv")

X = df[
    [
        "home_team",
        "away_team"
    ]
]

y = df["total_points"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "teams",
            OneHotEncoder(handle_unknown="ignore"),
            ["home_team", "away_team"]
        )
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regression", LinearRegression())
    ]
)

model.fit(
    X_train,
    y_train
)

print("Model training complete!")
```

This is the fastest way for a user to train the current demo model on the small dataset.

---

## Example Prediction

The notebook includes an example matchup:

```python
example_game = pd.DataFrame(
    {
        "home_team": [
            "Boston Celtics"
        ],

        "away_team": [
            "Los Angeles Lakers"
        ]
    }
)
```

The prediction is generated using:

```python
predicted_total = model.predict(
    example_game
)[0]
```

The output may look like:

```text
Boston Celtics vs Los Angeles Lakers

Predicted Total Points: 220.0
```

This means that the model predicts the two teams will score approximately **220 combined points**.

---

## Model Evaluation

The project currently evaluates the regression model using **Mean Absolute Error (MAE)**.

The code is:

```python
mae = mean_absolute_error(
    y_test,
    predictions
)
```

MAE measures the average difference between the model's predictions and the actual results.

For example, if:

```text
Mean Absolute Error = 14.26
```

then the model's predictions differ from the actual total score by approximately **14 points on average** in the test data.

Because the current dataset is very small, the current evaluation should be treated as an early demonstration rather than a reliable measure of final model performance.

---

## Major Functions

### `make_request(endpoint, params=None)`

Sends a GET request to TheSportsDB API.

Main responsibilities:

- Builds the request URL
- Sends the API request
- Checks for request errors
- Returns JSON data

---

### `find_nba_league()`

Searches TheSportsDB for basketball leagues and identifies the NBA.

Main responsibilities:

- Searches basketball leagues
- Finds the league named NBA
- Returns NBA league information
- Retrieves the NBA League ID

---

### `get_nba_teams()`

Downloads NBA team data from TheSportsDB.

Main responsibilities:

- Sends a request for NBA teams
- Extracts useful team fields
- Converts the response into a pandas DataFrame

---

### `get_nba_games(league_id)`

Downloads NBA game information for the selected season.

Main responsibilities:

- Uses the NBA League ID
- Requests season game data
- Extracts game information
- Converts the games into a pandas DataFrame

---

### `create_features(games_df)`

Creates additional columns from the raw game data.

Currently creates:

- `total_points`
- `score_difference`
- `home_win`

These engineered values make the dataset easier to use for analysis and machine learning.

---

### `save_data(teams_df, games_df)`

Saves the processed DataFrames as CSV files.

Creates:

```text
nba_teams.csv
nba_games.csv
```

---

### `main()`

Controls the overall ingestion pipeline.

It runs the following steps:

```text
Find NBA League
      ↓
Download Teams
      ↓
Download Games
      ↓
Create Features
      ↓
Save CSV Files
```

---

## Current Limitations

The current version is an initial prototype.

Important limitations include:

- The current dataset is small
- The current model predicts game-level total points rather than individual player statistics
- The model currently uses only the home and away teams as input features
- Injuries are not yet included
- Player minutes restrictions are not included
- Trades and lineup changes are not included
- Recent player performance is not yet included
- Opponent defensive strength is not yet included

Because of these limitations, the current predictions should be treated as demonstrations of the pipeline rather than reliable basketball forecasts.

---

## Future Development

The next stage of the project will focus on player-level predictions.

Possible future features include:

```text
recent_points_average
recent_rebounds_average
recent_assists_average
recent_minutes_average
opponent
home_or_away
player_position
team_performance
opponent_defense
```

The final model may predict outputs such as:

```text
Predicted Points = 27.5
Predicted Rebounds = 8.2
Predicted Assists = 6.4
```

The project may also add:

- A larger historical dataset
- Additional regression models
- Model comparison
- More detailed model evaluation
- Injury information
- Automated data updates
- AWS storage or cloud infrastructure
- A user interface or dashboard
- Explainability features

---

## Repository Structure

A recommended repository structure is:

```text
nba-predictive-analytics/
│
├── README.md
├── LICENSE
├── requirements.txt
│
├── nba_data_ingestion.ipynb
│
├── data/
│   ├── nba_games.csv
│   └── nba_teams.csv
│
├── bin/
│   └── run_demo.py
│
└── docs/
    └── functions.md
```

The `bin/` directory should contain example code showing how to run the project.

---

## Requirements File

A `requirements.txt` file can contain:

```text
requests
pandas
scikit-learn
```

Users can then install all required packages with:

```bash
pip install -r requirements.txt
```

---

## Example Code in `bin/`

A simple `bin/run_demo.py` file could contain:

```python
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression


df = pd.read_csv("nba_games.csv")

X = df[
    [
        "home_team",
        "away_team"
    ]
]

y = df["total_points"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "teams",
            OneHotEncoder(handle_unknown="ignore"),
            ["home_team", "away_team"]
        )
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regression", LinearRegression())
    ]
)

model.fit(
    X_train,
    y_train
)

example_game = pd.DataFrame(
    {
        "home_team": ["Boston Celtics"],
        "away_team": ["Los Angeles Lakers"]
    }
)

prediction = model.predict(
    example_game
)[0]

print(
    "Predicted Total Points:",
    round(prediction, 1)
)
```

---

## License

This project uses the **MIT License**.

with this:

```markdown
## License

This project uses the **MIT License**.

See the [LICENSE](LICENSE) file for the full license terms.

GitHub users can open the `LICENSE` file in the repository to view the full license terms.

---

## contact

For questions about this project, contact one of the project group members:

- Aiden Phillips
- Teahun Phou
- Ethan Whitesell
- Will Self

---

## Disclaimer

This project is for educational and research purposes.

Predictions generated by this model are statistical estimates and should not be treated as guaranteed outcomes or guaranteed betting advice.
