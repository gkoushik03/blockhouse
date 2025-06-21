<<<<<<< HEAD
def naive_best_ask_fill(order_size, venues):
    venues_sorted = sorted(venues, key=lambda v: v['ask'])
    executed = 0
    cost = 0.0
    for v in venues_sorted:
        qty = min(v['ask_size'], order_size - executed)
        cost += qty * (v['ask'] + v['fee'])
        executed += qty
        if executed >= order_size:
            break
    return executed, cost

def twap_fill(tick_snapshots, order_size):
    executed = 0
    cost = 0.0
    ticks = len(tick_snapshots)
    if ticks == 0:
        return executed, cost
    shares_per_tick = order_size // ticks
    for venues in tick_snapshots:
        venues_sorted = sorted(venues, key=lambda v: v['ask'])
        remaining = shares_per_tick
        for v in venues_sorted:
            qty = min(remaining, v['ask_size'])
            cost += qty * (v['ask'] + v['fee'])
            executed += qty
            remaining -= qty
            if remaining <= 0:
                break
    return executed, cost

def vwap_fill(order_size, venues):
    total_volume = sum(v['ask_size'] for v in venues)
    executed = 0
    cost = 0.0
    for v in venues:
        if total_volume == 0:
            break
        weight = v['ask_size'] / total_volume
        qty = int(weight * order_size)
        fill_qty = min(qty, v['ask_size'])
        executed += fill_qty
        cost += fill_qty * (v['ask'] + v['fee'])
    return executed, cost

def bps_saving(cost_benchmark, cost_sor):
    if cost_benchmark == 0:
        return 0.0
    return 10000 * (cost_benchmark - cost_sor) / cost_benchmark

=======
def naive_best_ask_fill(order_size, venues):
    venues_sorted = sorted(venues, key=lambda v: v['ask'])
    executed = 0
    cost = 0.0
    for v in venues_sorted:
        qty = min(v['ask_size'], order_size - executed)
        cost += qty * (v['ask'] + v['fee'])
        executed += qty
        if executed >= order_size:
            break
    return executed, cost

def twap_fill(tick_snapshots, order_size):
    executed = 0
    cost = 0.0
    ticks = len(tick_snapshots)
    if ticks == 0:
        return executed, cost
    shares_per_tick = order_size // ticks
    for venues in tick_snapshots:
        venues_sorted = sorted(venues, key=lambda v: v['ask'])
        remaining = shares_per_tick
        for v in venues_sorted:
            qty = min(remaining, v['ask_size'])
            cost += qty * (v['ask'] + v['fee'])
            executed += qty
            remaining -= qty
            if remaining <= 0:
                break
    return executed, cost

def vwap_fill(order_size, venues):
    total_volume = sum(v['ask_size'] for v in venues)
    executed = 0
    cost = 0.0
    for v in venues:
        if total_volume == 0:
            break
        weight = v['ask_size'] / total_volume
        qty = int(weight * order_size)
        fill_qty = min(qty, v['ask_size'])
        executed += fill_qty
        cost += fill_qty * (v['ask'] + v['fee'])
    return executed, cost

def bps_saving(cost_benchmark, cost_sor):
    if cost_benchmark == 0:
        return 0.0
    return 10000 * (cost_benchmark - cost_sor) / cost_benchmark

>>>>>>> 2a3eb59586c1d3426046e3e91d3fce0c60b90ce3
