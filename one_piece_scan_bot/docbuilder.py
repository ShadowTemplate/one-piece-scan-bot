import re

class Document:
    def __init__(self, source_url: str = None, document_type: str = 'pdf'):
        self.name = None
        self.source_url = None
        self.type = None
        self.supported_types = {
            'pdf',
            'epub',
        }
        self.set_url(source_url)
        self.set_type(document_type)
    
    def set_url(self, url: str) -> None:
        if url is None or not self._is_valid_url(url):
            print("Invalid URL!")
            return
        self.source_url = url

    def set_type(self, document_type: str) -> None:
        if self._is_supported_type(document_type):
            self.type = document_type
        else:
            print(f"Type {document_type} not supported for the {self.__class__.__name__} class!")

    def get_name(self):
        return self.name
    
    def get_supported_types(self):
        return self.supported_types

    def build_from_url(self):
        if self._is_supported_type(self.type):
            print(f"Generating {self.type} document from {self.source_url}...")
            if self.type == 'pdf':
                pass
            elif self.type == 'epub':
                pass
        else:
            print(f"Unsupported type for the {self.__class__.__name__} class, no documents will be generated")

    @ staticmethod
    def _is_valid_url(self, url: str) -> bool:
        # django url validation regex - https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45
        regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None

    def _is_supported_type(self, type: str) -> bool:
        return type in self.supported_types
    
    def _generate_pdf(self):
        # TODO implement
        print(f"Generated PDF file!")
        pass

    def _generate_epub(self):
        # TODO implement
        print(f"Generated EPUB file!")
        pass
