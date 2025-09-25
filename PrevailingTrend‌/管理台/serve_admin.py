#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import random
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, quote
from datetime import datetime, timedelta

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8090"))

# 受限目录映射（避免任意访问）
SAFE_KEYS = {
    "wind": os.path.abspath(os.path.join(ROOT_DIR, "..", "第一层模块", "万得行业分类")),
}

class AdminHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/domestic-hotspot":
            self._send_json(self._generate_hotspots())
            return
        if parsed.path == "/api/domestic-hotspot/stats":
            data = self._generate_hotspots()
            self._send_json(self._calc_stats(data["data"]))
            return
        if parsed.path == "/api/list-dir":
            params = parse_qs(parsed.query or "")
            key = (params.get("key") or [""])[0]
            max_depth = int((params.get("depth") or ["2"])[0])
            resp = self._list_dir_by_key(key, max_depth=max_depth)
            self._send_json({"success": True, "data": resp})
            return
        # 其它路径走静态文件
        return super().do_GET()

    def _send_json(self, payload, status=200):
        body = json.dumps(payload if "success" in payload else {"success": True, "data": payload}, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _generate_hotspots(self):
        random.seed()
        categories = [
            ("财经热点", 100), ("政策动态", 80), ("市场新闻", 120), ("行业资讯", 100),
            ("公司热点", 50), ("宏观经济", 50), ("投资热点", 50)
        ]
        sources = ["财新网", "新华财经", "人民日报", "中国产经新闻", "证券日报", "公司官网", "东方财富", "券商研报", "投资界"]
        sentiments = ["积极", "中性", "消极"]
        data = []
        idx = 1
        now = datetime.now()
        for cat, count in categories:
            for _ in range(count):
                title = f"{cat} 标题 {idx}"
                source = random.choice(sources)
                # 简单可点击URL（占位：通过搜索引擎检索标题）
                url = f"https://www.baidu.com/s?wd={quote(title)}"
                item = {
                    "id": f"HS_{idx:05d}",
                    "title": title,
                    "category": cat,
                    "content": f"关于{cat}的最新动态与解读 {idx}",
                    "heatScore": round(random.uniform(60, 100), 2),
                    "sentiment": random.choice(sentiments),
                    "source": source,
                    "url": url,
                    "publishTime": (now - timedelta(hours=random.randint(0, 72), minutes=random.randint(0, 59))).strftime("%Y-%m-%d %H:%M:%S"),
                }
                data.append(item)
                idx += 1
        return {"success": True, "data": data}

    def _calc_stats(self, data):
        stats = {
            "total_hotspots": len(data),
            "finance_hotspots": 0,
            "policy_hotspots": 0,
            "market_hotspots": 0,
            "industry_hotspots": 0,
            "company_hotspots": 0,
            "macro_hotspots": 0,
            "investment_hotspots": 0,
            "positive_count": 0,
            "neutral_count": 0,
            "negative_count": 0,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        cat_map = {
            "财经热点": "finance_hotspots",
            "政策动态": "policy_hotspots",
            "市场新闻": "market_hotspots",
            "行业资讯": "industry_hotspots",
            "公司热点": "company_hotspots",
            "宏观经济": "macro_hotspots",
            "投资热点": "investment_hotspots",
        }
        for item in data:
            key = cat_map.get(item.get("category"))
            if key:
                stats[key] += 1
            sentiment = item.get("sentiment")
            if sentiment == "积极":
                stats["positive_count"] += 1
            elif sentiment == "中性":
                stats["neutral_count"] += 1
            elif sentiment == "消极":
                stats["negative_count"] += 1
        p, n, z = stats["positive_count"], stats["negative_count"], stats["neutral_count"]
        stats["market_sentiment"] = "积极" if p >= n and p >= z else ("消极" if n >= p and n >= z else "中性")
        return {"success": True, "data": stats}

    def _list_dir_by_key(self, key: str, max_depth: int = 2):
        root = SAFE_KEYS.get(key)
        if not root or not os.path.isdir(root):
            return {"root": None, "items": []}
        def walk(d: str, depth: int):
            node = {"name": os.path.basename(d), "path": os.path.relpath(d, root), "type": "dir", "children": []}
            if depth >= max_depth:
                return node
            try:
                for name in sorted(os.listdir(d)):
                    fp = os.path.join(d, name)
                    if os.path.isdir(fp):
                        node["children"].append(walk(fp, depth + 1))
                    else:
                        try:
                            size = os.path.getsize(fp)
                        except OSError:
                            size = 0
                        node["children"].append({
                            "name": name,
                            "path": os.path.relpath(fp, root).replace("\\", "/"),
                            "type": "file",
                            "size": size
                        })
            except OSError:
                pass
            return node
        tree = walk(root, 0)
        return {"root": root, "items": tree}


def run():
    os.chdir(ROOT_DIR)
    httpd = HTTPServer(("", PORT), AdminHandler)
    print("========================================")
    print("管理台与API同端口服务器启动中...")
    print(f"端口: {PORT}")
    print("静态根目录:", ROOT_DIR)
    print("页面:  http://localhost:%d/index.html" % PORT)
    print("API:   /api/domestic-hotspot, /api/domestic-hotspot/stats, /api/list-dir?key=wind")
    print("========================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")

if __name__ == "__main__":
    run() 