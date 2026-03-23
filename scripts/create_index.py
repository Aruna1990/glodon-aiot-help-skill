#!/usr/bin/env python3
"""
语雀公开文档索引生成器
无需 Cookie，整理文档目录和链接
"""

import os
import json
from datetime import datetime

# 配置
BASE_URL = "https://glodon-cv-help.yuque.com/cuv0se/ol9231"
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge")

# 完整文档列表（59 篇）
ALL_DOCS = [
    # L0 - 平台入门
    {"slug": "yck25gn683z3wa2f", "title": "平台介绍", "level": 0, "category": "platform"},
    {"slug": "lpetkzefs5er4q5x", "title": "平台使用常见问题汇总", "level": 0, "category": "faq"},
    {"slug": "bwec6xi60uy9xkgo", "title": "平台更新记录", "level": 0, "category": "platform"},
    {"slug": "gnkvf1e12n27uppo", "title": "用户投诉举报处理系统", "level": 0, "category": "faq"},
    
    # L1 - 核心功能
    {"slug": "ouwzx8mgo63oboqg", "title": "行业 AI 模型", "level": 1, "category": "models"},
    {"slug": "bgmy2qkoqqk7whtq", "title": "AI 开发解决方案", "level": 1, "category": "solutions"},
    {"slug": "pqywkrbbk5x33c3b", "title": "基于基础数据构建简易 AI 助手", "level": 1, "category": "solutions"},
    {"slug": "guubsghryq8ub50h", "title": "基于结构化数据构建专家级 AI 助手", "level": 1, "category": "solutions"},
    {"slug": "krwnxgcybudy9ezg", "title": "如何评估 AI 助手的回答效果", "level": 1, "category": "evaluation"},
    {"slug": "txtyvrkagu3rd5af", "title": "AI 评标", "level": 1, "category": "solutions"},
    {"slug": "oeew9h8zliycqw7n", "title": "RAG 检索", "level": 1, "category": "knowledge"},
    {"slug": "hhgfdznfypkcz0t1", "title": "数据管理", "level": 1, "category": "knowledge"},
    {"slug": "pdo7imfg1lz43pap", "title": "模型精调", "level": 1, "category": "models"},
    {"slug": "cw6wurwnygkv1nne", "title": "知识库", "level": 1, "category": "knowledge"},
    {"slug": "mwhq7ogvirgkxp0l", "title": "知识库 API 对接文档", "level": 1, "category": "api"},
    {"slug": "caz83r4dkqw6vf5n", "title": "知识增强使用示例", "level": 1, "category": "knowledge"},
    {"slug": "xcrcis1brhczo6ei", "title": "Prompt 工程", "level": 1, "category": "prompt"},
    {"slug": "drznpftt901w3v5x", "title": "Prompt 模板", "level": 1, "category": "prompt"},
    {"slug": "empb7s1d9xaqyiko", "title": "prompt 样例库", "level": 1, "category": "prompt"},
    {"slug": "ei3ulfz03fv29148", "title": "应用对接", "level": 1, "category": "integration"},
    {"slug": "eobw4zqaky1c0dfg", "title": "应用集成", "level": 1, "category": "integration"},
    {"slug": "og2xis3p4aiggei3", "title": "插件管理", "level": 1, "category": "integration"},
    {"slug": "clcft0airk91f10q", "title": "coze studio", "level": 1, "category": "coze"},
    {"slug": "qr3laxwrxdosggc0", "title": "服务管理", "level": 1, "category": "api"},
    {"slug": "ku8iulvfl3e9sghk", "title": "服务 API 调用", "level": 1, "category": "api"},
    {"slug": "kdh2eggww4g1hb1s", "title": "调用统计", "level": 1, "category": "evaluation"},
    {"slug": "vchachdl95z8t7vl", "title": "LLM 生成评估", "level": 1, "category": "evaluation"},
    {"slug": "kccxr46vwdzo2g1a", "title": "知识检索评估", "level": 1, "category": "evaluation"},
    {"slug": "ku9i5oea97ynfzt4", "title": "平台认证 Token 说明文档", "level": 1, "category": "api"},
    {"slug": "tl0hylbi1hm61mu3", "title": "Key Secret 认证获取 Token", "level": 1, "category": "api"},
    
    # L2 - API 参考
    {"slug": "zgrpcamswepxgx47", "title": "工作流介绍", "level": 2, "category": "workflow"},
    {"slug": "qk98qatafge4zg9c", "title": "工作流构建", "level": 2, "category": "workflow"},
    {"slug": "etgvtorzglntmv39", "title": "API 调用", "level": 2, "category": "api"},
    {"slug": "aqondvmlgonuwl4g", "title": "Coze Studio 介绍", "level": 2, "category": "coze"},
    {"slug": "ecgfg25v3m5qk6nn", "title": "平台 Coze API 调用说明文档", "level": 2, "category": "coze"},
    {"slug": "thkdpzvfc9lffg7g", "title": "执行对话接口说明文档", "level": 2, "category": "api"},
    {"slug": "ydb3zwmy25oi4stq", "title": "yolo 评测", "level": 2, "category": "models"},
    {"slug": "ubzota0grvd9bbgy", "title": "OCR 检测 - 模式一", "level": 2, "category": "api"},
    {"slug": "hzbyt6vw97uglzu6", "title": "物体检测 - 模式一", "level": 2, "category": "api"},
    {"slug": "gnzn6e0mfy0iu4yi", "title": "物体检测 (std_layout)", "level": 2, "category": "api"},
    {"slug": "kl0ubv7tbgmqdhdf", "title": "图像分类 (img-cls)", "level": 2, "category": "api"},
    {"slug": "pybzps3xn6e4aw84", "title": "OCR 文本检测 (std_ocr_det)", "level": 2, "category": "api"},
    {"slug": "rgwg5gpqgo0mwdwh", "title": "OCR 文本分类 (std_ocr_cls)", "level": 2, "category": "api"},
    {"slug": "qtrdxuct1m9xmsem", "title": "OCR 文本识别 (std_ocr_rec)", "level": 2, "category": "api"},
    {"slug": "xc4cb74yd7le9y5y", "title": "有线表格识别 (bded-rec)", "level": 2, "category": "api"},
    {"slug": "ousq9u4rvr2o0nny", "title": "无线表格检测 (bdss-det)", "level": 2, "category": "api"},
    {"slug": "rony9ozk5zgrpr7h", "title": "无线表格识别 (bdss-rec)", "level": 2, "category": "api"},
    {"slug": "nhiqsgqg3q8agf56", "title": "印章去除 (ocr-stamp)", "level": 2, "category": "api"},
    {"slug": "xmmty1ige5rlltik", "title": "OCR 表格识别 (ocr-tab)", "level": 2, "category": "api"},
    {"slug": "gxisin2x8thxrtyr", "title": "OCR 公式识别 (formula-rec)", "level": 2, "category": "api"},
    {"slug": "gx9pc2lcin2e4tpl", "title": "水印去除 (ocr-watermark)", "level": 2, "category": "api"},
    {"slug": "wbz9fcq2neoscyhx", "title": "文本向量化 (embedding)", "level": 2, "category": "api"},
    {"slug": "isfh3b8uv6w1vyd3", "title": "文本重排序 (rerank)", "level": 2, "category": "api"},
    {"slug": "hgaeepgyz3eo4aa2", "title": "CAD 转图片 (cad_to_image)", "level": 2, "category": "api"},
    {"slug": "dbxiu8h799o37kez", "title": "大模型 (llm)", "level": 2, "category": "api"},
    {"slug": "gn4gig7iy7656gxz", "title": "AecDataIO-W101_v2", "level": 2, "category": "api"},
    {"slug": "tpwu4156wdu87m7g", "title": "AecDataIO-W101_v1", "level": 2, "category": "api"},
    {"slug": "esunsvy5pu5zlrrx", "title": "AecDataIO-W101", "level": 2, "category": "api"},
    {"slug": "nv9xb3gs2qicwt8g", "title": "OCR 文本检测 (PPOCR_v5)", "level": 2, "category": "api"},
]

