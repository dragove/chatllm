from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain

embeddings = HuggingFaceEmbeddings(
    model_name="infgrad/stella-base-zh",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)

loader = PyPDFLoader("./hdfs.pdf")
pages = loader.load_and_split()

db = Chroma.from_documents(pages, embedding=embeddings,
                                 persist_directory="./dbcache")

db.persist()

llm = ChatOpenAI(openai_api_base="http://localhost:8000/v1", openai_api_key="none")
pdf_qa = ConversationalRetrievalChain.from_llm(llm,
                                retriever=db.as_retriever(search_kwargs={"k": 1}))

history = [] 
while True:
    query = input("Q: ")
    result = pdf_qa({"question": query, "chat_history": history})
    print(f'A: {result["answer"]}')
    history.append((query, result["answer"]))


