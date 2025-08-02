# Risk Management Patterns

## Overview
Essential risk management patterns for quantitative trading systems, including position sizing, risk limits, and portfolio protection.

## Position Sizing

### Kelly Criterion Implementation

```python
import numpy as np
from typing import Dict, Optional

class KellyCriterion:
    """
    Kelly Criterion for optimal position sizing.
    f* = (p * b - q) / b
    where:
    - f* = fraction of capital to bet
    - p = probability of winning
    - b = net odds received on the bet (b to 1)
    - q = probability of losing (1 - p)
    """
    
    def __init__(self, max_kelly_fraction: float = 0.25):
        """
        Args:
            max_kelly_fraction: Maximum fraction of Kelly to use (default 0.25 for 1/4 Kelly)
        """
        self.max_kelly_fraction = max_kelly_fraction
    
    def calculate_position_size(self, 
                              win_probability: float,
                              win_return: float,
                              loss_return: float,
                              capital: float) -> float:
        """
        Calculate optimal position size using Kelly Criterion.
        
        Args:
            win_probability: Probability of winning trade
            win_return: Expected return on winning trade (as decimal, e.g., 0.05 for 5%)
            loss_return: Expected loss on losing trade (as positive decimal)
            capital: Total available capital
            
        Returns:
            Optimal position size in currency units
        """
        if win_probability <= 0 or win_probability >= 1:
            return 0.0
        
        # Calculate net odds
        b = win_return / loss_return
        p = win_probability
        q = 1 - p
        
        # Kelly formula
        kelly_fraction = (p * b - q) / b
        
        # Apply maximum Kelly fraction limit
        kelly_fraction = min(kelly_fraction, self.max_kelly_fraction)
        
        # Ensure non-negative
        kelly_fraction = max(0, kelly_fraction)
        
        return capital * kelly_fraction
    
    def calculate_from_historical(self,
                                returns: np.ndarray,
                                capital: float) -> float:
        """
        Calculate Kelly position size from historical returns.
        """
        winning_returns = returns[returns > 0]
        losing_returns = returns[returns < 0]
        
        if len(winning_returns) == 0 or len(losing_returns) == 0:
            return 0.0
        
        win_probability = len(winning_returns) / len(returns)
        avg_win = np.mean(winning_returns)
        avg_loss = np.mean(np.abs(losing_returns))
        
        return self.calculate_position_size(
            win_probability, avg_win, avg_loss, capital
        )
```

### Fixed Risk Position Sizing

```python
class FixedRiskPositionSizer:
    """
    Position sizing based on fixed risk per trade.
    """
    
    def __init__(self, risk_per_trade: float = 0.02):
        """
        Args:
            risk_per_trade: Maximum risk per trade as fraction of capital (default 2%)
        """
        self.risk_per_trade = risk_per_trade
    
    def calculate_position_size(self,
                              capital: float,
                              entry_price: float,
                              stop_loss_price: float,
                              commission_rate: float = 0.001) -> Dict[str, float]:
        """
        Calculate position size based on fixed risk amount.
        
        Returns:
            Dict containing position size, risk amount, and number of shares
        """
        risk_amount = capital * self.risk_per_trade
        
        # Calculate price difference including commission
        price_diff = abs(entry_price - stop_loss_price)
        total_cost_per_share = price_diff + (entry_price * commission_rate * 2)
        
        # Calculate number of shares
        num_shares = risk_amount / total_cost_per_share
        
        # Calculate position value
        position_value = num_shares * entry_price
        
        # Ensure position doesn't exceed capital
        if position_value > capital:
            num_shares = capital / entry_price
            position_value = capital
            actual_risk = num_shares * total_cost_per_share
        else:
            actual_risk = risk_amount
        
        return {
            'num_shares': int(num_shares),
            'position_value': position_value,
            'risk_amount': actual_risk,
            'risk_percentage': actual_risk / capital
        }
```

## Risk Limits and Controls

### Portfolio Risk Manager

