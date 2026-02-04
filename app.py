import streamlit as st
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_core.messages import HumanMessage, AIMessage
from main import get_agent


st.set_page_config(page_title="GenAI Research Assistant", page_icon="🤖")

st.title("🤖 GenAI Research Assistant")
st.caption("Powered by Gemini 2.5, LangChain & Custom Tools")

#initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! I can search the web, Wikipedia, or analyze your PDF. What do you need?"}
    ]
#display chat messages from history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

#handle user input
if prompt := st.chat_input("Type your message here..."):
    #add user message to chat history

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    #run agent 
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container()) 

        #get agent
        agent_executor = get_agent()
        
        #prepare history from Langchain
        chat_history = []
        for msg in st.session_state.messages[:-1]:
            if msg["role"] == "user":
                chat_history.append(HumanMessage(content=msg["content"]))
            else:
                chat_history.append(AIMessage(content=msg["content"]))

        #execute
        response = agent_executor.invoke(
            {
                "query": prompt,
                "chat_history": chat_history
            },
            callbacks=[st_callback]
        )
    
        output_text = response["output"]

        #display and save response
        st.write(output_text)
        st.session_state.messages.append({"role": "assistant", "content": output_text})