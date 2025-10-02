"""
Test script to verify skill extraction accuracy
"""
from text_processor import extract_skills_advanced

def test_skill_extraction():
    """Test skill extraction with various resume examples"""
    
    # Test case 1: Clear skills
    resume1 = """
    John Doe - Software Engineer
    
    Experienced software engineer with 5 years of experience in Python, JavaScript, and React.
    Proficient in AWS, Docker, and Kubernetes. Strong background in machine learning with
    TensorFlow and PyTorch. Skilled in SQL and database design.
    
    Skills:
    - Python
    - JavaScript
    - React
    - AWS
    - Docker
    - Machine Learning
    - TensorFlow
    - SQL
    """
    
    # Test case 2: No matching skills
    resume2 = """
    Jane Smith - Marketing Specialist
    
    Marketing professional with 3 years of experience in digital marketing, social media
    management, and content creation. Expert in SEO and Google Analytics. Strong
    communication and leadership skills.
    
    Skills:
    - Digital Marketing
    - Social Media
    - Content Creation
    - SEO
    - Google Analytics
    - Communication
    """
    
    # Test case 3: Mixed skills
    resume3 = """
    Robert Johnson - Data Scientist
    
    Data scientist with PhD in Statistics and 4 years of industry experience. Expertise in
    Python, R, and machine learning algorithms. Published research in deep learning
    applications. Experience with big data technologies like Spark and Hadoop.
    
    Skills:
    - Python
    - R
    - Machine Learning
    - Deep Learning
    - Statistical Modeling
    - SQL
    - Spark
    """
    
    test_cases = [
        ("Technical Resume", resume1),
        ("Non-Technical Resume", resume2),
        ("Data Science Resume", resume3)
    ]
    
    for name, resume in test_cases:
        print(f"\n{name}:")
        print("-" * 40)
        skills = extract_skills_advanced(resume)
        print(f"Skills found: {skills}")
        print(f"Number of skills: {len(skills)}")

if __name__ == "__main__":
    print("Testing Skill Extraction Accuracy")
    print("=" * 50)
    test_skill_extraction()