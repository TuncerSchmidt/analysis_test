from fastapi import FastAPI
from tradingview_ta import TA_Handler, Interval

app = FastAPI()

# Sırasıyla denenecek ABD borsaları
EXCHANGES = [
    "NASDAQ",
    "NASDAQGS",
    "NASDAQCM",
    "NYSE",
    "AMEX"
]

def try_analysis(symbol, exchange):
    handler = TA_Handler(
        symbol=symbol.upper(),
        screener="america",
        exchange="NASDAQ",
        interval=Interval.INTERVAL_1_DAY
    )
    return handler.get_analysis()


def get_tv_analysis(symbol: str):

    # 1️⃣ Tüm borsaları sırayla dene
    # for ex in EXCHANGES:
    try:
        analysis = try_analysis(symbol, ex)
        return {
            "symbol": symbol.upper(),
            "exchange": ex,
            "summary": analysis.summary,
            "indicators": analysis.indicators
        }
    except Exception:
        continue  # sıradaki exchange’e geç

    # 2️⃣ Eğer hepsi hata verirse → fallback: exchange=None
    try:
        analysis = try_analysis(symbol, None)
        return {
            "symbol": symbol.upper(),
            "exchange": "AUTO",
            "summary": analysis.summary,
            "indicators": analysis.indicators
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/tradingview/{symbol}")
def tradingview_endpoint(symbol: str):
    return get_tv_analysis(symbol)
