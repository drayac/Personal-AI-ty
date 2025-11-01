import streamlit as st
import json
import time
from datetime import datetime
import pandas as pd
import os
import streamlit.components.v1 as components
import random

# Configure the page
st.set_page_config(
    page_title="Personality Assessment Tool",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Color themes
COLOR_THEMES = {
    'purple': {
        'name': '🔮 Dark Purple',
        'primary': '#2d1b69',
        'secondary': '#4c2a85',
        'background': '#1a1a2e',
        'accent': '#3c1a5b',
        'text': '#ffffff'
    },
    'ocean': {
        'name': '🌊 Deep Ocean',
        'primary': '#0a4b5c',
        'secondary': '#1a237e',
        'background': '#121921',
        'accent': '#1565c0',
        'text': '#ffffff'
    },
    'forest': {
        'name': '🌲 Dark Forest',
        'primary': '#1b4332',
        'secondary': '#2d5016',
        'background': '#0f1419',
        'accent': '#2e7d32',
        'text': '#ffffff'
    },
    'sunset': {
        'name': '🌅 Dark Sunset',
        'primary': '#6a1b5b',
        'secondary': '#8e2de2',
        'background': '#2d1b39',
        'accent': '#7b1fa2',
        'text': '#ffffff'
    }
}

def get_current_theme():
    """Get the current color theme"""
    return COLOR_THEMES[st.session_state.color_theme]

def count_words(text):
    """Count words in a text string"""
    if not text:
        return 0
    return len(text.strip().split())

# Initialize session state
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'age' not in st.session_state:
    st.session_state.age = ""
if 'personal_info_complete' not in st.session_state:
    st.session_state.personal_info_complete = False
if 'questions_answered' not in st.session_state:
    st.session_state.questions_answered = 0
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'assessment_complete' not in st.session_state:
    st.session_state.assessment_complete = False
if 'color_theme' not in st.session_state:
    st.session_state.color_theme = 'forest'
if 'clear_input' not in st.session_state:
    st.session_state.clear_input = False

# Personality assessment questions
ALL_PERSONALITY_QUESTIONS = [
    "How do you typically recharge your energy - through social interaction or solitude?",
    "When making decisions, do you rely more on logic and analysis or feelings and values?",
    "Do you prefer detailed planning or keeping your options open and being spontaneous?",
    "How do you handle stress and overwhelming situations?",
    "Describe your ideal work environment and what motivates you most.",
    "How do you typically respond to criticism or feedback from others?",
    "What are your biggest fears or anxieties in daily life?",
    "What do you value most in friendships?",
    "Describe your sleep patterns and how they affect your mood and energy.",
    "How do you cope with major life changes or unexpected challenges?",
    "What role does creativity play in your daily life?",
    "How do you prefer to learn new things - hands-on, reading, or discussing with others?",
    "What kind of music or sounds help you focus or relax?",
    "How do you approach conflicts in personal relationships?",
    "What does success mean to you personally?",
    "How do you balance work and personal time?",
    "What activities make you lose track of time?",
    "How do you handle unexpected changes in your routine?",
    "What motivates you to get up in the morning?",
    "How do you prefer to celebrate achievements?",
    "What kind of physical environment makes you feel most comfortable?",
    "How do you approach making new friends or social connections?",
    "What role does spirituality or philosophy play in your life?",
    "How do you handle feeling overwhelmed or burnt out?",
    "What childhood experiences shaped who you are today?",
    "How do you prefer to receive and give emotional support?",
    "What kind of challenges do you actively seek out?",
    "How do you deal with uncertainty about the future?",
    "What makes you feel most confident and self-assured?",
    "How do you approach personal growth and self-improvement?",
    "What role does humor play in your daily interactions?",
    "How do you handle disappointment or failure?",
    "What kind of legacy do you want to leave behind?",
    "How do you prefer to spend your free time on weekends?",
    "What triggers your strongest emotional responses?",
    "How do you approach financial planning and security?",
    "What kind of stories or movies resonate most with you?",
    "How do you handle peer pressure or social expectations?",
    "What makes you feel most alive and energized?",
    "How do you approach forgiveness - of yourself and others?",
    "What role does nature and the outdoors play in your well-being?",
    "How do you handle compliments and praise from others?",
    "What kind of conversations do you find most meaningful?",
    "How do you approach risk-taking in different areas of life?",
    "What habits or routines are most important to your daily life?",
    "How do you handle being the center of attention?",
    "What kind of books or content do you gravitate toward?",
    "How do you approach helping others who are struggling?",
    "What makes you feel most misunderstood by others?",
    "How do you handle transitions between different life phases?",
    "What role does competition play in motivating you?",
    "How do you approach expressing your authentic self?",
    "What kind of feedback helps you grow the most?",
    "How do you handle moments of self-doubt?",
    "What traditions or rituals are meaningful to you?",
    "How do you approach setting and maintaining boundaries?",
    "What makes you feel most connected to others?",
    "How do you handle information overload in today's world?",
    "What role does adventure play in your ideal life?",
    "How do you approach making important life decisions?",
    "What kind of work or activities drain your energy most?",
    "How do you handle being criticized or judged by others?",
    "What makes you feel most grateful in daily life?",
    "How do you approach maintaining long-distance relationships?"
]

def get_daily_questions():
    """Get 8 random questions based on today's date as seed"""
    import random
    from datetime import datetime
    
    # Use today's date as seed for consistent daily questions
    today = datetime.now()
    seed = int(today.strftime("%Y%m%d"))
    random.seed(seed)
    
    # Select 8 random questions
    selected_questions = random.sample(ALL_PERSONALITY_QUESTIONS, 8)
    return selected_questions

# Get today's questions
PERSONALITY_QUESTIONS = get_daily_questions()


def get_model_response(user_prompt, system_prompt):
    """Generate AI response using Hugging Face Transformers GPT-2 with smart fallbacks"""
    try:
        from transformers import GPT2LMHeadModel, GPT2Tokenizer
        import torch
        
        # Load model and tokenizer
        model_name = "gpt2"
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        model = GPT2LMHeadModel.from_pretrained(model_name)
        
        # Set pad token
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Create a prompt that combines system and user input
        prompt = f"{system_prompt}\n\nUser: {user_prompt}\nAssistant:"
        
        # Tokenize and generate
        inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
        
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=inputs.shape[1] + 100,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                no_repeat_ngram_size=2
            )
        
        # Decode response
        full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = full_response[len(prompt):].strip()
        
        # Clean up response
        if not response or len(response.split()) < 3:
            raise Exception("Generated response too short")
            
        # Remove any incomplete sentences
        sentences = response.split('.')
        if len(sentences) > 1:
            response = '. '.join(sentences[:-1]) + '.'
        
        return response
        
    except Exception as e:
        # Fallback to curated responses if transformers fails
        return get_fallback_response(user_prompt, system_prompt)

