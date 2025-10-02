"""
Simple test to check if skill extraction is working
"""
try:
    from text_processor import extract_skills_advanced
    print("Module imported successfully")
    
    # Simple test
    test_text = "Experienced in Python, JavaScript, and React development"
    skills = extract_skills_advanced(test_text)
    print(f"Test text: {test_text}")
    print(f"Extracted skills: {skills}")
    
    # Test with name containing skill-like word
    test_text2 = "John Python - Software Engineer with JavaScript experience"
    skills2 = extract_skills_advanced(test_text2)
    print(f"Test text 2: {test_text2}")
    print(f"Extracted skills: {skills2}")
    print(f"Correctly avoided 'python' as skill: {'PASS' if 'python' not in skills2 else 'FAIL'}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()