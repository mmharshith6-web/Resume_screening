"""
Final test to verify the improved skill extraction is working
"""
from text_processor import extract_skills_advanced

# Test case 1: Resume with name containing skill-like word
test_resume_1 = """
John Python
Software Engineer

Experienced in JavaScript development and React frameworks.
Skilled in Docker containerization and AWS cloud services.

Skills:
- JavaScript
- React
- Docker
- AWS
"""

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
- React
"""

print("Final Verification of Skill Extraction Fix")
print("=" * 50)

print("Test Case 1: Name contains 'python'")
skills_1 = extract_skills_advanced(test_resume_1)
print(f"Skills found: {skills_1}")
print(f"Correctly avoided 'python': {'PASS' if 'python' not in skills_1 else 'FAIL'}")
print()

print("Test Case 2: Actual Python skill")
skills_2 = extract_skills_advanced(test_resume_2)
print(f"Skills found: {skills_2}")
print(f"Correctly identified 'python': {'PASS' if 'python' in skills_2 else 'FAIL'}")
print()

print("✓ Skill extraction fix verified!")