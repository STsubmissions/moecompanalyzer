# File: app.py
import os
import gradio as gr
from improved_competitor_analyzer import ImprovedCompetitorAnalyzer

valueserp_api_key = os.getenv("VALUESERP_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

def run_analysis(prospect_website, keywords_file):
    analyzer = ImprovedCompetitorAnalyzer(valueserp_api_key, openai_api_key, prospect_website)
    
    keywords = [line.decode('utf-8').strip() for line in keywords_file.readlines() if line.strip()]
    
    if not keywords:
        return "No keywords found in the uploaded file. Please check the file content."
    
    report = analyzer.run_analysis(keywords, location="United States")
    
    if report.empty:
        return "Analysis completed, but no data was returned. This might indicate an issue with the API responses or data processing."
    
    return report.to_html(index=False)

iface = gr.Interface(
    fn=run_analysis,
    inputs=[
        gr.Textbox(label="Prospect Website URL", placeholder="https://www.example.com"),
        gr.File(label="Upload Keywords File (.txt)", file_types=['.txt'])
    ],
    outputs=gr.HTML(label="Analysis Report"),
    title="Improved Competitor Analyzer",
    description="Enter the prospect website URL and upload a text file containing your keywords (one keyword per line) to run the competitor analysis.",
)

iface.launch()
