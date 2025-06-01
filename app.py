import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# App title
st.title("🔎 Smart Web Scraper")

# URL input
url = st.text_input("Enter a website URL to scrape:", "https://example.com")

if st.button("Scrape"):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract data (customize as needed)
        data = []
        for i, paragraph in enumerate(soup.find_all("p"), start=1):
            text = paragraph.get_text(strip=True)
            if text:
                data.append({"Index": i, "Text": text})

        if data:
            df = pd.DataFrame(data)

            # Display markdown table
            st.markdown("### 📄 Scraped Data (Markdown Table)")
            st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)

            # Download JSON
            json_data = json.dumps(data, indent=4)
            st.download_button("⬇ Download JSON", json_data, file_name="scraped_data.json", mime="application/json")

            # Download CSV
            csv_data = df.to_csv(index=False)
            st.download_button("⬇ Download CSV", csv_data, file_name="scraped_data.csv", mime="text/csv")

        else:
            st.warning("No paragraph content found on this page.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
