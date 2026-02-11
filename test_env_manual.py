import os
from pathlib import Path

# Manually read .env file (no dotenv dependency)
env_file = Path(__file__).parent / ".env"

if env_file.exists():
    print(f"✅ Found .env file at: {env_file}")
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    os.environ[key] = value
                    print(f"   Set {key}={value}")
else:
    print(f"❌ No .env file found at: {env_file}")

print("\n📋 Environment Variables:")
print(f"LLM_PROVIDER: {os.getenv('LLM_PROVIDER', 'NOT SET')}")
print(f"LOCAL_LLM_BASE_URL: {os.getenv('LOCAL_LLM_BASE_URL', 'NOT SET')}")
print(f"LOCAL_LLM_MODEL: {os.getenv('LOCAL_LLM_MODEL', 'NOT SET')}")