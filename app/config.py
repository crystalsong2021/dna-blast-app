import ssl
import certifi
import os

class Config:
    ENABLE_MOCK_DATA = False
    CACHE_DIR = "blast_cache"

# SSL fix for NCBI
ssl._create_default_https_context = lambda: ssl.create_default_context(
    cafile=certifi.where()
)

# Ensure cache directory exists
os.makedirs(Config.CACHE_DIR, exist_ok=True)