```python
from dataclasses import dataclass
from typing import List, Tuple
import pandas as pd

@dataclass
class RiskLimits:
    """Risk limit configuration."""
    max_position_size: float = 0.1  # Max 10% per position
    max_sector_exposure: float = 0.3  # Max 30% per sector
    max_correlation_exposure: float = 0.5  # Max 50% in correlated assets
    max_leverage: float = 1.0  # No leverage by default
    max_drawdown: float = 0.15  # Max 15% drawdown
    max_var_95: float = 0.05  # Max 5% VaR at 95% confidence

class PortfolioRiskManager:
    """
    Comprehensive portfolio risk management system.
    """
    
    def __init__(self, risk_limits: RiskLimits):
        self.risk_limits = risk_limits
        self.positions = {}
        self.historical_returns = pd.DataFrame()
    
    def check_position_limit(self,
                           symbol: str,
                           position_value: float,
                           portfolio_value: float) -> Tuple[bool, str]:
        """Check if position size is within limits."""
        position_pct = position_value / portfolio_value
        
        if position_pct > self.risk_limits.max_position_size:
            return False, f"Position size {position_pct:.1%} exceeds limit {self.risk_limits.max_position_size:.1%}"
        
        return True, "Position size within limits"
    
    def check_sector_exposure(self,
                            sector: str,
                            additional_exposure: float,
                            portfolio_value: float) -> Tuple[bool, str]:
        """Check sector concentration limits."""
        current_sector_exposure = sum(
            pos['value'] for symbol, pos in self.positions.items()
            if pos.get('sector') == sector
        )
        
        total_exposure = (current_sector_exposure + additional_exposure) / portfolio_value
        
        if total_exposure > self.risk_limits.max_sector_exposure:
            return False, f"Sector exposure {total_exposure:.1%} exceeds limit {self.risk_limits.max_sector_exposure:.1%}"
        
        return True, "Sector exposure within limits"
    
    def calculate_portfolio_var(self,
                              confidence_level: float = 0.95) -> float:
        """
        Calculate portfolio Value at Risk (VaR).
        """
        if self.historical_returns.empty:
            return 0.0
        
        # Calculate portfolio returns
        portfolio_returns = self.historical_returns.sum(axis=1)
        
        # Calculate VaR
        var_percentile = (1 - confidence_level) * 100
        var = np.percentile(portfolio_returns, var_percentile)
        
        return abs(var)
    
    def check_drawdown_limit(self) -> Tuple[bool, str]:
        """Check if current drawdown exceeds limit."""
        if self.historical_returns.empty:
            return True, "No drawdown data available"
        
        cumulative_returns = (1 + self.historical_returns.sum(axis=1)).cumprod()
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max
        current_drawdown = drawdown.iloc[-1]
        
        if abs(current_drawdown) > self.risk_limits.max_drawdown:
            return False, f"Drawdown {abs(current_drawdown):.1%} exceeds limit {self.risk_limits.max_drawdown:.1%}"
        
        return True, f"Current drawdown: {abs(current_drawdown):.1%}"
    
    def get_risk_report(self) -> Dict[str, any]:
        """Generate comprehensive risk report."""
        portfolio_value = sum(pos['value'] for pos in self.positions.values())
        
        # Position concentration
        position_concentrations = {
            symbol: pos['value'] / portfolio_value
            for symbol, pos in self.positions.items()
        }
        
        # Sector concentration
        sector_exposure = {}
        for symbol, pos in self.positions.items():
            sector = pos.get('sector', 'Unknown')
            sector_exposure[sector] = sector_exposure.get(sector, 0) + pos['value']
        
        sector_concentrations = {
            sector: value / portfolio_value
            for sector, value in sector_exposure.items()
        }
        
        # Calculate metrics
        var_95 = self.calculate_portfolio_var(0.95)
        drawdown_check = self.check_drawdown_limit()
        
        return {
            'portfolio_value': portfolio_value,
            'position_count': len(self.positions),
            'largest_position': max(position_concentrations.values()) if position_concentrations else 0,
            'sector_concentrations': sector_concentrations,
            'var_95': var_95,
            'drawdown_status': drawdown_check[1],
            'risk_score': self._calculate_risk_score()
        }
    
    def _calculate_risk_score(self) -> float:
        """Calculate overall portfolio risk score (0-100)."""
        score = 100.0
        
        # Penalize for concentration
        if self.positions:
            portfolio_value = sum(pos['value'] for pos in self.positions.values())
            max_position_pct = max(pos['value'] / portfolio_value for pos in self.positions.values())
            score -= (max_position_pct / self.risk_limits.max_position_size) * 20
        
        # Penalize for drawdown
        if not self.historical_returns.empty:
            _, drawdown_msg = self.check_drawdown_limit()
            if "exceeds" in drawdown_msg:
                score -= 30
        
        return max(0, score)
```

