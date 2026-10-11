# Live telemetry collector

Collects actual host CPU, memory and disk usage with `psutil`, probes only the AegisOps-owned localhost test service, and persists observations via SQLite. The live test-service URL is restricted to loopback HTTP for safety.
