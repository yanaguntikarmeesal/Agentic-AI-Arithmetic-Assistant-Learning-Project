
# ============================================================
# 🧮 AGENTIC AI ARITHMETIC ASSISTANT
# Streamlit + Groq + LangChain + LangGraph
# ============================================================

import operator
from typing import Literal
import streamlit as st

from typing_extensions import TypedDict, Annotated
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import (
    AnyMessage,
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
)
from langgraph.graph import StateGraph, START, END


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Arithmetic Assistant",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. CUSTOM CSS
# ============================================================

st.markdown("""
<style>
    .stApp {
        background-color: #f4f7fb;
    }

    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #243b64;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .info-card {
        background: white;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        margin-bottom: 12px;
    }

    .info-card h4 {
        color: #2563eb;
        margin-bottom: 8px;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        padding: 10px;
    }

    [data-testid="stChatMessage"] {
        border-radius: 12px;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🧮 AI Arithmetic Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'An Agentic AI calculator powered by Groq, LangChain and LangGraph'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# 4. SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "llm_calls" not in st.session_state:
    st.session_state.llm_calls = 0


# ============================================================
# 5. ARITHMETIC TOOLS
# ============================================================

@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@tool
def divide(a: float, b: float) -> float:
    """Divide the first number by the second number."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


tools = [add, multiply, divide]
tools_by_name = {item.name: item for item in tools}


# ============================================================
# 6. AGENT STATE
# ============================================================

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


# ============================================================
# 7. BUILD LANGGRAPH AGENT
# ============================================================

@st.cache_resource
def build_agent(api_key: str, model_name: str):

    model = ChatGroq(
        api_key=api_key,
        model=model_name,
        temperature=0,
    )

    model_with_tools = model.bind_tools(tools)

    def llm_call(state: MessagesState):
        """Call the language model."""

        system_message = SystemMessage(
            content=(
                "You are a helpful arithmetic assistant. "
                "Use the available tools for addition, multiplication, "
                "and division. Always use tools to perform calculations. "
                "For multi-step calculations, execute each step in order. "
                "Explain the final answer clearly. "
                "If the user asks something unrelated to arithmetic, "
                "politely explain your purpose."
            )
        )

        conversation = [system_message] + state["messages"]

        response = model_with_tools.invoke(conversation)

        return {
            "messages": [response],
            "llm_calls": state.get("llm_calls", 0) + 1,
        }

    def tool_node(state: MessagesState):
        """Execute tools requested by the model."""

        results = []
        last_message = state["messages"][-1]

        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            selected_tool = tools_by_name.get(tool_name)

            if selected_tool is None:
                observation = f"Unknown tool: {tool_name}"
            else:
                try:
                    observation = str(
                        selected_tool.invoke(tool_args)
                    )
                except Exception as error:
                    observation = f"Tool error: {error}"

            results.append(
                ToolMessage(
                    content=observation,
                    tool_call_id=tool_call["id"],
                )
            )

        return {"messages": results}

    def should_continue(
        state: MessagesState,
    ) -> Literal["tool_node", "__end__"]:

        last_message = state["messages"][-1]

        if last_message.tool_calls:
            return "tool_node"

        return END

    # Build graph
    graph_builder = StateGraph(MessagesState)

    graph_builder.add_node("llm_call", llm_call)
    graph_builder.add_node("tool_node", tool_node)

    graph_builder.add_edge(START, "llm_call")

    graph_builder.add_conditional_edges(
        "llm_call",
        should_continue,
        ["tool_node", END],
    )

    graph_builder.add_edge("tool_node", "llm_call")

    return graph_builder.compile()


# ============================================================
# 8. SIDEBAR
# ============================================================

with st.sidebar:

    st.title("⚙️ Settings")

    st.markdown("### 🔑 Groq API Configuration")

    api_key = st.text_input(
        "Enter your Groq API Key",
        type="password",
        help="Get your API key from the Groq Console.",
    )

    model_name = st.selectbox(
        "Select Groq Model",
        options=[
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b",
        ],
        index=0,
    )

    st.divider()

    st.markdown("### 🛠️ Available Tools")

    st.markdown("""
    - ➕ **Add** — Addition
    - ✖️ **Multiply** — Multiplication
    - ➗ **Divide** — Division
    """)

    st.divider()

    st.markdown("### 📚 Project Information")

    st.markdown("""
    **Technologies**
    - Python
    - Streamlit
    - Groq API
    - LangChain
    - LangGraph

    **Concepts**
    - Tool calling
    - Agent state
    - Conditional routing
    - Graph execution
    """)

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.llm_calls = 0
        st.rerun()


# ============================================================
# 9. WELCOME SECTION
# ============================================================

st.markdown("### 👋 Welcome!")

st.write(
    "Ask me to calculate numbers using natural language. "
    "I can perform addition, multiplication, division, "
    "and multi-step calculations."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <h4>➕ Addition</h4>
        Add two or more numbers.
        <br><br>
        Example: Add 25 and 75.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4>✖️ Multiplication</h4>
        Multiply numbers.
        <br><br>
        Example: Multiply 12 by 8.
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <h4>🔄 Multi-step</h4>
        Perform calculations in sequence.
        <br><br>
        Example: Add 5 and 10, then multiply by 2.
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 10. DISPLAY CHAT HISTORY
# ============================================================

st.markdown("### 💬 Chat with your AI Assistant")

for message in st.session_state.messages:

    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)

    elif isinstance(message, AIMessage):
        if message.content:
            with st.chat_message("assistant"):
                st.markdown(message.content)


# ============================================================
# 11. CHAT INPUT
# ============================================================

user_query = st.chat_input(
    "Enter your calculation... e.g. Add 10 and 20"
)


# ============================================================
# 12. PROCESS USER QUERY
# ============================================================

if user_query:

    if not api_key:
        st.warning(
            "🔑 Please enter your Groq API key in the sidebar."
        )
        st.stop()

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)

    # Add user message to conversation
    st.session_state.messages.append(
        HumanMessage(content=user_query)
    )

    try:
        with st.chat_message("assistant"):

            with st.spinner("🤖 AI is calculating..."):

                agent = build_agent(api_key, model_name)

                result = agent.invoke(
                    {
                        "messages": st.session_state.messages,
                        "llm_calls": 0,
                    },
                    config={"recursion_limit": 30},
                )

                final_message = result["messages"][-1]

                # Save full graph conversation
                st.session_state.messages = result["messages"]

                st.session_state.llm_calls += result["llm_calls"]

                if final_message.content:
                    st.markdown(final_message.content)
                else:
                    st.info("The assistant returned no text response.")

        st.rerun()

    except Exception as error:
        st.error(f"❌ Error: {error}")

        st.info(
            "Check your Groq API key, model access, "
            "internet connection, and API limits."
        )


# ============================================================
# 13. FOOTER
# ============================================================

st.divider()

st.markdown(
    "<center>🧠 Powered by Groq + LangChain + LangGraph</center>",
    unsafe_allow_html=True,
)

st.caption(
    "Agentic AI Arithmetic Assistant | Learning Project"
)

