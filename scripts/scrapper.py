import os
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv
import pandas as pd
import re

# Add this after imports and dotenv loading
# Your imports and dotenv loading here...

CATEGORY_KEYWORDS = {
    'finance': 'Finance',
    'accounting': 'Finance',
    'engineering': 'Engineering',
    'health': 'Healthcare',
    'health_care': 'Healthcare',
    'medical': 'Healthcare',
    'ict': 'IT/Tech',
    'ict_support': 'IT/Tech',
    'IT_upport': 'IT/Tech',
    'education': 'Education',
    'construction': 'Construction',
    'Site Engineer':'Construction',
    'intern': 'Internship',
    'logistics': 'Logistics',
    'driver': 'Logistics',
    'marketing': 'Marketing',
    'legal': 'Legal',
    'admin': 'Administration',
    'management': 'Management',
}

import re

def is_english(text):
    return all(ord(char) < 128 for char in text)

def parse_message(text, date):
    lines = text.splitlines()
    clean_lines = [line for line in lines if is_english(line.strip()) and line.strip() != '']
    text = "\n".join(clean_lines)

    job = {
        "date": date,
        "job_title": None,
        "organization": None,
        "location": None,
        "tags": [],
        "experience": None,
        "salary": None,
        "quantity_required": None,
        "gender": None,
        "deadline": None,
        "how_to_apply": None,
        "category": None,
        "raw_text": text
    }

    if clean_lines:
        job["job_title"] = clean_lines[0].strip()

    tags = re.findall(r"#\w+", text)
    job["tags"] = ", ".join(tags)

    if len(tags) >= 2:
        job["organization"] = tags[0].replace("#", "").replace("_", " ").title()
        job["location"] = tags[-1].replace("#", "").replace("_", " ").title()

    exp_match = re.search(r"#(\d+)_years", text)
    if exp_match:
        job["experience"] = exp_match.group(1)

    qty_match = re.search(r"Quanitity Required: (\d+)", text)
    if qty_match:
        job["quantity_required"] = qty_match.group(1)

    salary_match = re.search(r"Salary:\s*([\d,\.]+)", text)
    if salary_match:
        job["salary"] = salary_match.group(1)

    gender_match = re.search(r"Required Gender: ([^\n]+)", text)
    if gender_match:
        job["gender"] = gender_match.group(1).strip()

    deadline_match = re.search(r"Deadline:\s*(.*)", text)
    if deadline_match:
        job["deadline"] = deadline_match.group(1).strip()

    apply_match = re.search(r"How To Apply:\s*(.*)", text)
    if apply_match:
        job["how_to_apply"] = apply_match.group(1).strip()

    # ✅ Add category logic here
    for tag in tags:
        keyword = tag.lower().replace("#", "")
        if keyword in CATEGORY_KEYWORDS:
            job["category"] = CATEGORY_KEYWORDS[keyword]
            break

    return job



# Load environment variables from .env
load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE')
channel_username = '@hahujobsforfreshgraduates'

# Check if environment variables are loaded
if not all([api_id, api_hash, phone]):
    print("❌ Missing API_ID, API_HASH, or PHONE in .env file.")
    exit()

# Create the Telegram client
client = TelegramClient('job_scraper', api_id, api_hash)

