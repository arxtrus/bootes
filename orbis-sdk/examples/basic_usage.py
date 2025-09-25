"""
Orbis SDK Basic Usage Example
"""

from orbis.sdk import OrbisSDK
from orbis.sdk.exceptions import OrbisSDKException


def main():
    print("=== Orbis SDK Basic Usage Example ===\n")

    # 1. Create SDK instance
    print("1. SDK Initialization")
    sdk = OrbisSDK()

    # Or create individual services
    # stock_service = StockService()
    # forex_service = ForexService()
    # crypto_service = CryptoService()

    print("✓ SDK initialization completed\n")

    # 2. Stock data example
    print("2. Stock Data Query")
    try:
        # AAPL 1-year daily data
        stock_data = sdk.stock.get_data("AAPL", interval="1d", period="1y")
        print(f"✓ AAPL data query completed: {len(stock_data)} records")
        print(f"  Recent data:\n{stock_data.tail(3)}\n")

        # Real-time stock quote
        quote = sdk.stock.get_quote("AAPL")
        print(
            f"✓ AAPL real-time info: ${quote['regularMarketPrice']} ({quote['regularMarketChangePercent']:.2f}%)\n"
        )

    except OrbisSDKException as e:
        print(f"✗ Stock data query error: {e}\n")

    # 3. Forex data example
    print("3. Forex Data Query")
    try:
        # USD-based exchange rates
        forex_data = sdk.forex.get_data("USD")
        print(
            f"✓ USD exchange rate query completed: {len(forex_data['rates'])} currencies"
        )
        print(f"  KRW: {forex_data['rates']['KRW']}")
        print(f"  EUR: {forex_data['rates']['EUR']}")
        print(f"  JPY: {forex_data['rates']['JPY']}\n")

        # Specific currency pair
        usd_krw = sdk.forex.get_rate("USD", "KRW")
        print(f"✓ USD/KRW: {usd_krw['rate']}\n")

    except OrbisSDKException as e:
        print(f"✗ Forex data query error: {e}\n")

    # 4. Cryptocurrency data example
    print("4. Cryptocurrency Data Query")
    try:
        # Bitcoin price
        bitcoin_data = sdk.crypto.get_data("bitcoin", vs_currency="usd")
        print(f"✓ Bitcoin price: ${bitcoin_data['price']:,.2f}")
        print(f"  24h change: {bitcoin_data['change_24h']:.2f}%")
        print(f"  Volume: ${bitcoin_data['volume_24h']:,.0f}\n")

        # Top 10 cryptocurrencies
        top_cryptos = sdk.crypto.get_top_cryptos(limit=5)
        print("✓ Top 5 cryptocurrencies:")
        for i, crypto in enumerate(top_cryptos, 1):
            print(
                f"  {i}. {crypto['name']} ({crypto['symbol'].upper()}): ${crypto['current_price']:,.2f}"
            )
        print()

    except OrbisSDKException as e:
        print(f"✗ Cryptocurrency data query error: {e}\n")

    # 5. Error handling example
    print("5. Error Handling Example")
    try:
        # Query with invalid symbol
        sdk.stock.get_data("INVALID_SYMBOL")
    except OrbisSDKException as e:
        print(f"✓ Expected error handling: {e.error_code} - {e.message}\n")

    print("=== Example Completed ===")


if __name__ == "__main__":
    main()
