# Vietnamese stock data utilities using vnquant

from typing import Annotated, Optional
from pandas import DataFrame
import pandas as pd
from functools import wraps
from vnquant.data import DataLoader, FinanceLoader

from .utils import save_output, SavePathType

class VNQuantUtils:
    """Utility class for retrieving Vietnamese stock data via vnquant"""

    @staticmethod
    def is_vn_stock(symbol: str) -> bool:
        """Determine if a symbol represents a Vietnamese stock."""
        symbol = symbol.upper()
        return (len(symbol) <= 3 and symbol.isalpha()) or symbol.endswith(('HNX', 'UPC'))
    
    @staticmethod
    def get_stock_data(
        symbol: Annotated[str, "ticker symbol"],
        start_date: Annotated[str, "start date for retrieving stock price data, YYYY-mm-dd"],
        end_date: Annotated[str, "end date for retrieving stock price data, YYYY-mm-dd"],
        save_path: SavePathType = None,
    ) -> DataFrame:
        """Retrieve stock price data for designated Vietnamese ticker symbol"""
        symbol = symbol.upper()
        
        try:
            # Initialize DataLoader with the specified parameters
            loader = DataLoader(
                symbols=symbol, 
                start=start_date, 
                end=end_date, 
                data_source='vnd'
            )
            
            # Download the data
            stock_data = loader.download()
            
            # Extract data for the symbol
            if isinstance(stock_data.columns, pd.MultiIndex):
                if symbol in stock_data.columns.levels[0]:
                    stock_data = stock_data[symbol]
            
            # Rename columns to match yfinance format
            column_mapping = {
                'high': 'High',
                'low': 'Low',
                'open': 'Open',
                'close': 'Close',
                'volume': 'Volume',
                'adjust': 'Adj Close'
            }
            
            stock_data = stock_data.rename(columns={c.lower(): column_mapping.get(c.lower(), c) 
                                                 for c in stock_data.columns})
            
            if save_path:
                save_output(stock_data, f"Stock data for {symbol}", save_path)
                
            return stock_data
            
        except Exception as e:
            print(f"Error retrieving Vietnamese stock data for {symbol}: {e}")
            return pd.DataFrame()

    @staticmethod
    def get_stock_info(symbol: Annotated[str, "ticker symbol"]) -> dict:
        """Basic stock info - limited compared to yfinance"""
        symbol = symbol.upper()
        
        # Basic info that doesn't require API call
        info = {
            "symbol": symbol,
            "shortName": symbol,  # Would need additional API for real name
            "market": "Vietnam",
            "exchange": "HOSE" if len(symbol) <= 3 else "HNX",  # Simplified rule
        }
        
        return info
        
    @staticmethod
    def get_income_stmt(symbol: Annotated[str, "ticker symbol"]) -> DataFrame:
        """Get income statement data using FinanceLoader"""
        try:
            symbol = symbol.upper()
            loader = FinanceLoader(symbols=symbol)
            reports = loader.get_finan_report()
            return reports
        except Exception as e:
            print(f"Error retrieving income statement for {symbol}: {e}")
            return pd.DataFrame()