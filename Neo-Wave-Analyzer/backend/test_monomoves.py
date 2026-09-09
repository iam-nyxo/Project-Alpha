from core.models import Candle
from core.monomove_engine import MonomoveEngine

def run_test():
    # 1. Generate sample candlestick data with distinct peaks and troughs
    raw_candles = [
        Candle(index=0, time="10:00", open=100.0, high=102.0, low=99.0, close=101.0),
        Candle(index=1, time="10:05", open=101.0, high=105.0, low=100.5, close=104.0),
        Candle(index=2, time="10:10", open=104.0, high=108.0, low=103.0, close=107.5),  # Pivot High (Peak 1)
        Candle(index=3, time="10:15", open=107.5, high=107.0, low=102.0, close=103.0),
        Candle(index=4, time="10:20", open=103.0, high=104.0, low=98.0, close=99.0),   # Pivot Low (Trough 1)
        Candle(index=5, time="10:25", open=99.0, high=103.0, low=98.5, close=102.0),
        Candle(index=6, time="10:30", open=102.0, high=112.0, low=101.0, close=111.0), # Pivot High (Peak 2)
        Candle(index=7, time="10:35", open=111.0, high=110.0, low=105.0, close=106.0),
        Candle(index=8, time="10:40", open=106.0, high=107.0, low=100.0, close=101.0), # Pivot Low (Trough 2)
    ]

    # 2. Initialize Monomove Engine (pivot_depth=1 for quick test)
    engine = MonomoveEngine(pivot_depth=1)

    # 3. Execute Monomove Extraction
    monomoves = engine.extract_monomoves(raw_candles)

    # 4. Display Results
    print("\n==========================================")
    print("       NEO WAVE MONOMOVE ENGINE TEST      ")
    print("==========================================\n")
    print(f"Total Monomoves Extracted: {len(monomoves)}\n")

    for m in monomoves:
        print(f"Monomove #{m.id} [{m.direction}]")
        print(f"  - Start: Time {m.start_time} @ Price {m.start_price}")
        print(f"  - End:   Time {m.end_time} @ Price {m.end_price}")
        print(f"  - Delta Price (Height): {m.price_length} pts")
        print(f"  - Delta Time (Duration): {m.time_duration} bars")
        print("-" * 42)

if __name__ == "__main__":
    run_test()