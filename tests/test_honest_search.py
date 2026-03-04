#!/usr/bin/env python3
"""
简化版诚实文献搜索 - 测试用
"""

import requests
import json
from datetime import datetime

def simple_search():
    """简化搜索"""
    print("🔍 简化搜索测试")
    
    # 只搜索一个主题
    query = "intracerebral hemorrhage mouse"
    base_url = "https://api.crossref.org/works"
    
    try:
        params = {
            "query": query,
            "rows": 3,
            "sort": "relevance",
            "filter": "type:journal-article,from-pub-date:2015"
        }
        
        print(f"搜索: {query}")
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            items = data["message"]["items"]
            
            print(f"找到 {len(items)} 条记录")
            
            papers = []
            for item in items:
                title_list = item.get("title", [])
                title = title_list[0] if title_list else "无标题"
                doi = item.get("DOI", "")
                
                if not title or not doi:
                    continue
                
                # 简单验证
                doi_url = f"https://doi.org/{doi}"
                try:
                    verify = requests.head(doi_url, timeout=5, allow_redirects=True)
                    if verify.status_code in [200, 301, 302]:
                        year = item.get("created", {}).get("date-parts", [[0]])[0][0]
                        
                        paper_info = {
                            "title": title,
                            "doi": doi,
                            "doi_url": doi_url,
                            "year": year,
                            "verified": True,
                            "status_code": verify.status_code
                        }
                        
                        papers.append(paper_info)
                        print(f"  ✓ {title[:50]}...")
                        
                except Exception as e:
                    print(f"  ✗ {title[:50]}... (验证失败)")
            
            return papers
            
        else:
            print(f"API错误: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"搜索错误: {e}")
        return []

def main():
    """主函数"""
    papers = simple_search()
    
    print(f"\n📊 结果: {len(papers)} 篇可验证文献")
    
    if papers:
        print("\n📚 文献列表:")
        for i, paper in enumerate(papers, 1):
            print(f"{i}. {paper['title']}")
            print(f"   年份: {paper['year']}, DOI: {paper['doi']}")
            print(f"   验证: HTTP {paper['status_code']} - {paper['doi_url']}")
            print()
    
    # 保存结果
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"/home/node/clawd/honest_reports/{today}_test.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({
            "report_date": today,
            "paper_count": len(papers),
            "papers": papers,
            "timestamp": datetime.now().isoformat()
        }, f, indent=2, ensure_ascii=False)
    
    print(f"📁 数据已保存: {filename}")

if __name__ == "__main__":
    main()