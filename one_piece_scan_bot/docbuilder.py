from one_piece_scan_bot.pages_downloader import Mangapage

class Document:
    def __init__(self, source_url: str = None, document_type: str = 'pdf'):
        self.name = None
        self.source_url = None
        self.type = None
        self.supported_types = {
            'pdf',
            'epub',
        }
        self.images = None
        self.set_url(source_url)
        self.set_type(document_type)
    
    def set_url(self, url: str) -> None:
        if url is None or not Mangapage.is_valid_url(url):
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
            page = Mangapage(self.source_url)
            self.images = page.fetch_images("temp_images")

            print(f"Generating {self.type} document from {self.source_url}...")
            if self.type == 'pdf':
                self._generate_pdf()
            elif self.type == 'epub':
                self._generate_epub()
        else:
            print(f"Unsupported type for the {self.__class__.__name__} class, no documents will be generated")

    def _is_supported_type(self, type: str) -> bool:
        return type in self.supported_types
    
    def _generate_pdf(self):
        # TODO merge self.images into a single PDF file
        print(f"Generated PDF file!")
        # TODO delete the temporary folder with the images
        pass

    def _generate_epub(self):
        # TODO merge self.images into a single EPUB file - please consider that mloader can download directly in CBZ format!
        print(f"Generated EPUB file!")
        # TODO delete the temporary folder with the images
        pass