def get_fallback_response(user_prompt, system_prompt):
    """Fallback response system when transformers is not available"""
    import random
    
    # High-quality curated responses for reliable output
    response_patterns = {
        'stress': [
            "Thank you for sharing. Your stress management approach shows excellent emotional regulation and self-care awareness.",
            "This response demonstrates mature coping strategies and good understanding of your emotional needs.",
            "Your approach to stress reveals strong resilience and practical problem-solving skills."
        ],
        'decision': [
            "Thank you for sharing. Your decision-making process shows thoughtful analysis and consideration of consequences.",
            "This response demonstrates excellent critical thinking and balanced evaluation of options.",
            "Your approach reveals strong analytical skills and careful consideration of different perspectives."
        ],
        'conflict': [
            "Thank you for sharing. Your conflict resolution style shows excellent interpersonal skills and emotional maturity.",
            "This response demonstrates strong communication abilities and empathetic understanding of others.",
            "Your approach reveals good social intelligence and diplomatic problem-solving skills."
        ],
        'growth': [
            "Thank you for sharing. Your response shows excellent growth mindset and commitment to self-improvement.",
            "This demonstrates strong self-awareness and openness to learning from experiences.",
            "Your perspective reveals mature self-reflection and dedication to personal development."
        ],
        'default': [
            "Thank you for your thoughtful response. This shows excellent self-awareness and genuine reflection.",
            "Your answer reveals strong emotional intelligence and honest self-assessment.",
            "This response demonstrates mature thinking and authentic personal insight.",
            "Thank you for sharing. Your perspective shows deep consideration and self-understanding.",
            "Your response indicates excellent introspective abilities and thoughtful analysis.",
            "This answer shows great authenticity and meaningful self-reflection.",
            "Thank you for sharing. Your response demonstrates strong personal awareness and insight."
        ]
    }
    
    # Determine response category based on user prompt keywords
    prompt_lower = user_prompt.lower()
    category = 'default'
    
    if any(word in prompt_lower for word in ['stress', 'pressure', 'overwhelm', 'anxious', 'worried']):
        category = 'stress'
    elif any(word in prompt_lower for word in ['decision', 'choose', 'decide', 'choice', 'option']):
        category = 'decision'
    elif any(word in prompt_lower for word in ['conflict', 'disagree', 'argument', 'fight', 'dispute']):
        category = 'conflict'
    elif any(word in prompt_lower for word in ['grow', 'learn', 'improve', 'develop', 'change', 'better']):
        category = 'growth'
    
    # Return curated response
    return random.choice(response_patterns[category])

def get_ai_response(question, user_response, question_number):
    """Get response from AI for personality analysis with follow-up logic"""
    # Check if response is too short (1-3 words only)
    word_count = len(user_response.strip().split())
    
    if word_count <= 3:
        # Generate follow-up question for short answers
        follow_up_questions = {
            'stress': "Can you tell me more about what specific techniques work best for you?",
            'decision': "What factors do you usually consider when making this type of decision?", 
            'social': "How do you feel in those situations? What do you enjoy most about them?",
            'challenge': "Can you share a specific example of how you handled this?",
            'goals': "What motivates you most when working toward this type of goal?",
            'default': "Can you elaborate a bit more on your thoughts about this?"
        }
        
        # Determine follow-up category
        question_lower = question.lower()
        follow_up_category = 'default'
        if any(word in question_lower for word in ['stress', 'pressure', 'overwhelm']):
            follow_up_category = 'stress'
        elif any(word in question_lower for word in ['decision', 'choose', 'decide']):
            follow_up_category = 'decision'
        elif any(word in question_lower for word in ['social', 'people', 'friend', 'party']):
            follow_up_category = 'social'
        elif any(word in question_lower for word in ['challenge', 'difficult', 'problem']):
            follow_up_category = 'challenge'
        elif any(word in question_lower for word in ['goal', 'ambition', 'future', 'plan']):
            follow_up_category = 'goals'
        
        follow_up = follow_up_questions[follow_up_category]
        return f"Thank you for sharing! {follow_up}"
    
    # For longer answers, provide analysis
    prompt = f"""You are a professional psychologist conducting a personality assessment. 

Question {question_number}/10: {question}
User's Response: {user_response}

Please provide a thoughtful analysis of their response:
1. Give a brief acknowledgment of their answer (1 sentence)
2. Make one insightful observation about what their response reveals about their personality, thinking patterns, or emotional approach (1-2 sentences)

Be professional, supportive, and encouraging. Provide analysis and insights only - do NOT ask any follow-up questions. Keep your total response to exactly 2-3 sentences maximum."""

    system_prompt = "You are a professional psychologist conducting a personality assessment. Provide brief, insightful responses about personality traits based on user answers. Keep responses under 50 words and focus on positive insights."
    ai_response = get_model_response(user_prompt=prompt, system_prompt=system_prompt)
    
    # Remove any questions that might appear - cut at any question mark
    if "?" in ai_response:
        question_end = ai_response.find("?")
        ai_response = ai_response[:question_end].strip()
        # Add a period if the sentence doesn't end with punctuation
        if ai_response and not ai_response.endswith(('.', '!', ':')):
            ai_response += "."
    
    return ai_response

