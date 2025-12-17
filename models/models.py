from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
    
load_dotenv()

llm_basic = ChatAnthropic(model_name="claude-haiku-4-5-20251001", timeout=180, stop=["\n\nHuman:"])
llm_advanced = ChatAnthropic(model_name="claude-sonnet-4-5-20250929", timeout=180, stop=["\n\nHuman:"])