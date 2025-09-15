import os
import json
import markdown
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from collections import defaultdict, Counter
from config import Config

class PortfolioGenerator:
    def __init__(self):
        self.config = Config()
        self.env = Environment(loader=FileSystemLoader(self.config.TEMPLATES_DIR))
        
    def prepare_data(self, articles, summaries=None):
        """准备模板数据"""
        # 基础统计
        total_articles = len(articles)
        total_reads = sum(article.get('read_count', 0) for article in articles)
        total_likes = sum(article.get('like_count', 0) for article in articles)
        total_comments = sum(article.get('comment_count', 0) for article in articles)
        
        # 按阅读量和点赞数排序获取热门文章
        hot_articles = sorted(
            articles, 
            key=lambda x: x.get('read_count', 0) + x.get('like_count', 0) * 5, 
            reverse=True
        )[:6]
        
        # 最新文章（按发布时间排序）
        latest_articles = sorted(
            articles,
            key=lambda x: self._parse_date_for_sort(x.get('publish_time', '')),
            reverse=True
        )[:6]
        
        # 按月份统计
        monthly_stats = self._get_monthly_stats(articles)
        months_active = len(monthly_stats)
        
        # 提取技术关键词
        tech_keywords = self._extract_tech_keywords(articles)
        
        # 月度文章数统计
        monthly_counts = self._get_monthly_counts(articles)
        
        return {
            'total_articles': total_articles,
            'total_reads': total_reads,
            'total_likes': total_likes,
            'total_comments': total_comments,
            'avg_reads': total_reads // total_articles if total_articles > 0 else 0,
            'months_active': months_active,
            'hot_articles': hot_articles,
            'latest_articles': latest_articles,
            'monthly_stats': monthly_stats,
            'tech_keywords': tech_keywords[:20],  # 前20个关键词
            'monthly_counts': monthly_counts,
            'current_date': datetime.now().strftime('%Y-%m-%d'),
            'summaries': summaries or {}
        }
    
    def _parse_date_for_sort(self, date_str):
        """解析日期用于排序"""
        if not date_str:
            return datetime.min
        
        # 尝试不同的日期格式
        formats = [
            '%Y-%m-%d',
            '%Y年%m月%d日',
            '%m-%d',
            '%m月%d日'
        ]
        
        for fmt in formats:
            try:
                if fmt in ['%m-%d', '%m月%d日']:
                    # 对于只有月日的格式，假设是当年
                    parsed = datetime.strptime(date_str, fmt)
                    return parsed.replace(year=datetime.now().year)
                else:
                    return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return datetime.min
    
    def _get_monthly_stats(self, articles):
        """获取月度统计"""
        monthly = defaultdict(int)
        
        for article in articles:
            date = self._parse_date_for_sort(article.get('publish_time', ''))
            if date != datetime.min:
                month_key = date.strftime('%Y-%m')
                monthly[month_key] += 1
        
        # 返回最近6个月的统计
        return dict(sorted(monthly.items(), reverse=True)[:6])
    
    def _get_monthly_counts(self, articles):
        """获取完整的月度文章数统计"""
        monthly = defaultdict(int)
        
        for article in articles:
            date = self._parse_date_for_sort(article.get('publish_time', ''))
            if date != datetime.min:
                month_key = date.strftime('%Y-%m')
                monthly[month_key] += 1
        
        return dict(sorted(monthly.items(), reverse=True))
    
    def _extract_tech_keywords(self, articles):
        """提取技术关键词"""
        # 技术关键词词典
        tech_terms = {
            'Python', 'Java', 'JavaScript', 'C++', 'Go', 'Rust', 'TypeScript',
            'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask', 'Spring',
            'MySQL', 'Redis', 'MongoDB', 'PostgreSQL', 'Elasticsearch',
            'Docker', 'Kubernetes', 'Linux', 'Git', 'GitHub', 'CI/CD',
            'AI', '人工智能', '机器学习', '深度学习', 'ChatGPT', 'LLM',
            '算法', '数据结构', '设计模式', 'OOP', 'API',
            '前端', '后端', '全栈', '微服务', '分布式',
            '云计算', '大数据', '区块链', 'Web3',
            'TensorFlow', 'PyTorch', 'Pandas', 'NumPy',
            'AWS', '阿里云', '腾讯云',
            'Nginx', 'Apache', 'Tomcat',
            'JVM', 'GC', '性能优化',
            'CUDA', 'GPU', '并行计算',
            'Qt', 'LVGL', 'OpenGL',
            'Shell', 'Bash', 'PowerShell',
            'JSON', 'XML', 'YAML', 'ProtoBuf'
        }
        
        # 统计关键词出现次数
        keyword_count = Counter()
        
        for article in articles:
            title = article.get('title', '')
            content = article.get('content', '')
            text = (title + ' ' + content).upper()
            
            for term in tech_terms:
                if term.upper() in text or term in title or term in content:
                    keyword_count[term] += 1
        
        # 返回按出现频次排序的关键词
        return [keyword for keyword, count in keyword_count.most_common()]
    
    def generate_index_page(self, articles, summaries=None):
        """生成首页"""
        template = self.env.get_template('index.html')
        data = self.prepare_data(articles, summaries)
        
        html_content = template.render(**data)
        
        # 确保输出目录存在
        os.makedirs(self.config.OUTPUT_DIR, exist_ok=True)
        
        # 写入文件
        output_path = os.path.join(self.config.OUTPUT_DIR, 'index.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"首页已生成: {output_path}")
        return output_path
    
    def generate_articles_page(self, articles):
        """生成文章列表页"""
        template = self.env.get_template('articles.html')
        data = self.prepare_data(articles)
        
        # 为文章页面添加额外数据
        data.update({
            'articles': articles,
            'search_query': '',
            'current_page': 1,
            'total_pages': 1,
            'popular_keywords': data['tech_keywords'][:15]
        })
        
        html_content = template.render(**data)
        
        # 写入文件
        output_path = os.path.join(self.config.OUTPUT_DIR, 'articles.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"文章列表页已生成: {output_path}")
        return output_path
    
    def generate_summaries_page(self, summaries):
        """生成月度总结页"""
        template = self.env.get_template('summaries.html')
        
        # 计算总结页面的统计数据
        total_articles_in_summaries = sum(
            summary_data.get('article_count', 0) 
            for summary_data in summaries.values()
        )
        
        avg_articles_per_month = (
            total_articles_in_summaries // len(summaries) 
            if summaries else 0
        )
        
        # 找出最活跃的月份
        most_productive_month = max(
            summaries.keys(),
            key=lambda k: summaries[k].get('article_count', 0)
        ) if summaries else "暂无"
        
        # 转换Markdown格式的总结为HTML
        processed_summaries = {}
        for month_key, summary_data in summaries.items():
            processed_summary = summary_data.copy()
            # 简单的Markdown处理
            summary_text = summary_data.get('summary', '')
            processed_summary['summary'] = self._simple_markdown_to_html(summary_text)
            processed_summaries[month_key] = processed_summary
        
        data = {
            'summaries': processed_summaries,
            'total_articles_in_summaries': total_articles_in_summaries,
            'avg_articles_per_month': avg_articles_per_month,
            'most_productive_month': most_productive_month,
            'current_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        html_content = template.render(**data)
        
        # 写入文件
        output_path = os.path.join(self.config.OUTPUT_DIR, 'summaries.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"月度总结页已生成: {output_path}")
        return output_path
    
    def _simple_markdown_to_html(self, text):
        """简单的Markdown转HTML"""
        if not text:
            return ""
        
        # 使用Python的markdown库
        try:
            html = markdown.markdown(text)
            return html
        except:
            # 如果markdown库不可用，进行简单替换
            html = text.replace('\n', '<br>')
            html = html.replace('**', '<strong>').replace('**', '</strong>')
            html = html.replace('*', '<em>').replace('*', '</em>')
            return html
    
    def generate_portfolio(self, articles, summaries=None):
        """生成完整的作品集"""
        print("开始生成作品集...")
        
        # 生成各个页面
        index_path = self.generate_index_page(articles, summaries)
        articles_path = self.generate_articles_page(articles)
        
        if summaries:
            summaries_path = self.generate_summaries_page(summaries)
        else:
            print("未提供月度总结数据，跳过总结页面生成")
        
        print(f"作品集生成完成！输出目录: {self.config.OUTPUT_DIR}")
        print(f"- 首页: {index_path}")
        print(f"- 文章列表: {articles_path}")
        if summaries:
            print(f"- 月度总结: {summaries_path}")
        
        return self.config.OUTPUT_DIR

if __name__ == "__main__":
    generator = PortfolioGenerator()
    
    # 加载数据
    try:
        # 加载文章数据
        with open('articles.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
        
        # 尝试加载总结数据
        summaries = None
        try:
            with open('monthly_summaries.json', 'r', encoding='utf-8') as f:
                summaries = json.load(f)
        except FileNotFoundError:
            print("未找到月度总结文件，将只生成基础页面")
        
        # 生成作品集
        generator.generate_portfolio(articles, summaries)
        
    except FileNotFoundError:
        print("未找到articles.json文件，请先运行爬虫获取文章数据")
