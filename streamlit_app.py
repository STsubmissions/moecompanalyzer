import streamlit as st
import os

st.set_page_config(page_title="Improved Competitor Analyzer", layout="wide")

st.title("Improved Competitor Analyzer")
st.markdown("Enter the prospect website URL and upload a text file containing your keywords (one keyword per line) to run the competitor analysis.")

try:
    import pandas as pd
    from improved_competitor_analyzer import ImprovedCompetitorAnalyzer
except ImportError as e:
    st.error(f"Failed to import required modules: {str(e)}")
    st.stop()

# Input fields
prospect_website = st.text_input("Prospect Website URL", placeholder="https://www.example.com")
keywords_file = st.file_uploader("Upload Keywords File (.txt)", type=["txt"])

# Get API keys from environment variables or Streamlit secrets
valueserp_api_key = os.getenv("VALUESERP_API_KEY") or st.secrets.get("VALUESERP_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not valueserp_api_key or not openai_api_key:
    st.error("API keys are missing. Please set VALUESERP_API_KEY and OPENAI_API_KEY in your environment variables or Streamlit secrets.")
    st.stop()

def run_analysis(prospect_website, keywords_file):
    analyzer = ImprovedCompetitorAnalyzer(valueserp_api_key, openai_api_key, prospect_website)
    
    keywords = [line.decode('utf-8').strip() for line in keywords_file.readlines() if line.strip()]
    
    if not keywords:
        st.error("No keywords found in the uploaded file. Please check the file content.")
        return None
    
    report = analyzer.run_analysis(keywords, location="United States")
    
    if report.empty:
        st.warning("Analysis completed, but no data was returned. This might indicate an issue with the API responses or data processing.")
        return None
    
    return report

# Run analysis button
if st.button("Run Analysis"):
    if not prospect_website or not keywords_file:
        st.error("Please provide both the prospect website URL and keywords file.")
    else:
        with st.spinner("Running analysis..."):
            try:
                result = run_analysis(prospect_website, keywords_file)
                if result is not None:
                    st.success("Analysis complete!")
                    st.dataframe(result)
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")

# Add information about required API keys
st.sidebar.header("API Keys")
st.sidebar.info("This app requires valid ValueSERP and OpenAI API keys. Please ensure these are set in your Streamlit secrets or as environment variables.")

if __name__ == "__main__":
    st.sidebar.markdown("---")
    st.sidebar.markdown("Created with Streamlit")
