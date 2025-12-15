# Auto-generated fallback module from deepseek.ipynb
# --- Begin concatenated code cells ---

# --- Cell 1 ---
import re
from dotenv import load_dotenv

from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

from evaluate import load as load_metric
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# --- Cell 2 ---
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# MODEL = "gpt-3.5-turbo"
# MODEL = "mixtral:8x7b"
MODEL = "deepseek-r1:1.5b"

# --- Cell 3 ---
from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings
import re
model = OllamaLLM(model = MODEL)
embeddings = OllamaEmbeddings(model=MODEL)

model.invoke("tell me a joke")

def clean_output(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
 

# --- Cell 4 ---
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

chain = model | parser
chain.invoke("tell me a joke")

# --- Cell 5 ---
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("example.pdf")
pages = loader.load_and_split()
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
docs = splitter.split_documents(pages)

vectorstore = DocArrayInMemorySearch.from_documents(docs, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# --- Cell 6 ---
from langchain.prompts import PromptTemplate

template = """
Answer the question based on the Context below, If you can't 
answer the question, reply "I don't know"
Answer directly without showing your reasoning. Do not use <think> tags only show the Answer.
and if the Question was summarize the document so You are an expert teaching assistant. Summarize the document in a clear, structured way. 
Be concise but comprehensive and summarize it in 2-3 lines and please cover all the points explained in the document. 
Context: {context}

Question: {question}

"""
prompt = PromptTemplate.from_template(template)
print(prompt.format(context = "Context" , question = "This is a question"))

# --- Cell 7 ---
chain = prompt | model | parser

# --- Cell 8 ---
chain.invoke({
    "context":"my name is Ali",
    "question" : "What is my name"
    
})

# --- Cell 9 ---
retriever = vectorstore.as_retriever()
retriever.invoke("Adressing")

# --- Cell 10 ---
from operator import itemgetter

chain = (
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question"),
    }
    | prompt
    | model
    | parser
)
query = itemgetter("question")
response = chain.invoke({"question":"Summarize the whole document please"})
print(response)


# --- Cell 11 ---
import re
from evaluate import load

# install first: pip install bert_score
bertscore = load("bertscore")

reference = """Ben Iglesias, on his fifth return flight from Mars, experiences a mysterious accident.
When he awakens, his crew is dead and Earth is unrecognizable - a white desert with reduced oxygen.
He encounters a group of small, thin humans living in caves. 
Over three years, he adapts to this new world, marries one of them, and his wife becomes pregnant.
The story leaves unanswered whether he traveled through time or to an alternate Earth"""

# Remove <think> ... </think>
cleaned_response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

scores = bertscore.compute(predictions=[cleaned_response],
                           references=[reference],
                           lang="en")

best_score = scores["f1"][0] * 100
print(cleaned_response)
print(f"Best semantic similarity percentage: {best_score:.2f}%")


# --- Cell 12 ---
import re
from evaluate import load

bertscore = load("bertscore")

reference = """Ben Iglesias, on his fifth return flight from Mars, experiences a mysterious accident.
When he awakens, his crew is dead and Earth is unrecognizable - a white desert with reduced oxygen.
He encounters a group of small, thin humans living in caves. 
Over three years, he adapts to this new world, marries one of them, and his wife becomes pregnant.
The story leaves unanswered whether he traveled through time or to an alternate Earth"""

cleaned_response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

scores = bertscore.compute(predictions=[cleaned_response],
                           references=[reference],
                           lang="en")

best_score = scores["f1"][0] * 100

print(cleaned_response)
print(f"Best semantic similarity percentage: {best_score:.2f}%")


# --- Cell 13 ---
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load a pre-trained sentence embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # lightweight and fast

reference = """Ben Iglesias, on his fifth return flight from Mars, experiences a mysterious accident.
When he awakens, his crew is dead and Earth is unrecognizable - a white desert with reduced oxygen.
He encounters a group of small, thin humans living in caves. 
Over three years, he adapts to this new world, marries one of them, and his wife becomes pregnant.
The story leaves unanswered whether he traveled through time or to an alternate Earth"""

cleaned_response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

ref_embedding = embedding_model.encode([reference])
resp_embedding = embedding_model.encode([cleaned_response])

similarity = cosine_similarity(resp_embedding, ref_embedding)[0][0] * 100

print(cleaned_response)
print(f"Best semantic similarity percentage (cosine): {similarity:.2f}%")


# --- Cell 14 ---
def get_full_context(docs):
    return " ".join([doc.page_content for doc in docs])

full_context = get_full_context(docs)
print(full_context[:500])  



# --- Cell 15 ---

qg_template = """
You are an expert teaching assistant.

Based on the following context, generate:
- 5 multiple-choice questions (MCQs) with 4 options each (A, B, C, D) and specify the correct answer clearly.
- 5 essay or open-ended questions that test understanding, analysis, or explanation.

Make sure all questions are clear, relevant, and cover the most important facts, concepts, and ideas in the context.
Avoid repeating questions and ensure variety.

Format your answer exactly like this:

MCQs:
1. [Question text]
   A) ...
   B) ...
   C) ...
   D) ...
   (Answer: ...)

Essay Questions:
1. [Essay question text]
2. ...
3. ...
4. ...
5. ...

Context:
{context}
"""

qg_prompt = PromptTemplate.from_template(qg_template)


# --- Cell 16 ---
qg_chain = (qg_prompt | model | parser)

# --- Cell 17 ---
generated_questions = qg_chain.invoke({"context": full_context})


# --- Cell 18 ---
print("===== Generated Questions =====\n")
print(generated_questions)


# --- Cell 19 ---
#pip install streamlit

# --- Cell 20 ---
import streamlit as st
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import tempfile
import os

# ------------------- Streamlit UI Setup -------------------
st.set_page_config(page_title="Doc Mind – Your Study Partner")
st.title("📘 Doc Mind – Your Study Partner")

# ------------------- Load Model & Embeddings -------------------
@st.cache_resource
def get_llm():
    return OllamaLLM(model="deepseek-r1:1.5b")

@st.cache_resource
def get_embeddings():
    return OllamaEmbeddings(model="deepseek-r1:1.5b")

llm = get_llm()
embeddings = get_embeddings()

# ------------------- PDF Handling -------------------
def process_pdf(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(pdf_file.read())
        temp_path = temp_file.name

    loader = PyPDFLoader(temp_path)
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    docs = text_splitter.split_documents(pages)

    # Create FAISS vector store for local semantic search
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    return retriever, docs

# ------------------- Summarization -------------------
def summarize_content(retriever):
    summary_template = """
    You are an expert teaching assistant.
    Based on the following context, summarize it in simple, clear English.

    Context:
    {context}
    """
    prompt = PromptTemplate(template=summary_template, input_variables=["context"])
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=False,
    )
    return qa_chain.run("Summarize the document")

# ------------------- Question Generation -------------------
def generate_questions(retriever):
    question_template = """
    You are an expert educator.
    Using the following context, create:
    - 5 Multiple Choice Questions (MCQs) with 4 options each and correct answers.
    - 5 open-ended or essay questions.

    Context:
    {context}
    """
    prompt = PromptTemplate(template=question_template, input_variables=["context"])
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=False,
    )
    return qa_chain.run("Generate questions")

