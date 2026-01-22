import sys
print(f"Python Executable: {sys.executable}")

try:
    import langchain_groq
    print("SUCCESS: langchain_groq imported.")
except ImportError as e:
    print(f"ERROR: {e}")

try:
    import fastapi
    print("SUCCESS: fastapi imported.")
except ImportError as e:
    print(f"ERROR: {e}")
