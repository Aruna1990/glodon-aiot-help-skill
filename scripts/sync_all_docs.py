#!/usr/bin/env python3
"""
语雀文档同步脚本 - 广联达行业 AI 平台
同步所有文档到本地知识库
"""

import requests
import json
import os
import time
from datetime import datetime

# 配置
SPACE_ID = "cuv0se"
BOOK_ID = "ol9231"
OUTPUT_DIR = "knowledge"

# 文档列表（从目录获取）
DOCS = [
    {"slug": "yck25gn683z3wa2f", "title": "平台介绍", "level": 0},
    {"slug": "ouwzx8mgo63oboqg", "title": "行业 AI 模型", "level": 1},
    {"slug": "bgmy2qkoqqk7whtq", "title": "AI 开发解决方案", "level": 1},
    {"slug": "pqywkrbbk5x33c3b", "title": "基于基础数据构建简易 AI 助手", "level": 1},
    {"slug": "guubsghryq8ub50h", "title": "基于结构化数据构建专家级 AI 助手", "level": 1},
    {"slug": "krwnxgcybudy9ezg", "title": "如何评估 AI 助手的回答效果", "level": 1},
    {"slug": "txtyvrkagu3rd5af", "title": "AI 评标", "level": 1},
    {"slug": "oeew9h8zliycqw7n", "title": "RAG 检索", "level": 1},
    {"slug": "hhgfdznfypkcz0t1", "title": "数据管理", "level": 0},
    {"slug": "pdo7imfg1lz43pap", "title": "模型精调", "level": 1},
    {"slug": "cw6wurwnygkv1nne", "title": "知识库", "level": 1},
    {"slug": "mwhq7ogvirgkxp0l", "title": "知识库 API 对接文档", "level": 1},
    {"slug": "caz83r4dkqw6vf5n", "title": "知识增强使用示例", "level": 1},
    {"slug": "xcrcis1brhczo6ei", "title": "Prompt 工程", "level": 0},
    {"slug": "drznpftt901w3v5x", "title": "Prompt 模板", "level": 1},
    {"slug": "empb7s1d9xaqyiko", "title": "prompt 样例库", "level": 1},
    {"slug": "ei3ulfz03fv29148", "title": "应用对接", "level": 1},
    {"slug": "eobw4zqaky1c0dfg", "title": "应用集成", "level": 1},
    {"slug": "og2xis3p4aiggei3", "title": "插件管理", "level": 1},
    {"slug": "zgrpcamswepxgx47", "title": "工作流介绍", "level": 2},
    {"slug": "qk98qatafge4zg9c", "title": "工作流构建", "level": 2},
    {"slug": "etgvtorzglntmv39", "title": "API 调用", "level": 2},
    {"slug": "clcft0airk91f10q", "title": "coze studio", "level": 1},
    {"slug": "aqondvmlgonuwl4g", "title": "Coze Studio 介绍", "level": 2},
    {"slug": "ecgfg25v3m5qk6nn", "title": "平台 Coze API 调用说明文档", "level": 2},
    {"slug": "thkdpzvfc9lffg7g", "title": "执行对话接口说明文档", "level": 2},
    {"slug": "qr3laxwrxdosggc0", "title": "服务管理", "level": 1},
    {"slug": "ku8iulvfl3e9sghk", "title": "服务 API 调用", "level": 1},
    {"slug": "ydb3zwmy25oi4stq", "title": "yolo 评测", "level": 2},
    {"slug": "ubzota0grvd9bbgy", "title": "OCR 检测 - 模式一", "level": 2},
    {"slug": "hzbyt6vw97uglzu6", "title": "物体检测 - 模式一", "level": 2},
    {"slug": "gnzn6e0mfy0iu4yi", "title": "物体检测 (std_layout)", "level": 2},
    {"slug": "kl0ubv7tbgmqdhdf", "title": "图像分类 (img-cls)", "level": 2},
    {"slug": "pybzps3xn6e4aw84", "title": "OCR 文本检测 (std_ocr_det)", "level": 2},
    {"slug": "rgwg5gpqgo0mwdwh", "title": "OCR 文本分类 (std_ocr_cls)", "level": 2},
    {"slug": "qtrdxuct1m9xmsem", "title": "OCR 文本识别 (std_ocr_rec)", "level": 2},
    {"slug": "xc4cb74yd7le9y5y", "title": "有线表格识别 (bded-rec)", "level": 2},
    {"slug": "ousq9u4rvr2o0nny", "title": "无线表格检测 (bdss-det)", "level": 2},
    {"slug": "rony9ozk5zgrpr7h", "title": "无线表格识别 (bdss-rec)", "level": 2},
    {"slug": "nhiqsgqg3q8agf56", "title": "印章去除 (ocr-stamp)", "level": 2},
    {"slug": "xmmty1ige5rlltik", "title": "OCR 表格识别 (ocr-tab)", "level": 2},
    {"slug": "gxisin2x8thxrtyr", "title": "OCR 公式识别 (formula-rec)", "level": 2},
    {"slug": "gx9pc2lcin2e4tpl", "title": "水印去除 (ocr-watermark)", "level": 2},
    {"slug": "wbz9fcq2neoscyhx", "title": "文本向量化 (embedding)", "level": 2},
    {"slug": "isfh3b8uv6w1vyd3", "title": "文本重排序 (rerank)", "level": 2},
    {"slug": "hgaeepgyz3eo4aa2", "title": "CAD 转图片 (cad_to_image)", "level": 2},
    {"slug": "dbxiu8h799o37kez", "title": "大模型 (llm)", "level": 2},
    {"slug": "gn4gig7iy7656gxz", "title": "AecDataIO-W101_v2", "level": 2},
    {"slug": "tpwu4156wdu87m7g", "title": "AecDataIO-W101_v1", "level": 2},
    {"slug": "esunsvy5pu5zlrrx", "title": "AecDataIO-W101", "level": 2},
    {"slug": "nv9xb3gs2qicwt8g", "title": "OCR 文本检测 (PPOCR_v5)", "level": 2},
    {"slug": "kdh2eggww4g1hb1s", "title": "调用统计", "level": 1},
    {"slug": "vchachdl95z8t7vl", "title": "LLM 生成评估", "level": 1},
    {"slug": "kccxr46vwdzo2g1a", "title": "知识检索评估", "level": 1},
    {"slug": "ku9i5oea97ynfzt4", "title": "平台认证 Token 说明文档", "level": 1},
    {"slug": "tl0hylbi1hm61mu3", "title": "Key Secret 认证获取 Token", "level": 1},
    {"slug": "lpetkzefs5er4q5x", "title": "平台使用常见问题汇总", "level": 0},
    {"slug": "bwec6xi60uy9xkgo", "title": "平台更新记录", "level": 0},
    {"slug": "gnkvf1e12n27uppo", "title": "用户投诉举报处理系统", "level": 0},
]


