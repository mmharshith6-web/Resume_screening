"""
Check if all required packages are installed
"""
packages = [
    'nltk',
    'spacy',
    'sklearn',
    'pandas',
    'numpy',
    'PyPDF2',
    'docx2txt',
    'streamlit'
]

print("Checking required packages...")
print("=" * 40)

for package in packages:
    try:
        __import__(package)
        print(f"✓ {package} - OK")
    except ImportError as e:
        print(f"✗ {package} - MISSING ({e})")

print("\nChecking NLTK data...")
try:
    import nltk
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
        nltk.data.find('corpora/wordnet')
        print("✓ NLTK data - OK")
    except LookupError:
        print("✗ NLTK data - MISSING")
except ImportError:
    print("✗ NLTK - MISSING")

print("\nChecking SpaCy model...")
try:
    import spacy
    try:
        spacy.load("en_core_web_sm")
        print("✓ SpaCy en_core_web_sm model - OK")
    except OSError:
        print("✗ SpaCy en_core_web_sm model - MISSING")
except ImportError:
    print("✗ SpaCy - MISSING")