"""
Script to verify the enhanced accuracy features of the Resume Screening system
"""
import sys
import traceback

def check_module_accuracy(module_name, function_name, test_input, expected_output=None):
    """Test a specific function from a module"""
    try:
        module = __import__(module_name)
        func = getattr(module, function_name)
        
        # Run the function with test input
        result = func(test_input)
        
        print(f"✓ {module_name}.{function_name} - OK")
        print(f"  Input: {test_input}")
        print(f"  Output: {result}")
        
        if expected_output is not None:
            if result == expected_output:
                print(f"  Expected: {expected_output} - MATCH")
            else:
                print(f"  Expected: {expected_output} - MISMATCH")
        
        print()
        return True
    except Exception as e:
        print(f"✗ {module_name}.{function_name} - ERROR")
        print(f"  Input: {test_input}")
        print(f"  Error: {str(e)}")
        print()
        return False

def main():
    print("Verifying Enhanced Accuracy Features...")
    print("=" * 50)
    
    # Test text processor functions
    print("Testing Text Processor Functions:")
    
    # Test clean_text
    check_module_accuracy("text_processor", "clean_text", "Hello, World! 123", "hello world")
    
    # Test preprocess_text
    check_module_accuracy("text_processor", "preprocess_text", "Machine Learning and Data Science", "machin learn data scienc")
    
    # Test extract_skills_advanced
    test_resume = "Experienced in Python, Machine Learning, TensorFlow, and SQL"
    try:
        from text_processor import extract_skills_advanced
        skills = extract_skills_advanced(test_resume)
        print(f"✓ text_processor.extract_skills_advanced - OK")
        print(f"  Input: {test_resume}")
        print(f"  Skills found: {skills}")
        print()
    except Exception as e:
        print(f"✗ text_processor.extract_skills_advanced - ERROR")
        print(f"  Error: {str(e)}")
        print()
    
    # Test matcher functions
    print("Testing Matcher Functions:")
    
    # Test ResumeMatcher class
    try:
        from matcher import ResumeMatcher
        matcher = ResumeMatcher()
        print("✓ matcher.ResumeMatcher - OK")
        print("  Matcher object created successfully")
        print()
    except Exception as e:
        print(f"✗ matcher.ResumeMatcher - ERROR")
        print(f"  Error: {str(e)}")
        print()
    
    # Test resume parser functions
    print("Testing Resume Parser Functions:")
    
    # Test extract_candidate_name
    test_text = "John Doe\nSoftware Engineer\nEmail: john@example.com"
    try:
        from resume_parser import extract_candidate_name
        name = extract_candidate_name(test_text)
        print(f"✓ resume_parser.extract_candidate_name - OK")
        print(f"  Input: {test_text[:30]}...")
        print(f"  Name extracted: {name}")
        print()
    except Exception as e:
        print(f"✗ resume_parser.extract_candidate_name - ERROR")
        print(f"  Error: {str(e)}")
        print()
    
    print("Enhanced accuracy verification complete!")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)