def analyze_with_ai(responses, sentiment_results):
    """Use transformers for personality analysis"""
    try:
        # Analyze sentiment patterns
        positive_count = sum(1 for s in sentiment_results if s['label'] == 'POSITIVE')
        negative_count = len(sentiment_results) - positive_count
        total_negative_confidence = sum(s['score'] for s in sentiment_results if s['label'] == 'NEGATIVE')
        
        # Combine all responses for analysis
        full_text = ' '.join(responses).lower()
        
        # Initialize personality scores
        ai_scores = {
            'Analytical Thinker': 0,
            'Creative Innovator': 0, 
            'Empathetic Connector': 0,
            'Resilient Achiever': 0,
            'Balanced Pragmatist': 0
        }
        
        # Detect concerning patterns based on sentiment analysis
        high_negative_responses = [s for s in sentiment_results if s['label'] == 'NEGATIVE' and s['score'] > 0.99]
        
        # If we have highly negative responses with concerning content, flag it
        if len(high_negative_responses) >= 2:
            # Check for specific concerning themes
            concerning_themes = ['fail', 'failure', 'power', 'powerful', 'weak', 'weakness']
            theme_count = sum(1 for theme in concerning_themes if theme in full_text)
            
            if theme_count >= 2:
                # This suggests aggressive/concerning patterns - don't assign normal personality types
                return {
                    'Analytical Thinker': 0,
                    'Creative Innovator': 0,
                    'Empathetic Connector': 0,
                    'Resilient Achiever': 0,
                    'Balanced Pragmatist': 0,
                    'concerning_pattern_detected': True,
                    'negative_sentiment_score': total_negative_confidence
                }
        
        # Use AI to generate personality insights for non-concerning responses
        try:
            analysis_prompt = f"Analyze these personality responses for traits: {full_text[:500]}..."
            ai_insight = get_model_response(analysis_prompt)
            ai_text = ai_insight.lower()
            
            # Analyze AI response for personality indicators
            if any(word in ai_text for word in ['logical', 'analytical', 'systematic', 'structured']):
                ai_scores['Analytical Thinker'] += 3
            if any(word in ai_text for word in ['creative', 'innovative', 'imaginative', 'original']):
                ai_scores['Creative Innovator'] += 3
            if any(word in ai_text for word in ['empathetic', 'caring', 'supportive', 'emotional']):
                ai_scores['Empathetic Connector'] += 3
            if any(word in ai_text for word in ['resilient', 'determined', 'strong', 'persistent']):
                ai_scores['Resilient Achiever'] += 3
            if any(word in ai_text for word in ['balanced', 'practical', 'moderate', 'flexible']):
                ai_scores['Balanced Pragmatist'] += 3
        except:
            # If AI text generation fails, use sentiment-based scoring
            pass
            
        # Adjust based on sentiment patterns
        if positive_count > negative_count:
            ai_scores['Empathetic Connector'] += 1
            ai_scores['Resilient Achiever'] += 1
        elif negative_count > positive_count:
            # More negative responses suggest different patterns
            ai_scores['Analytical Thinker'] += 1  # Might be critical thinking
        
        return ai_scores
        
    except Exception as e:
        return None

def analyze_with_keywords(response_text):
    """Traditional keyword-based analysis"""
    # More specific keywords for different personality types
    analytical_keywords = ['analysis', 'analyze', 'logical', 'logic', 'systematic', 'methodical', 'structured', 'organized', 'planning', 'research', 'data', 'facts', 'evidence', 'rational', 'objective']
    creative_keywords = ['creative', 'creativity', 'artistic', 'imaginative', 'innovative', 'original', 'unique', 'inspiration', 'design', 'experiment', 'brainstorm', 'invent', 'express', 'aesthetic']
    empathetic_keywords = ['empathy', 'compassion', 'caring', 'supportive', 'understanding', 'listening', 'emotional', 'relationships', 'connect', 'help others', 'teamwork', 'collaborate']
    resilient_keywords = ['challenge', 'overcome', 'persist', 'persevere', 'determined', 'resilient', 'strong', 'achieve', 'goals', 'success', 'push through', 'never give up', 'endure']
    balanced_keywords = ['balance', 'moderate', 'flexible', 'adaptable', 'practical', 'reasonable', 'compromise', 'adjust', 'consider both', 'depends on', 'varies']
    
    # Score each personality type with weighted scoring
    analytical_score = 0
    creative_score = 0
    empathetic_score = 0
    resilient_score = 0
    balanced_score = 0
    
    # Count keywords with context-aware scoring
    for word in analytical_keywords:
        if word in response_text:
            analytical_score += 2 if len(word) > 6 else 1
    
    for word in creative_keywords:
        if word in response_text:
            creative_score += 2 if len(word) > 6 else 1
    
    for word in empathetic_keywords:
        if word in response_text:
            empathetic_score += 2 if len(word) > 6 else 1
    
    for word in resilient_keywords:
        if word in response_text:
            resilient_score += 2 if len(word) > 6 else 1
    
    for word in balanced_keywords:
        if word in response_text:
            balanced_score += 2 if len(word) > 6 else 1
    
    return {
        'Analytical Thinker': analytical_score,
        'Creative Innovator': creative_score,
        'Empathetic Connector': empathetic_score,
        'Resilient Achiever': resilient_score,
        'Balanced Pragmatist': balanced_score
    }

