from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

import os
os.environ["HF_DISABLE_MODEL_DOWNLOAD"] = "1"

print("loading embeddings model")
embeddings = HuggingFaceEmbeddings(
    model_name="infgrad/stella-base-zh",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)
print("loaoding embeddings model successfully")

print("load pdf file: \"the-fenix-project.pdf\"")
loader = PyPDFLoader("./the-fenix-project.pdf")
pages = loader.load_and_split()[60:100]

db = Chroma.from_documents(pages, embedding=embeddings)

print("load pdf file successfully and saved to chroma")

prompt_template = """使用以下上下文回答最下面的问题。如果你不知道答案，直接回复我不知道，不要编造回答

{context}

问题: {question}
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

chain_type_kwargs = {"prompt": PROMPT}

llm = ChatOpenAI(openai_api_base="http://localhost:8000/v1", openai_api_key="none")
pdf_qa = RetrievalQA.from_chain_type(llm, chain_type="stuff",
                              retriever=db.as_retriever(search_kwargs={"k": 1}),
                              chain_type_kwargs=chain_type_kwargs)

history = [] 
while True:
    query = input("Q: ")
    # result = pdf_qa({"question": query, "chat_history": history})
    result = pdf_qa(query)
    # print(f'A: {result["answer"]}')
    print(f'A: {result}')
    # history.append((query, result["answer"]))


