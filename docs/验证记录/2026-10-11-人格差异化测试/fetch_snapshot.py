#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""人格差异化实测 · 数据快照取数脚本（可复跑）
运行: /Users/xiaolv/.workbuddy/binaries/python/envs/default/bin/python fetch_snapshot.py
输出: data_snapshot.json（本目录）
依赖: akshare（托管 venv 已装）；口径与 skills/data-layer/README.md 一致。
"""
import akshare as ak, json, datetime
from pathlib import Path

OUT = Path(__file__).resolve().parent / "data_snapshot.json"
SYMBOL = "sh600519"   # 贵州茅台

df = ak.stock_zh_a_daily(symbol=SYMBOL, adjust="qfq").tail(260).reset_index(drop=True)
last = df.iloc[-1]
close = float(last["close"])
ma = {n: round(float(df["close"].tail(n).mean()), 2) for n in (5, 20, 60, 120)}
hi52, lo52 = round(float(df["high"].tail(250).max()), 2), round(float(df["low"].tail(250).min()), 2)

snap = {
    "标的": "贵州茅台 sh600519（测试用）",
    "数据来源": "AKShare: stock_zh_a_daily（新浪口径，前复权）",
    "取数日期": str(datetime.date.today()),
    "最新交易日": str(last["date"]),
    "行情快照": {
        "收盘": close, "MA5": ma[5], "MA20": ma[20], "MA60": ma[60], "MA120": ma[120],
        "近10日涨跌幅%": round((close / float(df["close"].iloc[-11]) - 1) * 100, 2),
        "近60日涨跌幅%": round((close / float(df["close"].iloc[-61]) - 1) * 100, 2),
        "52周最高": hi52, "52周最低": lo52,
        "52周区间位置%": round((close - lo52) / (hi52 - lo52) * 100, 1),
        "5日均量(万手)": round(float(df["volume"].tail(5).mean()) / 10000, 1),
        "20日均量(万手)": round(float(df["volume"].tail(20).mean()) / 10000, 1),
        "当日成交量(万手)": round(float(last["volume"]) / 10000, 1),
        "当日成交额(亿元)": round(float(last["amount"]) / 1e8, 1),
    },
    "免责": "本快照仅为仓库管线自检用；真实分析须按 data-layer 纪律补全来源与日期。",
}
try:
    pe = ak.stock_zh_valuation_baidu(symbol="600519", indicator="市盈率(TTM)", period="近一年").tail(1).iloc[0]
    pb = ak.stock_zh_valuation_baidu(symbol="600519", indicator="市净率", period="近一年").tail(1).iloc[0]
    snap["估值快照"] = {"来源": "AKShare: stock_zh_valuation_baidu（百度口径）",
                        "日期": str(pe["date"]), "PE(TTM)": float(pe["value"]), "市净率": float(pb["value"])}
except Exception as e:  # noqa: BLE001
    snap["估值快照"] = f"降级未取到：{e}"

OUT.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
print("已写出:", OUT)
