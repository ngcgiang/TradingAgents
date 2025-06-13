import os
import pandas as pd
from datetime import datetime, timedelta

# Import components to test
from tradingagents.dataflows import VNQuantUtils, get_VNQuant_data
from tradingagents.dataflows.stockstats_utils import StockstatsUtils
from tradingagents.dataflows.config import get_config, set_config

def test_vnquant_utils_direct():
    """Test direct access to VNQuantUtils methods"""
    print("\n===== Testing VNQuantUtils Directly =====")
    
    # Test with common Vietnamese stocks: VNM, FPT, VIC
    symbol = "VNM"  # Vietnam Dairy Products
    
    # Define date range (past 6 months)
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
    
    print(f"Fetching data for {symbol} from {start_date} to {end_date}...")
    
    # Test VNQuantUtils.is_vn_stock
    is_vn = VNQuantUtils.is_vn_stock(symbol)
    print(f"Is {symbol} a Vietnamese stock? {is_vn}")
    
    # Test VNQuantUtils.get_stock_data
    data = VNQuantUtils.get_stock_data(symbol, start_date, end_date)
    
    if data.empty:
        print(f"ERROR: No data returned for {symbol}")
    else:
        print(f"SUCCESS! Retrieved {len(data)} records for {symbol}")
        print("\nSample data:")
        print(data.head(3))
        print(f"Data columns: {data.columns.tolist()}")
    
    # Test VNQuantUtils.get_stock_info
    info = VNQuantUtils.get_stock_info(symbol)
    print("\nStock info:")
    print(info)
    
    return data

def test_interface_function():
    """Test the interface.py get_VNQuant_data function"""
    print("\n===== Testing Interface Function =====")
    
    symbol = "FPT"  # FPT Corporation
    
    # Define date range (past 3 months)
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    
    # Get config and ensure data directory exists
    config = get_config()
    data_dir = config.get("data_cache_dir", "data_cache")
    os.makedirs(os.path.join(data_dir, "market_data", "price_data"), exist_ok=True)
    
    print(f"Fetching data via interface for {symbol} from {start_date} to {end_date}...")
    
    # Call the interface function
    result = get_VNQuant_data(symbol, start_date, end_date, data_dir)
    
    # Check if function returned data
    if "No data found" in result:
        print(f"ERROR: {result}")
        return
    
    # Print first section of result string
    print("\nInterface function output preview:")
    print(result[:500])
    
    # Test cache functionality
    print("\nTesting cache functionality by calling again...")
    cached_result = get_VNQuant_data(symbol, start_date, end_date, data_dir)
    
    # Check if second call used cache
    if "cached" in cached_result:
        print("SUCCESS! Cache is working properly.")
    else:
        print("WARNING: Cache might not be working correctly.")
        
    # Verify cache file existence
    cache_file = os.path.join(
        data_dir, "market_data", "price_data", 
        f"{symbol}-VNQuant-data-{start_date}-{end_date}.csv"
    )
    if os.path.exists(cache_file):
        print(f"Cache file created at: {cache_file}")
    else:
        print("ERROR: Cache file not created")

def test_stockstats_integration():
    """Test using StockstatsUtils with Vietnamese stocks"""
    print("\n===== Testing StockstatsUtils Integration =====")
    
    symbol = "VIC"  # Vingroup
    indicator = "rsi_14"  # Relative Strength Index
    
    # Define date for analysis
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Get config
    config = get_config()
    data_dir = config.get("data_cache_dir", "data_cache")
    
    print(f"Calculating {indicator} for {symbol} on {current_date}...")
    
    try:
        # This will trigger online data fetch and calculation
        indicator_value = StockstatsUtils.get_stock_stats(
            symbol=symbol,
            indicator=indicator,
            curr_date=current_date,
            data_dir=data_dir,
            online=True
        )
        
        print(f"SUCCESS! {indicator} value for {symbol} on {current_date}: {indicator_value}")
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print("Try running with a different date or stock symbol.")

if __name__ == "__main__":
    print("====================================")
    print("TESTING VNQUANT DATA FLOW INTEGRATION")
    print("====================================")
    
    # Test VNQuantUtils directly
    data = test_vnquant_utils_direct()
    
    if not data.empty:
        # Test interface functions
        test_interface_function()
        
        # Test StockstatsUtils integration
        test_stockstats_integration()
    else:
        print("No data retrieved from VNQuantUtils, skipping further tests.")
    
    print("\n====================================")
    print("TEST COMPLETED")
    print("====================================")