# 量化交易機器學習最佳實踐指南

## 🚨 關鍵原則：時序數據的特殊性

在量化交易中，數據具有強烈的時序特性。違反時序完整性的模型在回測中可能表現優異，但在實盤交易中必定失敗。

## 1. 數據分割原則

### ❌ 絕對禁止
```python
# 錯誤：隨機分割
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 錯誤：標準 K-fold
from sklearn.model_selection import KFold
kf = KFold(n_splits=5, shuffle=True)
```

### ✅ 正確做法
```python
# 正確：時序分割
def temporal_train_test_split(data, train_ratio=0.7, val_ratio=0.15):
    n = len(data)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))
    
    train = data.iloc[:train_end]
    val = data.iloc[train_end:val_end]
    test = data.iloc[val_end:]
    
    return train, val, test

# 正確：時序交叉驗證
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5)
for train_idx, test_idx in tscv.split(X):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    # 訓練和評估
```

## 2. 特徵工程準則

### 避免未來信息洩漏

#### ❌ 常見錯誤
```python
# 錯誤1：使用未來數據的移動平均
df['sma'] = df['price'].rolling(window=20, center=True).mean()  # center=True 包含未來

# 錯誤2：使用全局統計量
df['normalized'] = (df['value'] - df['value'].mean()) / df['value'].std()

# 錯誤3：錯誤的標籤創建
df['target'] = df['price'].shift(-1) / df['price'] - 1  # 應該考慮可交易性
df['signal'] = df['indicator']  # 沒有延遲，假設即時可用
```

#### ✅ 正確做法
```python
# 正確1：只使用歷史數據
df['sma'] = df['price'].rolling(window=20, min_periods=20).mean()

# 正確2：使用擴展窗口或滾動窗口
df['normalized'] = df['value'].expanding().apply(
    lambda x: (x.iloc[-1] - x.mean()) / x.std() if len(x) > 1 else 0
)

# 正確3：考慮實際可交易時間
df['target'] = df['price'].shift(-2) / df['price'].shift(-1) - 1  # T+1 交易
df['signal'] = df['indicator'].shift(1)  # 信號延遲
```

### Point-in-Time 數據處理

```python
class PointInTimeFeatureEngine:
    """確保特徵計算的時間一致性"""
    
    def __init__(self):
        self.feature_history = {}
    
    def calculate_features(self, data, timestamp):
        """只使用timestamp之前的數據計算特徵"""
        historical_data = data[data.index < timestamp]
        
        if len(historical_data) < 20:  # 最小數據要求
            return None
            
        features = {
            'sma_20': historical_data['price'].tail(20).mean(),
            'std_20': historical_data['returns'].tail(20).std(),
            'volume_ratio': historical_data['volume'].tail(5).mean() / 
                          historical_data['volume'].tail(20).mean()
        }
        
        self.feature_history[timestamp] = features
        return features
```

## 3. 模型訓練最佳實踐

### Walk-Forward Analysis

```python
class WalkForwardValidator:
    """滾動窗口驗證"""
    
    def __init__(self, window_size=252, step_size=21, min_train_size=504):
        self.window_size = window_size
        self.step_size = step_size
        self.min_train_size = min_train_size
    
    def validate(self, data, model_class, feature_cols, target_col):
        results = []
        
        for i in range(self.min_train_size, len(data) - self.window_size, self.step_size):
            # 訓練集：從開始到當前位置
            train_data = data.iloc[:i]
            # 測試集：未來一個窗口
            test_data = data.iloc[i:i + self.window_size]
            
            # 訓練模型
            model = model_class()
            model.fit(train_data[feature_cols], train_data[target_col])
            
            # 預測
            predictions = model.predict(test_data[feature_cols])
            
            # 評估
            results.append({
                'train_end': train_data.index[-1],
                'test_start': test_data.index[0],
                'test_end': test_data.index[-1],
                'predictions': predictions,
                'actuals': test_data[target_col].values
            })
        
        return results
```

### 防止過擬合

```python
class RobustModelTrainer:
    """穩健的模型訓練器"""
    
    def __init__(self):
        self.models = []
        self.feature_importance = {}
    
    def train_ensemble(self, X_train, y_train, X_val, y_val):
        """訓練集成模型以提高穩健性"""
        
        # 1. 簡單線性模型（基準）
        from sklearn.linear_model import LinearRegression
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        self.models.append(('linear', lr))
        
        # 2. 正則化模型（防止過擬合）
        from sklearn.linear_model import Ridge, Lasso
        ridge = Ridge(alpha=1.0)
        ridge.fit(X_train, y_train)
        self.models.append(('ridge', ridge))
        
        # 3. 樹模型（有深度限制）
        from sklearn.ensemble import RandomForestRegressor
        rf = RandomForestRegressor(
            max_depth=5,  # 限制深度
            n_estimators=100,
            min_samples_leaf=50,  # 防止過擬合
            random_state=42
        )
        rf.fit(X_train, y_train)
        self.models.append(('rf', rf))
        
        # 4. 評估驗證集表現
        val_scores = {}
        for name, model in self.models:
            val_pred = model.predict(X_val)
            val_score = self._calculate_sharpe(y_val, val_pred)
            val_scores[name] = val_score
            
        # 5. 選擇最穩健的模型
        best_model = min(val_scores, key=lambda x: abs(val_scores[x] - 1.0))
        return self.models, val_scores, best_model
    
    def _calculate_sharpe(self, returns, predictions):
        """計算夏普比率"""
        strategy_returns = returns * np.sign(predictions)
        return np.sqrt(252) * strategy_returns.mean() / strategy_returns.std()
```

