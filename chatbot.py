from langchain.embeddings import OpenAIEmbeddings   
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain.retrievers import WikipediaRetriever

import pinecone
import time

from config import OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME, EMBEDDING_MODEL



# Helper functions
def print_source(result):
    sources = result["source_documents"]
    for i in range(min(3, len(sources))):
        print("="*60)
        print(f"Source [{i+1}] \t File: [{sources[i].metadata['source']}] \t Page: [{int(sources[i].metadata['page'])}]")
        print("="*60)
        print(sources[i].page_content)
        print("="*60)
        print()



def print_wiki_source(result):
    sources = result["source_documents"]
    for i in range(min(3, len(sources))):
        print("="*60)
        print(f"Source [{i+1}] \t Title: [{sources[i].metadata['title']}]")
        print(f"URL: [{sources[i].metadata['source']}]")
        print("="*60)
        print(sources[i].page_content)
        print("="*60)
        print()



def print_answer(result):
    print("="*30)
    print(" "*10 + "Question")
    print("="*30)
    print(result["question"])
    print("="*30)
    print()

    print("="*30)
    print(" "*10 + "Answer")
    print("="*30)
    print(result["answer"])
    print("="*30)
    print()
    


def if_existed(query, vectorstore):
    is_existed = True
    try:
        res = vectorstore.max_marginal_relevance_search(
            query=query,
            k=4,
            fetch_k=20,
            lambda_mult=0.5
        )
    except:
        is_existed = False
    
    return is_existed



def search(query, vector_chain, vectorstore, wiki_chain):
    if if_existed(query, vectorstore):
        res = vector_chain({"question": query})
        print_answer(res)
        print_source(res)
    else:
        print("Let me grab Wikipedia to answer your question......")
        res = wiki_chain({"question": query})
        print_answer(res)
        print_wiki_source(res)

    

# Initialize OpenAI
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

embedding_model = OpenAIEmbeddings(
    openai_api_key=OPENAI_API_KEY, 
    model=EMBEDDING_MODEL
)

print("="*30)
print("OpenAI initialization: OK")
print("="*30)
print()



# Initialize Pinecone vector storage
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENVIRONMENT
)

if PINECONE_INDEX_NAME not in pinecone.list_indexes():
    # we create a new index if it doesn't exist
    pinecone.create_index(
        name=PINECONE_INDEX_NAME,
        metric='cosine',
        dimension=1536  # 1536 dim of text-embedding-ada-002
    )
    # wait for index to be initialized
    time.sleep(1)

pinecone_index = pinecone.Index(PINECONE_INDEX_NAME)
pinecone_stats = pinecone_index.describe_index_stats()
print("="*30)
print("Pinecone initialization: OK")
print(pinecone_stats)
print("="*30)
print()


# Retriever
vectorstore = Pinecone(pinecone_index, embedding_model, "text")
retriever = vectorstore.as_retriever(
    search_type="mmr", 
    search_kwargs={
                    "k": 5,
                    "lambda_mult": 0.5, # the optimal mix of diversity and accuracy in the result set
                    }
)

wiki_retriever = WikipediaRetriever()

print("="*30)
print("Pinecone retriever: OK")
print("="*30)
print()



# Chat memory
memory = ConversationSummaryMemory(
    llm=llm, 
    memory_key="chat_history", 
    input_key='question', 
    output_key='answer', 
    return_messages=True
)
print("="*30)
print("Chat memory: OK")
print("="*30)
print()


# Conversational Retrieval Chain
conversation_qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    memory=memory,
    return_source_documents=True, 
    verbose=False
)

wiki_qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=wiki_retriever,
    memory=memory,
    return_source_documents=True,
    verbose=False
)

print("="*30)
print("Conversational Retrieval Chain: OK")
print("="*30)
print()

query = ""
while query != "quit":
    query = input("You: ")
    if query == "clear":
        memory.clear()
    elif query != "quit":
        search(query, conversation_qa_chain, vectorstore, wiki_qa_chain)

print("Chat bot exited.")


