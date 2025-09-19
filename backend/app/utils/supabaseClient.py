from supabase import create_client
from app.config import Config
import os


SUPABASE_URL = Config.SUPABASE_URL
SUPABASE_BUCKET = Config.SUPABASE_BUCKET
SUPABASE_SERVICE_ROLE_KEY = Config.SUPABASE_SERVICE_ROLE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def uploadFile(filename, format, expires_in=31536000):

    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(os.path.dirname(current_dir))
    videos_dir = os.path.join(backend_dir, "videos")
    
    local_file_path_with_suffix = os.path.join(videos_dir, f"{filename}_ManimCE_v0.19.0.{format}")
    local_file_path_without_suffix = os.path.join(videos_dir, f"{filename}.{format}")
    
    if os.path.exists(local_file_path_with_suffix):
        local_file_path = local_file_path_with_suffix
        print(f"Found file with Manim suffix: {local_file_path}")
    elif os.path.exists(local_file_path_without_suffix):
        local_file_path = local_file_path_without_suffix
        print(f"Found file without suffix: {local_file_path}")
    else:
        try:
            available_files = os.listdir(videos_dir)
            print(f"Available files in {videos_dir}: {available_files}")
        except:
            print(f"Could not list files in {videos_dir}")
        raise FileNotFoundError(f"Video file not found. Checked:\n- {local_file_path_with_suffix}\n- {local_file_path_without_suffix}")
    
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