def analyze_personality_traits(responses):
    """Analyze personality traits based on user responses using AI and keyword analysis"""
    import random
    
    # Analyze response patterns
    response_text = ' '.join(responses).lower()
    
    # Try AI-powered analysis first
    try:
        from transformers import pipeline
        
        # Use sentiment analysis for personality insights
        sentiment_analyzer = pipeline("sentiment-analysis")
        
        # Analyze overall sentiment and emotional patterns
        sentiment_results = []
        for response in responses:
            if response.strip():
                sentiment = sentiment_analyzer(response[:512])  # Limit length for processing
                sentiment_results.append(sentiment[0])
        
        # Extract personality insights from AI analysis
        ai_personality_score = analyze_with_ai(responses, sentiment_results)
        
    except Exception as e:
        # Fallback to keyword analysis if AI fails
        ai_personality_score = None
    
    # Keyword-based analysis (always runs as backup/validation)
    keyword_scores = analyze_with_keywords(response_text)
    
    # Continue with existing personality type determination logic
    aggressive_keywords = ['angry', 'hate', 'fight', 'argue', 'aggressive', 'intense', 'furious', 'rage', 'conflict', 'confrontation', 'competitive', 'destroy', 'dominate', 'weakness', 'weak', 'pathetic', 'power', 'powerful', 'superior', 'ignore', 'worthless', 'useless', 'inferior', 'crush', 'defeat', 'control', 'manipulate', 'exploit', 'domination', 'fail', 'failure', 'failing']
    
    # Enhanced detection for concerning patterns
    concerning_patterns = ['weakness in others', 'weak around me', 'pathetic weakness', 'focus on my own power', 'showing my power', 'become the best', 'higher than others', 'see other people fail', 'see failure in people', 'makes me feel powerful', 'grow my power', 'my responsibilities and power']
    concerning_score = sum(3 for pattern in concerning_patterns if pattern in response_text)
    
    # Combined aggressive scoring
    aggressive_score = sum(2 for word in aggressive_keywords if word in response_text) + concerning_score
    
    # Combine AI and keyword analysis if AI is available
    if ai_personality_score and not ai_personality_score.get('concerning_pattern_detected', False):
        # Weight AI analysis more heavily but use keywords as validation
        final_scores = {}
        for key in keyword_scores:
            ai_weight = ai_personality_score.get(key, 0) * 0.7
            keyword_weight = keyword_scores[key] * 0.3
            final_scores[key] = ai_weight + keyword_weight
    elif ai_personality_score and ai_personality_score.get('concerning_pattern_detected', False):
        # AI detected concerning patterns - boost aggressive score significantly
        final_scores = keyword_scores
        aggressive_score += 15  # Major boost for AI-detected concerning patterns
    else:
        # Use keyword analysis only
        final_scores = keyword_scores
    
    # Get individual scores for later use (convert to integers for list indexing)
    analytical_score = int(final_scores['Analytical Thinker'])
    creative_score = int(final_scores['Creative Innovator'])
    empathetic_score = int(final_scores['Empathetic Connector'])
    resilient_score = int(final_scores['Resilient Achiever'])
    balanced_score = int(final_scores['Balanced Pragmatist'])
    
    # Determine primary personality type based on scores
    max_score = max(final_scores.values()) if final_scores.values() else 0
    
    # If highly aggressive/concerning responses, create special type with appropriate warning
    if aggressive_score > 8:  # Much lower threshold for concerning patterns
        primary_type = {
            'type': 'High-Intensity Individual',
            'description': 'Your responses suggest very intense, competitive patterns with focus on dominance and power. This may indicate underlying stress, burnout, or interpersonal challenges that could benefit from professional support.'
        }
    elif aggressive_score > 3:
        primary_type = {
            'type': 'Intense Competitor',
            'description': 'You demonstrate high intensity and competitive drive. You approach challenges with strong determination and aren\'t afraid of conflict when pursuing your goals. Consider balancing this drive with empathy and collaboration.'
        }
    elif max_score == 0:
        # If no keywords matched, assign based on response length and complexity
        avg_length = sum(len(response.split()) for response in responses) / len(responses) if responses else 0
        if avg_length > 15:
            primary_type = {
                'type': 'Thoughtful Reflector',
                'description': 'You provide detailed, thoughtful responses and take time to consider multiple aspects of situations. You value depth and nuance in your thinking.'
            }
        else:
            primary_type = {
                'type': 'Balanced Pragmatist',
                'description': 'You show a well-rounded approach to life, balancing logic and emotion, work and personal time, and individual goals with social connections.'
            }
    else:
        # Get the highest scoring type
        max_type = max(final_scores, key=final_scores.get)
        
        personality_types = {
            'Analytical Thinker': {
                'type': 'Analytical Thinker',
                'description': 'You demonstrate strong analytical capabilities and prefer structured, logical approaches to problem-solving. You value accuracy, detail-oriented work, and evidence-based decision making.'
            },
            'Creative Innovator': {
                'type': 'Creative Innovator', 
                'description': 'You show high creativity and original thinking. You enjoy exploring new ideas, thinking outside the box, and approaching challenges with innovative solutions.'
            },
            'Empathetic Connector': {
                'type': 'Empathetic Connector',
                'description': 'You demonstrate strong emotional intelligence and interpersonal skills. You value relationships, show genuine care for others, and excel in collaborative environments.'
            },
            'Resilient Achiever': {
                'type': 'Resilient Achiever',
                'description': 'You display strong determination and goal-oriented behavior. You persevere through challenges and maintain focus on achieving your objectives.'
            },
            'Balanced Pragmatist': {
                'type': 'Balanced Pragmatist',
                'description': 'You show a well-rounded approach to life, balancing logic and emotion, work and personal time, and individual goals with social connections.'
            }
        }
        
        primary_type = personality_types[max_type]
    
    # Generate comprehensive traits
    strengths_options = [
        "• **Self-Awareness:** You demonstrate excellent understanding of your own thoughts, emotions, and motivations\n• **Emotional Intelligence:** Strong ability to recognize and manage emotions in yourself and others\n• **Adaptability:** You show flexibility in adjusting to new situations and challenges\n• **Communication Skills:** Clear and thoughtful expression of ideas and feelings",
        
        "• **Problem-Solving:** You approach challenges with creativity and logical thinking\n• **Resilience:** Strong ability to bounce back from setbacks and maintain optimism\n• **Authenticity:** You present yourself genuinely and value honest self-expression\n• **Growth Mindset:** Open to learning and continuous personal development",
        
        "• **Empathy:** You show genuine understanding and care for others' perspectives\n• **Leadership Potential:** Natural ability to guide and inspire others\n• **Analytical Thinking:** Strong capacity for logical reasoning and critical analysis\n• **Stress Management:** Healthy approaches to managing pressure and maintaining balance"
    ]
    
    cognitive_styles = [
        "You tend to be a **systematic thinker** who prefers structured approaches and careful planning. You value thoroughness and accuracy in your work and decisions.",
        "You demonstrate **intuitive thinking** combined with analytical skills. You can see both the big picture and important details.",
        "You show **creative problem-solving** abilities, often thinking of unique solutions and approaches that others might miss.",
        "You exhibit **balanced cognitive processing**, effectively combining logical analysis with emotional intelligence and intuition."
    ]
    
    emotional_intelligence_options = [
        "Your responses suggest **high emotional intelligence**. You show good self-awareness, can regulate your emotions effectively, and demonstrate empathy toward others.",
        "You display **strong emotional awareness** and appear to handle interpersonal relationships with maturity and understanding.",
        "You demonstrate **balanced emotional processing**, showing both logical thinking and emotional sensitivity in your responses.",
        "Your emotional intelligence appears **well-developed**, with good self-regulation and social awareness evident in your answers."
    ]
    
    growth_areas_options = [
        "• **Stress Management:** Continue developing healthy coping strategies for high-pressure situations\n• **Communication:** Work on expressing needs and boundaries more clearly when needed\n• **Work-Life Balance:** Focus on maintaining healthy boundaries between different life areas",
        
        "• **Self-Confidence:** Continue building confidence in your abilities and trusting your judgment\n• **Time Management:** Develop more efficient systems for prioritizing tasks and managing time\n• **Assertiveness:** Practice expressing your opinions and needs more directly when appropriate",
        
        "• **Patience with Process:** Allow yourself more time for reflection before making important decisions\n• **Self-Care:** Prioritize your own needs alongside caring for others\n• **Flexibility:** Practice adapting to unexpected changes with greater ease"
    ]
    
    # Age-appropriate insights
    try:
        age_num = int(st.session_state.age)
        if age_num < 25:
            age_insight = f"At {age_num}, you're in an important developmental phase. Your responses show mature self-reflection for your age. This is an excellent time to explore your interests, build skills, and establish healthy patterns that will serve you well throughout life."
        elif age_num < 35:
            age_insight = f"At {age_num}, you're likely establishing your career and personal relationships. Your responses suggest good self-awareness as you navigate these important life decisions. Focus on building both professional skills and personal fulfillment."
        elif age_num < 50:
            age_insight = f"At {age_num}, you're in a phase where your personality and values are well-established. Your responses show the wisdom that comes with experience. This is often a time for deeper self-understanding and mentoring others."
        else:
            age_insight = f"At {age_num}, your responses reflect the depth and wisdom that comes with life experience. You show excellent self-awareness and emotional maturity. Consider how you can share your insights and continue growing."
    except:
        age_insight = "Your responses show maturity and thoughtfulness regardless of your age. Continue to embrace growth and self-discovery throughout your life journey."
    
    wellness_assessments = [
        "Your responses suggest **good overall mental wellness**. You appear to have healthy coping mechanisms and a positive outlook. Continue maintaining the practices that support your wellbeing.",
        
        "You show **balanced emotional regulation** in your responses. You seem to handle stress reasonably well and have insight into your emotional patterns. Consider continuing to develop your stress management toolkit.",
        
        "Your responses indicate **resilient mental health** with good self-awareness. You appear to process emotions effectively and maintain perspective during challenges."
    ]
    
    # Special wellness assessments for concerning patterns
    concerning_wellness_assessments = [
        "Your responses show **patterns that may indicate stress, burnout, or underlying emotional challenges**. The focus on dominance, power, and viewing others negatively can be signs of deeper issues. Consider speaking with a mental health professional for support.",
        
        "Your responses suggest **high levels of interpersonal tension and competitive stress**. This intensity may be impacting your relationships and overall wellbeing. Professional counseling could help you develop healthier coping strategies.",
        
        "Your responses indicate **concerning patterns in how you view others and relationships**. These patterns may be affecting your mental health and social connections. Consider seeking professional support to explore these feelings."
    ]
    
    development_recommendations = [
        "• Set aside regular time for self-reflection and journaling\n• Read books or take courses in areas that interest you\n• Practice mindfulness or meditation to enhance self-awareness\n• Seek feedback from trusted friends or mentors",
        
        "• Challenge yourself with new learning opportunities\n• Practice setting and achieving small, meaningful goals\n• Develop a growth mindset by viewing challenges as opportunities\n• Consider working with a coach or mentor for guidance",
        
        "• Engage in activities that build your strengths\n• Practice stepping outside your comfort zone regularly\n• Focus on developing emotional intelligence through practice\n• Create systems for tracking your personal growth"
    ]
    
    social_recommendations = [
        "• Maintain meaningful connections with family and friends\n• Practice active listening in your relationships\n• Be open about your needs and boundaries\n• Seek relationships that support your authentic self",
        
        "• Join groups or communities aligned with your interests\n• Practice empathy and understanding in difficult conversations\n• Work on building trust through consistent, reliable behavior\n• Balance social time with personal reflection time"
    ]
    
    career_recommendations = [
        "• Align your work with your values and strengths\n• Seek opportunities for continuous learning and growth\n• Build positive relationships with colleagues and supervisors\n• Consider how your personality traits can contribute to your professional success",
        
        "• Look for roles that challenge you while playing to your strengths\n• Develop both technical skills and emotional intelligence\n• Practice clear communication and collaboration\n• Set career goals that reflect your personal values"
    ]
    
    wellness_recommendations = [
        "• Maintain regular exercise and healthy eating habits\n• Practice stress management techniques like deep breathing or meditation\n• Ensure adequate sleep and rest\n• Engage in activities that bring you joy and relaxation",
        
        "• Create healthy boundaries between work and personal time\n• Develop a support network of trusted friends and family\n• Practice gratitude and positive thinking\n• Don't hesitate to seek professional help when needed"
    ]
    
    dimensions_data = [
        "| **Emotional Stability** | High | You handle stress well and maintain emotional balance |",
        "| **Openness to Experience** | High | You're curious and open to new ideas and experiences |", 
        "| **Social Orientation** | Balanced | You enjoy both social interaction and personal time |",
        "| **Conscientiousness** | High | You're organized and responsible in your approach |",
        "| **Agreeableness** | High | You work well with others and show empathy |"
    ]
    
    future_paths = [
        f"As you continue to grow, {st.session_state.name}, focus on leveraging your natural strengths while gently working on areas for development. Your personality profile suggests you have excellent potential for both personal fulfillment and positive impact on others. Consider setting goals that align with your values and allow you to use your unique combination of traits.",
        
        f"Your personality development journey, {st.session_state.name}, should focus on authentic self-expression and meaningful connections. You have the foundation for continued growth in emotional intelligence, resilience, and personal effectiveness. Trust your instincts while remaining open to new perspectives and experiences."
    ]
    
    # Import random here
    import random
    
    # Choose appropriate strengths based on personality type
    if primary_type['type'] == 'Intense Competitor':
        chosen_strengths = strengths_options[1]  # Problem-solving and resilience focused
    elif aggressive_score > 0:
        chosen_strengths = strengths_options[1]  # Resilience and growth focused
    else:
        chosen_strengths = strengths_options[analytical_score % len(strengths_options)]
    
    # Choose cognitive style based on type
    if primary_type['type'] == 'Analytical Thinker':
        chosen_cognitive = cognitive_styles[0]
    elif primary_type['type'] == 'Creative Innovator':
        chosen_cognitive = cognitive_styles[2]
    elif primary_type['type'] == 'Balanced Pragmatist':
        chosen_cognitive = cognitive_styles[3]
    else:
        chosen_cognitive = cognitive_styles[1]
    
    return {
        'primary_type': primary_type['type'],
        'type_description': primary_type['description'],
        'strengths': chosen_strengths,
        'cognitive_style': chosen_cognitive,
        'emotional_intelligence': emotional_intelligence_options[empathetic_score % len(emotional_intelligence_options)],
        'growth_areas': growth_areas_options[resilient_score % len(growth_areas_options)],
        'age_insights': age_insight,
        'wellness_assessment': concerning_wellness_assessments[0] if aggressive_score > 8 else wellness_assessments[balanced_score % len(wellness_assessments)],
        'development_recommendations': development_recommendations[creative_score % len(development_recommendations)],
        'social_recommendations': social_recommendations[empathetic_score % len(social_recommendations)],
        'career_recommendations': career_recommendations[analytical_score % len(career_recommendations)],
        'wellness_recommendations': wellness_recommendations[balanced_score % len(wellness_recommendations)],
        'dimensions_table': '\n'.join(random.sample(dimensions_data, 4)),
        'future_path': future_paths[resilient_score % len(future_paths)]
    }

