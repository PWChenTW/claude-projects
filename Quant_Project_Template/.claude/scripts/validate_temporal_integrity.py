#!/usr/bin/env python3
"""
時序數據完整性驗證器
用於檢測量化交易模型中的常見時序問題
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
import warnings
from datetime import datetime, timedelta

class TemporalIntegrityValidator:
    """時序數據完整性驗證器"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.issues = []
        
    def validate_train_test_split(self, 
                                 train_data: pd.DataFrame, 
                                 val_data: pd.DataFrame = None,
                                 test_data: pd.DataFrame = None) -> Dict[str, Any]:
        """
        驗證訓練/驗證/測試集分割是否正確
        
        Returns:
            Dict containing validation results
        """
        results = {
            'valid': True,
            'issues': [],
            'warnings': []
        }
        
        # 檢查時間索引
        if not isinstance(train_data.index, pd.DatetimeIndex):
            results['issues'].append("訓練集沒有使用 DatetimeIndex")
            results['valid'] = False
            
        # 檢查時序順序
        train_end = train_data.index.max()
        
        if val_data is not None:
            val_start = val_data.index.min()
            val_end = val_data.index.max()
            
            if val_start <= train_end:
                results['issues'].append(
                    f"驗證集開始時間 ({val_start}) 早於或等於訓練集結束時間 ({train_end})"
                )
                results['valid'] = False
                
        if test_data is not None:
            test_start = test_data.index.min()
            
            if val_data is not None:
                if test_start <= val_end:
                    results['issues'].append(
                        f"測試集開始時間 ({test_start}) 早於或等於驗證集結束時間 ({val_end})"
                    )
                    results['valid'] = False
            else:
                if test_start <= train_end:
                    results['issues'].append(
                        f"測試集開始時間 ({test_start}) 早於或等於訓練集結束時間 ({train_end})"
                    )
                    results['valid'] = False
                    
        # 檢查數據重疊
        if val_data is not None:
            overlap = set(train_data.index) & set(val_data.index)
            if overlap:
                results['issues'].append(
                    f"訓練集和驗證集有 {len(overlap)} 個重疊的時間點"
                )
                results['valid'] = False
                
        if test_data is not None:
            if val_data is not None:
                overlap = set(val_data.index) & set(test_data.index)
                if overlap:
                    results['issues'].append(
                        f"驗證集和測試集有 {len(overlap)} 個重疊的時間點"
                    )
                    results['valid'] = False
                    
            overlap = set(train_data.index) & set(test_data.index)
            if overlap:
                results['issues'].append(
                    f"訓練集和測試集有 {len(overlap)} 個重疊的時間點"
                )
                results['valid'] = False
                
        # 建議的分割比例
        total_size = len(train_data)
        if val_data is not None:
            total_size += len(val_data)
        if test_data is not None:
            total_size += len(test_data)
            
        train_ratio = len(train_data) / total_size
        
        if train_ratio < 0.6:
            results['warnings'].append(
                f"訓練集比例 ({train_ratio:.1%}) 可能太小，建議至少 60%"
            )
        elif train_ratio > 0.8:
            results['warnings'].append(
                f"訓練集比例 ({train_ratio:.1%}) 可能太大，建議保留足夠的驗證/測試數據"
            )
            
        if self.verbose:
            self._print_results("訓練/測試集分割驗證", results)
            
        return results
        
    def check_look_ahead_bias(self, 
                             data: pd.DataFrame,
                             feature_columns: List[str],
                             target_column: str = None) -> Dict[str, Any]:
        """
        檢測潛在的前視偏差
        
        Args:
            data: 包含特徵的數據
            feature_columns: 特徵列名
            target_column: 目標列名（可選）
            
        Returns:
            Dict containing potential look-ahead bias issues
        """
        results = {
            'valid': True,
            'suspicious_features': [],
            'warnings': []
        }
        
        for col in feature_columns:
            if col not in data.columns:
                continue
                
            # 檢查是否使用了未來數據的跡象
            # 1. 檢查完美預測
            if target_column and target_column in data.columns:
                correlation = data[col].corr(data[target_column])
                if abs(correlation) > 0.99:
                    results['suspicious_features'].append({
                        'feature': col,
                        'issue': f'與目標變量相關性過高 ({correlation:.3f})',
                        'severity': 'HIGH'
                    })
                    results['valid'] = False
                    
            # 2. 檢查不合理的平滑度
            if len(data) > 100:
                # 計算自相關
                autocorr = data[col].autocorr(1)
                if autocorr > 0.999:
                    results['warnings'].append({
                        'feature': col,
                        'issue': f'自相關過高 ({autocorr:.3f})，可能使用了中心化窗口',
                        'severity': 'MEDIUM'
                    })
                    
            # 3. 檢查未來值洩漏
            # 通過檢查特徵值是否"預知"了未來的變化
            if len(data) > 20:
                future_corr = data[col].shift(-1).corr(data[col])
                if future_corr > 0.95:
                    results['warnings'].append({
                        'feature': col,
                        'issue': f'與未來值相關性過高 ({future_corr:.3f})',
                        'severity': 'MEDIUM'
                    })
                    
        if self.verbose:
            self._print_results("前視偏差檢測", results)
            
        return results
        
    def validate_feature_calculation(self, 
                                    data: pd.DataFrame,
                                    feature_func: callable,
                                    window_size: int = None) -> Dict[str, Any]:
        """
        驗證特徵計算是否符合時序要求
        
        Args:
            data: 原始數據
            feature_func: 特徵計算函數
            window_size: 窗口大小（如適用）
            
        Returns:
            Dict containing validation results
        """
        results = {
            'valid': True,
            'issues': []
        }
        
        # 測試特徵計算在不同時間點的一致性
        test_points = [len(data)//4, len(data)//2, 3*len(data)//4]
        
        for point in test_points:
            # 使用截斷的數據計算特徵
            truncated_data = data.iloc[:point]
            try:
                feature_truncated = feature_func(truncated_data)
                
                # 使用完整數據計算，然後截斷
                feature_full = feature_func(data)
                if isinstance(feature_full, pd.Series):
                    feature_full_truncated = feature_full.iloc[:point]
                else:
                    feature_full_truncated = feature_full[:point]
                
                # 比較結果
                if not np.allclose(feature_truncated, feature_full_truncated, rtol=1e-5):
                    results['issues'].append(
                        f"特徵計算在時間點 {point} 不一致，可能使用了未來數據"
                    )
                    results['valid'] = False
                    
            except Exception as e:
                results['issues'].append(f"特徵計算失敗: {str(e)}")
                results['valid'] = False
                
        if self.verbose:
            self._print_results("特徵計算驗證", results)
            
        return results
        
    def check_data_leakage(self, 
                          X_train: pd.DataFrame,
                          X_test: pd.DataFrame,
                          threshold: float = 0.001) -> Dict[str, Any]:
        """
        檢測訓練集和測試集之間的數據洩漏
        
        Args:
            X_train: 訓練特徵
            X_test: 測試特徵
            threshold: 相似度閾值
            
        Returns:
            Dict containing leakage detection results
        """
        results = {
            'valid': True,
            'duplicate_rows': 0,
            'similar_rows': 0,
            'suspicious_columns': []
        }
        
        # 檢查完全重複的行
        train_set = set(map(tuple, X_train.values))
        test_set = set(map(tuple, X_test.values))
        duplicates = train_set & test_set
        
        if duplicates:
            results['duplicate_rows'] = len(duplicates)
            results['valid'] = False
            results['issues'] = [f"發現 {len(duplicates)} 個完全重複的數據行"]
            
        # 檢查每列的統計特性
        for col in X_train.columns:
            if col not in X_test.columns:
                continue
                
            # 檢查是否有完全相同的值分布
            train_unique = X_train[col].nunique()
            test_unique = X_test[col].nunique()
            
            if train_unique == 1 and test_unique == 1:
                if X_train[col].iloc[0] == X_test[col].iloc[0]:
                    results['suspicious_columns'].append({
                        'column': col,
                        'issue': '訓練集和測試集的值完全相同'
                    })
                    
        if self.verbose:
            self._print_results("數據洩漏檢測", results)
            
        return results
        
    def validate_cross_validation(self, 
                                cv_splits: List[Tuple[np.ndarray, np.ndarray]],
                                time_index: pd.DatetimeIndex = None) -> Dict[str, Any]:
        """
        驗證交叉驗證是否符合時序要求
        
        Args:
            cv_splits: 交叉驗證分割 [(train_idx, test_idx), ...]
            time_index: 時間索引
            
        Returns:
            Dict containing CV validation results
        """
        results = {
            'valid': True,
            'issues': [],
            'warnings': []
        }
        
        for i, (train_idx, test_idx) in enumerate(cv_splits):
            # 檢查時序順序
            if time_index is not None:
                train_times = time_index[train_idx]
                test_times = time_index[test_idx]
                
                if train_times.max() >= test_times.min():
                    results['issues'].append(
                        f"第 {i+1} 折: 訓練集包含測試集之後的數據"
                    )
                    results['valid'] = False
                    
            # 檢查數據重疊
            overlap = set(train_idx) & set(test_idx)
            if overlap:
                results['issues'].append(
                    f"第 {i+1} 折: 訓練集和測試集有 {len(overlap)} 個重疊樣本"
                )
                results['valid'] = False
                
        # 檢查是否為時序交叉驗證（後面的折應該使用更多的訓練數據）
        train_sizes = [len(train_idx) for train_idx, _ in cv_splits]
        if not all(train_sizes[i] <= train_sizes[i+1] for i in range(len(train_sizes)-1)):
            results['warnings'].append(
                "交叉驗證折的訓練集大小不是遞增的，可能不是時序交叉驗證"
            )
            
        if self.verbose:
            self._print_results("交叉驗證檢查", results)
            
        return results
        
    def _print_results(self, title: str, results: Dict[str, Any]):
        """打印驗證結果"""
        print(f"\n{'='*50}")
        print(f"{title}")
        print('='*50)
        
        if results['valid']:
            print("✅ 通過驗證")
        else:
            print("❌ 發現問題:")
            if 'issues' in results:
                for issue in results['issues']:
                    print(f"  - {issue}")
                    
        if 'warnings' in results and results['warnings']:
            print("\n⚠️ 警告:")
            for warning in results['warnings']:
                if isinstance(warning, dict):
                    print(f"  - {warning['feature']}: {warning['issue']}")
                else:
                    print(f"  - {warning}")
                    
        if 'suspicious_features' in results and results['suspicious_features']:
            print("\n🔍 可疑特徵:")
            for feat in results['suspicious_features']:
                print(f"  - {feat['feature']}: {feat['issue']} [{feat['severity']}]")
                
        if 'suspicious_columns' in results and results['suspicious_columns']:
            print("\n🔍 可疑列:")
            for col in results['suspicious_columns']:
                print(f"  - {col['column']}: {col['issue']}")
                

def example_usage():
    """使用範例"""
    # 創建示例數據
    dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
    n = len(dates)
    
    # 創建帶有時序特性的數據
    data = pd.DataFrame({
        'price': 100 + np.cumsum(np.random.randn(n) * 0.5),
        'volume': np.random.exponential(1000, n),
        'returns': np.random.randn(n) * 0.01
    }, index=dates)
    
    # 添加一些特徵
    data['sma_20'] = data['price'].rolling(20).mean()  # 正確
    data['future_leak'] = data['price'].shift(-1)  # 錯誤：未來數據洩漏
    
    # 分割數據
    train_end = '2022-12-31'
    val_end = '2023-06-30'
    
    train_data = data[data.index <= train_end]
    val_data = data[(data.index > train_end) & (data.index <= val_end)]
    test_data = data[data.index > val_end]
    
    # 創建驗證器
    validator = TemporalIntegrityValidator(verbose=True)
    
    # 1. 驗證訓練/測試分割
    split_results = validator.validate_train_test_split(train_data, val_data, test_data)
    
    # 2. 檢查前視偏差
    feature_cols = ['sma_20', 'future_leak', 'volume']
    bias_results = validator.check_look_ahead_bias(
        train_data, 
        feature_cols, 
        target_column='returns'
    )
    
    # 3. 檢查數據洩漏
    X_train = train_data[['sma_20', 'volume']]
    X_test = test_data[['sma_20', 'volume']]
    leakage_results = validator.check_data_leakage(X_train, X_test)
    
    # 總結
    print("\n" + "="*50)
    print("驗證總結")
    print("="*50)
    
    all_valid = (split_results['valid'] and 
                bias_results['valid'] and 
                leakage_results['valid'])
    
    if all_valid:
        print("✅ 所有驗證通過！數據處理符合時序要求。")
    else:
        print("❌ 發現時序數據問題，請修正後再進行模型訓練。")
        

if __name__ == "__main__":
    example_usage()