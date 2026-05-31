# Classical Chinese Parallel Corpus - 古文现代文平行语料

> 结构化古文与现代文平行语料数据集，适用于机器翻译、古文理解、NLP研究

---

## Features / 功能特点

| 功能 | 说明 |
|------|------|
| 句级对齐 | 古文与现代文逐句人工标注对齐 |
| 四部典籍 | 经/史/子/集四部经典文献覆盖 |
| 完整字段 | 10个字段含出处、难度、题材、关键词、注释 |
| 难度分级 | 初级/中级/高级三级难度区分 |
| 语法注释 | 含通假字、词类活用等标注 |
| 命令行工具 | 搜索、统计、导出等功能完整 |
| Python API | 可直接作为模块使用 |

## Installation / 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/classical-chinese-parallel.git

cd classical-chinese-parallel

# Python 3.6+ 即可运行
python scripts/align.py --help
```

## Usage / 使用方法

### 命令行

```bash
# 查看统计信息
python scripts/align.py

# 搜索古文内容
python scripts/align.py "学而时习之"

# 按来源搜索
python scripts/align.py --source "论语"

# 按难度过滤
python scripts/align.py --difficulty "初级"

# 导出为JSON
python scripts/align.py --export output.json
```

### 数据结构

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | string | 唯一标识符 | "lunyu_001" |
| classical | string | 古文原文 | "学而时习之，不亦说乎？" |
| modern | string | 现代文翻译 | "学习了知识然后按时温习，不是很愉快吗？" |
| source | string | 出处（篇名） | "论语·学而" |
| dynasty | string | 朝代 | "春秋" |
| difficulty | string | 难度等级 | "初级" |
| genre | string | 题材分类 | "经" |
| keywords | array[string] | 关键词 | `["学习", "快乐"]` |
| notes | string | 语法/词汇注释 | "\"说\"通\"悦\"，意为喜悦、愉快" |

### Python 模块使用示例

```python
import json

# 加载语料
with open('data/sample.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# 按来源分组
from collections import Counter
source_count = Counter(item['source'] for item in corpus)

# 按难度过滤
advanced = [c for c in corpus if c['difficulty'] == '高级']
print(f"高级难度语料 {len(advanced)} 条")

# 搜索特定来源
lunyu_items = [c for c in corpus if '论语' in c['source']]
for item in lunyu_items:
    print(f"古文: {item['classical']}")
    print(f"今译: {item['modern']}")
    print("---")
```

### 数据来源

语料精选自先秦至明清的经典文献：

| 部类 | 文献 | 难度 |
|------|------|:----:|
| 经部 | 《论语》《孟子》《大学》《中庸》 | 初级-中级 |
| 史部 | 《史记》《资治通鉴》《战国策》 | 中级-高级 |
| 子部 | 《庄子》《老子》《韩非子》《孙子》 | 中级-高级 |
| 集部 | 《古文观止》历代名篇 | 高级 |

## Contributing / 贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md)

欢迎贡献：
- 补充平行语料
- 改进对齐质量
- 添加更多典籍
- 报告数据问题

## License / 许可证

MIT License - 参见 [LICENSE](LICENSE)

---

> 版本：1.0.0 | 更新日期：2026-05-30