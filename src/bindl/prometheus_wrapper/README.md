# 📊 Prometheus Metrics Exporter

A generic class for registering and exposing Prometheus metrics in Python, making it easy to instrument your applications for monitoring.

---

## 🚀 Overview

The `MetricsExporter` class supports all four Prometheus metric types:

- **Counter**: Cumulative metrics that only increase (e.g., number of requests).
- **Gauge**: Metrics that can go up or down (e.g., memory usage).
- **Histogram**: Captures distributions using buckets (e.g., request latency).
- **Summary**: Calculates quantiles (percentiles) for observations (e.g., latency percentiles).

It automatically starts an HTTP server exposing the metrics at the `/metrics` endpoint, ready for Prometheus scraping.

---


# Initialize and start the HTTP server on port 8000
```python
exporter = MetricsExporter(port=8000)
```

# Register metrics
```python
exporter.register_counter("requests_total", "Total number of requests", label_names=["method", "endpoint"])
exporter.register_gauge("cpu_temp_celsius", "CPU temperature in Celsius", label_names=["core"])
exporter.register_histogram("request_latency_seconds", "Request latency in seconds", label_names=["endpoint"], buckets=[0.1, 0.5, 1, 2, 5])
exporter.register_summary("response_size_bytes", "Response size in bytes", label_names=["endpoint"])
```

# Increment a counter
```python
exporter.inc_counter("requests_total", labels={"method": "GET", "endpoint": "/api/data"})
```

# Set a gauge value
```python
exporter.set_gauge("cpu_temp_celsius", 68.5, labels={"core": "core_0"})
```

# Observe a value in a histogram
```python
exporter.observe_histogram("request_latency_seconds", 0.35, labels={"endpoint": "/api/data"})
```

# Observe a value in a summary
```python
exporter.observe_summary("response_size_bytes", 1024, labels={"endpoint": "/api/data"})
```

⚠️ Important Notes


- You must register a metric before using it.
- Using an unregistered metric logs a warning.
- The HTTP server exposing the metrics runs in a daemon thread and won't block your app.
- Configure Prometheus to scrape metrics from: http://<host>:<port>/metrics.


💡 Usage Tips


- Use Counter for counting events that only increase (e.g., requests, errors).
- Use Gauge for fluctuating values (e.g., temperature, memory usage).
- Use Histogram to measure value distributions with buckets (e.g., latency buckets).
- Use Summary to get precise percentiles and statistical summaries.



Happy monitoring! 🚀📈
