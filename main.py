from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()  # Load environment variables from .env file

 # Example for Gemini model
llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro",)  # Example for Gemini model
llm2 = ChatAnthropic(model="claude-3-opus-20241022",)  # Example for Anthropic model
llm3 = ChatOpenAI(model="gpt-4o",)  # Example for OpenAI model

response = llm.invoke("Hello, how are you?")
print("OpenAI Response:", response.text)



