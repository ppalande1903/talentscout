import gradio as gr
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import time
import random

class CandidateInfo:
    def __init__(self):
        self.full_name = ""
        self.email = ""
        self.phone = ""
        self.experience_years = ""
        self.desired_position = ""
        self.location = ""
        self.tech_stack = []

class HiringAssistant:
    def __init__(self):
        self.conversation_stages = [
            "greeting", "name_collection", "email_collection", "phone_collection",
            "experience_collection", "position_collection", "location_collection",
            "tech_stack_collection", "technical_questions", "conclusion"
        ]
        self.stage_names = {
            "greeting": "Welcome",
            "name_collection": "Personal Info",
            "email_collection": "Contact Details", 
            "phone_collection": "Phone Verification",
            "experience_collection": "Experience",
            "position_collection": "Position Interest",
            "location_collection": "Location",
            "tech_stack_collection": "Technical Skills",
            "technical_questions": "Technical Assessment",
            "conclusion": "Completion"
        }
        self.current_stage_index = 0
        self.candidate_info = CandidateInfo()
        self.technical_questions = []
        self.current_question_index = 0
        self.conversation_ended = False
        
        # Tech keywords for extraction
        self.tech_keywords = [
            "python", "java", "javascript", "typescript", "react", "angular", "vue",
            "node.js", "django", "flask", "spring", "express", "mysql", "postgresql",
            "mongodb", "redis", "aws", "azure", "gcp", "docker", "kubernetes", "git"
        ]
        
        # Technical questions database
        self.question_templates = {
            "python": [
                "What is the difference between list and tuple in Python?",
                "Explain Python's GIL (Global Interpreter Lock) and its implications.",
                "How do you handle exceptions in Python? Provide an example."
            ],
            "javascript": [
                "What is the difference between == and === in JavaScript?",
                "Explain closures in JavaScript with an example.",
                "What is the event loop in JavaScript and how does it work?"
            ],
            "react": [
                "What is the difference between state and props in React?",
                "Explain the React component lifecycle methods.",
                "What are React Hooks and why are they useful?"
            ],
            "general": [
                "Describe a challenging technical problem you've solved recently.",
                "How do you stay updated with new technologies in your field?",
                "What's your approach to debugging complex issues in your code?"
            ]
        }
    
    def get_current_stage(self):
        if self.current_stage_index < len(self.conversation_stages):
            return self.conversation_stages[self.current_stage_index]
        return "conclusion"
    
    def get_stage_name(self, stage):
        return self.stage_names.get(stage, stage.replace('_', ' ').title())
    
    def get_progress(self):
        return (self.current_stage_index / len(self.conversation_stages)) * 100
    
    def advance_stage(self):
        self.current_stage_index += 1
    
    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone):
        digits_only = re.sub(r'\D', '', phone)
        return 10 <= len(digits_only) <= 15
    
    def extract_tech_stack(self, user_input):
        found_tech = []
        user_lower = user_input.lower()
        
        for tech in self.tech_keywords:
            if tech in user_lower:
                found_tech.append(tech.title())
        
        return found_tech
    
    def generate_technical_questions(self, tech_stack):
        questions = []
        
        for tech in tech_stack[:3]:
            tech_lower = tech.lower()
            if tech_lower in self.question_templates:
                questions.extend(self.question_templates[tech_lower][:2])
        
        if not questions:
            questions = self.question_templates["general"][:3]
        
        return questions[:5]
    
    def get_candidate_summary(self):
        summary = []
        if self.candidate_info.full_name:
            summary.append(f"**Name:** {self.candidate_info.full_name}")
        if self.candidate_info.email:
            summary.append(f"**Email:** {self.candidate_info.email}")
        if self.candidate_info.phone:
            summary.append(f"**Phone:** {self.candidate_info.phone}")
        if self.candidate_info.experience_years:
            summary.append(f"**Experience:** {self.candidate_info.experience_years} years")
        if self.candidate_info.desired_position:
            summary.append(f"**Position:** {self.candidate_info.desired_position}")
        if self.candidate_info.location:
            summary.append(f"**Location:** {self.candidate_info.location}")
        if self.candidate_info.tech_stack:
            summary.append(f"**Tech Stack:** {', '.join(self.candidate_info.tech_stack)}")
        
        return "\n".join(summary) if summary else "No information collected yet."
    
    def get_response(self, user_input):
        current_stage = self.get_current_stage()
        
        if current_stage == "greeting":
            self.advance_stage()
            return """Hello! 👋 Welcome to TalentScout's AI Hiring Assistant!

I'm here to help with your initial screening for technology positions. I'll gather some basic information about you and ask a few technical questions based on your expertise.

This should take about 5-10 minutes. You can end our conversation anytime by typing 'exit'.

Let's get started! What's your full name?"""

        elif current_stage == "name_collection":
            if user_input.strip():
                self.candidate_info.full_name = user_input.strip()
                self.advance_stage()
                return f"Nice to meet you, {self.candidate_info.full_name}! 😊\n\nCould you please provide your email address?"
            else:
                return "Please provide your full name to continue."

        elif current_stage == "email_collection":
            if self.validate_email(user_input.strip()):
                self.candidate_info.email = user_input.strip()
                self.advance_stage()
                return "Great! Now, what's your phone number?"
            else:
                return "Please provide a valid email address (e.g., john@example.com)."

        elif current_stage == "phone_collection":
            if self.validate_phone(user_input.strip()):
                self.candidate_info.phone = user_input.strip()
                self.advance_stage()
                return "Perfect! How many years of professional experience do you have in technology?"
            else:
                return "Please provide a valid phone number."

        elif current_stage == "experience_collection":
            if user_input.strip():
                self.candidate_info.experience_years = user_input.strip()
                self.advance_stage()
                return "Thanks! What position(s) are you interested in? (e.g., Software Developer, Data Scientist, DevOps Engineer)"
            else:
                return "Please specify your years of experience."

        elif current_stage == "position_collection":
            if user_input.strip():
                self.candidate_info.desired_position = user_input.strip()
                self.advance_stage()
                return "Excellent! What's your current location (city, state/country)?"
            else:
                return "Please specify the position you're interested in."

        elif current_stage == "location_collection":
            if user_input.strip():
                self.candidate_info.location = user_input.strip()
                self.advance_stage()
                return """Now for the technical part! 💻

Please tell me about your tech stack. List the programming languages, frameworks, databases, and tools you're proficient in.

For example: "Python, Django, React, PostgreSQL, AWS, Docker" """
            else:
                return "Please provide your current location."

        elif current_stage == "tech_stack_collection":
            if user_input.strip():
                tech_stack = self.extract_tech_stack(user_input)
                if tech_stack:
                    self.candidate_info.tech_stack = tech_stack
                    self.technical_questions = self.generate_technical_questions(tech_stack)
                    self.advance_stage()
                    return f"""Perfect! I've identified your expertise in: {', '.join(tech_stack)}

Now I'll ask you {len(self.technical_questions)} technical questions to assess your proficiency.

**Question 1:** {self.technical_questions[0] if self.technical_questions else "Tell me about a recent project you've worked on."}"""
                else:
                    return "I couldn't identify specific technologies. Please mention specific programming languages, frameworks, or tools you know (e.g., Python, React, MySQL, etc.)."
            else:
                return "Please tell me about your technical skills and tools you use."

        elif current_stage == "technical_questions":
            if user_input.strip():
                self.current_question_index += 1
                
                if self.current_question_index < len(self.technical_questions):
                    return f"Thank you for your answer! 👍\n\n**Question {self.current_question_index + 1}:** {self.technical_questions[self.current_question_index]}"
                else:
                    self.advance_stage()
                    return """Excellent! You've completed all the technical questions. 🎉

Thank you for taking the time to complete this screening! Our recruitment team will review your responses and contact you within 2-3 business days if your profile matches our current openings.

Is there anything else you'd like to know about TalentScout or our process?"""
            else:
                return "Please provide an answer to continue with the next question."

        else:
            self.conversation_ended = True
            return """Thank you for your interest in TalentScout! 🌟

Your information has been recorded and our team will be in touch soon.

Have a wonderful day, and good luck with your job search!"""

