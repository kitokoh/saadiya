import pandas as pd

class DmsModel:
    def __init__(self):
        self.documents = pd.DataFrame(columns=['Title', 'Type', 'Path'])
        self._load_initial_data()

    def _load_initial_data(self):
        # Initial data for demonstration
        data = [
            {'Title': 'Quote 1', 'Type': 'Quote', 'Path': '/path/to/quote1.pdf'},
            {'Title': 'Contract A', 'Type': 'Contract', 'Path': '/path/to/contract_a.pdf'}
        ]
        self.documents = pd.DataFrame(data)

    def get_documents(self):
        return self.documents

    def add_document(self, title, type, path):
        new_document = pd.DataFrame([{'Title': title, 'Type': type, 'Path': path}])
        self.documents = pd.concat([self.documents, new_document], ignore_index=True)

    def update_document(self, index, title, type, path):
        if 0 <= index < len(self.documents):
            self.documents.loc[index] = [title, type, path]

    def delete_document(self, index):
        if 0 <= index < len(self.documents):
            self.documents = self.documents.drop(index).reset_index(drop=True)
