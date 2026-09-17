"""
Tick is an abstract unit of real world time, which is equivalent to one microsecond.
To simulate clock skew, we will advance ticks in the tests when a network connection occurs.
"""
_tick_mcs: float = 0.0

def reset_ticks() -> None:
    global _tick_mcs
    _tick_mcs = 0.0

def get_current_tick_mcs() -> float:
    global _tick_mcs
    return _tick_mcs

def advance_ticks_mcs(ticks: float) -> None:
    global _tick_mcs
    _tick_mcs += ticks