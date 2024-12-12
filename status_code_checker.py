import streamlit as st
import pandas as pd
import requests
from io import StringIO

def main():
    st.title("URL Status Code Checker")

    # Step 1: File Upload
    st.header("Step 1: Upload Your CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Step 2: Read URLs from the uploaded CSV
        st.header("Step 2: Processing URLs")
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")
            return

        # Use the first column as URLs
        first_column_name = df.columns[0]
        urls = df[first_column_name]

        # Step 3: Check status codes
        status_codes = []
        progress_bar = st.progress(0)
        for i, url in enumerate(urls):
            try:
                response = requests.get(url, timeout=10)
                status_codes.append(response.status_code)
            except requests.exceptions.RequestException as e:
                status_codes.append("Error")

            # Update progress bar
            progress_bar.progress((i + 1) / len(urls))

        # Step 4: Add status codes to DataFrame
        df['Status_Code'] = status_codes

        # Step 5: Display results
        st.header("Step 3: Results")
        st.dataframe(df)

        # Step 6: Download results
        st.header("Step 4: Download Results")
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV with Status Codes",
            data=csv,
            file_name="url_status_codes.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
