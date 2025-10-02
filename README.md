# Resume Screening with NLP

This project implements an NLP-based resume screening system that matches candidate resumes with job descriptions. It uses TF-IDF vectorization and cosine similarity to rank candidates based on how well their resumes match a given job description.

## Enhanced Accuracy Features

The system now includes several improvements for better matching accuracy:

1. **Advanced TF-IDF Vectorization**:
   - Uses n-grams (1-2 word combinations) for better context understanding
   - Sublinear TF scaling to reduce bias toward longer documents
   - Improved stopword handling and preprocessing

2. **Multi-Metric Scoring**:
   - Combines cosine similarity (60% weight), Euclidean distance (20% weight), and custom text matching (20% weight)
   - More nuanced decision making with three categories: Fit, Potential Fit, Not Fit

3. **Enhanced Skill Extraction**:
   - Comprehensive database of 100+ technical and soft skills
   - **Sophisticated pattern matching** to avoid false positives
   - **Section-based extraction** that focuses on actual skill sections
   - **Word boundary matching** to ensure precise skill identification
   - **Context-aware matching** that considers where skills are mentioned

4. **Improved Text Preprocessing**:
   - POS tagging for more accurate lemmatization
   - Advanced tokenization and normalization

## Features

- Extract text from PDF and DOCX resume files
- Clean and preprocess text using NLTK and SpaCy
- Represent job descriptions and resumes using TF-IDF embeddings
- Calculate cosine similarity scores between job descriptions and resumes
- Rank candidates based on their similarity scores
- Identify top skills and missing skills for each candidate
- Simple Streamlit web interface for easy use
- Export results to CSV

## Installation

### Option 1: Using the installation script (Windows)

Double-click on `install_deps.bat` to automatically install all dependencies.

### Option 2: Manual installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Download required NLTK data:
   ```
   python -m nltk.downloader stopwords punkt wordnet averaged_perceptron_tagger
   ```
4. Download SpaCy model:
   ```
   python -m spacy download en_core_web_sm
   ```

## Usage

### Option 1: Using the run script (Windows)

Double-click on `run_app.bat` to start the application.

### Option 2: Manual execution

Run the Streamlit app:
```
streamlit run app.py
```

Or if streamlit is not in your PATH:
```
python -m streamlit run app.py
```

After running the command, open your browser and go to http://localhost:8501

## Project Structure

- `app.py`: Main Streamlit application
- `resume_parser.py`: Handles text extraction from PDF/DOCX files
- `text_processor.py`: Text cleaning and preprocessing functions
- `matcher.py`: TF-IDF vectorization and similarity matching
- `utils.py`: Utility functions for skills extraction and analysis
- `requirements.txt`: List of required Python packages
- `install_deps.bat`: Windows batch script to install dependencies
- `run_app.bat`: Windows batch script to run the application
- `verify_installation.py`: Script to verify all dependencies are installed
- `verify_accuracy.py`: Script to verify enhanced accuracy features
- `verify_skill_extraction.py`: Script to verify skill extraction accuracy

## How It Works

1. User inputs a job description and uploads multiple resumes
2. Text is extracted from all documents
3. Text is cleaned and preprocessed with advanced NLP techniques
4. TF-IDF vectors are created for the job description and all resumes
5. Multiple similarity metrics are calculated and combined for accuracy
6. Candidates are ranked by their composite similarity scores
7. Top skills and missing skills are identified for each candidate using sophisticated pattern matching
8. Results are displayed in a table and can be exported to CSV

## Sample Data

The project includes sample data files:

- `sample_jd.txt`: Sample job description

## Troubleshooting

If you encounter any issues:

1. Run `verify_installation.py` to check if all dependencies are properly installed
2. Run `verify_accuracy.py` to check if enhanced accuracy features are working
3. Run `verify_skill_extraction.py` to check if skill extraction is working correctly
4. Make sure you have Python 3.7 or higher installed
5. Ensure all required packages are installed by running `pip install -r requirements.txt`
6. If SpaCy model download fails, try running `python -m spacy download en_core_web_sm` as administrator

## Recent Improvements

### Fixed False Positive Skill Extraction (v2.2)
- **Problem**: Skills were being incorrectly extracted from names and unrelated text
- **Solution**: Implemented sophisticated section-based extraction and context-aware matching
- **Result**: More accurate skill identification with zero false positives

### Enhanced Skill Matching Accuracy (v2.1)
- **Problem**: Simple substring matching caused false positives
- **Solution**: Added word boundary matching and exact phrase matching
- **Result**: More precise skill identification

## License

This project is licensed under the MIT License - see the LICENSE file for details.