# Configuration settings for the Personality Assessment App

# App settings
APP_CONFIG = {
    "page_title": "Personality Assessment Tool",
    "page_icon": "🧠",
    "layout": "wide",
    "max_questions": 10,
    "session_timeout": 3600,  # 1 hour in seconds
}

# OpenAI settings
OPENAI_CONFIG = {
    "model": "gpt-3.5-turbo",
    "max_tokens_question": 200,
    "max_tokens_diagnosis": 800,
    "temperature": 0.7,
}

# Personality assessment categories
ASSESSMENT_CATEGORIES = {
    "big_five": {
        "Openness": "Creativity, curiosity, and openness to new experiences",
        "Conscientiousness": "Organization, responsibility, and goal-directed behavior",
        "Extraversion": "Sociability, assertiveness, and positive emotions",
        "Agreeableness": "Cooperation, trust, and empathy",
        "Neuroticism": "Emotional instability, anxiety, and stress reactivity"
    },
    "myers_briggs": {
        "E/I": "Extraversion vs Introversion",
        "S/N": "Sensing vs Intuition", 
        "T/F": "Thinking vs Feeling",
        "J/P": "Judging vs Perceiving"
    }
}

# Mental health indicators to watch for
MENTAL_HEALTH_INDICATORS = [
    "persistent sadness or depression",
    "excessive anxiety or worry",
    "social withdrawal",
    "sleep disturbances",
    "appetite changes",
    "difficulty concentrating",
    "mood swings",
    "substance use concerns",
    "thoughts of self-harm",
    "chronic stress"
]

# Professional help recommendations
PROFESSIONAL_HELP_TRIGGERS = [
    "thoughts of self-harm or suicide",
    "substance abuse",
    "severe depression symptoms",
    "panic attacks",
    "trauma responses",
    "eating disorders",
    "severe social anxiety",
    "persistent sleep issues"
]

# Styling and UI
UI_STYLES = {
    "primary_color": "#1f77b4",
    "success_color": "#2ca02c", 
    "warning_color": "#ff7f0e",
    "error_color": "#d62728",
    "info_color": "#17becf"
}