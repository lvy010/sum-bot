# 使用说明

## 🎉 项目测试成功！

你的CSDN博客作品集生成器已经成功运行并生成了精美的作品集网站。

## 📊 测试结果

✅ **依赖安装**: 成功安装所有必要依赖包  
✅ **爬虫功能**: 基础功能正常（注：CSDN有反爬限制，已用测试数据验证）  
✅ **AI总结功能**: 正常运行（支持无API密钥的简单统计总结）  
✅ **网页生成**: 成功生成3个精美页面  
✅ **本地服务器**: 已启动在端口8000  

## 🌐 查看作品集

作品集已生成到 `portfolio/` 目录，包含以下页面：

- **index.html** - 精美的首页，展示统计数据和热门文章
- **articles.html** - 文章列表页，支持搜索和筛选
- **summaries.html** - 月度总结页，展示AI生成的总结

### 访问方式

1. **本地文件访问**: 直接双击 `portfolio/index.html`
2. **本地服务器**: 访问 http://localhost:8000 （服务器已启动）
3. **命令行启动服务器**:
   ```bash
   cd portfolio
   python -m http.server 8000
   ```

## 🚀 实际使用

### 爬取真实CSDN数据

```bash
# 爬取所有文章（可能遇到反爬限制）
python main.py

# 爬取前5页文章
python main.py --max-pages 5

# 强制重新爬取
python main.py --force-refresh
```

### 只生成网站

```bash
# 使用已有数据生成网站
python main.py --generate-only
```

### 只爬取文章

```bash
# 只爬取文章，不生成网站
python main.py --scrape-only --max-pages 10
```

## ⚙️ 配置AI总结

如果你想使用AI生成更智能的月度总结：

1. 创建 `.env` 文件：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，添加你的OpenAI API密钥：
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. 重新生成总结：
   ```bash
   rm monthly_summaries.json
   python main.py --generate-only
   ```

## 📁 项目结构

```
sum-bot/
├── main.py              # 主程序
├── csdn_scraper.py      # CSDN爬虫
├── ai_summarizer.py     # AI总结生成器
├── portfolio_generator.py # 网页生成器
├── config.py            # 配置文件
├── test_data.py         # 测试数据生成器
├── templates/           # HTML模板
│   ├── base.html
│   ├── index.html
│   ├── articles.html
│   └── summaries.html
├── portfolio/           # 生成的作品集
├── articles.json        # 文章数据
└── monthly_summaries.json # 月度总结数据
```

## 🛠️ 自定义配置

编辑 `config.py` 文件可以修改：

- CSDN用户ID
- 输出目录
- 爬虫参数
- API配置

## 🔄 更新数据

- 要更新文章数据，使用 `--force-refresh` 参数
- 要只更新总结，删除 `monthly_summaries.json` 后重新运行
- 生成的网站会自动显示最新的统计数据

## 🎨 网站特色

- 📱 响应式设计，支持手机和桌面浏览
- 🎯 精美的统计图表和数据可视化
- 🔍 文章搜索和分类筛选
- 📈 AI生成的月度总结报告
- 🌈 现代化的UI设计，使用Bootstrap 5

## 📞 问题反馈

如果遇到任何问题，请检查：

1. 网络连接是否正常
2. Python依赖是否正确安装
3. CSDN是否有访问限制
4. API密钥是否正确配置

享受你的技术作品集吧！🎉
