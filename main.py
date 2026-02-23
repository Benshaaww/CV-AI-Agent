import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

#Step 1: The LLM (The Brain)

llm = ChatOpenAI(model = "gpt-4o", temperature = 0.2)

#Step 2: Text Splitting (The Shredder)

loader = PyPDFLoader("Benjamin Robert Shaw(plaintext).pdf")

data = loader.load()

#Step 2: Text Splitting (The Shredder)

rc_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200,
    separators = ["\n\n", "\n", " ", ""]
)

docs = rc_splitter.split_documents(data)

#Step 3: Embeddings & Vector Storage (The Filing Cabinet)

embedding_function = OpenAIEmbeddings(model = "text-embedding-3-small")

vectorstore = Chroma.from_documents(
    docs,
    embedding = embedding_function,
    persist_directory = "chroma_db"
)

#Step 4: The Retriever (The Librarian)

retreiver = vectorstore.as_retriever(
    search_type = "similarity",
    search_kwargs = {"k": 2}
)

#Step 5: The Prompt Template (The Rules of Engagement)

prompt_template = PromptTemplate(
    input_variables = ["question", "retrieved_chunks"],
    template = """
    You are an AI assistant. A user is going to ask you a question. I am going to give you 
    a few specific paragraphs from a resume. Answer the user's question using ONLY those paragraphs. 
    Do not make anything up.
    
    Here is the user's question: {question}
    
    Here are the retrieved chunks from the resume:
    {retrieved_chunks}
    
    Now, answer the user's question based on the information above.
    """
)

#Step 6: The Chain (Tying it all together)
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = ({"retrieved_chunks": retreiver | format_docs, "question": RunnablePassthrough()} 
| prompt_template 
| llm
)

print("-----CV AI Assistant Loaded------")
print("type 'exit' or type 'quit' to end the application.\n")

while True:
    userQuestion = input("Ask a question about Bejamin's CV: ")

    if userQuestion.lower() in ["exit", "quit"]:
        break

    if not userQuestion.strip():
        continue

    response = rag_chain.invoke(userQuestion)
    
    print(response.content + "\n")

