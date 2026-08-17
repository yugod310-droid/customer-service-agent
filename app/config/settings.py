import os

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    def load_dotenv():
        return False


load_dotenv()

PROJECT_NAME = os.getenv("PROJECT_NAME", "Customer Service Agent")
VERSION = os.getenv("PROJECT_VERSION", "0.1.0")
MODEL_PATH = os.getenv("MODEL_PATH", r"D:\AI\models\models\Qwen--Qwen2.5-3B-Instruct\snapshots\master")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEFAULT_PHONE = os.getenv("DEFAULT_PHONE", "13863727112")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "200"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))