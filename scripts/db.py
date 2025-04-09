import pandas as pd
from sqlalchemy import create_engine

# Replace with your actual values
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_NAME = "telegram_jobs"
DB_HOST = "localhost"
DB_PORT = "5432"

# SQLAlchemy connection
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Load cleaned data
df = pd.read_csv("../data/structured_telegram_cleaned.csv")  # Or whatever your cleaned file is

# Insert into PostgreSQL
df.to_sql("jobs", engine, index=False, if_exists="append")

print("✅ Data uploaded to PostgreSQL successfully!")
