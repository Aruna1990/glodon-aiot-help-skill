#!/usr/bin/env python3
"""
广联达行业 AI 平台 - 智能问答机器人
基于语雀文档知识库，回答问题并提供文档链接
"""

import os
import json
import re
from datetime import datetime
from typing import List, Dict, Tuple

# 配置
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge")
FAQ_FILE = os.path.join(KNOWLEDGE_DIR, "faq.json")
INDEX_FILE = os.path.join(KNOWLEDGE_DIR, "README.md")

# 文档索引（从同步的文档中提取）
DOC_INDEX = {
    "yck25gn683z3wa2f": {"title": "平台介绍", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/yck25gn683z3wa2f"},
    "ouwzx8mgo63oboqg": {"title": "行业 AI 模型", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/ouwzx8mgo63oboqg"},
    "bgmy2qkoqqk7whtq": {"title": "AI 开发解决方案", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/bgmy2qkoqqk7whtq"},
    "pqywkrbbk5x33c3b": {"title": "基于基础数据构建简易 AI 助手", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/pqywkrbbk5x33c3b"},
    "guubsghryq8ub50h": {"title": "基于结构化数据构建专家级 AI 助手", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/guubsghryq8ub50h"},
    "krwnxgcybudy9ezg": {"title": "如何评估 AI 助手的回答效果", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/krwnxgcybudy9ezg"},
    "txtyvrkagu3rd5af": {"title": "AI 评标", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/txtyvrkagu3rd5af"},
    "oeew9h8zliycqw7n": {"title": "RAG 检索", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/oeew9h8zliycqw7n"},
    "hhgfdznfypkcz0t1": {"title": "数据管理", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/hhgfdznfypkcz0t1"},
    "pdo7imfg1lz43pap": {"title": "模型精调", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/pdo7imfg1lz43pap"},
    "cw6wurwnygkv1nne": {"title": "知识库", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/cw6wurwnygkv1nne"},
    "mwhq7ogvirgkxp0l": {"title": "知识库 API 对接文档", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/mwhq7ogvirgkxp0l"},
    "caz83r4dkqw6vf5n": {"title": "知识增强使用示例", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/caz83r4dkqw6vf5n"},
    "xcrcis1brhczo6ei": {"title": "Prompt 工程", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/xcrcis1brhczo6ei"},
    "drznpftt901w3v5x": {"title": "Prompt 模板", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/drznpftt901w3v5x"},
    "empb7s1d9xaqyiko": {"title": "prompt 样例库", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/empb7s1d9xaqyiko"},
    "ei3ulfz03fv29148": {"title": "应用对接", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/ei3ulfz03fv29148"},
    "eobw4zqaky1c0dfg": {"title": "应用集成", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/eobw4zqaky1c0dfg"},
    "og2xis3p4aiggei3": {"title": "插件管理", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/og2xis3p4aiggei3"},
    "zgrpcamswepxgx47": {"title": "工作流介绍", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/zgrpcamswepxgx47"},
    "qk98qatafge4zg9c": {"title": "工作流构建", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/qk98qatafge4zg9c"},
    "etgvtorzglntmv39": {"title": "API 调用", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/etgvtorzglntmv39"},
    "clcft0airk91f10q": {"title": "coze studio", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/clcft0airk91f10q"},
    "aqondvmlgonuwl4g": {"title": "Coze Studio 介绍", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/aqondvmlgonuwl4g"},
    "ecgfg25v3m5qk6nn": {"title": "平台 Coze API 调用说明文档", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/ecgfg25v3m5qk6nn"},
    "thkdpzvfc9lffg7g": {"title": "执行对话接口说明文档", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/thkdpzvfc9lffg7g"},
    "qr3laxwrxdosggc0": {"title": "服务管理", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/qr3laxwrxdosggc0"},
    "ku8iulvfl3e9sghk": {"title": "服务 API 调用", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/ku8iulvfl3e9sghk"},
    "ydb3zwmy25oi4stq": {"title": "yolo 评测", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/ydb3zwmy25oi4stq"},
    "ubzota0grvd9bbgy": {"title": "OCR 检测 - 模式一", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/ubzota0grvd9bbgy"},
    "hzbyt6vw97uglzu6": {"title": "物体检测 - 模式一", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/hzbyt6vw97uglzu6"},
    "gnzn6e0mfy0iu4yi": {"title": "物体检测 (std_layout)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/gnzn6e0mfy0iu4yi"},
    "kl0ubv7tbgmqdhdf": {"title": "图像分类 (img-cls)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/kl0ubv7tbgmqdhdf"},
    "pybzps3xn6e4aw84": {"title": "OCR 文本检测 (std_ocr_det)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/pybzps3xn6e4aw84"},
    "rgwg5gpqgo0mwdwh": {"title": "OCR 文本分类 (std_ocr_cls)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/rgwg5gpqgo0mwdwh"},
    "qtrdxuct1m9xmsem": {"title": "OCR 文本识别 (std_ocr_rec)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/qtrdxuct1m9xmsem"},
    "xc4cb74yd7le9y5y": {"title": "有线表格识别 (bded-rec)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/xc4cb74yd7le9y5y"},
    "ousq9u4rvr2o0nny": {"title": "无线表格检测 (bdss-det)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/ousq9u4rvr2o0nny"},
    "rony9ozk5zgrpr7h": {"title": "无线表格识别 (bdss-rec)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/rony9ozk5zgrpr7h"},
    "nhiqsgqg3q8agf56": {"title": "印章去除 (ocr-stamp)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/nhiqsgqg3q8agf56"},
    "xmmty1ige5rlltik": {"title": "OCR 表格识别 (ocr-tab)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/xmmty1ige5rlltik"},
    "gxisin2x8thxrtyr": {"title": "OCR 公式识别 (formula-rec)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/gxisin2x8thxrtyr"},
    "gx9pc2lcin2e4tpl": {"title": "水印去除 (ocr-watermark)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/gx9pc2lcin2e4tpl"},
    "wbz9fcq2neoscyhx": {"title": "文本向量化 (embedding)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/wbz9fcq2neoscyhx"},
    "isfh3b8uv6w1vyd3": {"title": "文本重排序 (rerank)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/isfh3b8uv6w1vyd3"},
    "hgaeepgyz3eo4aa2": {"title": "CAD 转图片 (cad_to_image)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/hgaeepgyz3eo4aa2"},
    "dbxiu8h799o37kez": {"title": "大模型 (llm)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/dbxiu8h799o37kez"},
    "gn4gig7iy7656gxz": {"title": "AecDataIO-W101_v2", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/gn4gig7iy7656gxz"},
    "tpwu4156wdu87m7g": {"title": "AecDataIO-W101_v1", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/tpwu4156wdu87m7g"},
    "esunsvy5pu5zlrrx": {"title": "AecDataIO-W101", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/esunsvy5pu5zlrrx"},
    "nv9xb3gs2qicwt8g": {"title": "OCR 文本检测 (PPOCR_v5)", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/nv9xb3gs2qicwt8g"},
    "kdh2eggww4g1hb1s": {"title": "调用统计", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/kdh2eggww4g1hb1s"},
    "vchachdl95z8t7vl": {"title": "LLM 生成评估", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/vchachdl95z8t7vl"},
    "kccxr46vwdzo2g1a": {"title": "知识检索评估", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/kccxr46vwdzo2g1a"},
    "ku9i5oea97ynfzt4": {"title": "平台认证 Token 说明文档", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/ku9i5oea97ynfzt4"},
    "tl0hylbi1hm61mu3": {"title": "Key Secret 认证获取 Token", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/tl0hylbi1hm61mu3"},
    "lpetkzefs5er4q5x": {"title": "平台使用常见问题汇总", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/lpetkzefs5er4q5x"},
    "bwec6xi60uy9xkgo": {"title": "平台更新记录", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/bwec6xi60uy9xkgo"},
    "gnkvf1e12n27uppo": {"title": "用户投诉举报处理系统", "url": "https://glodon-cv-help.yuque.com/cuv0se/ol9231/gnkvf1e12n27uppo"},
}

# 平台地址
PLATFORM_URL = "https://copilot.glodon.com/"
KNOWLEDGE_BASE_URL = "https://glodon-cv-help.yuque.com/cuv0se/ol9231"

# 平台入门指南
PLATFORM_ACCESS_GUIDE = """
## 🚀 如何进入广联达行业 AI 平台

### 访问步骤

**步骤 1**: 打开浏览器访问
- 网址：**https://copilot.glodon.com/**

**步骤 2**: 使用广联达账号登录
- 首次登录需要完成实名认证

**步骤 3**: 选择租户
- 登录后选择对应的租户

**步骤 4**: 进入产品中心
- 默认进入或点击左侧"产品中心"

**步骤 5**: 点击"行业 AI 平台"
- 在产品中心页面找到 **"行业 AI 平台"** 卡片
- 点击进入即可访问

---

## 📋 首次使用准备

### 1. 账号准备
- 拥有广联达账号（没有可注册）
- 完成实名认证
- 企业用户需要企业管理员授权

### 2. 获取 API Key（开发者）
1. 登录平台后进入"个人中心"
2. 点击"API 管理"
3. 创建新的 API Key
4. 复制保存（仅显示一次）

### 3. 配置 IP 白名单（可选）
- 企业用户建议在控制台配置 IP 白名单
- 提高 API 调用安全性

---

## 🔑 常见问题

**Q: 忘记密码怎么办？**
A: 在登录页点击"忘记密码"，通过手机号或邮箱重置

**Q: 企业账号无法登录？**
A: 联系企业管理员确认账号权限和状态

**Q: API 调用失败？**
A: 检查 API Key 是否有效、IP 是否在白名单、配额是否用完

---

## 📞 获取帮助

- 📚 文档中心：{knowledge_url}
- 💬 在线客服：平台右下角"帮助"按钮
- 📧 技术支持：提交工单系统
""".format(knowledge_url=KNOWLEDGE_BASE_URL)


class AIBotAssistant:
    """广联达行业 AI 平台问答助手"""
    
    def __init__(self):
        self.faqs = self._load_faqs()
        self.doc_index = DOC_INDEX
    
    def _load_faqs(self) -> List[Dict]:
        """加载 FAQ 库"""
        if os.path.exists(FAQ_FILE):
            with open(FAQ_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('faqs', [])
        return []
    
    def _match_keywords(self, query: str, keywords: List[str]) -> int:
        """匹配关键词得分"""
        query_lower = query.lower()
        score = 0
        for kw in keywords:
            if kw.lower() in query_lower:
                score += 1
        return score
    
    def _search_faqs(self, query: str) -> List[Tuple[Dict, int]]:
        """搜索相关 FAQ"""
        results = []
        query_lower = query.lower()
        
        for faq in self.faqs:
            score = 0
            
            # 匹配问题（逐词匹配）
            q_words = faq['question'].lower().split()
            for word in q_words:
                if len(word) > 1 and word in query_lower:
                    score += 2
            
            # 匹配标签
            t_score = self._match_keywords(query, faq.get('tags', []))
            score += t_score * 3
            
            # 匹配分类
            c_score = self._match_keywords(query, [faq.get('category', '')])
            score += c_score * 2
            
            # 匹配答案内容
            if query_lower in faq['answer'].lower():
                score += 5
            
            if score > 0:
                results.append((faq, score))
        
        # 按得分排序
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:3]
    
    def _search_docs(self, query: str) -> List[Tuple[str, Dict, int]]:
        """搜索相关文档"""
        results = []
        query_lower = query.lower()
        
        for slug, doc in self.doc_index.items():
            score = 0
            title = doc['title'].lower()
            
            # 标题匹配
            if query_lower in title:
                score += 10
            else:
                # 关键词匹配
                query_words = query_lower.split()
                for word in query_words:
                    if len(word) > 1 and word in title:
                        score += 2
            
            # 特殊主题匹配
            if 'ocr' in query_lower and 'ocr' in title:
                score += 5
            if 'token' in query_lower and 'token' in title:
                score += 5
            if 'api' in query_lower and 'api' in title:
                score += 5
            if 'prompt' in query_lower and 'prompt' in title:
                score += 5
            if '知识库' in query and '知识库' in doc['title']:
                score += 5
            if '工作流' in query and '工作流' in doc['title']:
                score += 5
            
            if score > 0:
                results.append((slug, doc, score))
        
        # 按得分排序
        results.sort(key=lambda x: x[2], reverse=True)
        return results[:5]
    
    def _is_platform_access_question(self, query: str) -> bool:
        """判断是否是关于如何进入平台的问题"""
        keywords = [
            "怎么进入", "如何进入", "怎么访问", "如何访问",
            "平台地址", "平台网址", "登录入口", "入口在哪",
            "怎么登录", "如何登录", "从哪里进", "怎么使用",
            "第一次使用", "新手入门", "入门指南", "开始使用"
        ]
        query_lower = query.lower()
        return any(kw in query_lower for kw in keywords)
    
    def _should_trigger_learning(self, query: str) -> Tuple[bool, List[str]]:
        """
        判断是否应该触发自动学习
        
        Returns:
            (是否需要学习，建议学习的文档 slug 列表)
        """
        query_lower = query.lower()
        
        # 检测是否需要学习的关键词
        learning_triggers = [
            ("不知道", ["lpetkzefs5er4q5x"]),  # 常见问题
            ("没有", ["lpetkzefs5er4q5x"]),    # 常见问题
            ("找不到", ["lpetkzefs5er4q5x"]),  # 常见问题
            ("最新", ["bwec6xi60uy9xkgo"]),    # 更新记录
            ("更新", ["bwec6xi60uy9xkgo"]),    # 更新记录
        ]
        
        for trigger, slugs in learning_triggers:
            if trigger in query_lower:
                return True, slugs
        
        return False, []
    
    def answer(self, query: str) -> Dict:
        """
        回答用户问题
        
        Args:
            query: 用户问题
            
        Returns:
            包含答案和文档链接的字典
        """
        # 检查是否是平台入门问题
        if self._is_platform_access_question(query):
            return {
                "query": query,
                "answer": PLATFORM_ACCESS_GUIDE,
                "faq_answer": None,
                "related_docs": [
                    {"title": "平台介绍", "url": DOC_INDEX["yck25gn683z3wa2f"]["url"], "slug": "yck25gn683z3wa2f", "relevance": 10},
                    {"title": "平台使用常见问题汇总", "url": DOC_INDEX["lpetkzefs5er4q5x"]["url"], "slug": "lpetkzefs5er4q5x", "relevance": 8},
                    {"title": "平台认证 Token 说明文档", "url": DOC_INDEX["ku9i5oea97ynfzt4"]["url"], "slug": "ku9i5oea97ynfzt4", "relevance": 6},
                ],
                "timestamp": datetime.now().isoformat(),
                "is_guide": True
            }
        
        # 检查是否需要触发学习
        should_learn, learn_slugs = self._should_trigger_learning(query)
        
        # 搜索 FAQ
        faq_results = self._search_faqs(query)
        
        # 搜索文档
        doc_results = self._search_docs(query)
        
        # 生成回答
        response = {
            "query": query,
            "answer": "",
            "faq_answer": None,
            "related_docs": [],
            "timestamp": datetime.now().isoformat(),
            "should_learn": should_learn,
            "learn_slugs": learn_slugs
        }
        
        # 如果有 FAQ 匹配
        if faq_results and faq_results[0][1] >= 2:
            best_faq = faq_results[0][0]
            response["faq_answer"] = {
                "question": best_faq['question'],
                "answer": best_faq['answer'],
                "category": best_faq.get('category', '')
            }
            response["answer"] = best_faq['answer']
        
        # 添加相关文档链接
        for slug, doc, score in doc_results:
            response["related_docs"].append({
                "title": doc['title'],
                "url": doc['url'],
                "slug": slug,
                "relevance": score
            })
        
        # 如果没有找到匹配
        if not response["answer"] and not doc_results:
            response["answer"] = f"""抱歉，我暂时没有找到相关信息。

📚 **建议操作**：
1. 我可以帮您从语雀知识库学习相关文档
2. 查看 [平台使用常见问题汇总]({DOC_INDEX['lpetkzefs5er4q5x']['url']})
3. 联系技术支持

💡 **提示**: 说"去学习"可以让我更新知识库"""
        
        return response
    
    def format_response(self, response: Dict) -> str:
        """格式化回答为可读文本"""
        output = []
        
        # 平台入门指南（特殊处理）
        if response.get("is_guide"):
            output.append("🚀 **进入广联达行业 AI 平台指南**\n")
            output.append(response["answer"])
            output.append("")
        
        # FAQ 答案
        elif response.get("faq_answer"):
            faq = response["faq_answer"]
            output.append(f"📋 **{faq['question']}**\n")
            output.append(faq['answer'])
            output.append("")
        
        # 普通回答
        elif response.get("answer"):
            output.append(response["answer"])
            output.append("")
        
        # 相关文档
        docs = response.get("related_docs", [])
        if docs:
            output.append("📚 **相关文档**:\n")
            for i, doc in enumerate(docs[:5], 1):
                output.append(f"{i}. [{doc['title']}]({doc['url']})")
            output.append("")
        
        # 学习建议
        if response.get("should_learn") and response.get("learn_slugs"):
            output.append("🔄 **知识库更新建议**:\n")
            output.append("检测到可能是新问题，建议学习以下文档：")
            for slug in response["learn_slugs"]:
                if slug in DOC_INDEX:
                    output.append(f"- {DOC_INDEX[slug]['title']}: {DOC_INDEX[slug]['url']}")
            output.append("")
        
        # 知识库首页
        output.append("---")
        output.append("")
        output.append(f"📖 **平台地址**: {PLATFORM_URL}")
        output.append(f"📚 **知识库**: {KNOWLEDGE_BASE_URL}")
        
        return "\n".join(output)


def main():
    """命令行交互"""
    bot = AIBotAssistant()
    
    print("=" * 60)
    print("广联达行业 AI 平台 - 智能问答助手")
    print("=" * 60)
    print("输入问题，按回车提交。输入 'quit' 退出。\n")
    
    while True:
        try:
            query = input("🤔 你的问题：").strip()
            if not query:
                continue
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 再见！")
                break
            
            response = bot.answer(query)
            formatted = bot.format_response(response)
            
            print("\n" + "=" * 60)
            print(formatted)
            print("=" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误：{e}\n")


if __name__ == "__main__":
    main()
