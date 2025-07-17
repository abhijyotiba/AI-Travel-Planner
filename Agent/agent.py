from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
import os
from Tools.Calculator_And_currency_tool import CurrencyCalculator
from Tools.Place_search_tool import PlaceSearchTool
from Tools.weather_tool import WeatherTool
from Tools.itenary_planner_tool import ItineraryPlannerTool
from Prompt.system_prompt import SYSTEM_PROMPT
from utils.llm_loader import load_llm

load_dotenv()

class AgentGraph:
    def __init__(self):
        
        self.llm = load_llm()
        
        self.currency_convertor = CurrencyCalculator()
        self.place_search = PlaceSearchTool()
        self.weather_forcast = WeatherTool()
        self.itenary_planner = ItineraryPlannerTool()
        
        # Flatten the tools list properly
        self.tools = []
        self.tools.extend(self.currency_convertor.currency_calculator_tools_list)
        self.tools.extend(self.place_search.place_search_tool_list)
        self.tools.extend(self.weather_forcast.weather_tool_list)
        self.tools.extend(self.itenary_planner.itinerary_tool_list)
        
        # System prompt
        self.system_prompt = SYSTEM_PROMPT
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        
        # Initialize memory saver for conversation persistence
        self.memory = MemorySaver()
        
        # Build the graph on initialization
        self.graph = self.build_graph()
    
    def agent_function(self, state: MessagesState):
        """Main agent function"""
        user_question = state["messages"]
        # SYSTEM_PROMPT is already a SystemMessage object
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": [response]}
    
    def build_graph(self):
        """Build the LangGraph workflow"""
        builder = StateGraph(MessagesState)
        
        # Note: tools_condition expects a node named 'tools' (lowercase)
        builder.add_node("agent", self.agent_function)
        builder.add_node("tools", ToolNode(self.tools))
        
        builder.add_edge(START, "agent")
        builder.add_conditional_edges("agent", tools_condition)
        builder.add_edge("tools","agent")
        
        # Compile with memory saver for conversation persistence
        graph = builder.compile(checkpointer=self.memory)
        return graph
    
    def invoke_with_config(self, messages, session_id):
        """Invoke the graph with session-specific configuration"""
        config = {"configurable": {"thread_id": session_id}}
        return self.graph.invoke(messages, config=config)
    
    def get_session_history(self, session_id):
        """Get conversation history for a specific session"""
        try:
            config = {"configurable": {"thread_id": session_id}}
            # Get the current state for this session
            state = self.graph.get_state(config)
            return state.values.get("messages", []) if state.values else []
        except Exception as e:
            print(f"Error retrieving session history: {e}")
            return []
    
    def clear_session(self, session_id):
        """Clear conversation history for a specific session"""
        try:
            config = {"configurable": {"thread_id": session_id}}
            # Use the correct method to clear session state
            # Get current state first
            current_state = self.graph.get_state(config)
            if current_state and current_state.values:
                # Clear by setting empty messages
                empty_state = {"messages": []}
                # Use update_state to clear the session
                self.graph.update_state(config, empty_state, as_node="agent")
            return True
        except Exception as e:
            print(f"Error clearing session: {e}")
            return False

    def __call__(self):
        """Return the compiled graph"""
        return self.graph

