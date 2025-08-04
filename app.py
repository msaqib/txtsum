import tkinter as tk
import sys
import threading
import os

# Add the current directory to Python path to import gui_components
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import TextSummarizerGUI
class TextSummarizerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.gui = TextSummarizerGUI(self.root)
        
        # Set up callbacks
        self.gui.on_summarize = self.summarize_text
        self.gui.on_check_connection = self.check_ollama_connection
        self.gui.on_load_models = self.load_available_models
        
    def summarize_text(self, text, model, max_length):
        """
        Main summarization logic - replace this with actual LLM integration
        
        Args:
            text (str): Text to summarize
            model (str): Selected model name
            max_length (int): Maximum length for summary
            
        Returns:
            str: Generated summary
        """
        # TODO: Replace with actual Ollama integration
        # For now, return a placeholder summary
        
        # Example of what the actual implementation would look like:
        import ollama
        try:
            response = ollama.chat(
                model=model,
                messages=[{
                    'role': 'user', 
                    'content': f'Please summarize the following text in approximately {max_length} characters:\n\n{text}'
                }]
            )
            return response['message']['content']
        except Exception as e:
            raise Exception(f"Failed to generate summary: {str(e)}")
        
        # Placeholder implementation
        word_count = len(text.split())
        char_count = len(text)
        
        placeholder_summary = f"""PLACEHOLDER SUMMARY:
        
This is a placeholder summary for development purposes.

Original text statistics:
- Word count: {word_count}
- Character count: {char_count}
- Selected model: {model}
- Max length: {max_length}

To integrate with Ollama:
1. Install: pip install ollama
2. Uncomment the ollama code above
3. Make sure Ollama is running locally

The actual summary would appear here once LLM integration is complete."""

        return placeholder_summary
    
    def load_available_models(self):
        """
        Load list of available models from Ollama
        
        Returns:
            list: List of available model names
        """
        # TODO: Replace with actual Ollama integration
        # Example implementation:
        import ollama
        try:
            response = ollama.list()
            models = [model.model for model in response.models]
            return models
        except Exception as e:
            raise Exception(f"Failed to load models: {str(e)}")
        
        
    def check_ollama_connection(self):
        """
        Check if Ollama is running and accessible
        
        Returns:
            bool: True if connected, False otherwise
        """
        # TODO: Replace with actual Ollama connection check
        # Example implementation:
        import ollama
        try:
            # Try to list available models
            models = ollama.list()
            return True
        except:
            return False
        
        # Placeholder implementation
        print("Checking Ollama connection...")
        # For development, return True to simulate connection
        return True
        
    def run(self):
        """Start the application"""
        try:
            def init_model_loading():
                try:
                    if self.gui.on_check_connection and self.gui.on_check_connection():
                        self.root.after(0, self.gui.load_available_models)
                    else:
                        self.root.after(0, lambda: self.gui.update_status("● Ollama not reachable"))
                except Exception as e:
                    self.root.after(0, lambda: self.gui.update_status(f"● Error: {e}"))

            threading.Thread(target=init_model_loading, daemon=True).start()
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nApplication closed by user")
        except Exception as e:
            print(f"Application error: {e}")

def main():
    """Main entry point"""
    app = TextSummarizerApp()
    app.run()

if __name__ == "__main__":
    main()