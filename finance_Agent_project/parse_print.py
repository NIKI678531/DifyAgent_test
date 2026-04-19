def render_report(ticker: str, result: dict):
    print("\n=== AI Stock Analysis Report:", ticker.upper(), "===\n")
    print("Summary:")
    print(result.get("summary", "(no summary)"), "\n")

    print("Bullish Signals:")
    for s in result.get("bullish_signals", []):
        print("  •", s)
    print("\nBearish Signals:")
    for s in result.get("bearish_signals", []):
        print("  •", s)

    pt = result.get("price_target", {}) or {}
    base = pt.get("base")
    rng = pt.get("range")
    horizon = pt.get("time_horizon_days")
    print("\nPrice Target:")
    print(f"  Base: {base}  Range: {rng}  Horizon (days): {horizon}")

    conf = result.get("confidence")
    print(f"\nConfidence: {conf}")

    srcs = result.get("sources", [])
    if srcs:
        print("\nSources:")
        for u in srcs:
            print("  -", u)