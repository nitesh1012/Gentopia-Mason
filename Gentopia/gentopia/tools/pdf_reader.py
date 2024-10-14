import os
import requests
from typing import Any, Optional, Type, AnyStr 
from PyPDF2 import PdfReader
from gentopia.tools.basetool import BaseTool, BaseModel, Field

class PDFReadArgs(BaseModel):
    pdf_source: str = Field(..., description="Path or URL of the PDF to be processed.")

class PDFDocumentReader(BaseTool):
    

    name = "pdf_document_reader"
    description = "Extracts and summarizes PDF content. Input is a local path or an online URL."

    args_schema: Optional[Type[BaseModel]] = PDFReadArgs

    def _run(self, pdf_source: AnyStr) -> str:
        if self._is_url(pdf_source):
            pdf_source = self._fetch_pdf_from_url(pdf_source)
        return self._extract_text_from_pdf(pdf_source)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Asynchronous reading not implemented.")

    def _extract_text_from_pdf(self, file_location: str) -> str:
        try:
            with open(file_location, 'rb') as pdf_handle:
                reader = PdfReader(pdf_handle)
                all_text = "".join(page.extract_text() for page in reader.pages)
                summary_text = all_text[:1000] + "..." if len(all_text) > 1000 else all_text
                return summary_text
        except FileNotFoundError:
            return "Error: PDF file not found."
        except Exception as error:
            return f"Error reading the PDF: {str(error)}"

    def _fetch_pdf_from_url(self, url: str) -> str:
        try:
            file_name = url.split('/')[-1]
            pdf_data = requests.get(url).content
            with open(file_name, 'wb') as local_pdf:
                local_pdf.write(pdf_data)
            return file_name
        except Exception as error:
            return f"Error downloading the PDF: {str(error)}"

    def _is_url(self, source: str) -> bool:
        return source.startswith("http")



if __name__ == "__main__":
    # For a local file:
    result = PDFDocumentReader()._run("/path/to/local/file.pdf")
    print(result)

    # For a remote URL:
    result = PDFDocumentReader()._run("https://www.example.com/sample.pdf")
    print(result)
