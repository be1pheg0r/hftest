from langchain.embeddings.huggingface import HuggingFaceInstructEmbeddings
from llama_index import (ServiceContext, VectorStoreIndex,
                         load_index_from_storage, StorageContext,
                         )
from InstructorEmbedding import INSTRUCTOR
import os
from hftest import HF
import file_reader
from time import sleep

path_to_key = r"C:\Users\User\Desktop\Учёба\опд\траю лламу"
key_name = 'api key.txt'
full_key_path = os.path.join(path_to_key, key_name)
api_key = open(full_key_path, 'r').readline()
os.environ['OPENAI_API_KEY'] = api_key

service_context = ServiceContext.from_defaults(embed_model='hkunlp/instructor-large')
storage_context = StorageContext.from_defaults(persist_dir=r'C:\Users\User\Desktop\Учёба\опд\траю лламу\index data')
index = load_index_from_storage(storage_context)
query_eng = index.as_query_engine()
response = query_eng.query('fdfd')
print(response)