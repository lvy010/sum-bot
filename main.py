#!/usr/bin/env python3
"""
CSDN博客作品集生成器
自动爬取CSDN博客文章，生成AI月度总结，并创建精美的作品集网站
"""

import argparse
import json
import os
import sys
from datetime import datetime

from csdn_scraper import CSDNScraper
from smart_scraper import SmartCSDNScraper
from ai_summarizer import AISummarizer
from portfolio_generator import PortfolioGenerator
from config import Config

class CSDBlogPortfolio:
    def __init__(self):
        self.config = Config()
        self.scraper = CSDNScraper()
        self.smart_scraper = SmartCSDNScraper()
        self.summarizer = AISummarizer()
        self.generator = PortfolioGenerator()
        
    def scrape_articles(self, max_pages=None, force_refresh=False):
        """爬取文章"""
        articles_file = 'articles.json'
        
        # 检查是否已有数据且不强制刷新
        if os.path.exists(articles_file) and not force_refresh:
            print("发现已有文章数据，使用缓存数据...")
            print("如需重新爬取，请使用 --force-refresh 参数")
            with open(articles_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        print("开始爬取CSDN博客文章...")
        
        # 优先使用智能爬虫
        try:
            print("使用智能爬虫（推荐）...")
            articles = self.smart_scraper.get_article_list_smart(max_pages=max_pages or 5)
            
            # 获取文章内容
            if articles:
                print(f"获取到{len(articles)}篇文章，开始获取详细内容...")
                for i, article in enumerate(articles[:10], 1):  # 限制获取内容的文章数量
                    print(f"获取第{i}/{min(10, len(articles))}篇文章内容...")
                    content = self.smart_scraper.get_article_content_smart(article['url'])
                    article['content'] = content
                    if i >= 10:  # 最多获取10篇文章的详细内容
                        print("已获取前10篇文章的详细内容，其余文章只保留基本信息")
                        break
        except Exception as e:
            print(f"智能爬虫失败: {e}")
            print("回退到普通爬虫...")
            articles = self.scraper.scrape_all_articles(max_pages=max_pages)
        
        # 保存文章数据
        self.scraper.save_articles_to_json(articles, articles_file)
        
        return articles
    
    def generate_summaries(self, articles, force_refresh=False):
        """生成月度总结"""
        summaries_file = 'monthly_summaries.json'
        
        # 检查是否已有总结且不强制刷新
        if os.path.exists(summaries_file) and not force_refresh:
            print("发现已有月度总结，使用缓存数据...")
            print("如需重新生成，请使用 --force-refresh 参数")
            with open(summaries_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        print("开始生成AI月度总结...")
        summaries = self.summarizer.generate_all_monthly_summaries(articles)
        
        # 保存总结数据
        with open(summaries_file, 'w', encoding='utf-8') as f:
            json.dump(summaries, f, ensure_ascii=False, indent=2)
        
        print(f"月度总结已保存到 {summaries_file}")
        return summaries
    
    def generate_portfolio(self, articles, summaries):
        """生成作品集网站"""
        print("开始生成作品集网站...")
        output_dir = self.generator.generate_portfolio(articles, summaries)
        return output_dir
    
    def run_full_pipeline(self, max_pages=None, force_refresh=False):
        """运行完整流程"""
        try:
            print("=" * 60)
            print("CSDN博客作品集生成器")
            print("=" * 60)
            
            # 步骤1: 爬取文章
            print("\n📄 步骤1: 爬取博客文章")
            articles = self.scrape_articles(max_pages, force_refresh)
            print(f"✅ 成功获取 {len(articles)} 篇文章")
            
            # 步骤2: 生成月度总结
            print("\n🤖 步骤2: 生成AI月度总结")
            summaries = self.generate_summaries(articles, force_refresh)
            print(f"✅ 成功生成 {len(summaries)} 个月份的总结")
            
            # 步骤3: 生成作品集网站
            print("\n🌐 步骤3: 生成作品集网站")
            output_dir = self.generate_portfolio(articles, summaries)
            print(f"✅ 作品集网站已生成到: {output_dir}")
            
            # 显示统计信息
            self._show_statistics(articles, summaries)
            
            # 显示使用说明
            self._show_usage_instructions(output_dir)
            
            return True
            
        except Exception as e:
            print(f"❌ 生成过程中出现错误: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _show_statistics(self, articles, summaries):
        """显示统计信息"""
        total_reads = sum(article.get('read_count', 0) for article in articles)
        total_likes = sum(article.get('like_count', 0) for article in articles)
        total_comments = sum(article.get('comment_count', 0) for article in articles)
        
        print("\n📊 博客统计信息:")
        print(f"   • 总文章数: {len(articles)}")
        print(f"   • 总阅读量: {total_reads:,}")
        print(f"   • 总点赞数: {total_likes:,}")
        print(f"   • 总评论数: {total_comments:,}")
        print(f"   • 活跃月份: {len(summaries)}")
        
        if articles:
            avg_reads = total_reads // len(articles)
            print(f"   • 平均阅读量: {avg_reads}")
    
    def _show_usage_instructions(self, output_dir):
        """显示使用说明"""
        print("\n🎉 作品集生成完成！")
        print("\n📝 使用说明:")
        print(f"   1. 打开文件夹: {os.path.abspath(output_dir)}")
        print("   2. 双击 index.html 在浏览器中查看")
        print("   3. 或使用本地服务器:")
        print(f"      cd {output_dir}")
        print("      python -m http.server 8000")
        print("      然后访问: http://localhost:8000")
        
        print("\n🔄 更新说明:")
        print("   • 要更新数据，请使用 --force-refresh 参数重新运行")
        print("   • 要只更新总结，请删除 monthly_summaries.json 后重新运行")
        
        print(f"\n⚙️ 配置文件: config.py")
        print(f"   • 如需使用AI总结功能，请在 .env 文件中设置 OPENAI_API_KEY")

def main():
    parser = argparse.ArgumentParser(
        description="CSDN博客作品集生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s                          # 生成完整作品集
  %(prog)s --max-pages 10           # 只爬取前10页文章
  %(prog)s --force-refresh          # 强制重新爬取和生成
  %(prog)s --scrape-only            # 只爬取文章，不生成网站
  %(prog)s --generate-only          # 只生成网站（需要已有数据）
        """
    )
    
    parser.add_argument(
        '--max-pages', 
        type=int, 
        help='最大爬取页数（默认爬取所有页面）'
    )
    
    parser.add_argument(
        '--force-refresh', 
        action='store_true',
        help='强制重新爬取文章和生成总结'
    )
    
    parser.add_argument(
        '--scrape-only', 
        action='store_true',
        help='只爬取文章，不生成网站和总结'
    )
    
    parser.add_argument(
        '--generate-only', 
        action='store_true',
        help='只生成网站，使用已有的文章和总结数据'
    )
    
    parser.add_argument(
        '--no-ai', 
        action='store_true',
        help='不使用AI生成总结，只生成基础统计'
    )
    
    parser.add_argument(
        '--use-smart-scraper', 
        action='store_true',
        help='使用智能爬虫（推荐，能更好地处理反爬虫机制）'
    )
    
    args = parser.parse_args()
    
    # 创建主应用实例
    app = CSDBlogPortfolio()
    
    try:
        if args.scrape_only:
            # 只爬取文章
            articles = app.scrape_articles(args.max_pages, args.force_refresh)
            print(f"✅ 文章爬取完成，共获取 {len(articles)} 篇文章")
            
        elif args.generate_only:
            # 只生成网站
            if not os.path.exists('articles.json'):
                print("❌ 未找到文章数据，请先运行爬虫")
                return 1
            
            with open('articles.json', 'r', encoding='utf-8') as f:
                articles = json.load(f)
            
            summaries = {}
            if os.path.exists('monthly_summaries.json'):
                with open('monthly_summaries.json', 'r', encoding='utf-8') as f:
                    summaries = json.load(f)
            
            app.generate_portfolio(articles, summaries)
            print("✅ 作品集网站生成完成")
            
        else:
            # 运行完整流程
            success = app.run_full_pipeline(args.max_pages, args.force_refresh)
            return 0 if success else 1
    
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断操作")
        return 1
    except Exception as e:
        print(f"❌ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
