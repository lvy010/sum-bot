#!/usr/bin/env python3
"""
智能爬虫 - 专门处理CSDN反爬虫机制
包含多种反反爬策略：代理轮换、请求头轮换、智能延迟等
"""

import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import Config

class SmartCSDNScraper:
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        self.setup_session()
        
        # 用户代理池
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15'
        ]
        
    def setup_session(self):
        """设置会话"""
        # 设置重试策略
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        retry_strategy = Retry(
            total=5,
            backoff_factor=3,
            status_forcelist=[429, 500, 502, 503, 504, 521, 522, 524],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 设置连接池
        self.session.mount('https://', HTTPAdapter(pool_connections=1, pool_maxsize=1))
    
    def get_random_headers(self):
        """获取随机请求头"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
    
    def smart_delay(self, base_delay=3):
        """智能延迟 - 模拟人类行为"""
        # 基础延迟 + 随机延迟
        delay = base_delay + random.uniform(1, 4)
        
        # 偶尔添加更长的延迟，模拟用户阅读时间
        if random.random() < 0.1:  # 10%概率
            delay += random.uniform(5, 15)
            print(f"模拟用户阅读，额外等待{delay-base_delay:.1f}秒...")
        
        time.sleep(delay)
    
    def safe_request(self, url, max_retries=5):
        """安全请求 - 处理521等错误"""
        for attempt in range(max_retries):
            try:
                # 每次请求使用随机请求头
                headers = self.get_random_headers()
                
                # 添加Referer
                if attempt > 0:
                    headers['Referer'] = self.config.CSDN_BASE_URL
                
                print(f"请求 {url} (尝试 {attempt + 1}/{max_retries})")
                
                response = self.session.get(
                    url, 
                    headers=headers, 
                    timeout=30,
                    allow_redirects=True
                )
                
                # 检查响应状态
                if response.status_code == 200:
                    return response
                elif response.status_code == 521:
                    wait_time = (attempt + 1) * 10 + random.uniform(5, 15)
                    print(f"521错误，等待{wait_time:.1f}秒后重试...")
                    time.sleep(wait_time)
                    continue
                elif response.status_code == 403:
                    wait_time = (attempt + 1) * 15 + random.uniform(10, 20)
                    print(f"403错误，等待{wait_time:.1f}秒后重试...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"HTTP {response.status_code}: {response.reason}")
                    if attempt < max_retries - 1:
                        self.smart_delay(5)
                        continue
                    else:
                        break
                        
            except requests.exceptions.RequestException as e:
                print(f"请求异常: {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5
                    print(f"等待{wait_time}秒后重试...")
                    time.sleep(wait_time)
                    continue
                else:
                    break
        
        return None
    
    def get_article_list_smart(self, max_pages=3):
        """智能获取文章列表"""
        articles = []
        
        print(f"开始智能爬取，最多{max_pages}页...")
        
        for page in range(1, max_pages + 1):
            print(f"\n=== 爬取第{page}页 ===")
            
            # 构建URL
            url = f"{self.config.CSDN_BASE_URL}/article/list/{page}"
            
            # 智能延迟
            if page > 1:
                self.smart_delay()
            
            # 安全请求
            response = self.safe_request(url)
            
            if not response:
                print(f"第{page}页请求失败，跳过")
                continue
            
            # 解析页面
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找文章 - 多种选择器
            selectors = [
                'div.article-item-box',
                'div.blog-list-box', 
                'article',
                'div[class*="article"]',
                'div[class*="blog"]'
            ]
            
            article_items = []
            for selector in selectors:
                items = soup.select(selector)
                if items:
                    article_items = items
                    print(f"使用选择器 '{selector}' 找到{len(items)}篇文章")
                    break
            
            if not article_items:
                print("未找到文章，可能遇到反爬限制")
                print("页面内容预览:")
                print(response.text[:500])
                continue
            
            # 提取文章信息
            page_articles = []
            for item in article_items:
                article_info = self.extract_article_info_smart(item)
                if article_info:
                    page_articles.append(article_info)
            
            articles.extend(page_articles)
            print(f"第{page}页成功获取{len(page_articles)}篇文章")
            
            # 如果获取的文章很少，可能遇到了限制
            if len(page_articles) < 5 and page > 1:
                print("获取文章数量异常，可能遇到反爬限制，停止爬取")
                break
        
        return articles
    
    def extract_article_info_smart(self, item):
        """智能提取文章信息"""
        try:
            # 多种方式查找标题和链接
            title_elem = (
                item.select_one('h4 a') or
                item.find('a', class_='title') or
                item.find('h4') or
                item.find('a')
            )
            
            if not title_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            
            # 获取链接，优先从a标签获取
            if title_elem.name == 'a':
                article_url = title_elem.get('href', '')
            else:
                # 如果是h4等其他标签，查找内部的a标签
                link_elem = title_elem.find('a')
                article_url = link_elem.get('href', '') if link_elem else ''
            
            if not article_url.startswith('http'):
                article_url = urljoin(self.config.CSDN_BASE_URL, article_url)
            
            # 提取时间
            time_elem = item.find('span', class_='date') or item.find('time')
            publish_time = time_elem.get_text(strip=True) if time_elem else ""
            
            # 提取统计数据
            read_count = self.extract_number(item, ['阅读', 'read'])
            like_count = self.extract_number(item, ['点赞', 'like', '👍'])
            comment_count = self.extract_number(item, ['评论', 'comment'])
            
            return {
                'title': title,
                'url': article_url,
                'publish_time': publish_time,
                'read_count': read_count,
                'like_count': like_count,
                'comment_count': comment_count,
                'content': ''  # 稍后获取
            }
            
        except Exception as e:
            print(f"提取文章信息出错: {e}")
            return None
    
    def extract_number(self, element, keywords):
        """从元素中提取数字"""
        try:
            text = element.get_text()
            for keyword in keywords:
                if keyword in text:
                    import re
                    numbers = re.findall(r'\d+', text)
                    if numbers:
                        return int(numbers[0])
            return 0
        except:
            return 0
    
    def get_article_content_smart(self, article_url):
        """智能获取文章内容"""
        print(f"获取文章内容: {article_url}")
        
        # 智能延迟
        self.smart_delay(2)
        
        response = self.safe_request(article_url)
        if not response:
            return ""
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 多种内容选择器
        content_selectors = [
            '#content_views',
            '.markdown_views',
            '.htmledit_views', 
            'article',
            '.blog-content-box',
            '.article-content'
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                content = content_elem.get_text(separator='\n', strip=True)
                # 限制长度
                if len(content) > 1500:
                    content = content[:1500] + "..."
                return content
        
        return ""

if __name__ == "__main__":
    # 测试智能爬虫
    scraper = SmartCSDNScraper()
    articles = scraper.get_article_list_smart(max_pages=2)
    
    print(f"\n=== 爬取结果 ===")
    print(f"共获取 {len(articles)} 篇文章")
    
    for i, article in enumerate(articles[:3], 1):
        print(f"{i}. {article['title']}")
        print(f"   阅读: {article['read_count']}, 点赞: {article['like_count']}")
        print(f"   URL: {article['url']}")
        print()
