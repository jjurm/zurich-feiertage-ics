from pathlib import Path

from ics import Calendar, Event
from datetime import datetime
import pandas as pd

# Take PDFs from
# https://www.zh.ch/de/arbeiten-beim-kanton/rund-um-die-arbeitszeit.html
# and convert them to CSVs using prompts/pdfs_to_csv.txt

# Load the CSV files
assets_dir = Path("assets")
csv_files = [
    assets_dir / f"zurich_holidays_{year}.csv"
    for year in [2024, 2025]
]
holidays_df = pd.concat(
    pd.read_csv(csv_file) for csv_file in csv_files
)

# Create a new calendar
cal = Calendar()

# Populate the calendar with events
for _, row in holidays_df.iterrows():
    event = Event()
    event.name = row['name']

    # Add type-specific details to the event title and description
    if row['type'] == "Half day":
        event.name += " (Half Day)"
        event.description = "Half Day holiday.\nn" + row['description']
    elif row['type'] == "Quarter day":
        event.name += " (Quarter Day)"
        event.description = "Quarter Day holiday.\n\n" + row['description']
    else:
        event.description = row['description']

    # Set the event as full-day
    event.begin = datetime.strptime(row['date'], "%Y-%m-%d").date()
    event.make_all_day()

    # Add the event to the calendar
    cal.events.add(event)

# Save the calendar to an ICS file
output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)
ics_output_path = output_dir / "holidays.ics"
with open(ics_output_path, "w") as f:
    f.writelines(cal)

print(f"ICS file has been saved to {ics_output_path}")
