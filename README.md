# Customer Data ETL Pipeline

A small Python pipeline that reads customer records, cleans them, loads the valid rows into SQLite, and writes a data quality report.

ETL means three stages:

1. **Extract** reads `data/raw/customers.csv`.
2. **Transform** removes duplicate customer IDs, fills a blank status, and rejects rows with missing required values or an invalid email.
3. **Load** writes the valid rows to `database/customers.db`.

A fourth step writes `reports/data_quality_report.txt`.

## Folder map

```text
Cursor_ETL_Project/
├── main.py                     # Starts the pipeline
├── requirements.txt            # Python packages to install
├── README.md
├── data/
│   ├── raw/
│   │   └── customers.csv       # 20 sample records, including bad data
│   └── processed/              # Clean and rejected CSV files appear here
├── database/                   # customers.db appears here
├── reports/                    # data_quality_report.txt appears here
└── src/
    ├── config.py               # Shared file paths
    ├── extract.py              # Read the CSV
    ├── transform.py            # Clean and validate
    ├── load.py                 # Write SQLite
    ├── quality_report.py       # Write the four counts
    └── pipeline.py             # Calls the steps in order
```

## Sample data problems

The raw file has 20 rows and includes:

- Repeated customer IDs: 1001, 1002, 1003, and 1005
- Missing phone, city, signup date, status, first name, or email
- Invalid emails, such as a missing `@`, a missing domain ending, a double `@`, and a space

Phone, city, and signup date may be blank. A row is still valid when those optional fields are empty. A blank status becomes `unknown`.

## Run later

From this folder, after you approve the install:

```text
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

The quality report counts are:

| Count | Expected |
| --- | ---: |
| Total records | 20 |
| Valid records | 9 |
| Rejected records | 7 |
| Duplicate records | 4 |

`9 + 7 + 4 = 20`. Duplicate rows are counted separately from rejected rows.
