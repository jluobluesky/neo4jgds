
from datetime import datetime
crnttime=datetime.now()
timestr=crnttime.strftime("%m/%d/%Y, %H:%M:%S-%z")

import apps.libs.pylibGFuns as pylibGFuns
import apps.libs.pylibGFuns as pylibGFuns


# Print the time
# print(pylibGFuns.get_timestamp())

# code for KG system: neo4j
# 1) csv vector
# 2) KG vector
# 3) KG graph

# You can keep a free instance in Neo4j AuraDB Free indefinitely, 
# but it will automatically pause after three days of inactivity.

# 1) csv vector


# 2) KG vector
# assume that the KG is ready in neo4j

import dotenv
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

REVIEWS_CSV_PATH = "test/data/reviews.csv"
REVIEWS_CHROMA_PATH = "test/data/chroma_data"

dotenv.load_dotenv()

# use local neo4j

import os
os.environ["NEO4J_URI"] = 'neo4j://localhost:7687'
os.environ["NEO4J_USERNAME"] = 'neo4j'
os.environ["NEO4J_PASSWORD"] = 'neo4jmm1234'


# Print all environment variables
for key, value in os.environ.items():
    if key.endswith("PATH"):
        print(f"{key}: {value}")

# load the csv data into neo4j
from test.hospital_neo4j_etl.src.hospital_bulk_csv_write import (
    load_hospital_graph_from_csv,
    
)

load_hospital_graph_from_csv()

# run the chatbot
from test.chatbot_api.src.main import app

app.run(host='0.0.0.0', debug=True, port=8000)

# Create a Neo4j Vector Chain
# chatbot_api/src/chains/hospital_review_chain.py

# test the chain

from test.chatbot_api.src.chains.hospital_review_chain import reviews_vector_chain
# Lines 15 to 29 create the vector index in Neo4j. 
# neo4j_vector_index = Neo4jVector.from_existing_graph(

query = """What have patients said about hospital efficiency?
         Mention details from specific reviews."""

response = reviews_vector_chain.invoke(query)

print(response.get("result"))


# 3) KG graph cyper chain
from test.chatbot_api.src.chains.hospital_cypher_chain import (
    hospital_cypher_chain,graph
)

question = """What is the average visit duration for
emergency visits in North Carolina?"""
response = hospital_cypher_chain.invoke(question)
print(response.get("result"))

print(graph.get_schema)

# 4) chatbot agent
# chatbot_api/src/agents/hospital_rag_agent.py
from test.chatbot_api.src.agents.hospital_rag_agent import (
    hospital_rag_agent_executor,
)

response = hospital_rag_agent_executor.invoke(
    {"input": "What is the wait time at Wallace-Hamilton?"}
)
print(response.get("output"))

response = hospital_rag_agent_executor.invoke(
    {"input": "Which hospital has the shortest wait time?"}
)
print(response.get("output"))



# test local server: --------------

from neo4j import GraphDatabase

# Replace with your Neo4j connection details
# uri = "bolt://localhost:7687"
uri = "neo4j://localhost:7687"
username = "neo4j"
password = "neo4jmm1234"

driver = GraphDatabase.driver(uri, auth=(username, password))

def close():
    driver.close()

def run_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return result.data()

# Example usage
query = "CREATE (n:Greeting {message: $message}) RETURN n.message"
parameters = {"message": "Hello, Neo4j!"}
results = run_query(query, parameters)
print(results)

close()