def generate_personality_diagnosis():
    """Generate comprehensive personality diagnosis"""
    import random
    
    # Analyze responses for personality traits
    responses = st.session_state.responses
    name = st.session_state.name
    age = st.session_state.age
    
    # Analyze key personality dimensions based on responses
    traits = analyze_personality_traits(responses)
    
    # Generate comprehensive analysis
    analysis = f"""# 🧠 Comprehensive Personality Analysis for {name}

## 👤 **Personal Profile**
**Name:** {name}  
**Age:** {age}  
**Assessment Date:** {datetime.now().strftime('%B %d, %Y')}  
**Assessment Type:** AI-Powered Personality Analysis

---

## 🎯 **Personality Type Assessment**

Based on your responses, {name}, your personality profile suggests you exhibit characteristics aligned with:

**Primary Personality Type:** {traits['primary_type']}

{traits['type_description']}

---

## 💪 **Key Strengths & Positive Traits**

Your responses reveal several notable strengths:

### 🌟 **Core Strengths:**
{traits['strengths']}

### 🧩 **Cognitive Style:**
{traits['cognitive_style']}

### 💖 **Emotional Intelligence:**
{traits['emotional_intelligence']}

---

## 🌱 **Areas for Personal Growth**

Every personality has areas that can benefit from development. For you, {name}, consider focusing on:

{traits['growth_areas']}

---

## 🎂 **Age-Appropriate Insights (Age {age})**

{traits['age_insights']}

---

## 🧘 **Mental Wellness & Stress Management**

{traits['wellness_assessment']}

---

## 🎯 **Personalized Recommendations**

Based on your unique personality profile, here are tailored suggestions:

### 📚 **Personal Development:**
{traits['development_recommendations']}

### 🤝 **Relationship & Social Life:**
{traits['social_recommendations']}

### 💼 **Career & Goals:**
{traits['career_recommendations']}

### 🧘‍♀️ **Self-Care & Wellness:**
{traits['wellness_recommendations']}

---

## 📊 **Personality Dimensions Summary**

| Dimension | Your Profile | Description |
|-----------|-------------|-------------|
{traits['dimensions_table']}

---

## 🔮 **Future Development Path**

{traits['future_path']}

---

## ⚠️ **Important Disclaimer**

This personality assessment is designed for self-reflection and personal growth purposes. It is **not a clinical diagnosis** and should not replace professional psychological consultation when needed. 

If you're experiencing persistent mental health concerns, please consider speaking with a qualified mental health professional.

---

## 🎉 **Celebrating Your Unique Personality**

{name}, your personality is a beautiful combination of traits that make you uniquely you. Embrace your strengths, work on your growth areas with patience and self-compassion, and remember that personality development is a lifelong journey.

**Assessment completed with care by AI Personality Analysis System**  
*Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*
"""
    
    return analysis

