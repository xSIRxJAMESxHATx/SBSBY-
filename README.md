# SBSBY!

SBSBY! is a clean Cleveland sports hub built with Streamlit.

## Includes
- Cleveland Browns
- Cleveland Guardians
- Cleveland Cavaliers
- Ohio State Football
- Ohio State Men's Basketball

## Features
- Neutral site-wide design
- Team-specific accent colors
- Source fallback logic
- Auto-refreshing live score section
- News, stats, history, and market links

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Create a GitHub repository.
2. Add `app.py`, `requirements.txt`, and `README.md`.
3. Commit and push.
4. Go to https://share.streamlit.io/
5. Click **New app**.
6. Select your repo.
7. Set the main file path to `app.py`.
8. Deploy.

## Notes
This version avoids BeautifulSoup entirely, which helps prevent the `bs4` deployment error.
