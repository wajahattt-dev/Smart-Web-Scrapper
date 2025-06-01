import streamlit as st
import subprocess
import json
import pandas as pd
import os
import sys
import traceback

st.set_page_config(page_title="Smart Web Scraper", layout="wide")

st.title("🕷️ Smart Web Scraper")
st.write("Enter a URL to scrape data from it.")

url = st.text_input("🔗 Enter Website URL", placeholder="https://quotes.toscrape.com")

format_option = st.selectbox("📄 Choose download format", ("JSON", "CSV"))

if st.button("🔄 Run Scraper"):
    with st.spinner("Scraping in progress..."):
        try:
            # Run the scraper in a separate subprocess
            result = subprocess.run(
                [sys.executable, "website_scraper.py", url],
                capture_output=True,
                text=True,
                check=True
            )

            output_file = result.stdout.strip()

            if not os.path.exists(output_file):
                st.error("❌ Scraper completed but output file not found.")
            else:
                st.success(f"✅ Scraping finished! Download or view the data below.")

                # Load and display data
                with open(output_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                df = pd.json_normalize(data)

                search = st.text_input("🔍 Search in text or author")
                if search:
                    df = df[df['text'].str.contains(search, case=False, na=False) |
                            df['author'].str.contains(search, case=False, na=False)]

                st.dataframe(df, use_container_width=True)

                if format_option == "CSV":
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇️ Download CSV", csv, output_file.replace(".json", ".csv"), "text/csv")
                else:
                    json_str = json.dumps(data, indent=2)
                    st.download_button("⬇️ Download JSON", json_str, output_file, "application/json")

        except subprocess.CalledProcessError as e:
            st.error("❌ Scraper failed to run.")
            st.code(e.stderr)
        except Exception as e:
            st.error("❌ An unexpected error occurred.")
            st.code(traceback.format_exc())
