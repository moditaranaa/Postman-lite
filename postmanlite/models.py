from typing import Optional, Dict, Any
from pydantic import BaseModel, HttpUrl

class APIRequestModel(BaseModel):
    """
    Base model for API requests.
    """
    url: HttpUrl # validated URL input like "https://api.example.com"
    method: str # GET, POST, PUT, DELETE, etc.
    headers: Optional[Dict[str, str]] = None # GET, POST, PUT, DELETE, etc.
    body: Optional[Any]= None  # Optional body - can be any JSON



class APIResponseModel(BaseModel):
    """
    Base model for API responses.
    """
    status_code: int # Status code of the response
    headers: Optional[Dict[str, str]] # All response headers
    body: Any # Response body (JSON or text)


