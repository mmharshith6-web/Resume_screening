"""
Comprehensive test to verify skill extraction accuracy
"""
from text_processor import extract_skills_advanced

def test_skill_extraction_comprehensive():
    """Test skill extraction with various challenging scenarios"""
    
    # Test case 1: Resume with name containing skill-like word
    test_resume_1 = """
    John Python
    Software Engineer
    
    Experienced in JavaScript development and React frameworks.
    Strong problem-solving skills and team collaboration.
    
    Skills:
    - JavaScript
    - React
    - Problem Solving
    - Teamwork
    """
    
    print("Test Case 1: Name contains 'python'")
    print("Resume text:")
    print(test_resume_1)
    skills_1 = extract_skills_advanced(test_resume_1)
    print(f"Extracted skills: {skills_1}")
    print(f"Correctly avoided 'python' as skill: {'PASS' if 'python' not in skills_1 else 'FAIL'}")
    print()
    
    # Test case 2: Resume with actual Python skill
    test_resume_2 = """
    Jane Developer
    Senior Python Developer
    
    Experienced in Python programming, Django framework, and REST API development.
    Also skilled in JavaScript and React.
    
    Technical Skills:
    - Python
    - Django
    - JavaScript
    - REST
    """
    
    print("Test Case 2: Actual Python skill")
    print("Resume text:")
    print(test_resume_2)
    skills_2 = extract_skills_advanced(test_resume_2)
    print(f"Extracted skills: {skills_2}")
    print(f"Correctly identified 'python': {'PASS' if 'python' in skills_2 else 'FAIL'}")
    print()
    
    # Test case 3: Resume with no technical skills
    test_resume_3 = """
    Sarah Smith
    Marketing Manager
    
    Experienced in digital marketing, social media management, and brand development.
    Strong communication and leadership abilities.
    
    Professional Skills:
    - Digital Marketing
    - Social Media
    - Communication
    - Leadership
    """
    
    print("Test Case 3: Non-technical resume")
    print("Resume text:")
    print(test_resume_3)
    skills_3 = extract_skills_advanced(test_resume_3)
    print(f"Extracted skills: {skills_3}")
    print(f"Correctly found no technical skills: {'PASS' if len(skills_3) == 0 else 'FAIL'}")
    print()
    
    # Test case 4: Resume with complex skills
    test_resume_4 = """
    Michael Chen
    Data Scientist
    
    PhD in Statistics with expertise in machine learning, deep learning, and neural networks.
    Proficient in Python, R, and SQL. Experience with TensorFlow, PyTorch, and scikit-learn.
    Skilled in data visualization with matplotlib and seaborn.
    
    Technical Expertise:
    - Machine Learning
    - Deep Learning
    - Neural Networks
    - Python
    - R
    - SQL
    - TensorFlow
    - PyTorch
    - Scikit-learn
    - Data Visualization
    - Matplotlib
    - Seaborn
    """
    
    expected_skills = [
        'machine learning', 'deep learning', 'neural networks', 'python', 'r', 'sql',
        'tensorflow', 'pytorch', 'scikit-learn', 'data visualization', 'matplotlib', 'seaborn'
    ]
    
    print("Test Case 4: Complex technical resume")
    print("Resume text:")
    print(test_resume_4)
    skills_4 = extract_skills_advanced(test_resume_4)
    print(f"Expected skills: {expected_skills}")
    print(f"Extracted skills: {skills_4}")
    
    # Check how many expected skills were found
    found_count = len(set(skills_4) & set(expected_skills))
    total_expected = len(expected_skills)
    print(f"Accuracy: {found_count}/{total_expected} ({(found_count/total_expected)*100:.1f}%)")
    print()
    
    # Test case 5: Edge case with partial matches
    test_resume_5 = """
    Robert Johnson
    Customer Service Representative
    
    Experience with customer service software and problem-solving techniques.
    Good communication skills. Works with people.
    
    Skills:
    - Customer Service
    - Problem Solving
    - Communication
    """
    
    print("Test Case 5: Edge case partial matches")
    print("Resume text:")
    print(test_resume_5)
    skills_5 = extract_skills_advanced(test_resume_5)
    print(f"Extracted skills: {skills_5}")
    # Should not extract "java" from "javascript" when only "java" is meant
    print(f"Correctly avoided partial matches: {'PASS' if 'java' not in skills_5 else 'FAIL'}")
    print()

if __name__ == "__main__":
    print("Comprehensive Skill Extraction Accuracy Test")
    print("=" * 50)
    test_skill_extraction_comprehensive()
    print("Test completed!")