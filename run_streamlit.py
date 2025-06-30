"""
Launch script for Streamlit version
"""
import subprocess
import sys

def main():
    """Launch the Streamlit app"""
    try:
        print("🚀 Starting TalentScout AI Hiring Assistant (Streamlit)")
        print("📱 Open your browser and go to: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--theme.primaryColor", "#667eea",
            "--theme.backgroundColor", "#ffffff",
            "--theme.secondaryBackgroundColor", "#f8f9fa"
        ])
    except KeyboardInterrupt:
        print("\n👋 Thanks for using TalentScout AI Hiring Assistant!")
    except Exception as e:
        print(f"❌ Error starting the app: {e}")

if __name__ == "__main__":
    main()
