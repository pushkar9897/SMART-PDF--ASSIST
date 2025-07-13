# import os
# from dotenv import load_dotenv

# load_dotenv()
# GEMINI_KEY = os.getenv("")


import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_KEY = os.getenv("GOOGLE_GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
