from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
#from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_tool_calling_agent




load_dotenv()  # Load environment variables from .env file


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]



 # Example for Gemini model
llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro",)  # Example for Gemini model
llm2 = ChatAnthropic(model="claude-3-opus-20241022",)  # Example for Anthropic model
llm3 = ChatOpenAI(model="gpt-4o",)  # Example for OpenAI model

parser = PydanticOutputParser(pydantic_object=ResearchResponse)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are an expert research assistant. 
        You will research the given topic and provide a 
        concise summary along with credible sources and 
        tools used for the research. Answer the user query and use necessary tools. 
        Wrap the output in this format and provide no other text \n{format_instructions}"""),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

agent = create_tool_calling_agent(
    llm=llm,
    tools=[],
    prompt=prompt,
    # output_parser=parser,
)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=[],
    verbose=True,
)
raw_response = agent_executor.invoke(
    {
        "query":"What are the latest advancements in AI for healthcare?"
    }
)
print(raw_response)



