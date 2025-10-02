"""
Test script to verify all modules work correctly
"""
import os
from resume_parser import parse_resume
from text_processor import preprocess_text, extract_skills_advanced, calculate_text_similarity
from matcher import ResumeMatcher
from utils import load_sample_data, create_sample_resumes

def test_resume_parsing():
    """Test resume parsing functionality"""
    print("Testing resume parsing...")
    
    # Create sample resumes
    sample_resumes = create_sample_resumes()
    
    # Test parsing (using text directly for this test)
    for i, resume in enumerate(sample_resumes):
        print(f"Resume {i+1}: {resume['candidate_name']}")
        print(f"Text length: {len(resume['text'])}")
        print("---")

def test_text_processing():
    """Test text processing functionality"""
    print("Testing text processing...")
    
    # Load sample data
    sample_resumes = create_sample_resumes()
    
    # Test preprocessing
    for i, resume in enumerate(sample_resumes):
        processed_text = preprocess_text(resume['text'])
        print(f"Resume {i+1} processed text length: {len(processed_text)}")
        
        # Test skill extraction
        skills = extract_skills_advanced(resume['text'])
        print(f"Skills found: {skills}")
        
        # Test experience extraction
        # This would normally be done in the parser, but we'll simulate it here
        exp_years = 0  # In a real scenario, this would be extracted from the text
        print(f"Experience years: {exp_years}")
        print("---")

def test_matching():
    """Test matching functionality"""
    print("Testing matching...")
    
    # Load sample data
    jd_text = load_sample_data()
    sample_resumes = create_sample_resumes()
    
    # Preprocess job description
    processed_jd = preprocess_text(jd_text)
    
    # Preprocess resumes
    processed_resumes = []
    for resume in sample_resumes:
        processed_text = preprocess_text(resume['text'])
        processed_resumes.append({
            'candidate_name': resume['candidate_name'],
            'text': processed_text
        })
    
    # Test matching
    matcher = ResumeMatcher()
    matcher.fit_job_description(processed_jd)
    results = matcher.match_resumes(processed_resumes)
    
    # Display results
    for result in results:
        print(f"Candidate: {result['candidate_name']}")
        print(f"Overall Score: {result['score']:.4f}")
        print(f"Decision: {result['decision']}")
        print(f"Skills: {result['skills']}")
        print(f"Missing Skills: {result['missing_skills']}")
        
        # Show detailed scores if available
        if 'detailed_scores' in result:
            detailed = result['detailed_scores']
            print(f"  Cosine Score: {detailed['cosine']:.4f}")
            print(f"  Euclidean Score: {detailed['euclidean']:.4f}")
            print(f"  Custom Score: {detailed['custom']:.4f}")
        print("---")

def test_similarity_functions():
    """Test similarity calculation functions"""
    print("Testing similarity functions...")
    
    text1 = "Python machine learning data science artificial intelligence"
    text2 = "Data science Python machine learning neural networks"
    
    similarity = calculate_text_similarity(text1, text2)
    print(f"Similarity between '{text1}' and '{text2}': {similarity:.4f}")
    print("---")

if __name__ == "__main__":
    print("Running tests for Resume Screening with NLP modules...")
    print("=" * 50)
    
    test_resume_parsing()
    print()
    
    test_text_processing()
    print()
    
    test_similarity_functions()
    print()
    
    test_matching()
    print()
    
    print("All tests completed!")