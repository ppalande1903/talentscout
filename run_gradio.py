"""
Launch script for Gradio version
"""
import subprocess
import sys

def main():
    """Launch the Gradio app"""
    try:
        print("🚀 Starting TalentScout AI Hiring Assistant (Gradio)")
        print("📱 Open your browser and go to: http://localhost:7860")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        subprocess.run([sys.executable, "gradio_app.py"])
    except KeyboardInterrupt:
        print("\n👋 Thanks for using TalentScout AI Hiring Assistant!")
    except Exception as e:
        print(f"❌ Error starting the app: {e}")

if __name__ == "__main__":
    main()
