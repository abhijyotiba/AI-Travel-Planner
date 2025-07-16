import warnings
# Suppress SyntaxWarnings from langchain-tavily package
warnings.filterwarnings("ignore", category=SyntaxWarning, module="langchain_tavily")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Agent.agent import AgentGraph
from utils.save_document import save_document
from starlette.responses import JSONResponse
import os
import datetime
from dotenv import load_dotenv
from pydantic import BaseModel
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

@app.post("/query")
async def query_travel_agent(query:QueryRequest):
    try:
        print(query)
        graph = AgentGraph()
        react_app = graph()  # This now returns the compiled graph
        
        # Assuming request is a pydantic object like: {"question": "your text"}
        messages={"messages": [query.question]}
        output = react_app.invoke(messages)

        # If result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)
            
        # Save response to markdown file Locally
        #save_path = save_document(final_output)
        #print("Saved response to:", save_path)
    
        
        return {"answer": final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})