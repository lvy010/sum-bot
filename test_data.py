#!/usr/bin/env python3
"""
生成测试数据用于验证作品集生成功能
"""

import json
from datetime import datetime, timedelta

def generate_test_articles():
    """生成测试文章数据"""
    base_date = datetime(2025, 7, 1)
    
    articles = []
    
    # 模拟文章数据
    test_articles_data = [
        {
            "title": "[rStar] 解决方案节点 | BaseNode | MCTSNode",
            "content": "解决方案节点存储部分解决方案、行动、观察结果和评估。它们形成树状结构，使rStar能够探索多条路径并跟踪其进展。BaseNode提供核心结构，而MCTSNode为蒙特卡洛树搜索的学习过程添加了专用字段。",
            "read_count": 1026,
            "like_count": 33,
            "comment_count": 0,
            "days_offset": 0
        },
        {
            "title": "[rStar] 策略与奖励大语言模型",
            "content": "策略模型充当创意头脑风暴引擎，提出多样化的下一步。奖励模型充当严格裁判，用数值分数评估这些步骤的质量。这两个大语言模型与求解协调器协同工作。",
            "read_count": 1044,
            "like_count": 13,
            "comment_count": 0,
            "days_offset": 1
        },
        {
            "title": "[code-review] Probot应用核心 | 审查协调器",
            "content": "使用Probot框架监听GitHub事件，处理context信息，然后协调一系列操作：初始化AI通信器、获取代码变更、应用过滤规则、将代码发送给AI审查。",
            "read_count": 740,
            "like_count": 14,
            "comment_count": 0,
            "days_offset": 3
        },
        {
            "title": "[AI框架] TensorFlow模型优化实战",
            "content": "深入探讨TensorFlow模型优化技术，包括量化、剪枝、蒸馏等方法。通过实际案例展示如何将模型大小减少80%同时保持95%的准确率。",
            "read_count": 2156,
            "like_count": 67,
            "comment_count": 12,
            "days_offset": 10
        },
        {
            "title": "[算法] 动态规划经典问题解析",
            "content": "系统梳理动态规划的核心思想和解题模板，通过背包问题、最长公共子序列等经典题目，掌握DP的状态转移方程设计。",
            "read_count": 1834,
            "like_count": 45,
            "comment_count": 8,
            "days_offset": 15
        },
        {
            "title": "[Docker] 容器化部署最佳实践",
            "content": "从Docker基础到生产环境部署，涵盖镜像优化、多阶段构建、健康检查、日志管理等关键技术点。",
            "read_count": 1567,
            "like_count": 38,
            "comment_count": 5,
            "days_offset": 20
        },
        {
            "title": "[Python] 异步编程深度解析",
            "content": "详细介绍Python异步编程的核心概念，包括asyncio、协程、事件循环等，通过实际项目展示异步编程的威力。",
            "read_count": 2890,
            "like_count": 89,
            "comment_count": 23,
            "days_offset": 25
        },
        {
            "title": "[系统设计] 分布式缓存架构设计",
            "content": "深入分析Redis集群、一致性哈希、缓存雪崩等关键技术，设计高可用的分布式缓存系统。",
            "read_count": 3245,
            "like_count": 112,
            "comment_count": 34,
            "days_offset": 30
        },
        {
            "title": "[机器学习] 特征工程实战指南",
            "content": "从数据预处理到特征选择，全面介绍机器学习项目中的特征工程技术，提升模型性能的关键步骤。",
            "read_count": 1923,
            "like_count": 56,
            "comment_count": 15,
            "days_offset": 35
        },
        {
            "title": "[Web开发] React Hooks最佳实践",
            "content": "深入理解React Hooks的工作原理，通过实际案例展示useState、useEffect、自定义Hook等的正确用法。",
            "read_count": 2678,
            "like_count": 78,
            "comment_count": 19,
            "days_offset": 40
        },
        {
            "title": "[数据库] MySQL性能优化全攻略",
            "content": "从索引设计到查询优化，从配置调优到架构设计，全方位提升MySQL数据库性能。",
            "read_count": 4123,
            "like_count": 134,
            "comment_count": 45,
            "days_offset": 45
        },
        {
            "title": "[云原生] Kubernetes实战部署",
            "content": "从Pod到Service，从Deployment到Ingress，系统学习Kubernetes的核心概念和实际应用。",
            "read_count": 1789,
            "like_count": 42,
            "comment_count": 11,
            "days_offset": 50
        }
    ]
    
    for i, article_data in enumerate(test_articles_data):
        article_date = base_date + timedelta(days=article_data["days_offset"])
        
        article = {
            "title": article_data["title"],
            "url": f"https://blog.csdn.net/2301_80171004/article/details/{12345678 + i}",
            "publish_time": article_date.strftime("%Y-%m-%d"),
            "read_count": article_data["read_count"],
            "like_count": article_data["like_count"],
            "comment_count": article_data["comment_count"],
            "content": article_data["content"]
        }
        
        articles.append(article)
    
    return articles

def save_test_data():
    """保存测试数据到文件"""
    articles = generate_test_articles()
    
    # 保存文章数据
    with open('articles.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已生成 {len(articles)} 篇测试文章数据")
    print("📁 数据已保存到 articles.json")
    
    return articles

if __name__ == "__main__":
    save_test_data()
