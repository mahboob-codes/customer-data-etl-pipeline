"""Start the Customer Data ETL Pipeline.

Run this file from the project folder after pandas is installed:

    python main.py
"""

from src.pipeline import run_pipeline


if __name__ == "__main__":
    run_pipeline()
