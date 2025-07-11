# 🏦 Smart Order Routing and Backtesting Engine
# Look:https://www.loom.com/share/0ec33b2dc7ff4519b87f23dfccec167d?t=259&sid=7bd9d5d6-ee46-44fa-b910-42029b15119a
This project simulates a Smart Order Router (SOR) that allocates large orders across multiple venues, optimizing based on cost, queue position, and penalties for over/under-fills. The system includes:

- L2 order book stream (Kafka-based)
- Optimized allocation using custom objective
- Benchmark comparisons (TWAP, VWAP, Best Ask)
- EC2 deployment instructions

+------------------+       Kafka Topic        +--------------------+
|                  | -----------------------> |                    |
|  Kafka Producer  |   "mock_l1_stream" topic |  Kafka Consumer &   |
| (Streams L2 data |                          |   Backtest Runner   |
|  as JSON msgs)   |                          |                    |
+------------------+                          +--------------------+
                                                     |
                                                     | Calls
                                                     v
                                           +--------------------+
                                           |    Allocator       |
                                           | (Optimal order     |
                                           |  allocation logic) |
                                           +--------------------+
                                                     |
                                                     v
                                           +--------------------+
                                           |  Execution Metrics  |
                                           |  & Benchmarking     |
                                           +--------------------+
                                                     |
                                                     v
                                          +---------------------+
                                          |  Parameter Tuning &  |
                                          |  Results Reporting   |
                                          +---------------------+

---

## 📁 Project Structure

```plaintext
BlockhouseProject/
├── allocator.py            # Optimization logic
├── backtest.py             # Runs the allocation and benchmarks
├── kafka_producer.py       # Streams mock L2 order book data
├── cleaned_l2_orderbook.csv
├── requirements.txt
├── README.md
└── ...

# 📊 Smart Order Routing System with Kafka + Optimizer

A real-time Smart Order Routing (SOR) system that optimally executes orders across multiple venues using Kafka for streaming and a custom allocator for decision-making. The system compares optimized execution vs. benchmark strategies (TWAP, VWAP, Naive Best Ask).

---

## 📐 System Architecture

The system consists of the following components:

- **Kafka Producer (`kafka_producer.py`)**  
  Streams Level-2 order book data (`cleaned_l2_orderbook.csv`) into the Kafka topic `mock_l1_stream`.

- **Kafka Consumer & Optimizer (`backtest.py`)**  
  Listens to real-time L1 snapshots from Kafka, reconstructs per-timestamp venue books, and:
  - Applies optimal allocation via the `allocator.py` module
  - Tracks simulated fills based on constraints (fees, depth, penalties)
  - Stores snapshots for benchmark comparison

- **Allocator (`allocator.py`)**  
  Brute-force optimizer that finds the best venue allocation to minimize:
total_cost = cost + θ * (underfill + overfill) + λ_under * underfill + λ_over * overfill
- **Benchmark Models**
- **TWAP** – Evenly distributes the order across time snapshots
- **VWAP** – Allocates based on liquidity at each venue
- **Naive Best Ask** – Chooses the best prices greedily

---

## ⚙️ Setup Instructions

### 📦 Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
docker-compose up 
#   b l o c k h o u s e 
 
 