# Global assistant instance
assistant = HiringAssistant()

def chat_interface(message, history):
    """Main chat interface function"""
    global assistant
    
    if message.lower().strip() in ['exit', 'quit', 'bye', 'goodbye']:
        assistant.conversation_ended = True
        return "Thank you for your time! Have a great day! 👋"
    
    # Get response from assistant
    response = assistant.get_response(message)
    
    # Add some delay to simulate thinking
    time.sleep(1)
    
    return response

def get_progress_info():
    """Get current progress information"""
    global assistant
    current_stage = assistant.get_current_stage()
    progress = assistant.get_progress()
    stage_name = assistant.get_stage_name(current_stage)
    
    return f"**Current Stage:** {stage_name}\n**Progress:** {progress:.0f}% Complete"

def get_candidate_info():
    """Get candidate information summary"""
    global assistant
    return assistant.get_candidate_summary()

def reset_conversation():
    """Reset the conversation"""
    global assistant
    assistant = HiringAssistant()
    return "Conversation reset! Click 'Start Conversation' to begin again.", "", ""

def start_conversation():
    """Start the conversation"""
    global assistant
    welcome_message = assistant.get_response("")
    return [(None, welcome_message)]

# Custom CSS for better styling
custom_css = """
.gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.header-text {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
}

.info-panel {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #667eea;
}

.progress-panel {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #2196f3;
}

.candidate-panel {
    background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #9c27b0;
}
"""

