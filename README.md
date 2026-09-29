Here is a GitHub-ready `README.md` for your Agentic AI Arithmetic Assistant project. Copy the content below into a file named `README.md` in your project folder.

🧮 Agentic AI Arithmetic Assistant

# 🧮 Agentic AI Arithmetic Assistant

An interactive **Agentic AI Arithmetic Assistant** built using **Streamlit, Groq, LangChain, and LangGraph**. The application understands natural-language arithmetic questions and uses AI-powered tool calling to perform calculations.

## 🚀 Project Overview

This project demonstrates how an AI agent can use external tools to solve arithmetic problems. The agent uses a LangGraph workflow to decide when to call a calculation tool, execute the requested operation, and return a clear response to the user.

The application provides a chat-based interface where users can enter calculations in plain English.

## ✨ Features

* 🧮 **Addition:** Add two numbers.

* ✖️ **Multiplication:** Multiply two numbers.

* ➗ **Division:** Divide two numbers with division-by-zero handling.

* 🔄 **Multi-step Calculations:** Perform sequential arithmetic operations.

* 💬 **Interactive Chat Interface:** Ask calculations in natural language.

* 🤖 **AI Tool Calling:** Uses Groq-powered language models to select arithmetic tools.

* 🔁 **LangGraph Workflow:** Uses nodes, state management, and conditional routing.

* ⚙️ **Model Selection:** Choose between supported Groq models.

* 🗑️ **Clear Chat:** Reset the conversation.

* 🎨 **Custom UI:** Styled Streamlit interface with a sidebar and example cards.

## 🛠️ Technologies Used

| Technology | Purpose                             |
| ---------- | ----------------------------------- |
| Python     | Core programming language           |
| Streamlit  | Web application interface           |
| Groq API   | Language model inference            |
| LangChain  | Tool creation and model integration |
| LangGraph  | Agent workflow and state management |
| TypedDict  | Agent state definition              |

## 🧠 Agent Workflow

The application follows this workflow:

1. User enters a calculation.

2. The LLM node receives the user's question.

3. The model decides whether to call an arithmetic tool.

4. The tool node executes the selected operation.

5. The result is returned to the model.

6. The agent generates the final response.

7. The Streamlit interface displays the answer.

   User Input
   ↓
   LLM Node
   ↓
   Conditional Routing
   ↓
   Tool Node
   ↓
   Execute Arithmetic Tool
   ↓
   Return Tool Result to LLM
   ↓
   Final Answer
   ↓
   Streamlit Chat Interface

## 📂 Project Structure

```
Agentic_AI_Arithmetic_Assistant/
│
├── app.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```
git clone https://github.com/YOUR_USERNAME/Agentic_AI_Arithmetic_Assistant.git
```

Navigate to the project folder:

```
cd Agentic_AI_Arithmetic_Assistant
```

### 2. Create a Virtual Environment (Optional)

```
python -m venv venv
```

Activate it on Windows:

```
venv\Scripts\activate
```

### 3. Install Dependencies

```
python -m pip install -r requirements.txt
```

### 4. Configure the Groq API Key

1. Visit the [Groq Console](https://console.groq.com/keys).

2. Create an API key.

3. Run the application and enter your API key in the sidebar.

**Important:** Keep your API key private. Do not upload it to GitHub.

### 5. Run the Application

```
python -m streamlit run app.py
```

The application will open in your browser, usually at:

```
http://localhost:8501
```

## 📦 Requirements

Create a `requirements.txt` file with the following libraries:

```
streamlit
langchain
langchain-core
langchain-groq
langgraph
typing_extensions
```

## 💡 Example Queries

Try the following calculations:

| User Query                                   | Expected Result              |
| -------------------------------------------- | ---------------------------- |
| Add 10 and 20.                               | 30                           |
| Multiply 6 and 7.                            | 42                           |
| Divide 100 by 5.                             | 20                           |
| Divide 10 by 3.                              | Approximately 3.33           |
| Add 5 and 10, then multiply the result by 2. | 30                           |
| Divide 10 by 0.                              | Division-by-zero explanation |

## 📚 Concepts Learned

* Large Language Model (LLM) integration

* Tool calling with LangChain

* Custom Python arithmetic tools

* LangGraph state management

* Conditional edges and routing

* Graph compilation and invocation

* Multi-step tool execution

* Streamlit session state and chat interface

* API configuration and error handling

## 🔐 API Key Security

The application accepts the Groq API key through a password-type input in the sidebar.

* Never commit API keys to a public repository.

* Do not hardcode your API key in `app.py`.

* Use Streamlit secrets or environment variables for production deployment.

## 🔮 Future Improvements

* Add subtraction and exponentiation tools.

* Add calculation history and export options.

* Display the agent's workflow visually.

* Add mathematical expression parsing.

* Deploy the application using Streamlit Community Cloud.

* Add unit tests for arithmetic tools.

## 👨‍💻 Author

**Yanaguntikar Meesal**

## 📄 License

This project is intended for educational and learning purposes. Add a suitable open-source license if you plan to distribute the project.

---

⭐ If you find this project useful, consider giving the repository a star on GitHub.
