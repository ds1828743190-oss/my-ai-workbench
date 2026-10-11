#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data-layer · 开源路线适配脚本（AKShare 优先）
==============================================
统一数据层的最小可用实现：把"一句自然语言需求"映射到 AKShare 接口。
纪律（与 README.md §四 一致）：数字必标来源与日期；取不到就报降级，绝不编造。

用法:
    python3 akshare_adapter.py --selftest                # 自检：逐项测试可用性
    python3 akshare_adapter.py index-quote 000300        # 指数最新行情（沪深300）
    python3 akshare_adapter.py index-daily 000300 --days 60
    python3 akshare_adapter.py index-pe 沪深300           # 指数 PE（funddb 口径）
    python3 akshare_adapter.py bond-10y                  # 中债 10 年期国债收益率
    python3 akshare_adapter.py quote 510890              # 场内基金/ETF 行情（新浪口径）

依赖: akshare（缺省时给出清华镜像安装命令，不会自动联网安装）
"""
from __future__ import annotations
import argparse, sys, datetime, json

SOURCE = {
    "index_daily": "AKShare: stock_zh_index_daily",
    "index_spot": "AKShare: stock_zh_index_spot_sina",
    "index_pe": "AKShare: index_value_hist_funddb",
    "bond": "AKShare: bond_zh_us_rate",
    "etf": "AKShare: fund_etf_spot_em",
}

def _need_akshare():
    try:
        import akshare as ak  # noqa
        return ak
    except ImportError:
        print("[data-layer] 缺少 akshare。安装（清华镜像，约 1 分钟）：\n"
              "  pip install akshare -i https://pypi.tuna.tsinghua.edu.cn/simple\n"
              "或改用已授权的连接器路线（neodata / westock / dzh），见 README.md §三。",
              file=sys.stderr)
        sys.exit(2)

def _fmt(symbol: str) -> str:
    """指数代码规范化：支持 000300 / sh000300 两种写法。"""
    s = symbol.strip().lower()
    if s.startswith(("sh", "sz", "bj")):
        return s
    if s.startswith(("0", "3")):          # 深市系（含 399xxx 深证系列）
        return "sz" + s if s.startswith("399") else "sh" + s if s.startswith("000") else "sz" + s
    return s

def index_quote(symbol: str) -> dict:
    """指数最新行情（新浪口径）。⚠️ 指数代码需带市场前缀，沪深300=sh000300。"""
    ak = _need_akshare()
    code = _fmt(symbol)
    df = ak.stock_zh_index_spot_sina()
    row = df[df["代码"].astype(str).str.lower() == code]
    if row.empty:
        raise LookupError(f"未找到指数 {code}（可用代码示例：sh000300/sh000001/sz399006）")
    r = row.iloc[0].to_dict()
    return {
        "source": SOURCE["index_spot"], "date": str(datetime.date.today()),
        "code": code, "name": r.get("名称"), "close": r.get("最新价"),
        "change_pct": r.get("涨跌幅"), "amount": r.get("成交额"),
    }

def index_daily(symbol: str, days: int = 60) -> list[dict]:
    """指数日线（新浪口径，含历史）。"""
    ak = _need_akshare()
    code = _fmt(symbol)
    df = ak.stock_zh_index_daily(symbol=code).tail(days)
    out = []
    for _, r in df.iterrows():
        out.append({"date": str(r["date"]), "open": r["open"], "high": r["high"],
                    "low": r["low"], "close": r["close"], "volume": r["volume"]})
    return {"source": SOURCE["index_daily"], "code": code, "bars": out}

def index_pe(name: str = "沪深300") -> dict:
    """指数 PE。回退链：中证官方口径 → 乐咕口径。
    注意：两口径数值可差 ~0.5-1 倍（计算方式/样本不同）；核心策略流程请按
    「数据源交叉印证协议」与中证网/证券时报/每经媒体口径互验（正常范围 11~16 倍）。"""
    ak = _need_akshare()
    errors = []
    # ① 中证指数官方估值（口径最权威；更新可能滞后，返回值含日期）
    code = {"沪深300": "000300", "上证50": "000016", "中证500": "000905", "中证1000": "000852"}.get(name, name)
    try:
        df = ak.stock_zh_index_value_csindex(symbol=code)
        df = df.sort_values("日期")           # 该接口默认降序，统一升序后取最新
        last = df.iloc[-1]
        return {"source": "AKShare: stock_zh_index_value_csindex（中证官方口径）",
                "date": str(last["日期"]), "index": name,
                "pe_1": float(last["市盈率1"]), "pe_2": float(last["市盈率2"]),
                "dividend_yield_1": float(last["股息率1"]),
                "note": "中证官方口径；若日期滞后（>5 交易日）请以媒体三源口径互验"}
    except Exception as e:  # noqa: BLE001
        errors.append(f"csindex: {e}")
    # ② 乐咕口径（滚动市盈率，更新较快；数值与媒体口径或存差异）
    try:
        df = ak.stock_index_pe_lg(symbol=name)
        last = df.tail(1).iloc[0]
        return {"source": "AKShare: stock_index_pe_lg（乐咕口径）",
                "date": str(last["日期"]), "index": name,
                "pe_ttm": float(last["滚动市盈率"]), "pe_static": float(last["静态市盈率"]),
                "note": "乐咕滚动市盈率；与中证网/证券时报口径可能相差 0.5~1，需互验后采用"}
    except Exception as e:  # noqa: BLE001
        errors.append(f"lg: {e}")
    raise RuntimeError("；".join(errors) + f"；可降级联网搜「{name} 市盈率 TTM」（以中证网/证券时报/每经口径为准）")

def bond_10y() -> dict:
    """中债国债收益率曲线 10 年期（官方口径）。"""
    ak = _need_akshare()
    df = ak.bond_zh_us_rate(start_date="20200101")
    col = [c for c in df.columns if "中国国债收益率10年" in str(c)]
    if not col:
        raise RuntimeError("bond_zh_us_rate 未返回 10 年期中国国债列，换源：chinabond.com.cn")
    df = df.dropna(subset=[col[0]])
    last = df.tail(1).iloc[0]
    return {"source": SOURCE["bond"], "date": str(last.iloc[0]),
            "yield_10y_pct": round(float(last[col[0]]), 4)}

def etf_quote(code: str) -> dict:
    """ETF/场内基金最新行情（东财口径）。如红利低波 510890、国债ETF 511010。"""
    ak = _need_akshare()
    df = ak.fund_etf_spot_em()
    row = df[df["代码"].astype(str) == code.strip()]
    if row.empty:
        raise LookupError(f"未找到 ETF {code}")
    r = row.iloc[0].to_dict()
    return {"source": SOURCE["etf"], "date": str(datetime.date.today()),
            "code": code, "name": r.get("名称"), "close": r.get("最新价"),
            "change_pct": r.get("涨跌幅")}

def selftest():
    """逐项自检：全部输出结构化结果或明确的降级说明。"""
    tests = [
        ("index_quote(sh000300)", lambda: index_quote("000300")),
        ("index_daily(sz399006, 5)", lambda: index_daily("399006", 5)),
        ("index_pe(沪深300)", lambda: index_pe("沪深300")),
        ("bond_10y()", bond_10y),
        ("etf_quote(510890)", lambda: etf_quote("510890")),
    ]
    ok = bad = 0
    for name, fn in tests:
        try:
            res = fn()
            if isinstance(res, list) or (isinstance(res, dict) and "bars" in res):
                print(f"✅ {name}: {res['source']}，{len(res['bars'])} 条")
            else:
                print(f"✅ {name}: {json.dumps(res, ensure_ascii=False)}")
            ok += 1
        except Exception as e:  # noqa: BLE001
            print(f"⚠️ {name}: 降级 —— {e}")
            bad += 1
    print(f"\n自检结果：{ok} 通过 / {bad} 降级。降级项按 README §四-⑥ 纪律在产出中标注。")

def main():
    p = argparse.ArgumentParser(description="data-layer 开源适配（AKShare 优先）")
    p.add_argument("--selftest", action="store_true", help="逐项自检（等价于 selftest 子命令）")
    sub = p.add_subparsers(dest="cmd")
    sp = sub.add_parser("index-quote"); sp.add_argument("symbol")
    sp = sub.add_parser("index-daily"); sp.add_argument("symbol"); sp.add_argument("--days", type=int, default=60)
    sp = sub.add_parser("index-pe"); sp.add_argument("name", nargs="?", default="沪深300")
    sub.add_parser("bond-10y")
    sp = sub.add_parser("quote"); sp.add_argument("code")
    sub.add_parser("selftest")
    a = p.parse_args()
    if a.cmd == "selftest" or a.cmd is None:
        selftest(); return
    try:
        if a.cmd == "index-quote":  res = index_quote(a.symbol)
        elif a.cmd == "index-daily": res = index_daily(a.symbol, a.days)
        elif a.cmd == "index-pe":   res = index_pe(a.name)
        elif a.cmd == "bond-10y":   res = bond_10y()
        elif a.cmd == "quote":      res = etf_quote(a.code)
        print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"error": str(e), "degraded": True,
                          "action": "换源或降级联网搜索，并在产出中标注"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
