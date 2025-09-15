import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # CSDN博客配置
    CSDN_USER_ID = "2301_80171004"
    CSDN_BASE_URL = f"https://blog.csdn.net/{CSDN_USER_ID}"
    
    # OpenAI配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # 输出目录配置
    OUTPUT_DIR = "portfolio"
    ARTICLES_DIR = "articles"
    SUMMARIES_DIR = "monthly_summaries"
    TEMPLATES_DIR = "templates"
    
    # 爬虫配置
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 请求延迟（秒）- 增加延迟避免反爬
    REQUEST_DELAY = 3
    
    # 每页文章数
    ARTICLES_PER_PAGE = 20
