# Vietnamese stock data utilities using vnquant

from typing import Annotated, Optional
from pandas import DataFrame
import pandas as pd
import os
from vnquant.data import DataLoader
from .utils import save_output, SavePathType

class VNQuantUtils:
    """
    Utility class to interact with vnquant library for Vietnamese stock data
    """
    
    @staticmethod
    def get_stock_data(
        symbol: Annotated[str, "ticker symbol"],
        start_date: Annotated[
            str, "start date for retrieving stock price data, YYYY-mm-dd"
        ],
        end_date: Annotated[
            str, "end date for retrieving stock price data, YYYY-mm-dd"
        ],
        save_path: SavePathType = None,
    ) -> DataFrame:
        """Retrieve stock price data for designated Vietnamese ticker symbol"""
        # VNQuant requires symbols to be uppercase
        symbol = symbol.upper()
        
        # Initialize DataLoader and get data
        loader = DataLoader(symbols=symbol, start=start_date, end=end_date)
        stock_data = loader.download()
        
        # Extract data for the specific symbol
        if symbol in stock_data:
            data = stock_data[symbol]
        else:
            # If multi-level column index is present
            if isinstance(stock_data.columns, pd.MultiIndex):
                data = stock_data.xs(symbol, axis=1, level=0)
            else:
                data = stock_data
        
        # Rename columns to match yfinance format
        column_mapping = {
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume',
            'adjust': 'Adj Close'  # Adjusted close
        }
        data = data.rename(columns={col: column_mapping.get(col, col) for col in data.columns})
        
        return data
    
    @staticmethod
    def get_stock_info(
        symbol: Annotated[str, "ticker symbol"],
    ) -> dict:
        """Fetches and returns latest Vietnamese stock information."""
        # This would ideally use vnquant's info capabilities
        # For now, return a basic structure with symbol
        return {"symbol": symbol.upper(), "market": "Vietnam"}