# Smurfit WestRock ESG Performance Dashboard

Interactive Dash dashboard for the IIT Chicago ESG Analytics class project.
Built from the official 2024 Smurfit WestRock sustainability disclosures.

---

## Files

| File | Purpose |
|------|---------|
| `app.py` | Main Dash application (all code + data inline) |
| `requirements.txt` | Python dependencies |
| `Procfile` | Web server declaration for cloud platforms |
| `README.md` | This guide |

---

## Run locally

```bash
# 1. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch
python app.py
```

Open your browser at **http://localhost:8050**

---

## Deploy to Render (free tier — recommended for class)

1. Push this folder to a **GitHub repo**.
2. Go to https://render.com → New → Web Service.
3. Connect your repo.
4. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:server`
   - **Environment**: Python 3
5. Click **Create Web Service** — live URL provided in ~2 min.

## Deploy to Railway

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

## Deploy to Heroku

```bash
heroku create sw-esg-dashboard
git push heroku main
heroku open
```

---

## Data sources

All data is drawn directly from official Smurfit WestRock 2024 public disclosures:

- **Legacy Smurfit Kappa** trend data (2020-2024): Supporting Data PDF
- **Legacy WestRock** 2024 snapshot: Supplementary Information PDF
- Materiality topics: Planet Section PDF

> ⚠️ Data Integrity Note: 2024 reporting remains split across two legacy company datasets
> because the Smurfit WestRock merger closed mid-year 2024. Consolidated combined targets
> and KPIs are still being developed. Do not aggregate SK and WRK numbers.

---

## Dashboard sections

| Section | Data source | What it shows |
|---------|------------|---------------|
| KPI cards (top row) | SK trend + WRK 2024 | 7 headline environmental metrics |
| Scope 1 & 2 trend | Legacy SK 2020-2024 | Operational GHG direction |
| Water withdrawal | Legacy SK 2020-2024 | Water use efficiency trend |
| Waste pathways | Legacy SK 2020-2024 | Landfill vs recovery breakdown |
| Scope 3 hotspots | Legacy WRK 2024 | Value chain emission categories |
| Circularity metrics | Legacy SK 2020-2024 | Recovery rate + recycled fiber |
| Energy donut | Legacy WRK 2024 | Renewable vs non-renewable split |
| Key insights | Synthesised | 7 analyst takeaways |
