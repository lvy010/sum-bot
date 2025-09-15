import openai
from datetime import datetime, timedelta
import json
import re
from collections import defaultdict
from config import Config

class AISummarizer:
    def __init__(self):
        self.config = Config()
        if self.config.OPENAI_API_KEY:
            openai.api_key = self.config.OPENAI_API_KEY
        else:
            print("警告: 未设置OpenAI API密钥，将无法使用AI总结功能")
    
    def group_articles_by_month(self, articles):
        """按月份分组文章"""
        monthly_articles = defaultdict(list)
        
        for article in articles:
            # 解析发布时间
            publish_date = self._parse_date(article.get('publish_time', ''))
            if publish_date:
                month_key = publish_date.strftime('%Y-%m')
                monthly_articles[month_key].append(article)
        
        return dict(monthly_articles)
    
    def _parse_date(self, date_str):
        """解析各种格式的日期字符串"""
        if not date_str:
            return None
            
        # 常见的CSDN日期格式
        date_patterns = [
            r'(\d{4})-(\d{1,2})-(\d{1,2})',  # 2025-09-15
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',  # 2025年9月15日
            r'(\d{1,2})-(\d{1,2})',  # 09-15 (当年)
            r'(\d{1,2})月(\d{1,2})日',  # 9月15日 (当年)
        ]
        
        current_year = datetime.now().year
        
        for pattern in date_patterns:
            match = re.search(pattern, date_str)
            if match:
                try:
                    groups = match.groups()
                    if len(groups) == 3:  # 年月日
                        year, month, day = map(int, groups)
                    elif len(groups) == 2:  # 月日
                        year = current_year
                        month, day = map(int, groups)
                    else:
                        continue
                    
                    return datetime(year, month, day)
                except ValueError:
                    continue
        
        return None
    
    def generate_monthly_summary(self, articles, month_key):
        """为指定月份生成AI总结"""
        if not self.config.OPENAI_API_KEY:
            return self._generate_simple_summary(articles, month_key)
        
        # 准备文章内容
        articles_text = self._prepare_articles_for_summary(articles)
        
        # 构建提示词
        prompt = f"""
请根据以下{month_key}月份的CSDN博客文章，生成一份详细的月度总结报告。

文章内容：
{articles_text}

请按以下格式生成总结：

## {month_key} 月度博客总结

### 📊 基本统计
- 发布文章数量：{len(articles)}篇
- 主要技术领域：[请分析文章涉及的技术领域]
- 总阅读量：[计算总阅读量]
- 总点赞数：[计算总点赞数]

### 🎯 核心主题分析
[请分析本月文章的主要技术主题和方向]

### 💡 技术亮点
[请提取本月最有价值的技术内容和见解]

### 📈 成长收获
[请分析本月在技术学习和分享方面的成长]

### 🔥 热门文章
[请列出阅读量或点赞数较高的文章]

### 🚀 下月展望
[基于本月内容，建议下月可以关注的技术方向]

请用中文回答，内容要专业且有深度。
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的技术博客分析师，擅长分析技术文章并生成深度总结。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"AI总结生成失败: {e}")
            return self._generate_simple_summary(articles, month_key)
    
    def _prepare_articles_for_summary(self, articles):
        """准备文章内容用于AI总结"""
        articles_text = ""
        
        for i, article in enumerate(articles, 1):
            title = article.get('title', '无标题')
            content = article.get('content', '')[:500]  # 限制长度
            read_count = article.get('read_count', 0)
            like_count = article.get('like_count', 0)
            
            articles_text += f"""
{i}. 标题：{title}
   阅读量：{read_count} | 点赞数：{like_count}
   内容摘要：{content}...
   
"""
        
        return articles_text
    
    def _generate_simple_summary(self, articles, month_key):
        """生成简单的统计总结（不使用AI）"""
        total_reads = sum(article.get('read_count', 0) for article in articles)
        total_likes = sum(article.get('like_count', 0) for article in articles)
        total_comments = sum(article.get('comment_count', 0) for article in articles)
        
        # 提取关键词
        all_titles = ' '.join(article.get('title', '') for article in articles)
        keywords = self._extract_keywords(all_titles)
        
        # 找出热门文章
        hot_articles = sorted(articles, 
                            key=lambda x: x.get('read_count', 0) + x.get('like_count', 0) * 5, 
                            reverse=True)[:3]
        
        summary = f"""## {month_key} 月度博客总结

### 📊 基本统计
- 发布文章数量：{len(articles)}篇
- 总阅读量：{total_reads}
- 总点赞数：{total_likes}
- 总评论数：{total_comments}

### 🎯 主要关键词
{', '.join(keywords[:10])}

### 🔥 热门文章
"""
        
        for i, article in enumerate(hot_articles, 1):
            title = article.get('title', '无标题')
            reads = article.get('read_count', 0)
            likes = article.get('like_count', 0)
            summary += f"{i}. {title} (阅读:{reads}, 点赞:{likes})\n"
        
        return summary
    
    def _extract_keywords(self, text):
        """简单的关键词提取"""
        # 技术相关关键词
        tech_keywords = [
            'Python', 'Java', 'JavaScript', 'C++', 'Go', 'Rust',
            'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask',
            'MySQL', 'Redis', 'MongoDB', 'PostgreSQL',
            'Docker', 'Kubernetes', 'Linux', 'Git',
            'AI', '人工智能', '机器学习', '深度学习',
            '算法', '数据结构', '设计模式',
            '前端', '后端', '全栈', '微服务',
            '云计算', '大数据', '区块链'
        ]
        
        found_keywords = []
        text_upper = text.upper()
        
        for keyword in tech_keywords:
            if keyword.upper() in text_upper or keyword in text:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def generate_all_monthly_summaries(self, articles):
        """生成所有月份的总结"""
        monthly_articles = self.group_articles_by_month(articles)
        summaries = {}
        
        for month_key, month_articles in monthly_articles.items():
            print(f"正在生成{month_key}月份总结...")
            summary = self.generate_monthly_summary(month_articles, month_key)
            summaries[month_key] = {
                'summary': summary,
                'article_count': len(month_articles),
                'articles': month_articles
            }
        
        return summaries

if __name__ == "__main__":
    # 测试代码
    summarizer = AISummarizer()
    
    # 加载示例数据
    try:
        with open('articles.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
        
        summaries = summarizer.generate_all_monthly_summaries(articles)
        
        # 保存总结
        with open('monthly_summaries.json', 'w', encoding='utf-8') as f:
            json.dump(summaries, f, ensure_ascii=False, indent=2)
        
        print("月度总结生成完成！")
        
    except FileNotFoundError:
        print("未找到articles.json文件，请先运行爬虫获取文章数据")
