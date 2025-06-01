import streamlit as st
import subprocess
import json
import pandas as pd
import os
import re
from datetime import datetime

# Set page config first
st.set_page_config(page_title="🕷️ Smart Web Scraper", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.title("Smart Web Scraper By Wajahat Hussain")
    st.markdown("""
        **Smart Web Scraper** is a powerful and intuitive tool designed to help you
        extract data from websites with ease. Simply provide a URL, and our intelligent
        scraper will fetch the content, presenting it in a structured format (CSV or JSON)
        for your analysis and use.

        This application streamlines the process of web data collection, making it
        accessible even for those without extensive programming knowledge.
        """)
    st.markdown("---")
    st.markdown(f"""
        <div style="text-align: center; font-size: small; color: grey;">
            <p>Developed by Wajahat Hussain</p>
            <p>Team CodePulse Innovations</p>
            <p>&copy; {datetime.now().year} Smart Web Scraper. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)

# --- Main UI ---
st.title("🕷️ Smart Web Scraper Dashboard")

url = st.text_input("🌐 Enter the URL to scrape", "https://quotes.toscrape.com/")
format_option = st.radio("📁 Select output format", ["CSV", "JSON"], horizontal=True)

if st.button("🔄 Run Scraper"):
    with st.spinner("Running Scrapy spider..."):
        # Make sure outputs directory exists
        os.makedirs("outputs", exist_ok=True)

        # Run the scraper script
        result = subprocess.run(
            ["python", "website_scraper.py", url],
            capture_output=True,
            text=True
        )

        # Hide the stderr logs by commenting these lines out
        # st.subheader("📄 Scraper stderr")
        # st.code(result.stderr)

        if result.returncode != 0:
            st.error("❌ Scraper failed to run.")
        else:
            # Try to get the JSON path from stdout
            output_file = result.stdout.strip().replace("\\", "/").replace("\n", "").replace("\r", "")

            if not os.path.isfile(output_file):
                st.error(f"❌ Output file not found.\n\n{output_file}")
            else:
                st.success(f"✅ Scraping finished! File: `{output_file}`")

                with open(output_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                df = pd.json_normalize(data)

                # Optional search bar
                search = st.text_input("🔍 Search text in page title or URL")
                if search:
                    df = df[df['title'].str.contains(search, case=False, na=False) |
                            df['url'].str.contains(search, case=False, na=False)]

                st.dataframe(df, use_container_width=True)

                # --- Download buttons ---
                if format_option == "CSV":
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇️ Download CSV", csv, os.path.basename(output_file).replace(".json", ".csv"), "text/csv")
                else:
                    json_str = json.dumps(data, indent=2)
                    st.download_button("⬇️ Download JSON", json_str, os.path.basename(output_file), "application/json")
