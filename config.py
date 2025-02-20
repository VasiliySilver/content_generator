from decouple import config

GROQ_API_KEY = config("GROQ_API_KEY", cast=str, default="Your_default_API_key")
PROXY = "socks5://127.0.0.1:2080"  # Proxy if you work with VPN
