import warnings
# Suppress SyntaxWarnings from langchain-tavily package
warnings.filterwarnings("ignore", category=SyntaxWarning, module="langchain_tavily")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from Agent.agent import AgentGraph
from starlette.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
import os
import uuid
from typing import List, Optional

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None

class ClearSessionRequest(BaseModel):
    session_id: str
    
graph = AgentGraph()    

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        # Use session-based invocation with memory
        session_id = query.session_id or str(uuid.uuid4())
        
        print(f"Processing query for session: {session_id}")
        print(f"Query: {query.question}")
        
        # Create message input with proper format
        messages = {"messages": [HumanMessage(content=query.question)]}
        
        # Invoke with session configuration for memory persistence
        output = graph.invoke_with_config(messages, session_id)
        
        print(f"Graph output type: {type(output)}")
        print(f"Graph output: {output}")

        # Extract the AI response
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)
        
        return {"answer": final_output, "session_id": session_id}
    except Exception as e:
        print(f"Error in query_travel_agent: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/clear-session")
async def clear_session(request: ClearSessionRequest):
    """Clear conversation history for a specific session using LangGraph memory"""
    try:
        session_id = request.session_id
        if graph.clear_session(session_id):
            return {"message": f"Session {session_id} cleared successfully"}
        else:
            return {"message": f"Failed to clear session {session_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing session: {str(e)}")

@app.get("/session-info/{session_id}")
async def get_session_info(session_id: str):
    """Get information about a conversation session using LangGraph memory"""
    try:
        history = graph.get_session_history(session_id)
        message_count = len(history)
        
        return {
            "session_id": session_id,
            "message_count": message_count,
            "exists": message_count > 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting session info: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "AI Travel Agent is running"}


