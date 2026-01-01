# zurich-feiertage-ics

Publishes an iCalendar (`.ics`) feed with public holidays for Zurich (Kanton Zürich), ready to import/subscribe in Google Calendar (and other calendar apps).

## Use in Google Calendar

**Subscribe by URL** to keep holidays updated automatically (don’t download/import the file):

- Google Calendar → **Other calendars** → **+** → **From URL**
- Use https://raw.githubusercontent.com/jjurm/zurich-feiertage-ics/refs/heads/main/output/holidays.ics

## Add a new year

The generator auto-discovers all files matching `assets/zurich_holidays_<year>.csv`.
To add another year, just drop in a new CSV with that naming scheme.

1. Download the `Feiertage YYYY` PDF from:
   https://www.zh.ch/de/arbeiten-beim-kanton/rund-um-die-arbeitszeit.html
2. Convert the PDF to CSV using the prompt in `prompts/pdfs_to_csv.txt`.
   - Save it as `assets/zurich_holidays_<year>.csv`
   - Columns: `date,name,type,time,description`
3. Regenerate the calendar:

    ```sh
    pixi run generate-ics
    ```
