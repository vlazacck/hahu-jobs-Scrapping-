Job Data Scraper
This project scrapes job-related data from the @hahujobsforfreshgraduates Telegram channel and cleans it for analysis. The data is then stored in a PostgreSQL database for further use.

Features
Scrapes job listings from the @hahujobsforfreshgraduates Telegram channel.

Cleans the data, including handling missing values, standardizing formats, and removing irrelevant entries.

Stores the cleaned data in a PostgreSQL database for easy querying and analysis.

---

## 📌 Project Purpose

To extract and structure job opportunities posted in [@hahujobsforfreshgraduates](https://t.me/hahujobsforfreshgraduates) on Telegram, making it easier for fresh graduates to filter, search, and analyze job posts based on:

- Experience required
- Maximum Experience 
- Organization
- Application method
- Deadlines
- Tags / categories

---

## ⚙️ Features

- ✅ Scrapes messages from a public Telegram channel
- ✅ Filters and cleans text (removes non-English content)
- ✅ Parses important fields like job title, organization, location, experience, salary, etc.
- ✅ Categorizes jobs based on tags
- ✅ Exports structured data to a CSV file
- ✅ Normalizes deadline date format (e.g., `4/14/2025`, `13-Apr-25` → `2025-04-14`)
- ✅ Handles missing data by filling with sensible defaults (e.g., `gender = both`)
- ✅ Ready for analysis or dashboard integration

---

## 🏗️ Project Structure
. ├── scripts/ │ └── scrapper.py # Main async script for scraping Telegram   │ └── parser.py  for parsing  the texts   │ └──.env # Contains Telegram API credentials 
  ├── notebooks/ │ └── dataprossessing .ipynb # Jupyter Notebook for proscessing the raw data 
  ├── data/ │ ├── telegram_jobs.csv # Raw scraped messages    │ └──  structured_telegram_jobs.csv # structured output │ └── structured_telegram_cleaned.csv # Cleaned and structured output 
  ├── requirements.txt └── README.md

  ## 🚀 Getting Started

### 1. Clone the repo

git clone https://github.com/yourusername/telegram-job-scraper.git
cd telegram-job-scraper

2. Install dependencies


pip install -r requirements.txt

3. Set up environment variables
Create a .env file and fill in your Telegram credentials:

env

API_ID=your_api_id
API_HASH=your_api_hash
PHONE=+2519xxxxxxx
You can get your API_ID and API_HASH from my.telegram.org.

4. Run the scraper
bash
Copy code
python scripts/scrapper.py
This will create a telegram_jobs.csv file in your project directory.

5. Clean and parse data
Open notebooks/clean_jobs.ipynb and run it to:

Remove Amharic text

Extract structured fields

Normalize formats (e.g., deadline, experience)

Fill missing values
6.Set up PostgreSQL Database
Ensure PostgreSQL is installed and running. Create a database and update the connection settings in your script or configuration file. You can create the table using the following SQL schema:

sql
CREATE TABLE jobs (
    date TIMESTAMP,
    job_title VARCHAR(255),
    organization VARCHAR(255),
    location VARCHAR(255),
    tags TEXT,
    experience VARCHAR(255),
    salary DECIMAL,
    quantity_required INTEGER,
    gender VARCHAR(255),
    deadline DATE,
    how_to_apply TEXT,
    category VARCHAR(255),
    raw_text TEXT
);
 Run the Script
To scrape and upload the job data to the PostgreSQL database:

bash
Copy code
python db.py


📚 Dependencies
Telethon

pandas

python-dotenv

dateutil

psycopg2

sqlalchemy
Install all at once:

pip install -r requirements.txt

🙌 Acknowledgements
Inspired by the need to help fresh graduates discover job opportunities more easily.




            
