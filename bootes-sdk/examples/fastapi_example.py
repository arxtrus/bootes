"""
FastAPI integration example with bootes SDK
"""

import uvicorn
from bootes.sdk import BootesSDK
from bootes.sdk.exceptions import BootesSDKException
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    title="bootes Financial Data API",
    description="Financial data API using bootes SDK",
    version="1.0.0",
)

# Initialize SDK instance
sdk = BootesSDK()


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "bootes Financial Data API",
        "version": "1.0.0",
        "services": ["stock", "forex", "crypto"],
    }


# Stock-related endpoints
@app.get("/stock/{symbol}")
async def get_stock_data(
    symbol: str,
    interval: str = Query(
        "1d", description="Data interval (1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo)"
    ),
    period: str = Query(
        "1y",
        description="Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)",
    ),
):
    """Retrieve stock OHLCV data"""
    try:
        data = sdk.stock.get_data(symbol, interval=interval, period=period)

        # Convert DataFrame to JSON format
        result = {
            "symbol": symbol,
            "interval": interval,
            "period": period,
            "data_count": len(data),
            "data": data.reset_index().to_dict("records"),
        }

        return result

    except BootesSDKException as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}") from e


@app.get("/stock/{symbol}/quote")
async def get_stock_quote(symbol: str):
    """Retrieve real-time stock quote"""
    try:
        data = sdk.stock.get_quote(symbol)
        return data

    except BootesSDKException as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}") from e


# Forex-related endpoints
@app.get("/forex/rates")
async def get_forex_rates(
    base_currency: str = Query("USD", description="Base currency code"),
):
    """Retrieve exchange rate data"""
    try:
        data = sdk.forex.get_data(base_currency)
        return data

    except BootesSDKException as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}") from e


@app.get("/forex/rate")
async def get_forex_rate(
    from_currency: str = Query(..., description="From currency code"),
    to_currency: str = Query(..., description="To currency code"),
):
    """Retrieve exchange rate for specific currency pair"""
    try:
        data = sdk.forex.get_rate(from_currency, to_currency)
        return data

    except BootesSDKException as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}") from e


@app.get("/forex/major-pairs")
async def get_major_forex_pairs():
    """Retrieve exchange rates for major currency pairs"""
    try:
        data = sdk.forex.get_major_pairs()
        return data

    except BootesSDKException as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}") from e


# Cryptocurrency-related endpoints
@app.get("/crypto/{symbol}")
async def get_crypto_price(
    symbol: str,
    vs_currency: str = Query("usd", description="VS currency (usd, krw, eur, etc.)"),
):
    """Retrieve cryptocurrency price"""
    try:
        data = sdk.crypto.get_data(symbol, vs_currency=vs_currency)
        return data

    except BootesSDKException as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}") from e


@app.get("/crypto/{symbol}/market")
async def get_crypto_market_data(
    symbol: str, vs_currency: str = Query("usd", description="VS currency")
):
    """Retrieve detailed cryptocurrency market data"""
    try:
        data = sdk.crypto.get_market_data(symbol, vs_currency=vs_currency)
        return data

    except BootesSDKException as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}") from e


@app.get("/crypto/top")
async def get_top_cryptos(
    vs_currency: str = Query("usd", description="VS currency"),
    limit: int = Query(10, ge=1, le=250, description="Number of results"),
):
    """Retrieve top cryptocurrencies by market cap"""
    try:
        data = sdk.crypto.get_top_cryptos(vs_currency=vs_currency, limit=limit)
        return {"vs_currency": vs_currency, "limit": limit, "data": data}

    except BootesSDKException as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}") from e


@app.get("/crypto/search")
async def search_crypto(q: str = Query(..., min_length=2, description="Search query")):
    """Search cryptocurrencies"""
    try:
        data = sdk.crypto.search_crypto(q)
        return {"query": q, "results": data}

    except BootesSDKException as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}") from e


@app.exception_handler(BootesSDKException)
async def bootes_exception_handler(request, exc: BootesSDKException):
    """bootes SDK exception handler"""
    return HTTPException(
        status_code=400,
        detail={
            "error": exc.error_code,
            "message": exc.message,
            "details": exc.details,
        },
    )


if __name__ == "__main__":
    uvicorn.run("fastapi_example:app", host="0.0.0.0", port=8000, reload=True)
