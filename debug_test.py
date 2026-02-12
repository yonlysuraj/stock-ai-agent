from app.agents.planner_agent import analyze_stock
import sys

try:
    print("Testing stock analysis...")
    result = analyze_stock("AAPL")
    print("Result:", result)
except Exception as e:
    print("CRASHED:", e)
    import traceback
    traceback.print_exc()
