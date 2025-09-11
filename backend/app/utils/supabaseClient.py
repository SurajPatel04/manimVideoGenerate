from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def uploadFile(filename, format, expires_in=86400):

    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(os.path.dirname(current_dir))
    videos_dir = os.path.join(backend_dir, "videos")
    local_file_path = os.path.join(videos_dir, f"{filename}.{format}")
    bucket_path = f"videos/{filename}.{format}"

    if not os.path.exists(videos_dir):
        raise FileNotFoundError(f"Videos directory not found at: {videos_dir}")
    
    with open(local_file_path, "rb") as f:
        response = supabase.storage.from_(SUPABASE_BUCKET).upload(
            path=bucket_path,
            file=f,
            file_options={
                "cache-control": "3600",
                "upsert": "false"
            }
        )

    signed_url_response = supabase.storage.from_(SUPABASE_BUCKET).create_signed_url(
        path=bucket_path,
        expires_in=expires_in
    )
    
    
    # Handle different response structures
    if isinstance(signed_url_response, dict):
        # Try different possible keys
        signed_url = (signed_url_response.get("signed_url") or 
                     signed_url_response.get("signedURL") or 
                     signed_url_response.get("url") or
                     signed_url_response.get("data", {}).get("signed_url") or
                     signed_url_response.get("data", {}).get("signedURL"))
    elif isinstance(signed_url_response, str):
        signed_url = signed_url_response
    else:
        try:
            signed_url = getattr(signed_url_response, 'signed_url', None) or str(signed_url_response)
        except:
            signed_url = None
    
    print(f"Final signed URL: {signed_url}")
    
    if not signed_url:
        raise Exception(f"Failed to extract signed URL from response: {signed_url_response}")
    
    return signed_url
