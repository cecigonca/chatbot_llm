import sys
import os

# Adiciona o diretório base (chatbot_llm) ao Python Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.interface import rodar_interface

if __name__ == "__main__":
    rodar_interface()
