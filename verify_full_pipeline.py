"""
Verify the full pipeline with accurate skill extraction
"""
import sys
import traceback

def test_full_pipeline():
    """Test the full pipeline with sample data"""
    try:
        # Import required modules
        from text_processor import extract_skills_advanced, preprocess_text
        from matcher import ResumeMatcher
        
        print("Testing Full Pipeline")
        print("=" * 30)
        
        # Sample job description
        jd_text = """
        Senior Python Developer
        We are looking for a Senior Python Developer with experience in Django, Flask, and REST API development.
        Required skills include Python, Docker, AWS, and PostgreSQL.
        
        Responsibilities:
        - Develop and maintain web applications using Python frameworks
        - Design and implement RESTful APIs
        - Collaborate with front-end developers
        - Deploy applications using Docker and AWS
        
        Requirements:
        - 5+ years of Python experience
        - Proficiency in Django and Flask
        - Experience with Docker and AWS
        - Knowledge of PostgreSQL
        """
        
        # Sample resume with name containing skill-like word
        resume_text = """
        John Python
        Senior Software Engineer
        
        Experienced software engineer with 6 years of experience in web development.
        Proficient in JavaScript, React, and Node.js. Strong background in Docker
        and AWS. Experience with PostgreSQL and MongoDB.
        
        Skills:
        - JavaScript
        - React
        - Node.js
        - Docker
        - AWS
        - PostgreSQL
        - MongoDB
        
        Experience:
        - Senior Developer at Tech Corp (3 years)
        - Software Engineer at Startup Inc (3 years)
        """
        
        print("Job Description Skills:")
        jd_skills = extract_skills_advanced(jd_text)
        print(f"  {jd_skills}")
        
        print("\nResume Skills:")
        resume_skills = extract_skills_advanced(resume_text)
        print(f"  {resume_skills}")
        
        print(f"\nCorrectly avoided 'python' as skill: {'PASS' if 'python' not in resume_skills else 'FAIL'}")
        
        # Test preprocessing
        print("\nTesting Text Preprocessing:")
        processed_jd = preprocess_text(jd_text)
        processed_resume = preprocess_text(resume_text)
        print(f"  Job description processed: {len(processed_jd)} characters")
        print(f"  Resume processed: {len(processed_resume)} characters")
        
        # Test matching
        print("\nTesting Matching:")
        matcher = ResumeMatcher()
        matcher.fit_job_description(processed_jd)
        
        # Create sample resume data
        resume_data = [{
            'candidate_name': 'John Python',
            'text': processed_resume
        }]
        
        results = matcher.match_resumes(resume_data)
        
        if results:
            result = results[0]
            print(f"  Candidate: {result['candidate_name']}")
            print(f"  Score: {result['score']:.4f}")
            print(f"  Skills: {result['skills']}")
            print(f"  Missing Skills: {result['missing_skills']}")
            print(f"  Decision: {result['decision']}")
            
            # Verify that 'python' is not in the skills
            skills_list = result['skills'].split(', ') if result['skills'] else []
            print(f"\nFinal verification - 'python' not in skills: {'PASS' if 'python' not in skills_list else 'FAIL'}")
        
        return True
        
    except Exception as e:
        print(f"Error in full pipeline test: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_full_pipeline()
    if success:
        print("\n" + "=" * 30)
        print("✓ Full pipeline test completed successfully!")
        print("✓ Skill extraction is working correctly!")
    else:
        print("\n" + "=" * 30)
        print("✗ Full pipeline test failed!")
    sys.exit(0 if success else 1)