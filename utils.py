import pandas as pd
import os

def save_results_to_csv(results, filename="results.csv"):
    """Save matching results to CSV file"""
    # Create a copy of results without the detailed_scores for CSV export
    csv_results = []
    for result in results:
        csv_result = result.copy()
        # Remove detailed_scores for cleaner CSV
        if 'detailed_scores' in csv_result:
            del csv_result['detailed_scores']
        csv_results.append(csv_result)
    
    df = pd.DataFrame(csv_results)
    df.to_csv(filename, index=False)
    return filename

def load_sample_data():
    """Load sample job description and resumes for testing"""
    # Sample job description
    jd_text = """
    Senior Data Scientist
    We are seeking a Senior Data Scientist to lead our analytics team. The ideal candidate will have extensive experience with machine learning, deep learning, and big data technologies. Responsibilities include developing advanced predictive models, leading data science initiatives, and mentoring junior team members.
    
    Requirements:
    - Master's or PhD in Computer Science, Statistics, Mathematics, or related field
    - 5+ years of experience in data science
    - Expertise in Python, R, and SQL
    - Experience with TensorFlow, PyTorch, and scikit-learn
    - Strong background in deep learning and neural networks
    - Experience with cloud platforms (AWS, GCP, Azure)
    - Excellent leadership and communication skills
    - Published research in machine learning journals preferred
    """
    
    return jd_text

def create_sample_resumes():
    """Create sample resumes for testing"""
    resumes = [
        {
            'candidate_name': 'Alex Johnson',
            'text': """
            Alex Johnson
            Email: alex.johnson@email.com
            Phone: (555) 123-4567
            
            Senior Data Scientist with 7 years of experience in machine learning and artificial intelligence. PhD in Computer Science from Stanford University. Expert in Python, TensorFlow, and PyTorch. Led multiple successful AI projects resulting in 30% improvement in business metrics. Published researcher with 10+ papers in top-tier ML conferences.
            
            Skills:
            - Python
            - Machine Learning
            - Deep Learning
            - TensorFlow
            - PyTorch
            - SQL
            - Statistical Analysis
            - Data Visualization
            - AWS
            - Team Leadership
            """
        },
        {
            'candidate_name': 'Sarah Williams',
            'text': """
            Sarah Williams
            Email: sarah.williams@email.com
            Phone: (555) 987-6543
            
            Software Engineer with 4 years of experience in web development. Proficient in JavaScript, React, and Node.js. Experience with REST APIs and cloud platforms. Bachelor's degree in Computer Science from MIT. Recently completed online courses in data science and machine learning.
            
            Skills:
            - JavaScript
            - React
            - Node.js
            - HTML/CSS
            - Git
            - AWS
            - Basic Python
            - Machine Learning (beginner)
            """
        },
        {
            'candidate_name': 'Michael Chen',
            'text': """
            Michael Chen
            Email: m.chen@email.com
            Phone: (555) 456-7890
            
            Data Scientist with PhD in Statistics and 6 years of industry experience. Expertise in Python, R, and advanced machine learning algorithms. Published research in deep learning applications. Experience with big data technologies like Spark and Hadoop. Led data science teams of 5+ members.
            
            Skills:
            - Python
            - R
            - Machine Learning
            - Deep Learning
            - PyTorch
            - Statistical Modeling
            - SQL
            - Spark
            - Hadoop
            - Team Leadership
            - Research Publication
            """
        }
    ]
    
    return resumes