from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from schemas import ChatInput, ChatOutput
from prompts import JEDI_SYSTEM_PROMPT
from llm import generate_jedi_response
from yoda_transform import transform_to_osv
import uvicorn
import os
import models
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Jedi-inspired Wise Chatbot API",
    description="A chatbot that speaks with the wisdom of a Jedi.",
    version="1.0.0"
)

# CORS Config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Jedi-inspired Chatbot API is running. The Force is with you."}

@app.post("/chat", response_model=ChatOutput)
async def chat_endpoint(chat_input: ChatInput, db: Session = Depends(get_db)):
    """
    Process user message through the Jedi pipeline:
    1. Check/Create User
    2. Persist User Message
    3. DETECT & LOG HABITS (New!)
    4. Retrieve Context
    5. LLM Generation
    6. Grammar Transformation
    7. Persist Jedi Response
    """
    user_message = chat_input.message
    user_id = chat_input.user_id
    
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # Step 0: User Management
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        db_user = models.User(id=user_id)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    # Step 1: Persist User Message
    user_conv = models.Conversation(user_id=user_id, role="user", content=user_message)
    db.add(user_conv)
    db.commit()

    # Step 1.2: Habit Detection (Simple Keyword Matching)
    # in a real app, use an LLM to classification
    lower_msg = user_message.lower()
    detected_habit = None
    
    habits_map = {
        "water": "Hydration",
        "drank": "Hydration",
        "hydrate": "Hydration",
        "meditat": "Meditation", # meditated, meditating
        "exercise": "Exercise",
        "workout": "Exercise",
        "ran": "Exercise",
        "run": "Exercise",
        "gym": "Exercise",
        "sleep": "Sleep",
        "slept": "Sleep"
    }

    for keyword, habit_name in habits_map.items():
        if keyword in lower_msg:
            detected_habit = habit_name
            break
    
    if detected_habit:
        # Check if habit exists for user
        db_habit = db.query(models.Habit).filter(
            models.Habit.user_id == user_id, 
            models.Habit.name == detected_habit
        ).first()
        
        if not db_habit:
            db_habit = models.Habit(user_id=user_id, name=detected_habit)
            db.add(db_habit)
            db.commit()
            db.refresh(db_habit)
            
        # Log entry
        log_entry = models.HabitLog(habit_id=db_habit.id)
        db.add(log_entry)
        db.commit()
        
        # Add system note so Jedi knows to praise it
        # (We append this to the message context sent to LLM, but not saved in user chat history to keep it clean)
        user_message += f" [System Note: User completed habit '{detected_habit}']"

    # Step 1.5: Retrieve Context (Memory)
    # Fetch last 10 messages for this user, ordered by time
    history_records = db.query(models.Conversation)\
        .filter(models.Conversation.user_id == user_id)\
        .order_by(models.Conversation.created_at.desc())\
        .limit(10)\
        .all()
    
    # Reverse to chronological order (oldest first)
    history_records.reverse()
    
    # Format for LLM
    chat_history = [(msg.role, msg.content) for msg in history_records]

    # Step 2: LLM Generation
    raw_response = generate_jedi_response(JEDI_SYSTEM_PROMPT, user_message, chat_history)
    
    # Step 3: Grammar Transformation (Post-processing)
    # We apply this to ensure the OSV structure is strong, 
    # though the prompt also encourages it.
    final_response = transform_to_osv(raw_response)
    
    # Ensure we don't return empty
    if not final_response:
        final_response = "Meditate on this, I must."

    # Step 4: Persist Jedi Response
    jedi_conv = models.Conversation(user_id=user_id, role="jedi", content=final_response)
    db.add(jedi_conv)
    db.commit()

    return ChatOutput(reply=final_response)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
