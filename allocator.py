import itertools
def compute_cost(split, venues, order_size, λo, λu, θ):
    executed = 0
    cash_spent = 0
    for i in range(len(venues)):
        exe = min(split[i], venues[i]['ask_size'])
        executed += exe
        cash_spent += exe * (venues[i]['ask'] + venues[i]['fee'])
        maker_rebate = max(split[i] - exe, 0) * venues[i]['rebate']
        cash_spent -= maker_rebate

    underfill = max(order_size - executed, 0)
    overfill = max(executed - order_size, 0)
    risk_penalty = θ * (underfill + overfill)
    cost_penalty = λu * underfill + λo * overfill
    total_cost = cash_spent + risk_penalty + cost_penalty
    return total_cost

# --- Allocation function ---
def allocate(order_size, venues, λ_over, λ_under, θ_queue):
    step = 1  # fine granularity
    splits = []

    # Generate all possible splits with step=1 up to ask_size and order_size limit
    # WARNING: combinatorial explosion for many venues or large order_size
    # For practical use, optimize or prune search space
    ranges = []
    for v in venues:
        max_alloc = min(v['ask_size'], order_size)
        ranges.append(range(0, max_alloc + 1, step))

    best_cost = float('inf')
    best_split = None

    for split in itertools.product(*ranges):
        if sum(split) > order_size:
            continue  # no overfill
        if sum(split) == 0:
            continue  # ignore empty allocation

        cost = compute_cost(split, venues, order_size, λ_over, λ_under, θ_queue)
        if cost < best_cost:
            best_cost = cost
            best_split = split

    if best_split is None:
        best_split = tuple(0 for _ in venues)
        best_cost = float('inf')

    return list(best_split), best_cost