# CV-AI-Agent
This is a simple artificial intelligence system that scans my resume to provide answers regarding my experience and qualifications. My resume is loaded, divided into sections, and stored in a searchable database using Python and LangChain. 

Code Walkthrough: The Assistant's Operation
A detailed description of the main.py's fundamental logic, which describes how the RAG architecture takes in, stores, and retrieves data in order to respond to queries, can be found below.

1. Initialization and Setup
Justification: To start, the script imports all required modules from the LangChain ecosystem. Here, the load_dotenv() function is essential because it safely loads the OPENAI_API_KEY from the hidden.env file into the system environment, allowing the code to interact with OpenAI without requiring sensitive credentials to be hardcoded.

<img width="647" height="219" alt="image" src="https://github.com/user-attachments/assets/f9f600cd-29a4-48cd-bca2-aa81024d61e7" />


3. The Brain, or LLM
Justification: This sets up the application's core intelligence. We employ the gpt-4o model from OpenAI. For a CV assistant, setting the temperature to 0.2 is a conscious decision because it reduces the model's creativity and guarantees that it will only provide accurate, factual responses based on the resume data, not on hallucinations.

<img width="522" height="95" alt="image" src="https://github.com/user-attachments/assets/fb88d818-f3fa-4ca0-ae1d-a4602de539a1" />


5. Text splitting and document loading (The Shredder)
Justification: The RecursiveCharacterTextSplitter loads the plaintext PDF and then divides it into smaller, easier-to-manage chunks.
- chunk_size = 1000: A maximum of 1000 characters are contained in each piece.
- chunk_overlap = 200: There is a 200 character overlap between the chunks. By doing this, the contextual meaning of the text is preserved and ideas or sentences that are cut off at the end of one chunk are carried over to the next.
- 
<img width="664" height="266" alt="image" src="https://github.com/user-attachments/assets/4b72e146-a7ca-45a7-846b-bd8b2699d824" />


4. Vector storage and embeddings (the filing cabinet)
The explanation is that language models read numbers rather than words. The text fragments are transformed into numerical vectors by the OpenAIEmbeddings function. A local ChromaDB database is then used to store these vectors (persist_directory = "chroma_db"). This eliminates the need for you to reprocess the PDF each time the script is executed by enabling the system to store the data locally.

<img width="659" height="215" alt="image" src="https://github.com/user-attachments/assets/57b5a750-773f-4bca-961a-edde0881454d" />


6. The Prompt & Retriever (The Librarian)
Explanation: The retriever looks for the k=2 most mathematically similar text chunks in the Chroma database when a user asks a question.
The stringent "rules of engagement" are the PromptTemplate. It explicitly instructs the AI to use the supplied paragraphs and not to invent anything by dynamically injecting the user's {question} and the {retrieved_chunks} into a system prompt.

<img width="856" height="492" alt="image" src="https://github.com/user-attachments/assets/c275b4fa-7e12-4a6d-8132-76f5546622a8" />

8. The Chain & Interactive Loop
Explanation: * The Chain: Using LangChain Expression Language (LCEL), the rag_chain pipes the retrieved documents, formats them into a readable string, passes them into the prompt template, and finally feeds them to the LLM.
The Loop: A while True loop is implemented to keep the terminal application running seamlessly. It captures user input, invokes the RAG chain, and prints the AI's response until the user types exit or quit.
<img width="830" height="472" alt="image" src="https://github.com/user-attachments/assets/dad2cd50-f6cb-462a-850b-f9c89ec90042" />
