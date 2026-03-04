#!/usr/bin/env python3
"""
诚实文献搜索系统 - 只提供真实可验证的文献
"""

import requests
import json
from datetime import datetime

def search_honest_papers():
    """搜索真实可验证的文献"""
    print("🔍 诚实搜索系统 - 只提供真实文献")
    print("=" * 70)
    
    # 使用Crossref搜索真实DOI
    base_url = "https://api.crossref.org/works"
    
    # 搜索查询（小鼠脑出血相关）
    queries = [
        ("intracerebral hemorrhage mouse", "脑出血小鼠模型"),
        ("neuroinflammation stroke", "卒中神经炎症"),
        ("microglia activation brain injury", "小胶质细胞激活")
    ]
    
    all_real_papers = []
    
    for query_en, query_cn in queries:
        print(f"\n搜索: {query_cn} ({query_en})")
        
        try:
            params = {
                "query": query_en,
                "rows": 4,
                "sort": "relevance",
                "filter": "type:journal-article,from-pub-date:2015"
            }
            
            response = requests.get(base_url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                items = data["message"]["items"]
                
                print(f"  找到 {len(items)} 条记录")
                
                for item in items:
                    # 提取基本信息
                    title_list = item.get("title", [])
                    title = title_list[0] if title_list else "无标题"
                    doi = item.get("DOI", "")
                    
                    if not title or not doi:
                        continue
                    
                    # 验证DOI
                    doi_url = f"https://doi.org/{doi}"
                    try:
                        verify = requests.head(doi_url, timeout=10, allow_redirects=True)
                        is_accessible = verify.status_code in [200, 301, 302]
                        
                        if is_accessible:
                            # 获取详细信息
                            year = item.get("created", {}).get("date-parts", [[0]])[0][0]
                            
                            # 作者
                            authors = item.get("author", [])
                            author_names = []
                            for author in authors[:2]:
                                given = author.get("given", "")
                                family = author.get("family", "")
                                if given and family:
                                    author_names.append(f"{given} {family}")
                            
                            # 期刊
                            journal_list = item.get("container-title", [])
                            journal = journal_list[0] if journal_list else ""
                            
                            paper_info = {
                                "title": title,
                                "doi": doi,
                                "doi_url": doi_url,
                                "year": year,
                                "journal": journal,
                                "authors": author_names,
                                "verified": True,
                                "status_code": verify.status_code,
                                "search_query": query_cn,
                                "timestamp": datetime.now().isoformat()
                            }
                            
                            all_real_papers.append(paper_info)
                            print(f"  ✓ {title[:60]}...")
                            
                    except Exception as e:
                        print(f"  ✗ {title[:60]}... (验证失败: {e})")
                        
        except Exception as e:
            print(f"  搜索错误: {e}")
    
    return all_real_papers

def format_honest_report(papers):
    """生成诚实报告"""
    if not papers:
        return "❌ 本次搜索未找到可验证的文献\n\n⚠️ 说明：系统只显示经过验证的真实文献，不会编造信息"
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    report = f"📅 **诚实文献报告** - {today}\n\n"
    report += "🔍 **所有文献都经过DOI验证**\n"
    report += "✅ **绝不编造任何信息**\n\n"
    
    report += "📊 **搜索统计**\n"
    report += f"   搜索时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    report += f"   找到文献: {len(papers)} 篇\n"
    report += f"   已验证: {len(papers)} 篇\n"
    report += "   数据源: Crossref DOI数据库\n"
    report += "   验证方式: HTTP链接检查\n\n"
    
    report += "📚 **真实文献列表**\n\n"
    
    for i, paper in enumerate(papers[:6], 1):  # 最多6篇
        report += f"**{i}. {paper['title']}**\n"
        
        if paper["authors"]:
            report += f"   作者: {', '.join(paper['authors'])}\n"
        
        if paper["journal"]:
            report += f"   期刊: {paper['journal']}\n"
        
        if paper["year"]:
            report += f"   年份: {paper['year']}\n"
        
        report += f"   DOI: {paper['doi']}\n"
        report += f"   ✅ 验证: HTTP {paper['status_code']} - 可访问\n"
        report += f"   🔗 {paper['doi_url']}\n"
        report += f"   🔍 搜索词: {paper['search_query']}\n\n"
    
    report += "⚠️ **重要声明**\n"
    report += "1. 所有文献信息来自Crossref官方数据库\n"
    report += "2. 每个DOI都经过链接验证\n"
    report += "3. 绝不编造、虚构任何论文信息\n"
    report += "4. 如果搜索不到，会如实报告\n"
    report += "5. 质量优于数量，真实优于虚构\n"
    
    return report

def main():
    """主函数"""
    print("=" * 70)
    print("✅ 诚实文献搜索系统")
    print("=" * 70)
    
    # 搜索真实文献
    papers = search_honest_papers()
    
    print(f"\n{'='*70}")
    print(f"📊 结果: {len(papers)} 篇可验证真实文献")
    print("=" * 70)
    
    # 生成报告
    report = format_honest_report(papers)
    
    print(report)
    print("=" * 70)
    
    # 保存原始数据
    import os
    os.makedirs("/home/node/clawd/honest_reports", exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"/home/node/clawd/honest_reports/{today}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({
            "report_date": today,
            "paper_count": len(papers),
            "papers": papers,
            "disclaimer": "所有文献都经过DOI验证，绝不编造信息"
        }, f, indent=2, ensure_ascii=False)
    
    print(f"📁 原始数据已保存: {filename}")
    print("=" * 70)
    
    return report

if __name__ == "__main__":
    main()