# 分类说明
CATEGORIES = {
    "platform": "平台介绍",
    "faq": "常见问题",
    "models": "模型服务",
    "solutions": "解决方案",
    "knowledge": "知识库",
    "prompt": "Prompt 工程",
    "api": "API 参考",
    "integration": "应用集成",
    "workflow": "工作流",
    "coze": "Coze Studio",
    "evaluation": "评估中心",
}


def create_index_files():
    """创建索引文件"""
    print("=" * 60)
    print("📚 语雀公开文档索引生成")
    print("=" * 60)
    print("知识库：" + BASE_URL)
    print("输出目录：" + KNOWLEDGE_DIR)
    print("文档数量：" + str(len(ALL_DOCS)) + " 篇")
    print("=" * 60)
    print()
    
    # 按分类整理
    by_category = {}
    for doc in ALL_DOCS:
        cat = doc["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(doc)
    
    # 生成主索引
    index_content = "# 📚 广联达行业 AI 平台 - 文档索引\n\n"
    index_content += "> 知识库：" + BASE_URL + "\n"
    index_content += "> 生成时间：" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n"
    index_content += "> 文档总数：" + str(len(ALL_DOCS)) + " 篇\n\n"
    index_content += "---\n\n"
    
    # 按分类列出
    for cat, docs in sorted(by_category.items()):
        cat_name = CATEGORIES.get(cat, cat)
        index_content += "## " + cat_name + " (" + str(len(docs)) + ")\n\n"
        index_content += "| # | 标题 | Slug | 层级 |\n"
        index_content += "|---|------|------|------|\n"
        
        for i, doc in enumerate(docs, 1):
            url = BASE_URL + "/" + doc["slug"]
            index_content += "| " + str(i) + " | [" + doc["title"] + "](" + url + ") | `" + doc["slug"] + "` | L" + str(doc["level"]) + " |\n"
        
        index_content += "\n"
    
    # 保存主索引
    index_file = os.path.join(KNOWLEDGE_DIR, "INDEX.md")
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print("✓ 主索引：" + index_file)
    
    # 生成 JSON 索引
    json_file = os.path.join(KNOWLEDGE_DIR, "docs_index.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            "base_url": BASE_URL,
            "generated_at": datetime.now().isoformat(),
            "total_docs": len(ALL_DOCS),
            "categories": CATEGORIES,
            "documents": ALL_DOCS
        }, f, ensure_ascii=False, indent=2)
    
    print("✓ JSON 索引：" + json_file)
    
    # 为每个文档创建快捷访问文件
    print("\n📄 生成文档快捷访问...")
    for doc in ALL_DOCS:
        url = BASE_URL + "/" + doc["slug"]
        doc_file = os.path.join(KNOWLEDGE_DIR, doc["slug"] + ".md")
        
        # 如果文件已存在且有内容，跳过
        if os.path.exists(doc_file):
            file_size = os.path.getsize(doc_file)
            if file_size > 500:  # 已有内容
                continue
        
        content = "# " + doc["title"] + "\n\n"
        content += "> 📖 **在线查看**: " + url + "\n\n"
        content += "---\n\n"
        content += "## 文档信息\n\n"
        content += "- **分类**: " + CATEGORIES.get(doc["category"], doc["category"]) + "\n"
        content += "- **层级**: L" + str(doc["level"]) + "\n"
        content += "- **Slug**: `" + doc["slug"] + "`\n"
        content += "- **URL**: " + url + "\n"
        content += "\n---\n\n"
        content += "*点击上方链接在语雀中查看完整内容*\n"
        
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("✓ 已生成 " + str(len(ALL_DOCS)) + " 篇文档快捷访问")
    
    # 生成 README
    readme = "# 📚 广联达行业 AI 平台知识库\n\n"
    readme += "## 快速访问\n\n"
    readme += "- **知识库首页**: " + BASE_URL + "\n"
    readme += "- **文档索引**: [INDEX.md](./INDEX.md)\n"
    readme += "- **JSON 索引**: [docs_index.json](./docs_index.json)\n\n"
    readme += "## 分类导航\n\n"
    
    for cat, name in sorted(CATEGORIES.items()):
        count = len(by_category.get(cat, []))
        readme += "- **" + name + "**: " + str(count) + " 篇\n"
    
    readme += "\n## 使用说明\n\n"
    readme += "1. 打开 [INDEX.md](./INDEX.md) 浏览所有文档\n"
    readme += "2. 点击文档链接在语雀中查看完整内容\n"
    readme += "3. 或使用 `docs_index.json` 进行程序化访问\n\n"
    readme += "---\n\n"
    readme += "*索引生成时间*: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n"
    
    readme_file = os.path.join(KNOWLEDGE_DIR, "README.md")
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print("✓ README：" + readme_file)
    
    print("\n" + "=" * 60)
    print("✅ 索引生成完成！")
    print("=" * 60)
    print("\n📊 统计:")
    print("   文档总数：" + str(len(ALL_DOCS)) + " 篇")
    print("   分类数量：" + str(len(CATEGORIES)) + " 个")
    print("   索引文件：3 个")
    print("\n📁 文件:")
    print("   - knowledge/INDEX.md (主索引)")
    print("   - knowledge/docs_index.json (JSON 索引)")
    print("   - knowledge/README.md (使用说明)")
    print("   - knowledge/*.md (文档快捷访问)")
    print("\n🔗 访问方式:")
    print("   1. 打开 INDEX.md 浏览所有文档")
    print("   2. 点击链接在语雀查看完整内容")
    print("=" * 60)


if __name__ == "__main__":
    create_index_files()
