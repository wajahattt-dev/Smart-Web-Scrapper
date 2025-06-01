import streamlit as st
import json
from website_scraper import run_scraper

st.title("🌐 Universal Web Scraper")

url = st.text_input("Enter a URL to scrape (public site only)")

if st.button("Scrape"):
    try:
        output_file = run_scraper(url)
        with open(output_file, "r") as f:
            data = json.load(f)
        if data:
            st.success("✅ Scraping successful!")
            st.json(data[0])  # Display first item only
        else:
            st.warning("⚠️ No data found or site may be protected.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
