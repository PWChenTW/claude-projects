# Feature Specification Template - Quantitative Trading

## FEATURE
[Describe the specific trading feature, strategy component, or analysis requirement in detail. Include mathematical formulas, risk parameters, and performance objectives.]

### Example:
```
Implement a mean reversion strategy that:
- Identifies overbought/oversold conditions using Bollinger Bands (2 std dev)
- Enters long positions when price < lower band and RSI < 30
- Enters short positions when price > upper band and RSI > 70
- Uses dynamic position sizing based on Kelly Criterion
- Implements stop-loss at 2% and take-profit at 5%
- Trades liquid stocks with >$1M daily volume
```

## EXAMPLES
[Reference existing strategy patterns, indicator implementations, or similar trading systems in the codebase.]

### Example:
```python
# Reference existing indicator calculation from indicators/technical.py
def calculate_bollinger_bands(prices, window=20, num_std=2):
    rolling_mean = prices.rolling(window).mean()
    rolling_std = prices.rolling(window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return upper_band, rolling_mean, lower_band

# Similar strategy pattern in strategies/momentum.py
class MomentumStrategy(BaseStrategy):
    def generate_signals(self, data):
        # Signal generation logic
        pass
```

## DOCUMENTATION
[List relevant financial libraries, API documentation, academic papers, and market data sources.]

### Example:
```
- TA-Lib documentation: https://mrjbq7.github.io/ta-lib/
- Backtrader framework: https://www.backtrader.com/docu/
- Interactive Brokers API: https://interactivebrokers.github.io/tws-api/
- Kelly Criterion paper: "A New Interpretation of Information Rate" (1956)
- Bollinger Bands: https://www.bollingerbands.com/bollinger-bands
- Risk management: "The Mathematics of Money Management" by Ralph Vince
- Market microstructure: "Trading and Exchanges" by Larry Harris
```

## OTHER CONSIDERATIONS
[Market-specific constraints, regulatory requirements, execution considerations, and risk management rules.]

### Example:
```
- Market hours: Strategy only trades during regular market hours (9:30 AM - 4:00 PM ET)
- Minimum capital: $25,000 (PDT rule compliance)
- Position limits: Max 5% of portfolio per position, max 20% sector exposure
- Slippage model: 0.1% for liquid stocks, 0.3% for small-caps
- Commission structure: $0.005 per share, min $1 per trade
- Data requirements: 1-minute bars for intraday, daily bars for signals
- Backtesting period: Minimum 5 years including 2008 crisis and COVID-19
- Risk metrics: Max drawdown < 15%, Sharpe ratio > 1.5
- Regulatory: Must comply with Reg T margin requirements
- Execution: Use VWAP orders for positions > $100k
```