## Stop Loss Management

### Dynamic Stop Loss

```python
class DynamicStopLoss:
    """
    Dynamic stop loss adjustment based on volatility and price action.
    """
    
    def __init__(self,
                initial_stop_percentage: float = 0.02,
                atr_multiplier: float = 2.0,
                trailing_stop_percentage: float = 0.03):
        self.initial_stop_percentage = initial_stop_percentage
        self.atr_multiplier = atr_multiplier
        self.trailing_stop_percentage = trailing_stop_percentage
    
    def calculate_initial_stop(self,
                             entry_price: float,
                             atr: float,
                             position_type: str = 'long') -> float:
        """
        Calculate initial stop loss based on ATR.
        """
        atr_stop_distance = atr * self.atr_multiplier
        percentage_stop_distance = entry_price * self.initial_stop_percentage
        
        # Use the larger of ATR-based or percentage-based stop
        stop_distance = max(atr_stop_distance, percentage_stop_distance)
        
        if position_type == 'long':
            return entry_price - stop_distance
        else:  # short position
            return entry_price + stop_distance
    
    def update_trailing_stop(self,
                           current_price: float,
                           current_stop: float,
                           highest_price: float,
                           position_type: str = 'long') -> Tuple[float, float]:
        """
        Update trailing stop loss.
        
        Returns:
            Tuple of (new_stop_price, new_highest_price)
        """
        if position_type == 'long':
            # Update highest price
            new_highest = max(highest_price, current_price)
            
            # Calculate new stop based on highest price
            new_stop = new_highest * (1 - self.trailing_stop_percentage)
            
            # Stop can only move up, never down
            new_stop = max(current_stop, new_stop)
            
        else:  # short position
            # Update lowest price for short position
            new_highest = min(highest_price, current_price)
            
            # Calculate new stop based on lowest price
            new_stop = new_highest * (1 + self.trailing_stop_percentage)
            
            # Stop can only move down for shorts, never up
            new_stop = min(current_stop, new_stop)
        
        return new_stop, new_highest
```

## Portfolio Protection Strategies

### Correlation-Based Risk Management

```python
class CorrelationRiskManager:
    """
    Manage portfolio risk based on asset correlations.
    """
    
    def __init__(self, lookback_period: int = 252):
        self.lookback_period = lookback_period
        self.correlation_matrix = None
    
    def calculate_correlations(self, returns_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate rolling correlation matrix."""
        self.correlation_matrix = returns_df.tail(self.lookback_period).corr()
        return self.correlation_matrix
    
    def identify_correlation_clusters(self,
                                    threshold: float = 0.7) -> List[List[str]]:
        """
        Identify groups of highly correlated assets.
        """
        if self.correlation_matrix is None:
            return []
        
        clusters = []
        processed = set()
        
        for asset1 in self.correlation_matrix.index:
            if asset1 in processed:
                continue
            
            cluster = [asset1]
            
            for asset2 in self.correlation_matrix.columns:
                if asset2 != asset1 and asset2 not in processed:
                    if abs(self.correlation_matrix.loc[asset1, asset2]) > threshold:
                        cluster.append(asset2)
                        processed.add(asset2)
            
            if len(cluster) > 1:
                clusters.append(cluster)
                processed.add(asset1)
        
        return clusters
    
    def calculate_portfolio_correlation_risk(self,
                                           positions: Dict[str, float]) -> float:
        """
        Calculate overall portfolio correlation risk score.
        """
        if self.correlation_matrix is None or len(positions) < 2:
            return 0.0
        
        # Calculate weighted correlation
        position_symbols = list(positions.keys())
        total_value = sum(positions.values())
        
        weighted_correlation = 0.0
        weight_sum = 0.0
        
        for i, symbol1 in enumerate(position_symbols):
            for j, symbol2 in enumerate(position_symbols):
                if i < j and symbol1 in self.correlation_matrix.index and symbol2 in self.correlation_matrix.columns:
                    weight1 = positions[symbol1] / total_value
                    weight2 = positions[symbol2] / total_value
                    
                    correlation = self.correlation_matrix.loc[symbol1, symbol2]
                    weighted_correlation += weight1 * weight2 * abs(correlation)
                    weight_sum += weight1 * weight2
        
        return weighted_correlation / weight_sum if weight_sum > 0 else 0.0
```

