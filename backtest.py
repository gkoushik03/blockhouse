import json
from kafka import KafkaConsumer
from collections import defaultdict
from allocator import allocate
from benchmark import naive_best_ask_fill, twap_fill, vwap_fill, bps_saving

TOPIC = "mock_l1_stream"
BOOTSTRAP_SERVER = "localhost:9092"
ORDER_SIZE = 5000


def run_backtest(lambda_over, lambda_under, theta_queue):
    unfilled = ORDER_SIZE
    executed = 0
    cash_spent = 0.0

    known_venues = set()
    per_ts_snapshots = defaultdict(list)
    per_ts_snapshots_list = []

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVER,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )

    for message in consumer:
        data = message.value
        if not all(k in data for k in ['timestamp', 'venue_id', 'ask_price', 'ask_size']):
            continue

        ts = data['timestamp']
        venue = str(data['venue_id'])
        ask_px = float(data['ask_price'])
        ask_sz = int(data['ask_size'])

        known_venues.add(venue)

        per_ts_snapshots[ts].append({
            "venue": venue,
            "ask": ask_px,
            "ask_size": ask_sz,
            "fee": 0.002,
            "rebate": 0.001
        })

        if len(per_ts_snapshots[ts]) == len(known_venues):
            venues = per_ts_snapshots[ts]
            per_ts_snapshots_list.append(venues.copy())

            to_execute = min(unfilled, ORDER_SIZE)
            allocation, cost = allocate(to_execute, venues, lambda_over, lambda_under, theta_queue)

            for i, venue_info in enumerate(venues):
                fill_qty = min(allocation[i], venue_info["ask_size"])
                executed += fill_qty
                unfilled -= fill_qty
                cash_spent += fill_qty * (venue_info["ask"] + venue_info["fee"])

            del per_ts_snapshots[ts]

            if unfilled <= 0:
                break

    avg_fill_price = cash_spent / executed if executed else 0.0
    return {
        "lambda_over": lambda_over,
        "lambda_under": lambda_under,
        "theta_queue": theta_queue,
        "total_cash": cash_spent,
        "avg_fill_price": avg_fill_price,
        "snapshots": per_ts_snapshots_list
    }


def main():
    lambda_over = 0.4
    lambda_under = 0.6
    theta_queue = 0.3

    result = run_backtest(lambda_over, lambda_under, theta_queue)

    snapshots = result["snapshots"]
    last_snapshot = snapshots[-1] if snapshots else []

    naive_exec, naive_cost = naive_best_ask_fill(ORDER_SIZE, last_snapshot)
    twap_exec, twap_cost = twap_fill(snapshots, ORDER_SIZE)
    vwap_exec, vwap_cost = vwap_fill(ORDER_SIZE, last_snapshot)

    output = {
        "best_parameters": {
            "lambda_over": lambda_over,
            "lambda_under": lambda_under,
            "theta_queue": theta_queue
        },
        "optimized": {
            "total_cash": round(result["total_cash"], 2),
            "avg_fill_px": round(result["avg_fill_price"], 2)
        },
        "baselines": {
            "best_ask": {"total_cash": round(naive_cost, 2), "avg_fill_px": round(naive_cost / naive_exec, 2) if naive_exec else 0},
            "twap": {"total_cash": round(twap_cost, 2), "avg_fill_px": round(twap_cost / twap_exec, 2) if twap_exec else 0},
            "vwap": {"total_cash": round(vwap_cost, 2), "avg_fill_px": round(vwap_cost / vwap_exec, 2) if vwap_exec else 0},
        },
        "savings_vs_baselines_bps": {
            "best_ask": round(bps_saving(naive_cost, result["total_cash"]), 2),
            "twap": round(bps_saving(twap_cost, result["total_cash"]), 2),
            "vwap": round(bps_saving(vwap_cost, result["total_cash"]), 2)
        }
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
