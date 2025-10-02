"""
Script to verify that all dependencies are properly installed
"""
import sys

def check_import(module_name):
    try:
        __import__(module_name)
        print(f"✓ {module_name} - OK")
        return True
    except ImportError as e:
        print(f"✗ {module_name} - MISSING ({e})")
        return False

def main():
    print("Checking Resume Screening with NLP dependencies...")
    print("=" * 50)
    
    # List of required modules
    modules = [
        "streamlit",
        "pandas",
        "numpy",
        "sklearn",
        "nltk",
        "spacy",
        "PyPDF2",
        "docx2txt",
        "docx"
    ]
    
    # Special handling for docx (it's actually python-docx)
    def check_docx():
        try:
            from docx import Document
            print("✓ docx (python-docx) - OK")
            return True
        except ImportError:
            print("✗ docx (python-docx) - MISSING")
            return False
    
    # Check each module
    all_good = True
    for module in modules:
        # Special handling for docx
        if module == "docx":
            if not check_docx():
                all_good = False
        else:
            if not check_import(module):
                all_good = False
    
    # Check NLTK data
    try:
        import nltk
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            nltk.data.find('corpora/wordnet')
            print("✓ NLTK data - OK")
        except LookupError:
            # Try to download if not found
            print("⚠ NLTK data - NOT FOUND, attempting to download...")
            try:
                nltk.download('punkt')
                nltk.download('stopwords')
                nltk.download('wordnet')
                print("✓ NLTK data - DOWNLOADED SUCCESSFULLY")
            except Exception as e:
                print(f"✗ NLTK data - DOWNLOAD FAILED ({e})")
                all_good = False
    except ImportError:
        print("✗ NLTK - MISSING")
        all_good = False
    
    # Check SpaCy model
    try:
        import spacy
        spacy.load("en_core_web_sm")
        print("✓ SpaCy en_core_web_sm model - OK")
    except (OSError, ImportError):
        print("✗ SpaCy en_core_web_sm model - MISSING (run 'python -m spacy download en_core_web_sm')")
        all_good = False
    
    print("=" * 50)
    if all_good:
        print("All dependencies are properly installed! You're ready to run the application.")
    else:
        print("Some dependencies are missing. Please install them before running the application.")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)