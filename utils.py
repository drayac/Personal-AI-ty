import streamlit as st
import json
from datetime import datetime
import pandas as pd
from config import ASSESSMENT_CATEGORIES, MENTAL_HEALTH_INDICATORS

def export_results_to_csv(responses, questions, analysis):
    """Export assessment results to CSV format"""
    data = []
    for i, (question, response) in enumerate(zip(questions, responses)):
        data.append({
            "Question_Number": i + 1,
            "Question": question,
            "Response": response,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    df = pd.DataFrame(data)
    return df.to_csv(index=False)

def validate_response_length(response, min_length=10):
    """Validate that response meets minimum length requirement"""
    return len(response.strip()) >= min_length

def calculate_response_sentiment(responses):
    """Simple sentiment analysis of responses"""
    positive_words = ['happy', 'good', 'positive', 'excited', 'confident', 'optimistic', 'grateful']
    negative_words = ['sad', 'bad', 'negative', 'anxious', 'depressed', 'worried', 'stressed']
    
    sentiment_scores = []
    
    for response in responses:
        response_lower = response.lower()
        positive_count = sum(1 for word in positive_words if word in response_lower)
        negative_count = sum(1 for word in negative_words if word in response_lower)
        
        if positive_count + negative_count == 0:
            sentiment_scores.append(0)  # Neutral
        else:
            sentiment_scores.append((positive_count - negative_count) / (positive_count + negative_count))
    
    return sentiment_scores

def generate_personality_summary(analysis_text):
    """Extract key personality traits from analysis"""
    traits = []
    
    # Look for Big Five traits
    for trait, description in ASSESSMENT_CATEGORIES["big_five"].items():
        if trait.lower() in analysis_text.lower():
            traits.append(trait)
    
    # Look for Myers-Briggs indicators
    mb_indicators = []
    for indicator, description in ASSESSMENT_CATEGORIES["myers_briggs"].items():
        for letter in indicator.split('/'):
            if letter in analysis_text.upper():
                mb_indicators.append(letter)
    
    return {
        "big_five_traits": traits,
        "myers_briggs_indicators": mb_indicators
    }

def check_mental_health_flags(responses, analysis_text):
    """Check for potential mental health concerns"""
    flags = []
    
    # Check responses for concerning content
    concerning_phrases = [
        'want to hurt myself', 'thoughts of death', 'end it all', 'no point',
        'can\'t cope', 'overwhelming', 'panic', 'can\'t sleep', 'don\'t eat'
    ]
    
    for response in responses:
        response_lower = response.lower()
        for phrase in concerning_phrases:
            if phrase in response_lower:
                flags.append(f"Concerning phrase detected: '{phrase}'")
    
    # Check analysis for mental health indicators
    for indicator in MENTAL_HEALTH_INDICATORS:
        if indicator.lower() in analysis_text.lower():
            flags.append(f"Mental health indicator: {indicator}")
    
    return flags

def format_analysis_output(analysis_text):
    """Format the AI analysis for better readability"""
    # Split by common section headers
    sections = {}
    current_section = "Overview"
    current_content = []
    
    lines = analysis_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this line is a section header
        if any(header in line.lower() for header in ['personality type', 'strengths', 'growth', 'mental health', 'recommendations']):
            # Save previous section
            if current_content:
                sections[current_section] = '\n'.join(current_content)
            
            # Start new section
            current_section = line.replace('*', '').replace('#', '').strip()
            current_content = []
        else:
            current_content.append(line)
    
    # Don't forget the last section
    if current_content:
        sections[current_section] = '\n'.join(current_content)
    
    return sections

def generate_recommendations(personality_traits, mental_health_flags):
    """Generate personalized recommendations based on assessment"""
    recommendations = []
    
    # Personality-based recommendations
    if 'Neuroticism' in personality_traits:
        recommendations.append("Consider stress management techniques like meditation or deep breathing exercises")
    
    if 'Introversion' in personality_traits:
        recommendations.append("Ensure you have adequate alone time to recharge")
    
    if 'Extraversion' in personality_traits:
        recommendations.append("Maintain social connections and seek collaborative environments")
    
    # Mental health flag recommendations
    if mental_health_flags:
        recommendations.append("Consider speaking with a mental health professional")
        recommendations.append("Practice self-care and reach out to trusted friends or family")
    
    # General wellness recommendations
    recommendations.extend([
        "Maintain regular sleep schedule",
        "Engage in regular physical activity",
        "Practice mindfulness or meditation",
        "Keep a journal for self-reflection"
    ])
    
    return recommendations

class AssessmentAnalyzer:
    """Class to handle comprehensive assessment analysis"""
    
    def __init__(self, responses, questions, ai_analysis):
        self.responses = responses
        self.questions = questions
        self.ai_analysis = ai_analysis
        self.sentiment_scores = calculate_response_sentiment(responses)
        self.personality_summary = generate_personality_summary(ai_analysis)
        self.mental_health_flags = check_mental_health_flags(responses, ai_analysis)
        self.formatted_analysis = format_analysis_output(ai_analysis)
        
    def get_comprehensive_report(self):
        """Generate a comprehensive assessment report"""
        report = {
            "assessment_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_questions": len(self.questions),
            "responses_analyzed": len(self.responses),
            "sentiment_analysis": {
                "average_sentiment": sum(self.sentiment_scores) / len(self.sentiment_scores),
                "sentiment_range": f"{min(self.sentiment_scores):.2f} to {max(self.sentiment_scores):.2f}"
            },
            "personality_traits": self.personality_summary,
            "mental_health_flags": self.mental_health_flags,
            "ai_analysis": self.formatted_analysis,
            "recommendations": generate_recommendations(
                self.personality_summary.get("big_five_traits", []),
                self.mental_health_flags
            )
        }
        
        return report
    
    def export_to_json(self):
        """Export complete analysis to JSON"""
        report = self.get_comprehensive_report()
        report["raw_responses"] = [
            {"question": q, "response": r} 
            for q, r in zip(self.questions, self.responses)
        ]
        
        return json.dumps(report, indent=2)
    
    def get_risk_level(self):
        """Assess overall risk level based on flags"""
        if len(self.mental_health_flags) == 0:
            return "Low", "No significant mental health concerns detected"
        elif len(self.mental_health_flags) <= 2:
            return "Moderate", "Some areas of concern - consider self-care strategies"
        else:
            return "High", "Multiple concerns detected - professional consultation recommended"