## 4. 模型評估準則

### 正確的評估指標

```python
class QuantMetrics:
    """量化交易專用評估指標"""
    
    @staticmethod
    def calculate_metrics(returns, predictions):
        """計算完整的評估指標"""
        
        # 方向準確率
        direction_accuracy = np.mean(np.sign(returns) == np.sign(predictions))
        
        # 策略收益
        strategy_returns = returns * np.sign(predictions)
        
        # 夏普比率
        sharpe = np.sqrt(252) * strategy_returns.mean() / strategy_returns.std()
        
        # 最大回撤
        cumulative = (1 + strategy_returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Calmar比率
        annual_return = strategy_returns.mean() * 252
        calmar = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0
        
        return {
            'direction_accuracy': direction_accuracy,
            'sharpe_ratio': sharpe,
            'max_drawdown': max_drawdown,
            'calmar_ratio': calmar,
            'annual_return': annual_return,
            'annual_volatility': strategy_returns.std() * np.sqrt(252)
        }
```

## 5. 實盤部署檢查清單

### 部署前驗證

```python
class DeploymentValidator:
    """部署前的最終檢查"""
    
    def validate_model_for_production(self, model, test_data):
        """生產環境部署前的驗證"""
        
        checks = {
            'data_dependency': self._check_data_dependencies(model),
            'latency': self._check_inference_latency(model, test_data),
            'stability': self._check_prediction_stability(model, test_data),
            'feature_availability': self._check_feature_availability(model),
            'error_handling': self._check_error_handling(model, test_data)
        }
        
        all_passed = all(checks.values())
        
        return {
            'ready_for_production': all_passed,
            'checks': checks,
            'warnings': self._generate_warnings(checks)
        }
    
    def _check_data_dependencies(self, model):
        """檢查數據依賴是否合理"""
        # 確保模型不依賴於未來數據
        # 檢查特徵計算的時間複雜度
        return True
    
    def _check_inference_latency(self, model, test_data):
        """檢查推理延遲"""
        import time
        sample = test_data.iloc[0:1]
        
        start = time.time()
        for _ in range(100):
            _ = model.predict(sample)
        latency = (time.time() - start) / 100
        
        return latency < 0.001  # 1ms 閾值
    
    def _check_prediction_stability(self, model, test_data):
        """檢查預測穩定性"""
        predictions = []
        for _ in range(10):
            pred = model.predict(test_data)
            predictions.append(pred)
        
        # 檢查預測是否一致
        variance = np.var(predictions, axis=0).mean()
        return variance < 1e-6
```

## 6. 常見陷阱與解決方案

### 陷阱1：Survivorship Bias（倖存者偏差）
- **問題**：只使用當前存在的股票數據
- **解決**：包含已退市股票的歷史數據

### 陷阱2：Transaction Cost（交易成本）
- **問題**：忽略手續費和滑點
- **解決**：在回測中加入現實的成本模型

### 陷阱3：Market Impact（市場衝擊）
- **問題**：假設可以以歷史價格無限交易
- **解決**：根據流動性調整倉位大小

### 陷阱4：Regime Change（市場狀態改變）
- **問題**：模型在新市場環境失效
- **解決**：定期重新訓練，監控模型表現

## 7. 監控與維護

```python
class ModelMonitor:
    """生產環境模型監控"""
    
    def __init__(self, model, baseline_metrics):
        self.model = model
        self.baseline_metrics = baseline_metrics
        self.performance_history = []
    
    def monitor_performance(self, new_data, predictions, actuals):
        """監控模型表現"""
        
        current_metrics = QuantMetrics.calculate_metrics(actuals, predictions)
        
        # 性能退化檢測
        degradation = self._detect_degradation(current_metrics)
        
        # 數據漂移檢測
        data_drift = self._detect_data_drift(new_data)
        
        # 預測分布變化
        prediction_drift = self._detect_prediction_drift(predictions)
        
        alert = degradation or data_drift or prediction_drift
        
        return {
            'timestamp': pd.Timestamp.now(),
            'metrics': current_metrics,
            'degradation': degradation,
            'data_drift': data_drift,
            'prediction_drift': prediction_drift,
            'alert': alert,
            'recommendation': self._get_recommendation(alert, degradation, data_drift)
        }
    
    def _detect_degradation(self, current_metrics):
        """檢測性能退化"""
        sharpe_degradation = (
            current_metrics['sharpe_ratio'] < 
            self.baseline_metrics['sharpe_ratio'] * 0.7
        )
        return sharpe_degradation
    
    def _get_recommendation(self, alert, degradation, drift):
        """生成建議"""
        if alert:
            if degradation and drift:
                return "立即停止交易，需要重新訓練模型"
            elif degradation:
                return "降低倉位，監控後續表現"
            elif drift:
                return "數據分布改變，考慮重新訓練"
        return "模型運行正常"
```

## 總結

成功的量化交易機器學習模型必須：

1. **嚴格遵守時序完整性**：永遠不使用未來信息
2. **充分驗證**：使用 Walk-forward 分析和樣本外測試
3. **保持簡單**：複雜模型容易過擬合
4. **持續監控**：市場是動態的，模型需要適應
5. **風險管理**：永遠不要完全依賴單一模型

記住：在量化交易中，一個在回測中表現平庸但穩健的模型，往往比一個回測完美但過擬合的模型更有價值。