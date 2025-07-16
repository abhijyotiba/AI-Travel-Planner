from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
import os
from Tools.Calculator_And_currency_tool import CurrencyCalculator
from Tools.Place_search_tool import PlaceSearchTool
from Tools.weather_tool import WeatherTool
from Tools.itenary_planner_tool import ItineraryPlannerTool
from Prompt.system_prompt import SYSTEM_PROMPT

load_dotenv()

class AgentGraph:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            model="mistralai/mistral-small-3.2-24b-instruct"
        )
        
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
        
        # Simple system prompt
        self.system_prompt = SYSTEM_PROMPT
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        
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
        
        graph = builder.compile()
        return graph
    
    def __call__(self):
        """Return the compiled graph"""
        return self.graph

