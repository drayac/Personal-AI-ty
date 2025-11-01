# AI Personality Assessment

A beautiful, **privacy-focused** personality assessment tool powered by **local AI**. Get comprehensive personality insights without sharing your data with cloud services.

## ✨ Features

- **🔒 100% Private**: All AI processing happens locally on your computer
- **🎨 Beautiful Interface**: Modern, gradient-based design with smooth interactions
- **🤖 Local AI**: Powered by Ollama with Llama 2 model (no API keys needed)
- **📊 Comprehensive Analysis**: 10 carefully designed personality questions
- **🔄 Navigate Freely**: Go back and edit previous answers
- **💬 AI Insights**: Get one thoughtful follow-up question per response
- **📈 Progress Tracking**: Visual progress bar and response history
- **📥 Export Results**: Download complete assessment as JSON

## 🚀 Quick Start

**One command setup:**

```bash
chmod +x setup.sh && ./setup.sh
```

**Then run:**

```bash
source personality_app_env/bin/activate
streamlit run personality_app.py
```

The app will open at `http://localhost:8501` with a beautiful, private AI personality assessment ready to use!

## 🛠️ Manual Setup

If you prefer to set up manually:

### 1. Install Python Dependencies

```bash
# Create and activate virtual environment
python3 -m venv personality_app_env
source personality_app_env/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Install Ollama (Local AI)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Download the AI model
ollama pull llama2

# Start Ollama server
ollama serve
```

### 3. Run the App

```bash
# In a new terminal, with virtual environment activated
source personality_app_env/bin/activate
streamlit run personality_app.py
```

## 🎯 How It Works

1. **🚀 Start Assessment**: Beautiful welcome screen guides you through setup
2. **✍️ Answer Questions**: Respond to 10 thoughtful personality questions
3. **🤖 AI Insights**: Get one personalized follow-up question per response
4. **🔄 Navigate Freely**: Go back to edit any previous answer
5. **📊 Get Analysis**: Receive comprehensive personality insights
6. **📥 Save Results**: Download your complete assessment

## 🎨 Visual Features

- **Gradient Backgrounds**: Beautiful color schemes throughout the interface
- **Real-time Status**: Live Ollama connection indicator in sidebar
- **Progress Tracking**: Visual progress bar and completed questions overview
- **Smooth Interactions**: Hover effects and transitions for better UX
- **Responsive Design**: Works great on desktop and tablet devices

## 🧠 Assessment Coverage

### Personality Dimensions
1. **Energy Sources** (Introversion/Extraversion)
2. **Decision Making** (Thinking/Feeling) 
3. **Life Approach** (Planning/Spontaneity)
4. **Stress Management** & Coping Strategies
5. **Work Environment** Preferences
6. **Feedback Reception** & Growth Mindset
7. **Core Fears** & Anxieties
8. **Relationship Dynamics** & Social Connection
9. **Sleep & Mood** Patterns
10. **Change Adaptation** & Resilience

### AI Analysis Provides
- **Personality Type** Classification (Myers-Briggs style)
- **Core Strengths** & Natural Talents
- **Growth Areas** & Development Opportunities  
- **Mental Health Indicators** (Stress, Anxiety, Mood)
- **Personalized Recommendations** & Coping Strategies

## 🔧 Technical Details

### Requirements
- **Python 3.8+**
- **4GB+ RAM** (for Llama 2 model)
- **5GB+ Storage** (for model download)
- **Modern Browser** (Chrome, Firefox, Safari, Edge)

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **AI Backend**: Ollama serving Llama 2 model locally
- **Data Storage**: Local session state (no external databases)
- **Privacy**: All processing happens on your computer

## 🛠️ Troubleshooting

### Common Issues

**🔴 "Ollama not running" error:**
```bash
# Start Ollama server
ollama serve
```

**🔴 "Model not found" error:**
```bash
# Download the required model
ollama pull llama2
```

**🔴 First response is slow:**
- This is normal - the model loads on first use
- Subsequent responses will be faster

**🔴 App won't start:**
```bash
# Ensure virtual environment is activated
source personality_app_env/bin/activate

# Reinstall if needed
pip install -r requirements.txt
```

### Quick Diagnostics

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Check downloaded models
ollama list

# Restart everything
killall ollama
ollama serve &
streamlit run personality_app.py
```

## 🔒 Privacy & Ethics

### Data Privacy
- **100% Local Processing**: No data ever leaves your computer
- **No Cloud Services**: All AI processing happens locally  
- **No Data Collection**: App doesn't store or transmit personal information
- **Session-Based**: Data only exists during your session

### Ethical Use
- **Educational Purpose**: For self-reflection and personal growth
- **Not Diagnostic**: Not a replacement for professional psychology
- **Responsible AI**: Prompts encourage seeking professional help when appropriate
- **Transparent**: Open source code for full transparency

## 📚 Additional Resources

### Understanding Your Results
- Research Myers-Briggs personality types
- Explore Big Five personality framework
- Consider professional personality assessments
- Use insights for personal development

### Mental Health Support
- Contact professional counselors for serious concerns
- Explore therapy options in your area
- Use results as conversation starters with mental health professionals
- Remember: AI insights complement but don't replace human expertise

## 🤝 Contributing

This is an open-source educational project. Feel free to:
- Report issues or suggestions
- Improve the interface design
- Add new personality questions
- Enhance AI prompts for better insights
- Translate to other languages

---

**Disclaimer**: This tool is for educational and self-reflection purposes only. It does not replace professional psychological assessment or mental health consultation. Always seek professional help for serious mental health concerns.