# ------------------- UI Workflow -------------------
uploaded_file = st.file_uploader("📄 Upload your PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Processing document..."):
        retriever, docs = process_pdf(uploaded_file)

    if st.button("🧠 Summarize Document"):
        with st.spinner("Generating summary..."):
            summary = summarize_content(retriever)
            st.subheader("📘 Summary:")
            st.write(summary)

    if st.button("❓ Generate Questions"):
        with st.spinner("Generating questions..."):
            questions = generate_questions(retriever)
            st.subheader("📝 Questions:")
            st.write(questions)
else:
    st.info("👆 Upload a PDF file to get started.")


# --- Cell 21 ---

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Memory list
chat_history = []

# Prompt template that considers previous chat
chat_template = """
You are an expert teaching assistant AI.
Answer questions based on the document context below.
Be concise, clear, and polite.
If the answer is not in the document, reply "I don't know".

Previous conversation:
{chat_history}

Context:
{context}

Question:
{question}

Answer:
"""

chat_prompt = PromptTemplate(
    template=chat_template,
    input_variables=["chat_history", "context", "question"]
)

# --- Cell 22 ---

# Build a RetrievalQA chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=model,
    retriever=retriever,
    combine_docs_chain_kwargs={"prompt": chat_prompt}
)

# Interactive loop
print("Chatbot is ready! Type 'exit' to quit.")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting chatbot. Goodbye!")
        break

    # Combine previous chat history
    history_text = "\n".join([f"You: {q}\nAI: {a}" for q, a in chat_history])

    # Run the QA chain
    response = qa_chain({
    "question": user_input,
    "chat_history": chat_history
    })

#    Save only the text answer (not the full dict)
    chat_history.append((user_input, response["answer"]))

    print(f"AI: {response}")

# --- Cell 23 ---
#pip install groq langchain langchain_groq

# --- Cell 24 ---
from langchain_groq import ChatGroq
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate

# 1. Build vectorstore
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

pages = loader.load_and_split()
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
docs = splitter.split_documents(pages)

vectorstore = DocArrayInMemorySearch.from_documents(docs, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 2. Groq LLM
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)

# 3. Prompt
prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant.

Conversation History:
{history}

Relevant context from documents:
{context}

User question:
{question}

If the answer is not found in context, respond: "I don't know from the documents."
""")

# --- Cell 25 ---
# 4. Build RAG chain 
rag_chain = (
    {
        "context": lambda x: retriever.invoke(x["question"]),  
        "history": lambda x: x["history"],
        "question": lambda x: x["question"]
    }
    | prompt
    | llm
    | StrOutputParser()
)

# 5. Chat loop
history = ""

print("Chatbot ready! Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    answer = rag_chain.invoke({
        "question": user_input,
        "history": history
    })

    print("AI:", answer)

    history += f"\nUser: {user_input}\nAI: {answer}\n"

# --- Cell 26 ---



# --- End concatenated code cells ---


# Helpful runner: try to call common entrypoints if present
if __name__ == '__main__':
    if 'main' in globals():
        try:
            main()
        except Exception as e:
            print('Error running main():', e)
    else:
        print('No main() function found in notebook code. Inspect this file for functions to call.')
