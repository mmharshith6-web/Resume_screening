import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from text_processor import extract_skills_advanced, calculate_text_similarity
from sklearn.metrics.pairwise import euclidean_distances

class ResumeMatcher:
    def __init__(self):
        # Use a more sophisticated TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=10000,
            ngram_range=(1, 2),  # Include bigrams for better context
            min_df=1,
            max_df=0.8,
            sublinear_tf=True  # Apply sublinear TF scaling
        )
        self.jd_vector = None
        self.jd_skills = []
        self.jd_text = ""
        
    def fit_job_description(self, jd_text):
        """Fit the vectorizer on the job description"""
        # Store job description text
        self.jd_text = jd_text
        
        # Store job description skills
        self.jd_skills = extract_skills_advanced(jd_text)
        
        # Fit and transform the job description
        self.jd_vector = self.vectorizer.fit_transform([jd_text])
        
    def match_resume(self, resume_text):
        """Match a resume against the job description"""
        if self.jd_vector is None:
            raise ValueError("Job description not fitted yet. Call fit_job_description first.")
            
        # Transform resume text using the same vectorizer
        resume_vector = self.vectorizer.transform([resume_text])
        
        # Calculate cosine similarity
        cosine_score = cosine_similarity(self.jd_vector, resume_vector)[0][0]
        
        # Calculate Euclidean distance (inverse for similarity)
        euclidean_dist = euclidean_distances(self.jd_vector, resume_vector)[0][0]
        euclidean_score = 1 / (1 + euclidean_dist)  # Convert distance to similarity
        
        # Calculate custom text similarity
        custom_similarity = calculate_text_similarity(self.jd_text, resume_text)
        
        # Weighted combination of all scores for better accuracy
        # Give more weight to cosine similarity as it's more reliable
        final_score = 0.6 * cosine_score + 0.2 * euclidean_score + 0.2 * custom_similarity
        
        # Extract resume skills with improved accuracy
        resume_skills = extract_skills_advanced(resume_text)
        
        # Find missing skills
        missing_skills = list(set(self.jd_skills) - set(resume_skills))
        
        return {
            'score': final_score,
            'skills': resume_skills,
            'missing_skills': missing_skills,
            'cosine_score': cosine_score,
            'euclidean_score': euclidean_score,
            'custom_score': custom_similarity
        }
    
    def match_resumes(self, resumes_data):
        """Match multiple resumes against the job description"""
        results = []
        
        for resume_data in resumes_data:
            candidate_name = resume_data['candidate_name']
            resume_text = resume_data['text']
            
            # Match resume
            match_result = self.match_resume(resume_text)
            
            # Determine fit decision based on enhanced criteria
            # Use a more nuanced threshold
            if match_result['score'] > 0.3:
                decision = "Fit" if match_result['score'] > 0.5 else "Potential Fit"
            else:
                decision = "Not Fit"
            
            results.append({
                'candidate_name': candidate_name,
                'score': match_result['score'],
                'skills': ', '.join(match_result['skills']),
                'missing_skills': ', '.join(match_result['missing_skills']),
                'decision': decision,
                'detailed_scores': {
                    'cosine': match_result['cosine_score'],
                    'euclidean': match_result['euclidean_score'],
                    'custom': match_result['custom_score']
                }
            })
            
        # Sort results by score (descending)
        results = sorted(results, key=lambda x: x['score'], reverse=True)
        
        return results