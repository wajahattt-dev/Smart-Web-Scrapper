import streamlit as st
import pandas as pd
import json
from io import StringIO, BytesIO

# Sample data
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 22],
    "Country": ["USA", "UK", "Canada"]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Title
st.title("📊 Display and Download JSON/CSV Data")

# --- Display Markdown Table ---
st.subheader("📋 Data as Markdown Table")
markdown_table = df.to_markdown(index=False)
st.markdown(f"```markdown\n{markdown_table}\n```")

# --- Download Buttons ---

# CSV Download
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
csv_bytes = csv_buffer.getvalue().encode('utf-8')
st.download_button(
    label="⬇️ Download CSV",
    data=csv_bytes,
    file_name="data.csv",
    mime="text/csv"
)

# JSON Download
json_str = df.to_json(orient="records", indent=2)
json_bytes = json_str.encode('utf-8')
st.download_button(
    label="⬇️ Download JSON",
    data=json_bytes,
    file_name="data.json",
    mime="application/json"
)
