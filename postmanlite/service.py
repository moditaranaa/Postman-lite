import httpx
from typing import Dict, Any

async def make_api_request(
    url: str,
    method: str,
    headers: Dict[str, str] = None,
    body: Any = None
) -> Dict[str, Any]:
    """
    Makes an actual HTTP request using httpx and returns the response details.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=body
            )
            return {
                "status_code": response.status_code,
                "headers":dict(response.headers),
                "body": try_parse_response(response)
            }
        except httpx.RequestError as e:
            return {
                "status_code": 500,
                "headers": None,
                "body": f"Request failed: {str(e)}"
            }
        except Exception as e:
            return {
                "status_code": 500,
                "headers": None,
                "body": f"Unhandled exception: {str(e)}"
            }
        
def try_parse_response(response: httpx.Response) -> Any:
    """
    Try to return JSON response if possible, otherwise plain text.
    """
    try:
        # If content-type is JSON, parse as JSON
        if "application/json" in response.headers.get("content-type", ""):
            return response.json()
        else:
            return response.text
    except Exception:
        return response.text