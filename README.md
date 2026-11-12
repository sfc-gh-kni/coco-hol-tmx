# TMX CoCo hands-on lab guide

Attendee guide for a two-hour virtual lab that uses Cortex Code (CoCo) in Snowsight. Each attendee picks their team and initials in the sidebar, creates their own Apache Iceberg table of 2026 US stock prices from Snowflake Curated Data (Free) in their team's database and S3 external volume, then explores it, writes and validates SQL, and builds and deploys a Streamlit in Snowflake app over it.

Team object names are generated in `components.py` from the `DEV_EDX_HACKATHONTOR_` / `DEV_HACKATHONTOR_` prefixes.

This repo holds only the public, attendee-facing instructions. It contains no credentials, account details or data.

Run locally:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
