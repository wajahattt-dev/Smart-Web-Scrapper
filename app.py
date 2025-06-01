import streamlit as st
import subprocess
import json
import pandas as pd
import os
from datetime import datetime
import traceback

# Set page config first
st.set_page_config(page_title="🕷️ Smart Web Scraper", layout="wide")

# Sidebar and UI code here (same as before) ...

st.title("🕷️ Smart Web Scraper Dashboard")

url = st.text_input("🌐 Enter the URL to scrape", "https://quotes.toscrape.com/")
format_option = st.radio("📁 Select output format", ["CSV", "JSON"], horizontal=True)

if st.button("🔄 Run Scraper"):
    with st.spinner("Running Scrapy spider..."):
        try:
            # Run the scraper script as a subprocess and pass the URL
            result = subprocess.run(
                ["python3", "website_scraper.py", url],
                capture_output=True,
                text=True,
                check=True
            )

            output_file = result.stdout.strip()

            if not os.path.isfile(output_file):
                st.error(f"❌ Output file not found.\n\n{output_file}")
            else:
                st.success(f"✅ Scraping finished! File: `{output_file}`")

                with open(output_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                df = pd.json_normalize(data)

                search = st.text_input("🔍 Search text in quote or author")
                if search:
                    df = df[df['text'].str.contains(search, case=False, na=False) |
                            df['author'].str.contains(search, case=False, na=False)]

                st.dataframe(df, use_container_width=True)

                if format_option == "CSV":
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇️ Download CSV", csv, os.path.basename(output_file).replace(".json", ".csv"), "text/csv")
                else:
                    json_str = json.dumps(data, indent=2)
                    st.download_button("⬇️ Download JSON", json_str, os.path.basename(output_file), "application/json")

        except subprocess.CalledProcessError as e:
            st.error(f"❌ Scraper failed to run.\n{e.stderr}")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.text("Full traceback:")
            st.code(traceback.format_exc())