async def scrape_channel():
    try:
        print("🔌 Connecting to Telegram...")
        await client.start(phone)

        if not await client.is_user_authorized():
            print("⚠️ Please check your phone for a Telegram login code.")
            return

        print("✅ Successfully connected to Telegram.")
    except SessionPasswordNeededError:
        print("🔐 Two-step verification is enabled. Please enter your password in code.")
        return
    except Exception as e:
        print(f"❌ Failed to connect to Telegram: {str(e)}")
        return

    try:
        print(f"🔍 Accessing channel: {channel_username}")
        channel = await client.get_entity(channel_username)
    except Exception as e:
        print(f"❌ Failed to access channel: {str(e)}")
        return

    all_messages = []
    offset_id = 0
    limit = 100
    total_messages = 0
    total_count = 1000  # Adjust as needed

    print("📥 Starting message scraping...\n")
    while total_messages < total_count:
        print(f"\r⏳ Scraped {total_messages}/{total_count} messages...", end="", flush=True)

        try:
            history = await client(GetHistoryRequest(
                peer=channel,
                limit=limit,
                offset_date=None,
                offset_id=offset_id,
                max_id=0,
                min_id=0,
                add_offset=0,
                hash=0
            ))
        except Exception as e:
            print(f"\n❌ Error while fetching history: {str(e)}")
            break

        if not history.messages:
            print("\n✅ No more messages to scrape.")
            break

        messages = history.messages
        for message in messages:
            if hasattr(message, 'message') and message.message:
                all_messages.append({
                    'date': message.date,
                    'text': message.message,
                    'views': getattr(message, 'views', None)
                })

        total_messages += len(messages)
        offset_id = messages[-1].id
        await asyncio.sleep(1)  # Avoid rate limiting

            # After all messages are collected
    structured_jobs = []

    for msg in all_messages:
        parsed = parse_message(msg["text"], msg["date"])
        structured_jobs.append(parsed)

    df_clean = pd.DataFrame(structured_jobs)
    df_clean.to_csv("../data/structured_telegram_jobs.csv", index=False)
    print("✅ Structured data saved to structured_telegram_jobs.csv")


    # Save results to CSV
    df = pd.DataFrame(all_messages)
    df.to_csv('../data/telegram_jobs.csv', index=False)
    print(f"\n✅ Successfully scraped {len(all_messages)} messages to telegram_jobs.csv")
    

# Run the async function
if __name__ == "__main__":
    asyncio.run(scrape_channel())

def is_english(text):
    """Returns True if all characters in text are ASCII (English)."""
    return all(ord(char) < 128 for char in text)

def parse_message(text, date):
    # Remove non-English lines
    lines = text.splitlines()
    clean_lines = [line for line in lines if is_english(line.strip()) and line.strip() != '']
    text = "\n".join(clean_lines)

    job = {
        "date": date,
        "job_title": None,
        "organization": None,
        "location": None,
        "tags": [],
        "experience": None,
        "salary": None,
        "quantity_required": None,
        "gender": None,
        "deadline": None,
        "how_to_apply": None,
        "raw_text": text
    }

    # Extract title (first line)
    if clean_lines:
        job["job_title"] = clean_lines[0].strip()

    # Extract tags
    tags = re.findall(r"#\w+", text)
    job["tags"] = ", ".join(tags)
    
    # Organization & Location (next few tags after job title)
    if len(tags) >= 2:
        job["organization"] = tags[0].replace("#", "").replace("_", " ").title()
        job["location"] = tags[-1].replace("#", "").replace("_", " ").title()

    # Experience
    exp_match = re.search(r"#(\d+)_years", text)
    if exp_match:
        job["experience"] = exp_match.group(1)

    # Quantity
    qty_match = re.search(r"Quanitity Required: (\d+)", text)
    if qty_match:
        job["quantity_required"] = qty_match.group(1)

    # Salary
    salary_match = re.search(r"Salary:\s*([\d,\.]+)", text)
    if salary_match:
        job["salary"] = salary_match.group(1)

    # Gender
    gender_match = re.search(r"Required Gender: ([^\n]+)", text)
    if gender_match:
        job["gender"] = gender_match.group(1).strip()

    # Deadline
    deadline_match = re.search(r"Deadline:\s*(.*)", text)
    if deadline_match:
        job["deadline"] = deadline_match.group(1).strip()

    # How to apply
    apply_match = re.search(r"How To Apply:\s*(.*)", text)
    if apply_match:
        job["how_to_apply"] = apply_match.group(1).strip()


    return job
