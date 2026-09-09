from typing import List
from .models import Candle, Monomove

class MonomoveEngine:
    def __init__(self, pivot_depth: int = 2):
        """
        pivot_depth: Identify Peak/Trough 
        """
        self.pivot_depth = pivot_depth

    def extract_monomoves(self, candles: List[Candle]) -> List[Monomove]:
        if len(candles) < (self.pivot_depth * 2 + 1):
            return []

        # 1. Pivot Highs & Pivot Lows 
        pivots = []  # List of tuples: (index, type, price, time)
        
        for i in range(self.pivot_depth, len(candles) - self.pivot_depth):
            current = candles[i]
            
            # Check Pivot High
            is_high = all(current.high > candles[i - j].high and current.high > candles[i + j].high 
                          for j in range(1, self.pivot_depth + 1))
            
            # Check Pivot Low
            is_low = all(current.low < candles[i - j].low and current.low < candles[i + j].low 
                         for j in range(1, self.pivot_depth + 1))

            if is_high:
                pivots.append((i, "HIGH", current.high, current.time))
            elif is_low:
                pivots.append((i, "LOW", current.low, current.time))

        if not pivots:
            return []

        # 2. Continuous ZigZag Vector Isolation
        monomoves: List[Monomove] = []
        filtered_pivots = [pivots[0]]

        for p in pivots[1:]:
            prev_p = filtered_pivots[-1]
            if p[1] == prev_p[1]:  # Same type (e.g. HIGH -> HIGH)
                # Keep the extreme point
                if p[1] == "HIGH" and p[2] > prev_p[2]:
                    filtered_pivots[-1] = p
                elif p[1] == "LOW" and p[2] < prev_p[2]:
                    filtered_pivots[-1] = p
            else:
                filtered_pivots.append(p)

        # 3. Build Monomove Objects
        for i in range(len(filtered_pivots) - 1):
            p1 = filtered_pivots[i]
            p2 = filtered_pivots[i + 1]

            direction = "UP" if p2[2] > p1[2] else "DOWN"
            price_length = abs(p2[2] - p1[2])
            time_duration = p2[0] - p1[0]

            monomove = Monomove(
                id=i + 1,
                direction=direction,
                start_index=p1[0],
                end_index=p2[0],
                start_time=p1[3],
                end_time=p2[3],
                start_price=p1[2],
                end_price=p2[2],
                price_length=round(price_length, 2),
                time_duration=time_duration
            )
            monomoves.append(monomove)

        return monomoves