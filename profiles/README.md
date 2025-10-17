# Profiling scripts

## Quickstart

### 1) timeit (micro-benchmark)
```
python profiles/timeit_profile.py
```
Outputs a single timing for `Cart.get_total_price()` with a large quantity.

### 2) cProfile (end-to-end checkout)
```
python profiles/cprofile_checkout.py
```
Prints top 30 cumulative functions during a seeded checkout flow.
