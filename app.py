import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

st.set_page_config(page_title="Smart Web Scraper", layout="wide")
st.title("🔍 Smart Web Scraper")

# URL input
url = st.text_input("Enter the URL to scrape", "https://example.com")

# Scrape button
if st.button("Scrape"):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        data = []

        # Extract text content
        for tag in soup.find_all(["p", "span", "div"]):
            text = tag.get_text(strip=True)
            if text:
                data.append({
                    "Type": "Text",
                    "Content": text,
                    "Tag": tag.name,
                    "Attribute": "",
                    "URL": ""
                })

        # Extract links
        for link in soup.find_all("a", href=True):
            data.append({
                "Type": "Link",
                "Content": link.get_text(strip=True),
                "Tag": "a",
                "Attribute": "href",
                "URL": link["href"]
            })

        # Extract images
        for img in soup.find_all("img", src=True):
            alt = img.get("alt", "")
            data.append({
                "Type": "Image",
                "Content": alt,
                "Tag": "img",
                "Attribute": "src",
                "URL": img["src"]
            })

        # Extract headings
        for level in range(1, 7):
            for heading in soup.find_all(f"h{level}"):
                text = heading.get_text(strip=True)
                if text:
                    data.append({
                        "Type": f"Heading h{level}",
                        "Content": text,
                        "Tag": f"h{level}",
                        "Attribute": "",
                        "URL": ""
                    })

        if data:
            df = pd.DataFrame(data)

            st.markdown("### 🧾 Scraped Data (Markdown Table)")
            st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)

            # JSON download
            json_data = json.dumps(data, indent=4)
            st.download_button("⬇ Download JSON", json_data, file_name="scraped_data.json", mime="application/json")

            # CSV download
            csv_data = df.to_csv(index=False)
            st.download_button("⬇ Download CSV", csv_data, file_name="scraped_data.csv", mime="text/csv")
        else:
            st.warning("No content was extracted from the page.")

    except Exception as e:
        st.error(f"Error during scraping: {e}")