### Maximum Drawdown Protection

```python
class DrawdownProtection:
    """
    Protect portfolio from excessive drawdowns.
    """
    
    def __init__(self,
                max_drawdown_limit: float = 0.15,
                recovery_threshold: float = 0.05):
        self.max_drawdown_limit = max_drawdown_limit
        self.recovery_threshold = recovery_threshold
        self.peak_value = 0
        self.in_drawdown_protection = False
    
    def update(self, portfolio_value: float) -> Dict[str, any]:
        """
        Update drawdown protection status.
        
        Returns:
            Dict with protection status and recommendations
        """
        # Update peak value
        if portfolio_value > self.peak_value:
            self.peak_value = portfolio_value
            
        # Calculate current drawdown
        current_drawdown = (self.peak_value - portfolio_value) / self.peak_value
        
        recommendations = {
            'reduce_positions': False,
            'stop_trading': False,
            'position_size_multiplier': 1.0,
            'status_message': ''
        }
        
        # Check if entering drawdown protection
        if current_drawdown >= self.max_drawdown_limit and not self.in_drawdown_protection:
            self.in_drawdown_protection = True
            recommendations['stop_trading'] = True
            recommendations['status_message'] = f"Maximum drawdown limit reached: {current_drawdown:.1%}"
            
        # Check if still in drawdown protection
        elif self.in_drawdown_protection:
            recovery_level = self.peak_value * (1 - self.recovery_threshold)
            
            if portfolio_value >= recovery_level:
                self.in_drawdown_protection = False
                recommendations['status_message'] = "Drawdown protection lifted - normal trading resumed"
            else:
                recommendations['reduce_positions'] = True
                recommendations['position_size_multiplier'] = 0.5
                recommendations['status_message'] = f"In drawdown protection mode - reduced position sizing"
                
        # Warning zone
        elif current_drawdown >= self.max_drawdown_limit * 0.8:
            recommendations['position_size_multiplier'] = 0.75
            recommendations['status_message'] = f"Approaching drawdown limit: {current_drawdown:.1%}"
        
        else:
            recommendations['status_message'] = f"Normal operation - Drawdown: {current_drawdown:.1%}"
        
        return {
            'current_drawdown': current_drawdown,
            'peak_value': self.peak_value,
            'in_protection': self.in_drawdown_protection,
            'recommendations': recommendations
        }
```

## Best Practices

1. **Never risk more than you can afford to lose** - Use strict position sizing
2. **Diversify across uncorrelated assets** - Monitor correlation clusters
3. **Use multiple risk metrics** - Don't rely on a single measure
4. **Implement pre-trade risk checks** - Validate all trades before execution
5. **Monitor real-time risk exposure** - Track portfolio risk continuously
6. **Use stop losses consistently** - Every position should have an exit plan
7. **Scale down in drawdowns** - Reduce risk when losing
8. **Regularly stress test** - Simulate extreme market conditions
9. **Document risk events** - Learn from risk management failures
10. **Automate risk controls** - Remove emotional decision-making