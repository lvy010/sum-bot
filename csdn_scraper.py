import requests
from bs4 import BeautifulSoup
import time
import json
import re
from datetime import datetime
from urllib.parse import urljoin
from config import Config

class CSDNScraper:
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        
        # 更完善的请求头，模拟真实浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        self.session.headers.update(headers)
        
        # 设置超时和重试
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        retry_strategy = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504, 521, 522, 524]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
    def get_article_list(self, max_pages=None):
        """获取所有文章列表"""
        articles = []
        page = 1
        
        while True:
            print(f"正在爬取第{page}页...")
            
            # 构建文章列表URL
            url = f"{self.config.CSDN_BASE_URL}/article/list/{page}"
            
            try:
                # 添加随机延迟，模拟人类行为
                import random
                delay = random.uniform(1, 3)
                time.sleep(delay)
                
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找文章列表 - 尝试多种可能的选择器
                article_items = (
                    soup.find_all('div', class_='article-item-box') or
                    soup.find_all('div', class_='article-list') or 
                    soup.find_all('article') or
                    soup.find_all('div', class_='blog-list-box')
                )
                
                if not article_items:
                    print(f"第{page}页没有找到文章，可能遇到反爬限制或页面结构变化")
                    print(f"页面内容预览: {response.text[:200]}...")
                    break
                
                for item in article_items:
                    article_info = self._extract_article_info(item)
                    if article_info:
                        articles.append(article_info)
                
                print(f"第{page}页获取到{len(article_items)}篇文章")
                
                # 检查是否达到最大页数
                if max_pages and page >= max_pages:
                    break
                
                page += 1
                
                # 增加页面间延迟
                time.sleep(self.config.REQUEST_DELAY + random.uniform(1, 2))
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 521:
                    print(f"遇到521错误，等待{self.config.REQUEST_DELAY * 2}秒后重试...")
                    time.sleep(self.config.REQUEST_DELAY * 2)
                    continue
                else:
                    print(f"HTTP错误 {e.response.status_code}: {e}")
                    break
            except Exception as e:
                print(f"爬取第{page}页时出错: {e}")
                # 尝试继续下一页
                if page < 3:  # 前3页出错就停止
                    break
                else:
                    page += 1
                    continue
        
        return articles
    
    def _extract_article_info(self, item):
        """从文章项中提取信息"""
        try:
            # 文章标题和链接
            title_elem = item.find('h4', class_='') or item.find('a')
            if not title_elem:
                return None
                
            title = title_elem.get_text(strip=True)
            article_url = title_elem.get('href', '')
            
            if not article_url.startswith('http'):
                article_url = urljoin(self.config.CSDN_BASE_URL, article_url)
            
            # 发布时间
            time_elem = item.find('span', class_='date')
            publish_time = time_elem.get_text(strip=True) if time_elem else ""
            
            # 阅读量、点赞数、评论数
            stats = self._extract_stats(item)
            
            return {
                'title': title,
                'url': article_url,
                'publish_time': publish_time,
                'read_count': stats.get('read_count', 0),
                'like_count': stats.get('like_count', 0),
                'comment_count': stats.get('comment_count', 0),
                'content': ''  # 稍后获取
            }
            
        except Exception as e:
            print(f"提取文章信息时出错: {e}")
            return None
    
    def _extract_stats(self, item):
        """提取文章统计信息"""
        stats = {'read_count': 0, 'like_count': 0, 'comment_count': 0}
        
        # 查找统计信息
        stat_elements = item.find_all('span', class_=['read-num', 'praise', 'comment'])
        
        for elem in stat_elements:
            text = elem.get_text(strip=True)
            numbers = re.findall(r'\d+', text)
            if numbers:
                count = int(numbers[0])
                if '阅读' in text:
                    stats['read_count'] = count
                elif '点赞' in text:
                    stats['like_count'] = count
                elif '评论' in text:
                    stats['comment_count'] = count
        
        return stats
    
    def get_article_content(self, article_url):
        """获取文章详细内容"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                print(f"正在获取文章内容: {article_url} (尝试 {attempt + 1}/{max_retries})")
                
                # 添加随机延迟
                import random
                time.sleep(random.uniform(2, 4))
                
                # 添加Referer头，模拟从列表页点击进入
                headers = {'Referer': self.config.CSDN_BASE_URL}
                response = self.session.get(article_url, timeout=20, headers=headers)
                
                # 检查响应状态
                if response.status_code == 521:
                    print(f"遇到521错误，等待{5 + attempt * 2}秒后重试...")
                    time.sleep(5 + attempt * 2)
                    continue
                
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找文章内容 - 尝试多种选择器
                content_elem = (
                    soup.find('div', {'id': 'content_views'}) or
                    soup.find('div', class_='markdown_views') or 
                    soup.find('div', class_='htmledit_views') or
                    soup.find('article') or
                    soup.find('div', class_='blog-content-box')
                )
                
                if content_elem:
                    # 清理HTML标签，保留文本内容
                    content = content_elem.get_text(separator='\n', strip=True)
                    # 限制内容长度，避免过长
                    if len(content) > 2000:
                        content = content[:2000] + "..."
                    return content
                else:
                    print(f"无法找到文章内容: {article_url}")
                    return ""
                    
            except requests.exceptions.HTTPError as e:
                if e.response and e.response.status_code == 521:
                    print(f"521错误，尝试 {attempt + 1}/{max_retries}")
                    if attempt < max_retries - 1:
                        time.sleep(5 + attempt * 3)
                        continue
                else:
                    print(f"HTTP错误: {e}")
                    break
            except Exception as e:
                print(f"获取文章内容时出错: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                break
        
        return ""
    
    def scrape_all_articles(self, max_pages=None, include_content=True):
        """爬取所有文章（包括内容）"""
        print("开始爬取CSDN博客文章...")
        
        # 获取文章列表
        articles = self.get_article_list(max_pages)
        print(f"共找到{len(articles)}篇文章")
        
        if include_content:
            # 获取每篇文章的详细内容
            for i, article in enumerate(articles, 1):
                print(f"正在获取第{i}/{len(articles)}篇文章内容...")
                content = self.get_article_content(article['url'])
                article['content'] = content
                time.sleep(self.config.REQUEST_DELAY)
        
        return articles
    
    def save_articles_to_json(self, articles, filename="articles.json"):
        """保存文章到JSON文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"文章已保存到 {filename}")

if __name__ == "__main__":
    scraper = CSDNScraper()
    
    # 爬取前5页文章（测试用）
    articles = scraper.scrape_all_articles(max_pages=5)
    
    # 保存到JSON文件
    scraper.save_articles_to_json(articles)
    
    print(f"爬取完成！共获取{len(articles)}篇文章")
