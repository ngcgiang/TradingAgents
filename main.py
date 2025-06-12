from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.dataflows.vnquant_utils import VNQuantUtils

# Create a custom config
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4.1-nano"  # Use a different model
config["quick_think_llm"] = "gpt-4.1-nano"  # Use a different model
config["max_debate_rounds"] = 1  # Increase debate rounds
config["online_tools"] = True  # Increase debate rounds

# Initialize with custom config
ta = TradingAgentsGraph(debug=True, config=config)

# forward propagate
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)

# Memorize mistakes and reflect
# ta.reflect_and_remember(1000) # parameter is the position returns

# Get data for VNM (Vietnam Dairy Products JSC)
from tradingagents.dataflows import VNQuantUtils, get_VNQuant_data_online

# Test direct VNQuantUtils
df = VNQuantUtils.get_stock_data('VNM', start_date='2023-01-01', end_date='2023-12-31')
print(df.head())

# Test interface function
vn_data = get_VNQuant_data_online('VNM', '2023-01-01', '2023-12-31')
print(vn_data[:500])  # Print first 500 chars
