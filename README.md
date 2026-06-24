# Bay Area Electrification Incentives Live Dashboard

This is a starter Streamlit dashboard built around:

`bay_area_electrification_incentive_dashboard.xlsx`

## Run locally

Open Terminal, go into this folder, then run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

If you are on Mac and the folder is in Downloads, the command may look like:

```bash
cd ~/Downloads/bay_area_live_dashboard_project
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `bay_area_electrification_incentive_dashboard.xlsx`
3. Go to Streamlit Community Cloud.
4. Create a new app from your GitHub repo.
5. Set the main file path to `app.py`.
6. Deploy.
