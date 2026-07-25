# SBSBY!

SBSBY! is a Cleveland sports hub built in Streamlit.

It includes:
- Cleveland Browns
- Cleveland Guardians
- Cleveland Cavaliers
- Ohio State Football
- Ohio State Men's Basketball

Features:
- Scores and schedule links
- News/article link extraction
- Stats snapshots
- Historical context
- Prediction market links
- Browns-themed UI

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Put `app.py`, `requirements.txt`, and `README.md` in a GitHub repository.
2. Commit and push the files.
3. Go to https://share.streamlit.io/
4. Click **New app**.
5. Choose your GitHub repo.
6. Set the main file path to `app.py`.
7. Click **Deploy**.

## Notes

You can later upgrade this app by adding:
- live sports APIs
- data tables from official feeds
- better player trend charts
- matchup prediction-market pages for each game
