"""
Script to verify the accuracy of skill extraction
"""
import sys
import traceback

def test_skill_extraction_accuracy():
    """Test the accuracy of skill extraction with known inputs"""
    try:
        from text_processor import extract_skills_advanced
        
        # Test case 1: Resume with clear technical skills
        test_resume_1 = """
        Michael Chen
        Senior Software Engineer
        
        Experienced in Python, JavaScript, and React development. 
        Worked with AWS, Docker, and Kubernetes in production environments.
        Strong background in machine learning with TensorFlow and PyTorch.
        
        Technical Skills:
        - Python
        - JavaScript
        - React
        - AWS
        - Docker
        - Kubernetes
        - Machine Learning
        - TensorFlow
        - PyTorch
        """
        
        expected_skills_1 = ['python', 'javascript', 'react', 'aws', 'docker', 'kubernetes', 'machine learning', 'tensorflow', 'pytorch']
        extracted_skills_1 = extract_skills_advanced(test_resume_1)
        
        print("Test Case 1: Technical Resume")
        print(f"Expected skills: {expected_skills_1}")
        print(f"Extracted skills: {extracted_skills_1}")
        print(f"Accuracy: {len(set(extracted_skills_1) & set(expected_skills_1))}/{len(expected_skills_1)}")
        print()
        
        # Test case 2: Resume with no technical skills
        test_resume_2 = """
        Sarah Williams
        Marketing Manager
        
        Experienced marketing professional with focus on digital marketing,
        social media management, and brand development. Strong communication
        and leadership skills.
        
        Skills:
        - Digital Marketing
        - Social Media
        - Brand Development
        - Communication
        - Leadership
        """
        
        expected_skills_2 = []  # No technical skills expected
        extracted_skills_2 = extract_skills_advanced(test_resume_2)
        
        print("Test Case 2: Non-Technical Resume")
        print(f"Expected skills: {expected_skills_2}")
        print(f"Extracted skills: {extracted_skills_2}")
        print(f"Accuracy: No false positives = {'PASS' if len(extracted_skills_2) == 0 else 'FAIL'}")
        print()
        
        # Test case 3: Edge case with partial word matches
        test_resume_3 = """
        John Python
        Customer Service Representative
        
        Experience in customer service and problem solving.
        Good communication skills. Works with people.
        """
        
        # Should NOT extract "python" as a skill since it's a name, not a programming language skill
        extracted_skills_3 = extract_skills_advanced(test_resume_3)
        
        print("Test Case 3: Edge Case (Name contains 'python')")
        print(f"Resume contains 'Python' as a name")
        print(f"Extracted skills: {extracted_skills_3}")
        print(f"Correctly avoided false positive: {'PASS' if 'python' not in extracted_skills_3 else 'FAIL'}")
        print()
        
        return True
        
    except Exception as e:
        print(f"Error in skill extraction test: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Verifying Skill Extraction Accuracy...")
    print("=" * 50)
    
    success = test_skill_extraction_accuracy()
    
    if success:
        print("✓ Skill extraction verification completed successfully")
    else:
        print("✗ Skill extraction verification failed")
        
    sys.exit(0 if success else 1)