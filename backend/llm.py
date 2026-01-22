import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    # Fallback or warning - though in production code we might want to raise error
    print("Warning: GROQ_API_KEY not found in environment variables.")

def get_groq_llm():
    """
    Initialize and return the Groq LLM instance.
    Uses llama3-70b-8192 as preferred model.
    """
    return ChatGroq(
        temperature=0.6,
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.3-70b-versatile",
        max_tokens=200
    )

def generate_jedi_response(system_prompt: str, user_message: str, history: list = []) -> str:
    """
    Generates a response using the Groq LLM with the specified system prompt.
    Accepts an optional history list of tuples (role, content).
    """
    try:
        llm = get_groq_llm()
        
        messages = [("system", system_prompt)]
        
        # Add history to messages
        for role, content in history:
            # map database roles to langchain roles if needed
            # "user" -> "human", "jedi" -> "ai"
            lc_role = "human" if role == "user" else "ai"
            messages.append((lc_role, content))
            
        messages.append(("human", "{message}"))

        prompt = ChatPromptTemplate.from_messages(messages)
        
        chain = prompt | llm | StrOutputParser()
        
        response = chain.invoke({"message": user_message})
        return response
    except Exception as e:
        print(f"Error generating response: {e}")
        return "The Force is clouded. Try again later, you must."
