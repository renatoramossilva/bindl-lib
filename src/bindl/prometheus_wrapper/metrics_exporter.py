"""Prometheus Metrics Exporter"""

import threading
from typing import Any, Optional
from prometheus_client import Counter, Gauge, Histogram, Summary, start_http_server
from bindl.logger import setup_logger


LOG = setup_logger(__name__)


class MetricsExporter:
    """
    Generic class for registering and exposing Prometheus metrics.

    Supports all four Prometheus metric types:
    - Counter: cumulative metric (only increases)
    - Gauge: arbitrary value that can go up or down (e.g., memory)
    - Histogram: captures distributions using buckets (e.g., durations)
    - Summary: captures quantiles (e.g., latency)

    Automatically starts an HTTP server to expose metrics at /metrics.
    """

    def __init__(self, port: Optional[int] = None, addr: Optional[str] = None):
        """
        Starts the Prometheus metrics HTTP server.

        ** Attributes **
            port: Port where the /metrics endpoint will be exposed.
            addr: Address to bind the HTTP server to. Default is "0.0.0.0".

        If 'port' and 'addr' is not defined, MetricsExporter class does not
        starts http server.
        """
        if port and addr:
            self.port = port
            self.addr = addr
            self._start_http_server()

        self.counters: dict[str, Any] = {}
        self.gauges: dict[str, Any] = {}
        self.histograms: dict[str, Any] = {}
        self.summaries: dict[str, Any] = {}

    def _start_http_server(self):
        thread = threading.Thread(
            target=start_http_server, args=(self.port,), kwargs={"addr": self.addr}
        )
        thread.daemon = True
        thread.start()

    def register_counter(
        self, name: str, description: str, label_names: Optional[list[Any]] = None
    ):
        """
        Registers a Counter metric.

        ** Attributes **
            name: Metric name.
            description: Metric description.
            label_names: Optional list of label names.
        """
        label_names = label_names or []
        self.counters[name] = Counter(name, description, label_names)

    def inc_counter(
        self, name: str, labels: Optional[dict[str, str]] = None, value: float = 1
    ):
        """
        Increments a Counter metric.

        ** Attributes **:
            name: Metric name.
            labels: Optional labels to apply.
            value: Increment value (default is 1).
        """
        metric = self.counters.get(name)
        if metric is None:
            LOG.warning("Counter %r is not registered.", name)
            return
        if labels:
            metric.labels(**labels).inc(value)
        else:
            metric.inc(value)

    def register_gauge(
        self, name: str, description: str, label_names: Optional[list[Any]] = None
    ):
        """
        Registers a Prometheus Gauge metric.

        A Gauge is a metric that represents a single numerical value that can go up or down.
        It's useful for things like current memory usage, temperature, number of active users, etc.

        This method must be called once before using `set_gauge()` on the same metric name.

        ** Attributes **:
            name: Unique name of the metric (snake_case recommended).
            description: Human-readable description of what the metric measures.
            label_names: List of label names (keys) that will be used
                when setting the gauge.

        Example:
            exporter.register_gauge(
                name="cpu_temperature_celsius",
                description="Current temperature of the CPU in Celsius",
                label_names=["core"]
            )
        """
        label_names = label_names or []
        self.gauges[name] = Gauge(name, description, label_names)

    def set_gauge(
        self, name: str, value: float, labels: Optional[dict[str, str]] = None
    ):
        """
        Sets the current value of a registered Gauge metric.

        This method updates the value of a Gauge. You can optionally provide labels
        if the Gauge was registered with label names.

        ** Attributes **:
            name: Name of the Gauge metric (must be registered first).
            value: The numerical value to assign to the gauge.
            labels: Dictionary of label key-value pairs, if labels were defined.

        ** Warning **
            Raises a warning if the metric was not registered using `register_gauge()`.

        ** Example Usage **:
            # Without labels:
            exporter.set_gauge("active_sessions", 42)

            # With labels:
            exporter.set_gauge(
                name="cpu_temperature_celsius",
                value=68.5,
                labels={"core": "core_0"}
            )
        """
        metric = self.gauges.get(name)
        if metric is None:
            LOG.warning("Gauge %r is not registered.", name)
            return
        if labels:
            metric.labels(**labels).set(value)
        else:
            metric.set(value)

    def register_histogram(
        self,
        name: str,
        description: str,
        label_names: Optional[list[str]] = None,
        buckets: Optional[list[float]] = None,
    ):
        """
        Registers a Prometheus Histogram metric.

        A Histogram counts observations into configurable buckets and tracks
        the total sum and count. Useful for measuring latency, response time,
        file size distributions, etc.

        You can provide custom buckets or use the default ones.

        ** Attributes **
            name: Unique name for the metric.
            description: Description of what the metric measures.
            label_names: List of label keys (default is []).
            buckets: Custom bucket upper bounds (default: Prometheus default buckets).

        ** Example Usage **
            exporter.register_histogram(
                name="job_duration_seconds",
                description="Duration of background jobs",
                label_names=["job_type"],
                buckets=[0.1, 0.5, 1, 2, 5, 10]
            )
        """
        if label_names is None:
            label_names = []

        if buckets is not None:
            self.histograms[name] = Histogram(
                name, description, labelnames=label_names, buckets=buckets
            )
        else:
            self.histograms[name] = Histogram(name, description, labelnames=label_names)

    def observe_histogram(
        self, name: str, value: float, labels: Optional[dict[str, str]] = None
    ):
        """
        Observes a single value for a registered Histogram metric.

        This records a measurement and places it in the appropriate bucket. Histogram
        also tracks the total number of observations and their sum.

        ** Attributes **:
            name (str): Name of the registered Histogram metric.
            value (float): Value to observe (e.g., elapsed time in seconds).
            labels (dict[str, str], optional): Label values if defined for the metric.

        ** Warning **
            Raises a warning if the Histogram metric has not been registered.

        ** Example Usage **
            exporter.observe_histogram(
                name="job_duration_seconds",
                value=1.37,
                labels={"job_type": "data_backup"}
            )
        """
        metric = self.histograms.get(name)
        if metric is None:
            LOG.warning("Histogram %r is not registered.", name)
            return
        if labels:
            metric.labels(**labels).observe(value)
        else:
            metric.observe(value)

    def register_summary(
        self, name: str, description: str, label_names: Optional[list[Any]] = None
    ):
        """
        Registers a Prometheus Summary metric.

        A Summary captures individual observations and calculates configurable quantiles
        (e.g., 0.5, 0.9, 0.99). It's ideal for tracking response times, latencies,
        and any metric where percentiles are meaningful.

        Must be registered before using `observe_summary`.

        ** Attributes **:
            name: Unique name for the metric.
            description: Description of what the metric measures.
            label_names: List of label keys to categorize metrics (default is []).

        ** Example Usage **
            exporter.register_summary(
                name="request_duration_seconds",
                description="Duration of HTTP requests in seconds",
                label_names=["method", "endpoint"]
            )
        """
        label_names = label_names or []
        self.summaries[name] = Summary(name, description, label_names)

    def observe_summary(
        self, name: str, value: float, labels: Optional[dict[str, str]] = None
    ):
        """
        Observes a single value for a registered Summary metric.

        This records a new sample for the summary, which will be used to compute quantiles
        like median, p90, p99, and also track the total count and sum of all observations.

        ** Attributes **:
            name: Name of the registered Summary metric.
            value: The numeric value to observe (e.g., time in seconds).
            labels: Values for the labels if defined.

        ** Warning **
            Raises a warning if the Summary metric has not been registered.

        ** Example Usage **
           exporter.observe_summary(
                name="request_duration_seconds",
                value=0.245,
                labels={"method": "GET", "endpoint": "/users"}
            )
        """
        metric = self.summaries.get(name)
        if metric is None:
            LOG.warning("Summary %r is not registered.", name)
            return
        if labels:
            metric.labels(**labels).observe(value)
        else:
            metric.observe(value)
