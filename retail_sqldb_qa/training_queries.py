from langchain.embeddings import HuggingFaceEmbeddings
from chromadb.config import Settings
from langchain.vectorstores import Chroma # There are other Vector stores too like Chroma, Pinecone, Weaviate, Milvus

few_shots = [
    {'Question' : "How many t-shirts do we have left for Nike in XS size and white color?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
     'SQLResult': "Result of the SQL query",
     'Answer' : '37'},

    {'Question': "How much is the total price of the inventory for all Small size t-shirts?",
     'SQLQuery': "SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
     'SQLResult': "Result of the SQL query",
     'Answer': '16801'},

    {'Question': "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?" ,
     'SQLQuery' : """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
(select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi'
group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
 """,
     'SQLResult': "Result of the SQL query",
     'Answer': '25851.400000'},

     {'Question' : "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?",
      'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
      'SQLResult': "Result of the SQL query",
      'Answer' : '26413'},

    {'Question': "How many white color Levi's shirt I have?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
     'SQLResult': "Result of the SQL query",
     'Answer' : '276'
     }
]

# add a custom query along with the answer to the few shots list as shown above

# Load HuggingFaceEmbeddings model to creat our own embedding vector store
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')


to_vectorize = [" ".join(example.values()) for example in few_shots] # vectorizing the few shots

persist_directory = "./chroma_data"
settings = Settings(persist_directory=persist_directory)

# creating embeddings and updating the chroma_data
vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots, persist_directory=persist_directory)

# Save the Database
vectorstore.persist() # This will either create or update the exisiting Chroma Database