# Create the Gradio interface
with gr.Blocks(css=custom_css, title="TalentScout AI Hiring Assistant", theme=gr.themes.Soft()) as demo:
    # Header
    gr.HTML("""
    <div class="header-text">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤖 TalentScout AI Hiring Assistant</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Your intelligent partner for tech talent screening</p>
    </div>
    """)
    
    with gr.Row():
        # Left column - Chat interface
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(
                height=500,
                show_label=False,
                container=True,
                bubble_full_width=False,
                avatar_images=("👤", "🤖")
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Type your response here...",
                    show_label=False,
                    container=False,
                    scale=4
                )
                send_btn = gr.Button("Send", variant="primary", scale=1)
            
            with gr.Row():
                start_btn = gr.Button("🚀 Start Conversation", variant="secondary")
                reset_btn = gr.Button("🔄 Reset Conversation", variant="stop")
        
        # Right column - Information panels
        with gr.Column(scale=1):
            # About section
            gr.HTML("""
            <div class="info-panel">
                <h3>ℹ️ About This Assistant</h3>
                <ul style="margin: 1rem 0;">
                    <li>✅ Collecting basic information</li>
                    <li>✅ Understanding your tech stack</li>
                    <li>✅ Asking relevant technical questions</li>
                    <li>✅ Providing smooth interview experience</li>
                </ul>
                <div style="margin-top: 1rem; padding: 1rem; background: rgba(0,0,0,0.05); border-radius: 8px; font-size: 0.9rem;">
                    <strong>Privacy Notice:</strong> All data is handled securely and used only for recruitment purposes.
                </div>
            </div>
            """)
            
            # Progress section
            progress_display = gr.Markdown(
                value="**Current Stage:** Welcome\n**Progress:** 0% Complete",
                elem_classes=["progress-panel"]
            )
            
            # Candidate info section
            candidate_display = gr.Markdown(
                value="No information collected yet.",
                elem_classes=["candidate-panel"]
            )
    
    # Event handlers
    def respond(message, chat_history):
        if not message.strip():
            return chat_history, ""
        
        # Add user message to history
        chat_history.append((message, None))
        
        # Get bot response
        bot_response = chat_interface(message, chat_history)
        
        # Add bot response to history
        chat_history[-1] = (message, bot_response)
        
        return chat_history, ""
    
    def update_info():
        progress_info = get_progress_info()
        candidate_info = get_candidate_info()
        return progress_info, candidate_info
    
    # Button events
    send_btn.click(
        respond,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    ).then(
        update_info,
        outputs=[progress_display, candidate_display]
    )
    
    msg.submit(
        respond,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    ).then(
        update_info,
        outputs=[progress_display, candidate_display]
    )
    
    start_btn.click(
        start_conversation,
        outputs=[chatbot]
    ).then(
        update_info,
        outputs=[progress_display, candidate_display]
    )
    
    reset_btn.click(
        reset_conversation,
        outputs=[chatbot, progress_display, candidate_display]
    )
    
    # Footer
    gr.HTML("""
    <div style="text-align: center; padding: 2rem; color: #666; border-top: 1px solid #eee; margin-top: 2rem;">
        <h3>🏢 TalentScout - Connecting Tech Talent with Opportunities</h3>
        <p><small>Built with Gradio • Powered by AI • Designed for Excellence</small></p>
    </div>
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True,
        debug=True
    )
