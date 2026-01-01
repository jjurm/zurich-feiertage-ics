from pathlib import Path

from datetime import datetime, date, timezone, timedelta
import uuid

import polars as pl
from icalendar import Calendar, Event

# Take PDFs from the 'Feiertage' section of
# https://www.zh.ch/de/arbeiten-beim-kanton/rund-um-die-arbeitszeit.html
# and convert them to CSVs using prompts/pdfs_to_csv.txt

# Load the CSV files
assets_dir = Path("assets")
csv_files = sorted(assets_dir.glob("zurich_holidays_*.csv"))

holidays_df = pl.concat(
    [pl.read_csv(csv_file) for csv_file in csv_files],
    how="vertical",
)

# Create a new calendar
cal = Calendar()
cal.add("prodid", "-//zurich-feiertage-ics//")
cal.add("version", "2.0")
cal.add("calscale", "GREGORIAN")
cal.add("x-wr-calname", "Zurich Holidays")

# Populate the calendar with events
for row in holidays_df.to_dicts():
    event = Event()

    summary = row["name"]
    description = row["description"]

    # Add type-specific details to the event title and description
    if row["type"] == "Half day":
        summary += " (Half Day)"
        description = "Half Day holiday.\n\n" + description
    elif row["type"] == "Quarter day":
        summary += " (Quarter Day)"
        description = "Quarter Day holiday.\n\n" + description

    event.add("summary", summary)
    event.add("description", description)

    # All-day event: DTSTART/DTEND as DATE (DTEND is exclusive, so add 1 day)
    start: date = datetime.strptime(row["date"], "%Y-%m-%d").date()
    event.add("dtstart", start)
    event.add("dtend", start + timedelta(days=1))

    # Required / recommended fields
    event.add(
        "uid",
        f"{uuid.uuid5(uuid.NAMESPACE_URL, f'{start.isoformat()}|{summary}')}@zurich-feiertage-ics",
    )
    event.add("dtstamp", datetime.now(timezone.utc))

    cal.add_component(event)

# Save the calendar to an ICS file
output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)
ics_output_path = output_dir / "holidays.ics"

# icalendar outputs bytes
ics_bytes = cal.to_ical()
ics_output_path.write_bytes(ics_bytes)

print(f"ICS file has been saved to {ics_output_path}")
