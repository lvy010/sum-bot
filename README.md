# CSDN博客作品集生成器

🚀 自动爬取你的CSDN博客文章，使用AI生成月度总结，并创建精美的个人作品集网站！

## ✨ 功能特点

- 📄 **智能爬取**: 自动爬取CSDN博客的所有文章，包括标题、内容、统计数据等
- 🤖 **AI总结**: 使用OpenAI GPT生成专业的月度技术总结和分析
- 🎨 **精美界面**: 现代化响应式设计，支持移动端访问
- 📊 **数据分析**: 详细的博客统计和技术标签分析
- 🔄 **自动化**: 一键运行，自动完成整个作品集生成流程

## 🛠️ 安装配置

### 1. 环境要求

- Python 3.7+
- 网络连接

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置设置

复制环境变量模板：
```bash
cp .env.example .env
```

编辑 `.env` 文件，添加你的OpenAI API密钥（可选）：
```env
OPENAI_API_KEY=your_openai_api_key_here
```

> 📝 如果不设置API密钥，系统会生成基础的统计总结

### 4. 修改配置

编辑 `config.py` 文件，修改你的CSDN用户ID：
```python
CSDN_USER_ID = "your_csdn_user_id"  # 将 2301_80171004 改为你的用户ID
```

## 🚀 使用方法

### 快速开始

生成完整的博客作品集：
```bash
python main.py
```

### 高级选项

```bash
# 只爬取前10页文章
python main.py --max-pages 10

# 强制重新爬取所有数据
python main.py --force-refresh

# 只爬取文章，不生成网站
python main.py --scrape-only

# 只生成网站（需要已有数据）
python main.py --generate-only

# 查看所有选项
python main.py --help
```

### 分步骤运行

如果你想分步骤执行，可以单独运行各个模块：

```bash
# 1. 爬取文章
python csdn_scraper.py

# 2. 生成月度总结
python ai_summarizer.py

# 3. 生成作品集网站
python portfolio_generator.py
```

## 📁 项目结构

```
sum-bot/
├── main.py                 # 主程序入口
├── config.py              # 配置文件
├── csdn_scraper.py        # CSDN爬虫模块
├── ai_summarizer.py       # AI总结生成模块
├── portfolio_generator.py # 网站生成模块
├── requirements.txt       # 依赖包列表
├── .env.example          # 环境变量模板
├── templates/            # HTML模板文件夹
│   ├── base.html         # 基础模板
│   ├── index.html        # 首页模板
│   ├── articles.html     # 文章列表模板
│   └── summaries.html    # 月度总结模板
└── portfolio/            # 生成的作品集网站（运行后创建）
    ├── index.html        # 网站首页
    ├── articles.html     # 文章列表页
    └── summaries.html    # 月度总结页
```

## 🎯 生成的作品集包含

### 📊 首页特色
- 个人技术统计概览
- 热门文章展示
- 最新文章列表
- 技术标签云
- 月度发文统计

### 📝 文章列表页
- 所有文章的完整列表
- 按时间/热度排序
- 文章搜索功能
- 月份筛选
- 详细统计信息

### 🤖 月度总结页
- AI生成的专业月度分析
- 技术成长轨迹
- 核心主题提取
- 热门文章统计
- 下月技术展望

## 🔧 自定义配置

### 修改爬虫设置

在 `config.py` 中可以调整：
- 请求延迟时间
- 每页文章数量
- 用户代理字符串
- 输出目录路径

### 自定义网站样式

模板文件位于 `templates/` 目录，你可以：
- 修改 `base.html` 调整整体布局
- 编辑CSS样式自定义外观
- 添加新的页面模板

### AI总结提示词

在 `ai_summarizer.py` 中可以修改AI总结的提示词，定制总结风格和内容重点。

## 📈 使用场景

- 🎓 **求职简历**: 展示你的技术博客作品集
- 📚 **学习记录**: 回顾自己的技术成长历程
- 🔍 **内容分析**: 了解自己的写作主题和趋势
- 🌐 **个人网站**: 创建专业的个人技术展示页面
- 📊 **数据统计**: 分析博客的阅读和互动数据

## ⚠️ 注意事项

1. **爬虫礼仪**: 程序已设置合理的请求延迟，请勿频繁运行
2. **API限制**: OpenAI API有使用限制和费用，请合理使用
3. **数据缓存**: 程序会缓存数据，避免重复爬取
4. **网络环境**: 确保网络连接稳定，部分地区可能需要代理

## 🔄 更新数据

- 使用 `--force-refresh` 参数重新爬取最新文章
- 删除 `articles.json` 文件重新爬取文章数据  
- 删除 `monthly_summaries.json` 文件重新生成AI总结

## 📞 技术支持

如果遇到问题，请检查：

1. **网络连接**: 确保能正常访问CSDN
2. **Python版本**: 需要Python 3.7+
3. **依赖包**: 运行 `pip install -r requirements.txt`
4. **配置文件**: 检查 `config.py` 中的用户ID设置
5. **权限问题**: 确保有文件写入权限

## 🎉 开始使用

现在就开始创建你的专属技术博客作品集吧！

```bash
python main.py
```

生成完成后，打开 `portfolio/index.html` 在浏览器中查看你的作品集。

---

**作者**: lvy-  
**项目**: CSDN博客作品集生成器  
**技术栈**: Python, Jinja2, Bootstrap, OpenAI API