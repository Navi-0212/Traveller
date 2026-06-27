import os
import uvicorn

if __name__ == "__main__":
    # Railway injects a PORT env var. Default to 8000 for local.
    port = int(os.environ.get("PORT", 8000))
    # Bind to 0.0.0.0 in production to accept external routing, 127.0.0.1 for local.
    is_prod = os.environ.get("PORT") is not None or os.environ.get("RAILWAY_ENVIRONMENT") is not None
    host = "0.0.0.0" if is_prod else "127.0.0.1"
    
    uvicorn.run("app.main:app", host=host, port=port, reload=not is_prod)
