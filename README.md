# Telemetry Processing Engine

A modular, multi-stage data engineering pipeline designed to ingest, clean, and analyze raw environmental satellite sensor telemetry streams.

-- System Architecture Overview
Real-world physical tracking data from aerospace payloads frequently suffers from transmission degradation, hardware dropouts, and environmental interference. This engine establishes a programmatic pipeline that transitions raw data across three distinct computational layers:

1. Systems Layer (C): Ingests the raw binary/text telemetry arrays, executes real-time validation checks against physical boundaries, and strips out corrupted frames.
2. Automation Layer (Python): Processes the filtered, clean payloads and automates structural logging operations to disk storage.
3. Analytics Layer (MySQL): Imports log structures into relational database schemas to execute analytical queries on spatial tracking fields.

-- Core Data Rules & Engineering Constraints
* Aerospace Hardware Sentinels: The core parser scans for the universal sentinel code of -9999.0. This value indicates a physical payload failure or dropped telemetry packet. The engine systematically isolates and drops these frames to prevent statistical skewing.
* Component Safety Thresholds: Valid operating limits are strictly enforced between -40.0 C and 85.0 C, derived from standard industrial hardware datasheets. Out-of-bounds metrics are flagged as operational anomalies.

-- Repository File Structure
* parser.c -- Written in C. Models structured data coordinates (Latitude, Longitude) and maps iterative conditional logic over raw memory streams to discard corruption.
* ingest.py -- Written in Python. Standardizes file I/O operations and safely logs structured streaming outputs into a permanent repository trace file.
* database.sql -- Written in MySQL. Defines data schemas (DDL/DML) and runs advanced analytical window functions (RANK, ROW_NUMBER, and SUM OVER tracking) to evaluate thermal load metrics.

-- Target Output Objectives
* Eliminates corrupted placeholder segments without crashing systemic calculations.
* Safely isolates hardware failures from valid environmental datasets.
* Computes stable streaming trends ready for ingestion into relational schemas.
