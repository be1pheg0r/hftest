from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from llama_index import (StorageContext, VectorStoreIndex,
                         load_index_from_storage, ServiceContext
                         )
import os
import file_reader
from time import sleep


class HF:
    '''
    рабочее тело чат-бота
    ИНСТРУКЦИЯ:
    при вызове класса (ЛЮБОМ) self.index - рабочие индексы, сбрасывается (техническая изюминка кода),
    это значит что процессинг должен происходить внутри ЭТОГО класса, иначе работать не будет
    как работать:
    1. создаешь экз класса, векторка строится по стоковым документам
    2. вызываешь build_vectors, если НОВЫЕ ДОКИ В "inp data"
    3. через query генеришь ответы
    4. связываешь тг и это через создание логов (пример в log.txt) или(и) придумай как связать через классы(это не сложно)
    interface - чисто тест, в работе не используется, на хостинге вызываться не будет
    '''

    def __init__(self):
        # api_key
        key_name = 'api key.txt'
        api_key = open(key_name).readline()
        os.environ['OPENAI_API_KEY'] = api_key
        self.save_path = "index data"  # all-MiniLM-L12-v2
        self.embed_model = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L12-v2")
        self.documents = file_reader.file_reader().return_docs()
        service_context = ServiceContext.from_defaults(embed_model=self.embed_model)
        self.index = VectorStoreIndex.from_documents(documents=
                                                     self.documents, service_context=service_context
                                                     )
        self.index.storage_context.persist(persist_dir=self.save_path)

    def build_vectors(self):  # построение и сохранение векторного пространства (только при наличии доков)
        self.documents = file_reader.file_reader().return_docs()
        service_context = ServiceContext.from_defaults(embed_model=self.embed_model)
        self.index = VectorStoreIndex.from_documents(documents=
                                                     self.documents, service_context=service_context
                                                     )
        self.index.storage_context.persist(persist_dir=self.save_path)

    def load_vectors(self):  # загрузка пространства (не работает)
        self.storage_context = StorageContext.from_defaults(persist_dir=self.save_path)
        self.index = load_index_from_storage(self.storage_context, embed_model=self.embed_model)

    def query(self, request):  # ответ
        query_eng = self.index.as_query_engine()
        response = query_eng.query('ответь на русском языке, ' + request)
        print(response)
        to_log = str(response)
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(f'{request} - {to_log}\n')

    def interface(self):
        flag = False
        while not flag:
            print('-' * 18)
            print('интерфейс работы с векторами')
            print('-' * 18)
            print('1 - построить пространство')
            print('2 - произвести тестовый запрос')
            print('3 - выход')
            print('-' * 18)
            request = input('введите необходимую операцию: ')
            print('-' * 18)
            if request == '1':
                self.build_vectors()
                print('-' * 18)
                sleep(2)
            if request == '2':
                req = input('введите запрос: ')
                print('-' * 18)
                try:
                    self.query(req)
                except Exception as e:
                    print(e)
                sleep(2)

            if request == '3':
                quit()


HF().interface()
