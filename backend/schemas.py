from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    category: str
    cover_image_url: str | None = None
    file_path: str

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True

class ConversionResponse(BaseModel):
    download_url: str

class RagUploadResponse(BaseModel):
    book_id: str
    message: str

class RagQuery(BaseModel):
    query: str
    book_id: str

class RagQueryResponse(BaseModel):
    response: str