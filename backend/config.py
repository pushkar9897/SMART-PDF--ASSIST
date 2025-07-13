# import os
# from dotenv import load_dotenv

# load_dotenv()
# GEMINI_KEY = os.getenv("AIzaSyBIUsa9x28jX0mC21dUxENxR-d-qMtID80")


import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_KEY = os.getenv("GOOGLE_GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")