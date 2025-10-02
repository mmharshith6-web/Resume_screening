@echo off
echo Installing dependencies for Resume Screening with NLP...
echo.
pip install -r requirements.txt
echo.
echo Downloading NLTK data...
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
echo.
echo Downloading SpaCy model...
python -m spacy download en_core_web_sm
echo.
echo Installation complete!
pause