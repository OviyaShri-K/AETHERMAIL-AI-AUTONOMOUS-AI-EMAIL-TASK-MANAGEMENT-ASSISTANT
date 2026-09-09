import os

def load_env_file(filepath):
    """Lightweight .env file parser with zero third-party dependency."""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    val = val.strip().strip("'").strip('"')
                    os.environ.setdefault(key.strip(), val)

# Load .env / .env.example from backend or project root
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(backend_dir)

for candidate in [
    os.path.join(backend_dir, ".env"),
    os.path.join(backend_dir, ".env.example"),
    os.path.join(root_dir, ".env"),
    os.path.join(root_dir, ".env.example")
]:
    load_env_file(candidate)

class Settings:
    # 1. Database Connection URL (Supabase PostgreSQL)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{os.path.join(backend_dir, 'local_dev.db')}"
    )
    
    # 2. Supabase Cloud API Credentials
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # 3. Google Gemini API Key
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # 4. Cloudinary Cloud Media & Attachment Storage Credentials
    CLOUDINARY_CLOUD_NAME: str = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY: str = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET", "")
    CLOUDINARY_URL: str = os.getenv("CLOUDINARY_URL", "")
    
    # 5. App Environment
    APP_ENV: str = os.getenv("APP_ENV", "development")

settings = Settings()
