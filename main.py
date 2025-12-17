from fastapi import FastAPI
from tradingview_ta import TA_Handler, Interval

app = FastAPI()

def get_tv_analysis(symbol: str):
    try:
        handler = TA_Handler(
            symbol=symbol.upper(),
            exchange="NASDAQ",
            screener="america",
            interval=Interval.INTERVAL_1_DAY
        )

        analysis = handler.get_analysis()

        return {
            "symbol": symbol.upper(),
            "summary": analysis.summary,
            "indicators": analysis.indicators
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/tradingview/{symbol}")
def tradingview_endpoint(symbol: str):
    return get_tv_analysis(symbol)
