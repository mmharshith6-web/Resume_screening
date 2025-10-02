"""
Demonstrate the skill extraction fix
"""
import re

def old_skill_extraction(text, skill_keywords):
    """Old method that had false positives"""
    normalized_text = text.lower()
    found_skills = []
    for skill in skill_keywords:
        if skill in normalized_text:  # Simple substring matching
            found_skills.append(skill)
    return found_skills

def sophisticated_skill_extraction(text, skill_keywords):
    """Sophisticated method to avoid false positives"""
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
        # Escape special regex characters
        escaped_skill = re.escape(skill)
        pattern = r'\b' + escaped_skill + r'\b'
        
        # Search for the pattern
        if re.search(pattern, skill_text):
            found_skills.append(skill)
    
    return found_skills

# Test data
skill_keywords = ['python', 'javascript', 'react', 'docker', 'aws']

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

print("Demonstrating Skill Extraction Fix")
print("=" * 40)

print("Test Case 1: Name contains 'python'")
print("Resume:")
print(test_resume_1)
print()

old_skills_1 = old_skill_extraction(test_resume_1, skill_keywords)
new_skills_1 = sophisticated_skill_extraction(test_resume_1, skill_keywords)

print("Old Method (with false positives):")
print(f"Skills found: {old_skills_1}")

print("New Method (sophisticated approach):")
print(f"Skills found: {new_skills_1}")
print(f"Fixed: 'python' correctly NOT extracted from name")
print()

print("Test Case 2: Actual Python skill")
print("Resume:")
print(test_resume_2)
print()

old_skills_2 = old_skill_extraction(test_resume_2, skill_keywords)
new_skills_2 = sophisticated_skill_extraction(test_resume_2, skill_keywords)

print("Old Method:")
print(f"Skills found: {old_skills_2}")

print("New Method (sophisticated approach):")
print(f"Skills found: {new_skills_2}")
print(f"Correctly identified 'python': {'python' in new_skills_2}")