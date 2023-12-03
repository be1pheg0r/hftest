from llama_index import SimpleDirectoryReader
import docx2txt
import aspose.words as aw
import os


class file_reader:

    def __init__(self):
        self.get_path = "inp data"
        self.take_path = "data"
        self.read_data = None

    def txt_import(self):
        count = False
        for file in os.listdir(self.get_path):
            if os.path.isfile(os.path.join(self.get_path, file)) and file.endswith('.txt'):
                source_file = os.path.join(self.get_path, file)
                next_file = os.path.join(self.take_path, file)
                os.rename(source_file, next_file)
                count = True
        if count:
            print('импорт .txt завершен')

    def files_with_extension(self):
        for file in os.listdir(self.get_path):
            if os.path.isfile(os.path.join(self.get_path, file)):
                if file.endswith('.docx') or file.endswith('.pdf'):
                    return True
        return False

    def return_docs(self):
        if self.files_with_extension():
            self.word_2_txt()
            self.pdf_2_txt()
        self.read_data = SimpleDirectoryReader('data').load_data()
        return self.read_data

    def pdf_2_txt(self):
        files = os.listdir(self.get_path)
        for file in files:
            try:
                pdf_path = os.path.abspath(os.path.join(self.get_path, file))
                pdf = aw.Document(pdf_path)
                txt_name = file[:-3] + "txt"
                txt = os.path.abspath(os.path.join(self.take_path, txt_name))
                pdf.save(txt)
                os.remove(pdf_path)
                print(f'Конвертация {file} завершена')
            except:
                pass
        print('Конвертация pdf завершена')

    def word_2_txt(self):
        for root, dirs, files in os.walk(self.get_path):
            for file in files:
                if file.endswith('.docx'):

                    docx_file_path = os.path.join(root, file)

                    text_file_path = os.path.join(self.take_path, os.path.splitext(file)[0] + '.txt')
                    if not os.path.exists(text_file_path):
                        try:
                            text = docx2txt.process(docx_file_path)
                            with open(text_file_path, 'w', encoding='utf-8') as text_file:
                                text_file.write(text)
                            os.remove(docx_file_path)
                            print(f'{file} преобразован успешно')
                        except Exception as e:
                            print(f'ошибка, {file} - {e}')
                    else:
                        print(f'{file} уже отформатирован')
        print('конвертация .docx завершена')
