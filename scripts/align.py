#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
古文现代文平行语料 - 对齐工具

用法:
    python align.py                        # 显示统计信息
    python align.py "关键词"                # 搜索
    python align.py --source "论语"        # 按来源搜索
    python align.py --difficulty "初级"     # 按难度过滤
    python align.py --author "庄子"         # 按相关作者/思想流派搜索
    python align.py --export output.json   # 导出为JSON
"""

import json
import argparse
import sys
import os
from typing import List, Dict, Any
from collections import Counter


def load_data(filename: str) -> List[Dict[str, Any]]:
    """加载数据文件"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 找不到数据文件 {data_path}")
        return []
    except json.JSONDecodeError:
        print(f"错误: 数据文件格式错误 {data_path}")
        return []


def search(corpus: List[Dict], keyword: str) -> List[Dict]:
    """搜索包含关键词的语料"""
    kw = keyword.lower()
    results = []
    for item in corpus:
        classical_lower = item.get('classical', '').strip('，。！？').lower()
        modern_lower = item.get('modern', '').strip('，。！？').lower()
        source_lower = item.get('source', '').lower()
        if kw in classical_lower or kw in modern_lower or kw in source_lower:
            results.append(item)
    return results


def print_stats(corpus: List[Dict]):
    """打印统计信息"""
    print("\n" + "=" * 60)
    print("          古文现代文平行语料 统计")
    print("=" * 60)

    print(f"\n📊 总体数据:")
    print(f"   语料总数: {len(corpus)}")

    # 来源统计
    source_counter = Counter(item.get('source', '未知') for item in corpus)
    print(f"\n📖 来源分布:")
    for source, count in sorted(source_counter.items(), key=lambda x: -x[1]):
        print(f"   {source}: {count}条")

    # 难度分布
    diff_counter = Counter(item.get('difficulty', '未知') for item in corpus)
    print(f"\n📈 难度分布:")
    for diff, count in sorted(diff_counter.items(), key=lambda x: -x[1]):
        print(f"   {diff}: {count}条")

    # 朝代分布
    dynasty_counter = Counter(item.get('dynasty', '未知') for item in corpus)
    print(f"\n🏛️  朝代分布:")
    for dynasty, count in sorted(dynasty_counter.items(), key=lambda x: -x[1]):
        print(f"   {dynasty}: {count}条")

    # 题材分布
    genre_counter = Counter(item.get('genre', '未知') for item in corpus)
    print(f"\n📚 题材分布:")
    for genre, count in sorted(genre_counter.items(), key=lambda x: -x[1]):
        print(f"   {genre}: {count}条")

    print("\n" + "=" * 60 + "\n")


def print_item(item: Dict):
    """格式化打印一条语料"""
    print("-" * 60)
    print(f"  【出处】{item['source']} ({item['dynasty']}, {item['difficulty']})")
    print(f"  📜 古文: {item['classical']}")
    print(f"  📝 现代: {item['modern']}")
    if item.get('keywords'):
        print(f"  标签: {', '.join(item['keywords'])}")
    if item.get('notes'):
        print(f"  注释: {item['notes']}")
    print("-" * 60)
    print()


def main():
    parser = argparse.ArgumentParser(
        description='古文现代文平行语料 - 对齐与检索工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python align.py                            # 显示统计
    python align.py "学而"                     # 关键词搜索
    python align.py --source "论语"            # 按来源过滤
    python align.py --difficulty "初级"         # 按难度过滤
    python align.py --genre "经"               # 按题材过滤
    python align.py --export output.json       # 导出结果
        """
    )

    parser.add_argument('keyword', nargs='?', help='关键词搜索')
    parser.add_argument('--source', '-s', help='按来源过滤')
    parser.add_argument('--difficulty', '-d', choices=['初级', '中级', '高级'], help='按难度过滤')
    parser.add_argument('--genre', '-g', help='按题材过滤')
    parser.add_argument('--export', '-e', help='导出结果到JSON文件')
    parser.add_argument('--limit', '-l', type=int, default=20, help='限制结果数量')

    args = parser.parse_args()

    corpus = load_data('sample.json')
    if not corpus:
        sys.exit(1)

    results = corpus.copy()

    # 应用过滤
    if args.keyword:
        results = search(results, args.keyword)
    if args.source:
        results = [r for r in results if args.source in r.get('source', '')]
    if args.difficulty:
        results = [r for r in results if r.get('difficulty') == args.difficulty]
    if args.genre:
        results = [r for r in results if r.get('genre') == args.genre]

    # 无搜索参数时显示统计
    if not args.keyword and not args.source and not args.difficulty and not args.genre:
        print_stats(corpus)
        return

    # 导出
    if args.export:
        output_path = args.export
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"已导出 {len(results)} 条结果到 {output_path}")
        return

    # 打印结果
    if not results:
        print("未找到匹配结果。")
        sys.exit(0)

    total = len(results)
    if total > args.limit:
        print(f"\n找到 {total} 条结果，显示前 {args.limit} 条:\n")
        results = results[:args.limit]
    else:
        print(f"\n找到 {total} 条结果:\n")

    for item in results:
        print_item(item)


if __name__ == '__main__':
    main()