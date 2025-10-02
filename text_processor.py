import nltk
import spacy
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter
import string

# Download required NLTK data (run once)
try:
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
except LookupError:
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

# Load SpaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Please install the SpaCy English model: python -m spacy download en_core_web_sm")
    nlp = None

def clean_text(text):
    """Clean and preprocess text"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def tokenize_and_lemmatize(text):
    """Tokenize and lemmatize text using NLTK with POS tagging"""
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords and punctuation
    tokens = [token for token in tokens if token not in stop_words and token not in string.punctuation]
    
    # Lemmatize with POS tagging
    tokens = [lemmatizer.lemmatize(token, get_wordnet_pos(token)) for token in tokens]
    
    return ' '.join(tokens)

def extract_entities_spacy(text):
    """Extract named entities using SpaCy"""
    if nlp is None:
        return []
    
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def preprocess_text(text):
    """Complete text preprocessing pipeline"""
    # Clean text
    cleaned_text = clean_text(text)
    
    # Tokenize and lemmatize
    processed_text = tokenize_and_lemmatize(cleaned_text)
    
    return processed_text

def extract_noun_phrases(text):
    """Extract noun phrases using SpaCy"""
    if nlp is None:
        return []
    
    doc = nlp(text)
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]
    return noun_phrases

def extract_key_terms(text, top_n=20):
    """Extract key terms based on frequency and TF-IDF-like scoring"""
    # Preprocess text
    processed_text = preprocess_text(text)
    
    # Tokenize
    tokens = word_tokenize(processed_text)
    
    # Remove single characters
    tokens = [token for token in tokens if len(token) > 2]
    
    # Count frequency
    freq_dist = Counter(tokens)
    
    # Get top N terms
    top_terms = [term for term, freq in freq_dist.most_common(top_n)]
    
    return top_terms

def extract_skills_advanced(text):
    """Extract skills using a sophisticated approach to avoid false positives"""
    # Common skills keywords (expanded list)
    skill_keywords = [
        # Programming Languages
        'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust', 'scala',
        'r', 'matlab', 'sql', 'typescript', 'dart', 'perl', 'shell', 'bash',
        
        # Web Technologies
        'html', 'css', 'react', 'angular', 'vue', 'node', 'django', 'flask', 'spring', 'express',
        'asp.net', 'jquery', 'bootstrap', 'sass', 'less', 'webpack', 'npm', 'rest', 'graphql',
        
        # Databases
        'mysql', 'postgresql', 'mongodb', 'oracle', 'sql server', 'redis', 'elasticsearch',
        'cassandra', 'firebase', 'dynamodb', 'sqlite',
        
        # Machine Learning & AI
        'machine learning', 'deep learning', 'neural networks', 'tensorflow', 'pytorch', 'keras',
        'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'opencv', 'nltk', 'spacy',
        'computer vision', 'natural language processing', 'reinforcement learning', 'xgboost',
        'data science', 'artificial intelligence', 'data mining', 'predictive modeling',
        
        # Cloud & DevOps
        'aws', 'azure', 'google cloud', 'docker', 'kubernetes', 'jenkins', 'git', 'github',
        'gitlab', 'ci/cd', 'terraform', 'ansible', 'puppet', 'chef', 'openshift', 'heroku',
        'serverless', 'lambda', 'ec2', 's3', 'gcp', 'cloudformation',
        
        # Data & Analytics
        'data analysis', 'data visualization', 'tableau', 'power bi', 'excel', 'statistics',
        'hadoop', 'spark', 'hive', 'pig', 'kafka', 'airflow', 'etl', 'big data',
        
        # Mobile Development
        'android', 'ios', 'flutter', 'react native', 'xamarin', 'ionic', 'cordova',
        
        # Software Engineering
        'agile', 'scrum', 'kanban', 'jira', 'confluence', 'testing', 'unit testing',
        'integration testing', 'test automation', 'selenium', 'junit', 'pytest',
        'object-oriented programming', 'design patterns', 'software architecture',
        'microservices', 'api development', 'debugging', 'refactoring',
        
        # Soft Skills
        'communication', 'leadership', 'teamwork', 'problem solving', 'critical thinking',
        'project management', 'time management', 'adaptability', 'creativity',
        'attention to detail', 'customer service', 'negotiation', 'mentoring'
    ]
    
    # Split text into lines and process each line
    lines = text.lower().split('\n')
    found_skills = []
    
    # Common section headers where skills are listed
    skill_section_indicators = ['skill', 'technical', 'expertise', 'competenc', 'proficienc']
    
    # Look for skill sections
    in_skill_section = False
    skill_lines = []
    
    for line in lines:
        # Check if we're entering a skill section
        if any(indicator in line for indicator in skill_section_indicators):
            in_skill_section = True
            continue
            
        # If we're in a skill section, collect lines until we hit an empty line or new section
        if in_skill_section:
            if line.strip() == '' or any(word in line for word in ['experience', 'education', 'project']):
                in_skill_section = False
            elif line.strip():
                skill_lines.append(line)
    
    # If no skill section found, use the whole text but be more careful
    if not skill_lines:
        # Look for bullet points or lines that look like skills
        for line in lines:
            if line.strip().startswith(('-', '*', '•', '·')) or ':' in line:
                skill_lines.append(line)
        
        # If still nothing, use lines that contain common skill-related words
        if not skill_lines:
            skill_indicators = ['proficient', 'experienced', 'skilled', 'knowledge', 'ability']
            for line in lines:
                if any(indicator in line.lower() for indicator in skill_indicators):
                    skill_lines.append(line)
    
    # If still nothing, use a more restrictive approach on the whole text
    skill_text = ' '.join(skill_lines) if skill_lines else text.lower()
    
    # If we're using the whole text, be extra careful
    if not skill_lines:
        # Add boundaries to avoid matching in names
        skill_text = ' ' + skill_text + ' '
    
    for skill in skill_keywords:
        # Escape special regex characters and add word boundaries
        escaped_skill = re.escape(skill)
        pattern = r'\b' + escaped_skill + r'\b'
        
        # Search for the pattern
        if re.search(pattern, skill_text):
            found_skills.append(skill)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_skills = []
    for skill in found_skills:
        if skill not in seen:
            seen.add(skill)
            unique_skills.append(skill)
    
    return unique_skills

def extract_experience_years(text):
    """Extract years of experience from text"""
    # Pattern to match experience mentions
    patterns = [
        r'(\d+)\s*years?\s*experience',
        r'experience\s*of\s*(\d+)\s*years?',
        r'(\d+)\s*years?\s*(?:of\s*)?experience',
        r'experience[:\s]*(\d+)\s*years?'
    ]
    
    years = []
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        years.extend([int(match) for match in matches])
    
    # Return average if multiple matches, otherwise return the value or 0
    if years:
        return sum(years) / len(years)
    return 0

def calculate_text_similarity(text1, text2):
    """Calculate similarity between two texts using multiple methods"""
    # Preprocess texts
    processed_text1 = preprocess_text(text1)
    processed_text2 = preprocess_text(text2)
    
    # Extract key terms
    terms1 = set(extract_key_terms(processed_text1))
    terms2 = set(extract_key_terms(processed_text2))
    
    # Calculate Jaccard similarity
    intersection = terms1.intersection(terms2)
    union = terms1.union(terms2)
    
    if len(union) == 0:
        return 0.0
    
    jaccard_similarity = len(intersection) / len(union)
    
    # Calculate cosine similarity (simplified)
    # In a real implementation, you would use TF-IDF vectors
    vector1 = Counter(terms1)
    vector2 = Counter(terms2)
    
    # Get common terms
    common_terms = set(vector1.keys()) & set(vector2.keys())
    
    # Calculate dot product
    dot_product = sum(vector1[term] * vector2[term] for term in common_terms)
    
    # Calculate magnitudes
    magnitude1 = sum(value**2 for value in vector1.values()) ** 0.5
    magnitude2 = sum(value**2 for value in vector2.values()) ** 0.5
    
    if magnitude1 == 0 or magnitude2 == 0:
        cosine_similarity = 0.0
    else:
        cosine_similarity = dot_product / (magnitude1 * magnitude2)
    
    # Weighted average of both similarities
    final_similarity = 0.4 * jaccard_similarity + 0.6 * cosine_similarity
    
    return final_similarity