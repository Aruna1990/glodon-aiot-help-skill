#!/bin/bash
# 批量学习核心文档脚本

KNOWLEDGE_DIR="$(cd "$(dirname "$0")" && pwd)/knowledge"
BASE_URL="https://glodon-cv-help.yuque.com/cuv0se/ol9231"

echo "============================================================"
echo "📚 广联达行业 AI 平台 - 批量学习核心文档"
echo "============================================================"

# 核心文档列表
declare -A DOCS=(
    ["yck25gn683z3wa2f"]="平台介绍"
    ["lpetkzefs5er4q5x"]="平台使用常见问题汇总"
    ["ku9i5oea97ynfzt4"]="平台认证 Token 说明文档"
    ["tl0hylbi1hm61mu3"]="Key Secret 认证获取 Token"
    ["etgvtorzglntmv39"]="API 调用"
    ["thkdpzvfc9lffg7g"]="执行对话接口说明文档"
    ["ku8iulvfl3e9sghk"]="服务 API 调用"
    ["xcrcis1brhczo6ei"]="Prompt 工程"
    ["cw6wurwnygkv1nne"]="知识库"
    ["hhgfdznfypkcz0t1"]="数据管理"
)

count=0
total=${#DOCS[@]}

for slug in "${!DOCS[@]}"; do
    title="${DOCS[$slug]}"
    ((count++))
    
    echo ""
    echo "[$count/$total] 📥 $title"
    echo "    https://glodon-cv-help.yuque.com/cuv0se/ol9231/$slug"
    
    # 使用 openclaw web_fetch 获取内容
    # 这里生成命令，实际执行需要调用工具
    echo "    命令：openclaw web-fetch https://glodon-cv-help.yuque.com/cuv0se/ol9231/$slug"
    
    sleep 0.5
done

echo ""
echo "============================================================"
echo "✅ 命令生成完成"
echo "============================================================"
