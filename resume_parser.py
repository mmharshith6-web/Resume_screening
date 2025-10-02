import PyPDF2
import docx2txt
import re
from text_processor import extract_experience_years

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        text = docx2txt.process(file_path)
        return text
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return ""

def extract_candidate_name(text):
    """Extract candidate name from resume text with improved accuracy"""
    # Look for name patterns (improved approach)
    lines = text.split('\n')
    
    # Common name patterns
    name_patterns = [
        r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # Standard name pattern
        r'^([A-Z][a-z]+(?:\s+[A-Z]\.?\s*[A-Z][a-z]+)*)',  # With middle initial
        r'Name[:\s]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',  # With "Name:" prefix
    ]
    
    # Check first few lines for names
    for i, line in enumerate(lines[:10]):
        line = line.strip()
        # Skip lines that look like addresses, emails, or phone numbers
        if line and not re.match(r'.*@\w+|.*\d{3}.*\d{3}.*\d{4}|.*street|.*road|.*avenue|.*drive|.*email|.*phone', line.lower()):
            # Try each pattern
            for pattern in name_patterns:
                match = re.search(pattern, line)
                if match:
                    return match.group(1)
    
    # Fallback: return first line that looks like a name
    for i, line in enumerate(lines[:5]):
        line = line.strip()
        # Return first line that looks like a name (has at least two words, starts with capital)
        if line and re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+', line):
            return line
            
    return "Unknown Candidate"

def extract_contact_info(text):
    """Extract contact information from resume"""
    # Extract email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    email = email_match.group(0) if email_match else ""
    
    # Extract phone number
    phone_match = re.search(r'(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}', text)
    phone = phone_match.group(0) if phone_match else ""
    
    return {
        'email': email,
        'phone': phone
    }

def extract_education(text):
    """Extract education information"""
    # Common education keywords
    edu_keywords = ['education', 'university', 'college', 'degree', 'bachelor', 'master', 'phd', 'bs', 'ms', 'ba', 'ma']
    
    # Split text into lines
    lines = text.split('\n')
    education_lines = []
    
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in edu_keywords):
            # Include this line and a few following lines
            for j in range(i, min(i+5, len(lines))):
                if lines[j].strip():
                    education_lines.append(lines[j].strip())
            break
    
    return ' '.join(education_lines)

def parse_resume(file_path):
    """Main function to parse resume based on file extension"""
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
        candidate_name = extract_candidate_name(text)
    elif file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
        candidate_name = extract_candidate_name(text)
    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX files.")
    
    # Extract additional information
    contact_info = extract_contact_info(text)
    education = extract_education(text)
    experience_years = extract_experience_years(text)
    
    return {
        'text': text,
        'candidate_name': candidate_name,
        'contact_info': contact_info,
        'education': education,
        'experience_years': experience_years
    }