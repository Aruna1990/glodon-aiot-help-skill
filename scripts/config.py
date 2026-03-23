#!/usr/bin/env python3
"""
统一配置管理

集中管理所有学习脚本的配置信息，避免重复代码
"""

import os
from pathlib import Path

# 技能根目录
SKILL_DIR = Path(__file__).resolve().parent.parent
# 知识库目录（技能目录内）
KNOWLEDGE_DIR = SKILL_DIR / "knowledge"

# ==================== 行业 AI 平台文档 ====================
class IndustryAIPlatform:
    """行业 AI 平台文档配置"""
    BASE_URL = "https://glodon-cv-help.yuque.com/cuv0se/ol9231"
    API_BASE = "https://glodon-cv-help.yuque.com/api"
    BOOK_ID = "41611578"
    OUTPUT_DIR = KNOWLEDGE_DIR
    
    # 核心文档列表
    CORE_DOCS = [
        {"slug": "yck25gn683z3wa2f", "title": "平台介绍"},
        {"slug": "lpetkzefs5er4q5x", "title": "平台使用常见问题汇总"},
        {"slug": "ku9i5oea97ynfzt4", "title": "平台认证 Token 说明文档"},
        {"slug": "tl0hylbi1hm61mu3", "title": "Key Secret 认证获取 Token"},
        {"slug": "etgvtorzglntmv39", "title": "API 调用"},
        {"slug": "thkdpzvfc9lffg7g", "title": "执行对话接口说明文档"},
        {"slug": "ku8iulvfl3e9sghk", "title": "服务 API 调用"},
        {"slug": "xcrcis1brhczo6ei", "title": "Prompt 工程"},
        {"slug": "cw6wurwnygkv1nne", "title": "知识库"},
        {"slug": "hhgfdznfypkcz0t1", "title": "数据管理"},
    ]


# ==================== AIoT 平台对接文档 ====================
class AIoTPlatform:
    """AIoT 平台对接文档配置"""
    BASE_URL = "https://glodon-cv-help.yuque.com/lzh2bp/gwam63"
    API_BASE = "https://glodon-cv-help.yuque.com/api"
    BOOK_ID = "29345082"
    OUTPUT_DIR = KNOWLEDGE_DIR / "02-aiot-platform"
    
    # 核心文档列表
    CORE_DOCS = [
        {"slug": "tt25tc", "title": "Glodon AIoT 产品系统 API 接入文档", "public": True},
        {"slug": "kqg83f", "title": "身份认证", "public": False},
        {"slug": "pzx9r2", "title": "获取 Access Token", "public": False},
        {"slug": "m7h4n1", "title": "API 调用规范", "public": False},
    ]


# ==================== NPM SDK 文档 ====================
class NPMSDK:
    """NPM SDK 文档配置"""
    OUTPUT_DIR = KNOWLEDGE_DIR / "03-coze-studio" / "sdk"
    
    # SDK 包列表
    PACKAGES = [
        {
            "name": "@glodon-aiot/chat-app-sdk",
            "npm_url": "https://www.npmjs.com/package/@glodon-aiot/chat-app-sdk",
            "registry_url": "https://registry.npmjs.org/@glodon-aiot/chat-app-sdk",
            "description": "Coze Studio 前端 SDK（新版）"
        },
        {
            "name": "@glodon-aiot/bot-client-ui",
            "npm_url": "https://www.npmjs.com/package/@glodon-aiot/bot-client-ui",
            "registry_url": "https://registry.npmjs.org/@glodon-aiot/bot-client-ui",
            "description": "旧版 SDK（已废弃）"
        }
    ]


# ==================== 通用配置 ====================
class Common:
    """通用配置"""
    # User-Agent
    USER_AGENT = "Mozilla/5.0 (compatible; GlodonAIHelp/1.7; +https://glodon-cv-help.yuque.com)"
    
    # 请求超时（秒）
    REQUEST_TIMEOUT = 30
    
    # 学习状态文件
    STATE_FILE = KNOWLEDGE_DIR / ".learn_state.json"
    
    # 文档来源清单
    DOCUMENT_SOURCES_FILE = KNOWLEDGE_DIR / "00-DOCUMENT-SOURCES.md"