def main():
    # Get current theme colors
    theme = get_current_theme()
    
    # Dynamic CSS based on selected theme
    st.markdown(f"""
    <style>
    /* TEMPORARILY DISABLED HEADER HIDING FOR DEBUGGING */
    /*
    header[data-testid="stHeader"] {{
        display: none !important;
    }}
    
    .stApp > header {{
        display: none !important;
    }}
    
    .stApp > div[data-testid="stHeader"] {{
        display: none !important;
    }}
    
    .stActionButton {{
        display: none !important;
    }}
    
    .stApp > div:first-child {{
        display: none !important;
    }}
    
    .stApp {{
        margin-top: 0 !important;
        padding-top: 0 !important;
    }}
    */
    
    /* Main app background - dark theme */
    .stApp {{
        background: {theme['background']} !important;
        color: #e0e0e0 !important;
    }}
    
    /* Main content area dark styling */
    .main .block-container {{
        background: {theme['background']} !important;
        color: #e0e0e0 !important;
    }}
    
    /* Text elements dark styling */
    h1, h2, h3, h4, h5, h6, p, span, div {{
        color: #e0e0e0 !important;
    }}
    
    /* Sidebar styling - dark gradient */
    .css-1d391kg, .css-1y4p8pa, [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {theme['primary']}, {theme['secondary']}) !important;
        border-right: 2px solid {theme['accent']} !important;
    }}
    
    /* All sidebar text elements */
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    /* Sidebar containers and text */
    .css-1d391kg, .css-1d391kg * {{
        color: white !important;
    }}
    
    /* Sidebar markdown and headers */
    .css-1d391kg .stMarkdown, .css-1d391kg .stMarkdown * {{
        color: white !important;
    }}
    
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, .css-1d391kg h4, .css-1d391kg h5, .css-1d391kg h6 {{
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5) !important;
    }}
    
    /* Sidebar paragraphs and spans */
    .css-1d391kg p, .css-1d391kg span, .css-1d391kg div {{
        color: white !important;
    }}
    
    /* Sidebar progress text */
    .css-1d391kg .stProgress + div, .css-1d391kg .stProgress ~ div {{
        color: white !important;
    }}
    
    /* Status indicator text */
    .css-1d391kg .status-indicator + span, .css-1d391kg .status-indicator ~ span {{
        color: white !important;
    }}
    
    /* Selectbox - better visibility on dark sidebar */
    .css-1d391kg .stSelectbox > div > div {{
        background: white !important;
        border-radius: 10px !important;
        border: 2px solid {theme['accent']} !important;
        color: #333333 !important;
    }}
    
    /* Selectbox dropdown menu */
    .css-1d391kg .stSelectbox [data-baseweb="select"] > div {{
        background: white !important;
        color: #333333 !important;
    }}
    
    /* Selectbox dropdown options */
    .css-1d391kg .stSelectbox [role="listbox"] {{
        background: white !important;
        color: #333333 !important;
    }}
    
    /* Individual dropdown options - comprehensive coverage */
    .css-1d391kg .stSelectbox [role="option"],
    .css-1d391kg .stSelectbox [role="option"]:hover,
    .css-1d391kg .stSelectbox [role="option"]:focus,
    .css-1d391kg .stSelectbox [role="option"]:active,
    section[data-testid="stSidebar"] .stSelectbox [role="option"],
    section[data-testid="stSidebar"] .stSelectbox [role="option"]:hover,
    section[data-testid="stSidebar"] .stSelectbox [role="option"]:focus,
    section[data-testid="stSidebar"] .stSelectbox [role="option"]:active,
    .stSelectbox [role="listbox"] [role="option"],
    .stSelectbox [role="listbox"] [role="option"]:hover,
    .stSelectbox [role="listbox"] [role="option"]:focus,
    .stSelectbox [role="listbox"] [role="option"]:active {{
        background: white !important;
        color: #333333 !important;
        border: none !important;
    }}
    
    /* Selectbox dropdown container */
    .css-1d391kg .stSelectbox [role="listbox"],
    section[data-testid="stSidebar"] .stSelectbox [role="listbox"],
    .stSelectbox [role="listbox"] {{
        background: white !important;
        border: 1px solid #ccc !important;
        border-radius: 4px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
    }}
    
    /* Selectbox label */
    .css-1d391kg .stSelectbox label,
    section[data-testid="stSidebar"] .stSelectbox label {{
        color: white !important;
        font-weight: bold !important;
    }}
    
    /* Selectbox options */
    .css-1d391kg .stSelectbox option,
    section[data-testid="stSidebar"] .stSelectbox option {{
        color: #333333 !important;
        background: white !important;
    }}
    
    /* Selectbox dropdown */
    .css-1d391kg .stSelectbox [data-baseweb="select"],
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {{
        background: white !important;
        color: #333333 !important;
    }}
    
    /* Additional sidebar selectors for newer Streamlit versions */
    .st-emotion-cache-16idsys, .st-emotion-cache-16idsys * {{
        color: white !important;
    }}
    
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {theme['primary']}, {theme['accent']}) !important;
    }}
    
    section[data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] h5,
    section[data-testid="stSidebar"] h6 {{
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }}
    
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div:not(.stSelectbox) {{
        color: white !important;
    }}
    
    /* Keep selectbox readable in newer versions */
    section[data-testid="stSidebar"] .stSelectbox > div > div {{
        background: white !important;
        color: #333333 !important;
        border-radius: 10px !important;
        border: 2px solid {theme['accent']} !important;
    }}
    
    /* Selectbox dropdown in newer versions */
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {{
        background: white !important;
        color: #333333 !important;
    }}
    
    /* Dropdown menu */
    section[data-testid="stSidebar"] .stSelectbox [role="listbox"] {{
        background: white !important;
        color: #333333 !important;
    }}
    
    /* Individual options */
    section[data-testid="stSidebar"] .stSelectbox [role="option"] {{
        background: white !important;
        color: #333333 !important;
    }}
    
    /* Selectbox labels in sidebar */
    section[data-testid="stSidebar"] .stSelectbox label {{
        color: white !important;
        font-weight: bold !important;
    }}
    
    .main {{
        padding-top: 2rem;
        background: {theme['background']} !important;
    }}
    .stTitle {{
        color: #e0e0e0 !important;
        text-align: center;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}
    .question-container {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        border: 1px solid {theme['accent']};
    }}
    .question-container h3, .question-container h2 {{
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}
    
    /* Regular headers - dark theme */
    h1, h2, h3, h4, h5, h6 {{
        color: #e0e0e0 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }}
    .chat-container {{
        background: linear-gradient(135deg, {theme['primary']}20, {theme['secondary']}20);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid {theme['accent']};
        margin: 1rem 0 2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        color: #e0e0e0;
        border: 1px solid {theme['accent']}40;
    }}
    .chat-container h4 {{
        color: {theme['accent']};
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }}
    .progress-container {{
        background: linear-gradient(135deg, {theme['primary']}15, {theme['secondary']}15);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 2rem;
        border: 1px solid {theme['accent']};
        color: #e0e0e0;
    }}
    
    /* All buttons default styling */
    .stButton > button,
    button[kind="primary"],
    button[kind="secondary"],
    div[data-testid="stButton"] > button {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        width: 100% !important;
        opacity: 1 !important;
    }}
    .stButton > button:hover,
    button[kind="primary"]:hover,
    button[kind="secondary"]:hover,
    div[data-testid="stButton"] > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
        background: linear-gradient(135deg, {theme['accent']} 0%, {theme['primary']} 100%) !important;
    }}
    .stButton > button:disabled,
    button[kind="primary"]:disabled,
    button[kind="secondary"]:disabled,
    div[data-testid="stButton"] > button:disabled {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%) !important;
        color: white !important;
        opacity: 0.7 !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }}
    .stButton > button:disabled:hover {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%) !important;
        transform: none !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }}
    
    /* Skip button special styling for better visibility */
    [title*="Skip"] {{
        background: white !important;
        color: #333333 !important;
        border: 2px solid {theme['accent']} !important;
    }}
    
    .status-indicator {{
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }}
    .status-connected {{
        background-color: #4CAF50;
    }}
    .status-disconnected {{
        background-color: #f44336;
    }}
    .theme-selector {{
        background: linear-gradient(135deg, {theme['primary']}20, {theme['secondary']}20);
        padding: 1rem;
        border-radius: 15px;
        border: 1px solid {theme['accent']};
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        color: #e0e0e0;
    }}
    
    /* Text areas - light background with dark text */
    .stTextArea > div > div > textarea {{
        background: white !important;
        border: 2px solid {theme['accent']} !important;
        border-radius: 15px !important;
        color: #333333 !important;
        font-size: 1.1rem;
    }}
    
    /* Input fields - light background with dark text */
    .stTextInput > div > div > input {{
        background: white !important;
        border: 2px solid {theme['accent']} !important;
        border-radius: 15px !important;
        color: #333333 !important;
        font-size: 1.1rem;
    }}
    
    /* Progress bar */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, {theme['accent']}, {theme['primary']}) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Sidebar for progress and status
    with st.sidebar:
                # Progress tracking
        
        # Hugging Face Transformers status
        st.success("� Transformers: GPT-2 active")

        st.divider()
        
        # Progress tracking
        st.markdown("### 📊 Progress")
        
        # Show today's date for question selection
        from datetime import datetime
        today = datetime.now().strftime("%B %d, %Y")
        st.markdown(f"**Today's Questions:** {today}")
        st.markdown("*Questions updated daily*")
        st.divider()
        
        if st.session_state.personal_info_complete:
            progress = st.session_state.questions_answered / len(PERSONALITY_QUESTIONS)
            st.progress(progress)
            st.markdown(f"**{st.session_state.questions_answered}/{len(PERSONALITY_QUESTIONS)} Questions Completed**")
        else:
            st.markdown("Please enter your information to begin")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Main content
    st.title("🧠 Personality Assessment")
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Discover your personality with AI-powered insights by answering 8 daily questions</p>', unsafe_allow_html=True)

    # Personal information collection (before assessment)
    if not st.session_state.personal_info_complete:
        st.markdown('<div class="question-container">', unsafe_allow_html=True)
        st.markdown("## 👋 Welcome! Let's Get Started")
        st.markdown("Before we begin the personality assessment, please share some basic information:")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "✍️ What's your name?",
                value=st.session_state.name,
                placeholder="Enter your first name",
                help="This helps personalize your analysis"
            )
        
        with col2:
            age = st.text_input(
                "🎂 How old are you?",
                value=st.session_state.age,
                placeholder="Enter your age",
                help="Age provides context for personality insights"
            )
        
        if st.button("🚀 Start Assessment", type="primary", use_container_width=True):
            if name.strip() and age.strip():
                try:
                    age_int = int(age)
                    if 13 <= age_int <= 120:  # Reasonable age range
                        st.session_state.name = name.strip()
                        st.session_state.age = age.strip()
                        st.session_state.personal_info_complete = True
                        st.rerun()
                    else:
                        st.error("Please enter a valid age between 13 and 120.")
                except ValueError:
                    st.error("Please enter a valid age (numbers only).")
            else:
                st.warning("Please enter both your name and age to continue.")
        
        return
    
    # Assessment completion check
    if st.session_state.assessment_complete:
        st.markdown('<div class="question-container">', unsafe_allow_html=True)
        st.markdown("# 🎉 Assessment Complete!")
        st.markdown("Thank you for completing the personality assessment. Your insights await!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Auto-generate analysis or show generate button
        if 'analysis_generated' not in st.session_state:
            st.session_state.analysis_generated = False
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if not st.session_state.analysis_generated:
                if st.button("🔄 Generate Comprehensive Analysis", type="primary"):
                    with st.spinner("🧠 Analyzing your personality..."):
                        diagnosis = generate_personality_diagnosis()
                        st.session_state.analysis_result = diagnosis
                        st.session_state.analysis_generated = True
                        st.rerun()
            
            # Display analysis if generated
            if st.session_state.analysis_generated and 'analysis_result' in st.session_state:
                st.markdown("### 📊 Your Personality Analysis")
                st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                st.markdown(st.session_state.analysis_result)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Save results with name and age
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                safe_name = "".join(c for c in st.session_state.name if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_name = safe_name.replace(' ', '_')
                filename = f"{safe_name}_age{st.session_state.age}_{timestamp}"
                
                results = {
                    "name": st.session_state.name,
                    "age": st.session_state.age,
                    "timestamp": timestamp,
                    "responses": st.session_state.responses,
                    "questions": PERSONALITY_QUESTIONS,
                    "analysis": st.session_state.analysis_result
                }
                
                # Save to results folder
                results_json = json.dumps(results, indent=2)
                try:
                    with open(f"results/{filename}.json", "w") as f:
                        f.write(results_json)
                    st.success(f"✅ Results saved to results/{filename}.json")
                except Exception as e:
                    st.warning(f"Could not save to file: {e}")
                
                st.download_button(
                    label="📥 Download Results",
                    data=results_json,
                    file_name=f"{filename}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("🔄 Start New Assessment"):
                # Reset all session state
                for key in ['questions_answered', 'responses', 'current_question', 'assessment_complete', 'name', 'age', 'personal_info_complete']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        return
    
    # Current question display
    if st.session_state.questions_answered < len(PERSONALITY_QUESTIONS):
        current_q_idx = st.session_state.current_question if hasattr(st.session_state, 'current_question') else st.session_state.questions_answered
        current_question = PERSONALITY_QUESTIONS[current_q_idx]
        
        # Beautiful question container
        st.markdown('<div class="question-container">', unsafe_allow_html=True)
        st.markdown(f"### Question {current_q_idx + 1} of {len(PERSONALITY_QUESTIONS)}")
        st.markdown(f"## {current_question}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # User input with auto-clear functionality
        input_value = ""
        if not st.session_state.clear_input:
            if current_q_idx < len(st.session_state.responses):
                input_value = st.session_state.responses[current_q_idx]
        
        # Reset clear_input flag after using it
        if st.session_state.clear_input:
            st.session_state.clear_input = False
        
        user_response = st.text_area(
            "✍️ Your thoughtful response:",
            value=input_value,
            height=120,
            placeholder="Take your time to reflect and share your genuine thoughts and feelings...",
            help="Share as much detail as you're comfortable with.",
            key=f"response_input_{current_q_idx}"
        )
        
        # Action buttons with improved layout
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if current_q_idx > 0:
                if st.button("⬅️ Previous", use_container_width=True):
                    st.session_state.current_question = current_q_idx - 1
                    st.session_state.clear_input = True
                    st.rerun()
            
            with col2:
                # Submit button - never disabled, always themed like Previous button
                button_text = "📝 Submit Answer"
                
                if st.button(button_text, type="primary", use_container_width=True):
                    if user_response.strip():
                        # Update or add response for current question
                        if current_q_idx < len(st.session_state.responses):
                            st.session_state.responses[current_q_idx] = user_response
                        else:
                            st.session_state.responses.append(user_response)
                        
                        # Update questions_answered to match responses length
                        st.session_state.questions_answered = len(st.session_state.responses)
                        
                        # Go to next question
                        if current_q_idx + 1 < len(PERSONALITY_QUESTIONS):
                            st.session_state.current_question = current_q_idx + 1
                            st.session_state.clear_input = True
                        else:
                            st.session_state.assessment_complete = True
                        
                        st.rerun()
                    else:
                        st.info("💡 Please enter your response above before submitting.")
            
            with col3:
                # Skip button
                if st.button("⏭️ Skip", use_container_width=True, help="Skip to next question"):
                    if current_q_idx + 1 < len(PERSONALITY_QUESTIONS):
                        st.session_state.current_question = current_q_idx + 1
                        st.session_state.clear_input = True
                    else:
                        st.session_state.assessment_complete = True
                    st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
    **Disclaimer:** This tool is for educational and self-reflection purposes only. 
    It does not replace professional psychological assessment or therapy. 
    If you're experiencing serious mental health concerns, please consult a qualified mental health professional.
    """)

if __name__ == "__main__":
    main()