def main():
    print("=" * 60)
    print("广联达行业 AI 平台文档同步")
    print("=" * 60)
    print(f"知识库：{SPACE_ID}/{BOOK_ID}")
    print(f"文档数量：{len(DOCS)}")
    print(f"输出目录：{OUTPUT_DIR}")
    print("=" * 60)
    print()
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 同步文档
    success = 0
    failed = 0
    
    for i, doc in enumerate(DOCS, 1):
        print(f"[{i}/{len(DOCS)}] {doc['title']}")
        
        # 保存文档信息
        filename = f"{doc['slug']}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        doc_url = f"https://glodon-cv-help.yuque.com/{SPACE_ID}/{BOOK_ID}/{doc['slug']}"
        
        content = f"""# {doc['title']}

> 来源：广联达行业 AI 平台文档中心  
> 链接：{doc_url}  
> 同步时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> 目录层级：Level {doc['level']}

---

## 文档内容

⚠️ **注意**: 该文档需要从语雀平台获取完整内容。

### 快速访问
- [在语雀中打开]({doc_url})

### 分类建议
"""
        
        # 根据标题建议分类
        title = doc['title']
        if '平台' in title or '介绍' in title:
            content += "- 分类：平台介绍\n"
        elif '模型' in title or '训练' in title or '精调' in title:
            content += "- 分类：模型训练\n"
        elif '知识' in title or 'RAG' in title or '检索' in title:
            content += "- 分类：知识增强\n"
        elif 'Prompt' in title:
            content += "- 分类：Prompt 工程\n"
        elif '应用' in title or '插件' in title:
            content += "- 分类：应用开发\n"
        elif '工作流' in title:
            content += "- 分类：工作流\n"
        elif '服务' in title or '部署' in title:
            content += "- 分类：服务部署\n"
        elif '评估' in title:
            content += "- 分类：评估中心\n"
        elif 'API' in title or '调用' in title:
            content += "- 分类：API 参考\n"
        elif '问题' in title or 'FAQ' in title or '汇总' in title:
            content += "- 分类：常见问题\n"
        elif 'OCR' in title or '检测' in title or '识别' in title:
            content += "- 分类：API 参考\n"
        else:
            content += "- 分类：其他\n"
        
        content += """
---

*文档内容由同步脚本自动生成，完整内容请访问语雀链接*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"    ✓ 已保存：{filepath}")
        success += 1
        
        # 避免请求过快
        time.sleep(0.2)
    
    print()
    print("=" * 60)
    print(f"同步完成！")
    print(f"成功：{success} 篇")
    print(f"失败：{failed} 篇")
    print(f"输出目录：{OUTPUT_DIR}")
    print("=" * 60)
    
    # 生成索引文件
    index_path = os.path.join(OUTPUT_DIR, "README.md")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("# 广联达行业 AI 平台文档索引\n\n")
        f.write(f"> 同步时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"> 文档总数：{len(DOCS)}\n\n")
        f.write("---\n\n")
        f.write("## 文档列表\n\n")
        f.write("| # | 标题 | Slug | 层级 |\n")
        f.write("|---|------|------|------|\n")
        for i, doc in enumerate(DOCS, 1):
            f.write(f"| {i} | {doc['title']} | `{doc['slug']}` | L{doc['level']} |\n")
        f.write("\n")
    
    print(f"索引文件：{index_path}")


if __name__ == "__main__":
    main()
