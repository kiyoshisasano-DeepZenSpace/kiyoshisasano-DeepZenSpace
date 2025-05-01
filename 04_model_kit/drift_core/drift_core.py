import time
import random
import math

class LatencyGate:
    def __init__(self, mode='dissipative', range_ms=(220, 1200)):
        self.mode = mode
        self.range_ms = range_ms

    def delay(self):
        if self.mode == 'dissipative' and random.random() < 0.4:
            return None
        time.sleep(random.uniform(*self.range_ms) / 1000.0)
        return True

class DriftTrajectory:
    def evolve(self, t=None):
        t = t or time.time()
        phase = math.sin(t * 0.3)
        if phase > 0.7:
            return 'resonant'
        elif phase < -0.7:
            return 'inverted'
        return 'neutral'

def observe():
    gate = LatencyGate()
    traj = DriftTrajectory()
    for _ in range(3):
        if not gate.delay():
            print("[dissipated]")
            continue
        state = traj.evolve()
        print(f"[{state}] silence acknowledged")

if __name__ == '__main__':
    observe()
