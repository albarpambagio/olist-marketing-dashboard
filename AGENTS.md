# AGENTS.md

## Project Overview

Three portfolio dashboard projects analyzing Olist Brazilian E-Commerce data (2016-2018). Each project follows the same end-to-end analytics workflow.

| Project | Focus | Location |
|---------|-------|----------|
| Sales Dashboard | Revenue, customer retention, product performance | `olist-sales-dashboard/` |
| Operations Dashboard | Delivery performance, seller reliability, logistics | `olist-ops-dashboard/` |
| Marketing Funnel | Lead conversion, channel ROI, LTV by source | `olist-marketing-dashboard/` |

**Tech Stack**: PostgreSQL (port 5433) → Python ETL → Power BI Desktop

## Setup Commands

### Prerequisites
- PostgreSQL 13+ running on port 5433
- Python 3.8+ with `psycopg2-binary`
- Kaggle CLI for data download

### Install Dependencies
```bash
pip install psycopg2-binary pandas
```

### Data Download
```bash
# Olist E-Commerce (Sales, Ops)
kaggle datasets download -d olistbr/brazilian-ecommerce -p ./data --unzip

# Marketing Funnel (Marketing project only)
kaggle datasets download -d olistbr/marketing-funnel-olist -p ./data --unzip
```

### Marketing Database Setup (run in project root)
```bash
# 1. Load marketing funnel data
python sql/load_marketing_data.py
# 2. Load e-commerce base tables (if not already loaded)
python sql/load_data_v2.py
# 3. Create combined star schema
python sql/phase3_starschema.py
# 4. Create KPI views
python sql/phase4_kpis.py
# 5. Create funnel analysis + cross-tab views
python sql/phase5_funnel.py
# 6. Create profile by channel view (Slide 6)
python sql/phase7_slide6.py
```

## Development Workflow

### Phase Pipeline

Each project follows a 6-phase workflow:

```
Phase 1: Setup        → sql/load_data.py, sql/load_data_v2.py
Phase 2: Clean & EDA  → sql/phase2_cleaning_eda.py, logs/phase2_cleaning_eda.log.md
Phase 3: Star Schema  → sql/phase3_starschema.py, logs/phase3_starschema.log.md
Phase 4: KPIs         → sql/phase4_kpis.py
Phase 5: Advanced     → sql/phase5_funnel.py (Marketing only)
Phase 6: Segmentation → sql/phase6_advanced.py (RFM, Cohort)
Phase 7: Slide 6      → sql/phase7_slide6.py (Profile by Channel)
```

### Working on Each Project

1. Navigate to project folder: `cd olist-sales-dashboard`
2. Run ETL pipeline: `python sql/load_data_v2.py`
3. Verify data: Connect Power BI to `localhost:5433`, database `olist`
4. Import views: `fact_orders`, `dim_date`, `dim_product`, `dim_customer`

### Database Connection (Power BI)
```
Server: localhost:5433
Database: olist
Authentication: Username/Password (postgres/your_password)
```

## Testing Instructions

### Verify Data Loading
```bash
psql -h localhost -p 5433 -U postgres -d olist -c "SELECT COUNT(*) FROM orders"
# Expected: ~99,441 rows
```

### Verify Star Schema
```bash
psql -h localhost -p 5433 -d olist -c "SELECT COUNT(*) FROM fact_orders"
# Should match delivered orders: ~96,478

psql -h localhost -p 5433 -d olist -c "SELECT COUNT(*) FROM dim_date"
# Should cover: 2016-09 to 2018-10
```

### Verify KPIs
```bash
# Revenue check
psql -h localhost -p 5433 -d olist -c "SELECT SUM(revenue) FROM fact_orders"
# Expected: ~$13.17M (Sales project)

# Repeat customer rate
psql -h localhost -p 5433 -d olist -c "SELECT AVG(is_repeat_customer::int) FROM fact_orders"
# Expected: ~3%
```

### Common Issues & Fixes
- **Port conflict**: PostgreSQL default 5432, this project uses 5433
- **Missing tables**: Run `sql/01_create_tables.sql` first
- **Duplicate geolocation**: Use `geo_deduped` view for location analysis

## Code Style

### Python Scripts
- Snake_case naming: `load_data_v2.py`, `phase2_cleaning_eda.py`
- Docstrings for functions
- Logging to `logs/` folder with `.log.md` extension
- Error handling with try/except, log failures

### SQL Conventions
- Views named: `kpi_*`, `fact_*`, `dim_*`
- Primary keys: `*_id` or `date_key`
- Foreign keys: explicit `_id` suffix
- Timestamps: use `date` type, not `timestamp`

### Project Structure
```
project/
├── data/           # CSV files (add to .gitignore if large)
├── sql/            # Python ETL scripts (.py) + SQL files (.sql)
├── logs/           # Phase logs (*.log.md) + insights.md
├── docs/           # Dashboard guide, DASH framework, interview prep
│   ├── archive/    # Deprecated or historical docs
│   └── SKILL.md    # AI agent skills for this project
└── README.md       # Stakeholder-facing report
```

## Build and Deployment

### Power BI Dashboard
1. Open Power BI Desktop
2. Get Data → PostgreSQL
3. Enter connection: `localhost:5433`, database: `olist`
4. Select views: `fact_orders`, `dim_date`, `dim_product`, `dim_customer`
5. Build dashboards using star schema model

### GitHub Repository
Each project is a separate repo:
- `github.com/albarpambagio/olist-sales-dashboard`
- `github.com/albarpambagio/olist-ops-dashboard`
- `github.com/albarpambagio/olist-marketing-dashboard`

### Data Source Attribution
- **Source**: [Olist Brazilian E-Commerce (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **License**: CC BY-NC-SA 4.0

## Pull Request Guidelines

### Title Format
```
[Project] Description
# Example: [Sales] Add RFM segmentation view
```

### Required Checks
- [ ] SQL scripts run without errors
- [ ] Row counts reconcile with source data
- [ ] KPI values match expected ranges
- [ ] README updated with new findings

### Before Commit
```bash
# Verify all phases run
python sql/load_data_v2.py
python sql/phase3_starschema.py
python sql/phase4_kpis.py

# Check logs
cat logs/phase2_cleaning_eda.log.md

# Create Slide 6 view
python sql/phase7_slide6.py
```

## Additional Notes

### Key Metrics by Project

| Project | Primary KPI | Secondary |
|---------|-------------|-----------|
| Sales | Revenue ($13.17M) | Repeat Rate (3%), AOV ($137) |
| Ops | On-Time Rate (92%) | Delivery Time (12 days), Freight % |
| Marketing | Conversion (10.5%) | LTV ($95.61/MQL) |

### Monorepo Structure
The three projects are siblings. To work on a specific project:
```bash
cd D:/PROJECT/data_analyst_porto/olist-sales-dashboard
python sql/load_data_v2.py
```

### Common Commands Reference
```bash
# Start PostgreSQL (if using homebrew on macOS)
brew services start postgresql@13

# Connect to database
psql -h localhost -p 5433 -U postgres -d olist

# List all tables
psql -h localhost -p 5433 -d olist -c "\dt"

# View schema
psql -h localhost -p 5433 -d olist -c "\d fact_orders"
```