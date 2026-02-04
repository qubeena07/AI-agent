# from dotenv import load_dotenv
# from pydantic import BaseModel
# from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import PydanticOutputParser
# #from langchain.agents import AgentExecutor, create_openai_tools_agent
# from langchain_classic.agents import AgentExecutor
# from langchain_classic.agents import create_tool_calling_agent
# from tools import search_tool , wiki_tool , save_tool



# load_dotenv()  # Load environment variables from .env file


# class ResearchResponse(BaseModel):
#     topic: str
#     summary: str
#     sources: list[str]
#     tools_used: list[str]



#  # Example for Gemini model
# llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro",)  # Example for Gemini model
# llm2 = ChatAnthropic(model="claude-3-opus-20241022",)  # Example for Anthropic model
# llm3 = ChatOpenAI(model="gpt-4o",)  # Example for OpenAI model

# parser = PydanticOutputParser(pydantic_object=ResearchResponse)
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", """You are an expert research assistant. 
#         You will research the given topic and provide a 
#         concise summary along with credible sources and 
#         tools used for the research. Answer the user query and use necessary tools. 
#         Wrap the output in this format and provide no other text \n{format_instructions}"""),
#         ("placeholder", "{chat_history}"),
#         ("human", "{query}"),
#         ("placeholder", "{agent_scratchpad}"),
#     ]
# ).partial(format_instructions=parser.get_format_instructions())

# tools = [search_tool, wiki_tool,save_tool]

# agent = create_tool_calling_agent(
#     llm=llm,
#     tools=tools,
#     prompt=prompt,
#     # output_parser=parser,
# )
# agent_executor = AgentExecutor.from_agent_and_tools(
#     agent=agent,
#     tools=tools,
#     verbose=True,
# )

# query = input("What can I search for you today? ")

# raw_response = agent_executor.invoke(
#     {
#         "query": query
#     }
# )

# try:
#     output = raw_response.get("output")
#     if isinstance(output, list):
#         output = "".join(
#             part.get("text", "") if isinstance(part, dict) else str(part)
#             for part in output
#         )
#     elif output is not None and not isinstance(output, str):
#         output = str(output)

#     structured_response = parser.parse(output or "")
#     print(f"\nStructured Response:{structured_response}\n")
# except Exception as e:
#     print(f"Error parsing response: {e}")



# main.py
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

from tools import search_tool, wiki_tool, save_tool
from rag_tool import get_rag_tool # Import your new RAG tool

load_dotenv()

def get_agent():
    # Initialize Model
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro")

    # Initialize Tools (Add RAG tool if file exists)
    tools = [search_tool, wiki_tool, save_tool]
    rag_tool = get_rag_tool("knowledge.pdf") # specific file to search
    if rag_tool:
        tools.append(rag_tool)

    # Create Prompt (Added chat_history handling)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful research assistant. Use your tools to find information."),
            ("placeholder", "{chat_history}"), # KEY for memory
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    # Create Agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Return Executor
    return AgentExecutor(agent=agent, tools=tools, verbose=True)