from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool
from datetime import datetime

def save_to_txt(data:str, filename:str="research_output.txt"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_filename = f"{filename.split('.')[0]}_{timestamp}.txt"
    with open(full_filename, "a",encoding="utf-8") as f:
        f.write(data)
    return f"Data saved to {full_filename}"

save_tool = Tool(
    name="Save_to_Text_File",
    func=save_to_txt,
    description="Saves the provided data to a text file with a timestamped filename. Use this tool when you need to store research findings or any other information for future reference.",
    )

search = DuckDuckGoSearchRun()

search_tool = Tool(
    name="DuckDuckGo_Search",
    func=search.run,
    description="Search the web for relevant information to answer the user's query. Use this tool when you need to find current information or specific details about a topic.",
    )

api_wrapper = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)


