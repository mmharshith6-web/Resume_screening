import streamlit as st
import pandas as pd
import os
import tempfile
from resume_parser import parse_resume
from text_processor import preprocess_text, extract_skills_advanced
from matcher import ResumeMatcher
from utils import save_results_to_csv

# Set page configuration
st.set_page_config(
    page_title="Resume Screening with NLP",
    page_icon="📄",
    layout="wide"
)

# App title
st.title("📄 Resume Screening with NLP")
st.markdown("---")

# Sidebar for job description input
st.sidebar.header("Job Description")
jd_text = st.sidebar.text_area("Enter the job description:", height=300)

# Sidebar for resume uploads
st.sidebar.header("Upload Resumes")
uploaded_files = st.sidebar.file_uploader(
    "Upload resume files (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

# Process button
if st.sidebar.button("Process Resumes", type="primary"):
    if not jd_text:
        st.error("Please enter a job description.")
    elif not uploaded_files:
        st.error("Please upload at least one resume.")
    else:
        with st.spinner("Processing resumes... This may take a moment for accurate analysis."):
            try:
                # Preprocess job description
                processed_jd = preprocess_text(jd_text)
                
                # Parse and preprocess resumes
                resumes_data = []
                temp_files = []
                
                for uploaded_file in uploaded_files:
                    # Create a temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        temp_file_path = tmp_file.name
                        temp_files.append(temp_file_path)
                    
                    # Parse resume
                    resume_data = parse_resume(temp_file_path)
                    
                    # Preprocess resume text
                    processed_text = preprocess_text(resume_data['text'])
                    resume_data['text'] = processed_text
                    
                    resumes_data.append(resume_data)
                
                # Match resumes with enhanced accuracy
                matcher = ResumeMatcher()
                matcher.fit_job_description(processed_jd)
                results = matcher.match_resumes(resumes_data)
                
                # Display results
                st.subheader("Matching Results")
                if results:
                    # Convert to DataFrame for better display
                    df = pd.DataFrame(results)
                    # Format score as percentage
                    df['score'] = df['score'].apply(lambda x: f"{x*100:.2f}%")
                    
                    # Display detailed scores in expander
                    with st.expander("View Detailed Scoring Information"):
                        st.write("The matching score is calculated using a combination of:")
                        st.markdown("""
                        - **Cosine Similarity** (60% weight): Measures textual similarity
                        - **Euclidean Distance** (20% weight): Measures vector distance
                        - **Custom Text Similarity** (20% weight): Keyword and phrase matching
                        """)
                        st.write("Decision criteria:")
                        st.markdown("""
                        - **Fit**: Score > 50%
                        - **Potential Fit**: Score 30-50%
                        - **Not Fit**: Score < 30%
                        """)
                    
                    # Display as table
                    st.dataframe(df, use_container_width=True)
                    
                    # Save to CSV
                    csv_filename = save_results_to_csv(results, "matching_results.csv")
                    
                    # Download button
                    with open(csv_filename, "rb") as file:
                        st.download_button(
                            label="Download Results as CSV",
                            data=file,
                            file_name="resume_matching_results.csv",
                            mime="text/csv"
                        )
                else:
                    st.warning("No matching results found.")
                
                # Clean up temporary files
                for temp_file in temp_files:
                    if os.path.exists(temp_file):
                        os.unlink(temp_file)
                        
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
else:
    # Show instructions
    st.info("👈 Enter a job description and upload resumes to get started!")
    
    # Show sample data section
    with st.expander("View Sample Data Format"):
        st.markdown("""
        ### Job Description Example:
        ```
        Data Scientist
        We are looking for a Data Scientist to join our team. The ideal candidate will have experience with machine learning, statistical analysis, and data visualization. Responsibilities include developing predictive models, analyzing large datasets, and communicating insights to stakeholders.
        
        Requirements:
        - Bachelor's degree in Computer Science, Statistics, or related field
        - 3+ years of experience in data science
        - Proficiency in Python and SQL
        - Experience with machine learning frameworks (TensorFlow, PyTorch)
        - Strong analytical and problem-solving skills
        - Excellent communication skills
        ```
        
        ### Supported Resume Formats:
        - PDF (.pdf)
        - Word Documents (.docx)
        """)
        
    # Show accuracy improvements
    with st.expander("View Enhanced Accuracy Features"):
        st.markdown("""
        ### Improved Matching Accuracy:
        - **Advanced TF-IDF Vectorization**: Uses n-grams and sublinear TF scaling
        - **Multi-Metric Scoring**: Combines cosine similarity, Euclidean distance, and custom text matching
        - **Enhanced Skill Extraction**: Comprehensive skill database with 100+ technical skills
        - **Better Text Preprocessing**: POS tagging and improved lemmatization
        - **Nuanced Decision Making**: Three-tier decision system (Fit/Potential Fit/Not Fit)
        """)