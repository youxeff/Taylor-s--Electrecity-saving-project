# Taylor's Electricity-saving Project

A small project to model, analyze, and reduce household electricity consumption. This repository contains code, data schema, and documentation to collect usage data, run simulations, and test energy-saving strategies.

## Table of contents
- About
- Features
- Repository layout
- Prerequisites
- Installation
- Usage
- Configuration
- Data format
- Testing
- Contributing
- License
- Contact

## About
This project helps estimate electricity consumption, evaluate savings strategies, and produce reports and visualizations. It is intended to be modular so new data sources, strategies, and visualization components can be added.

## Features
- Import electricity usage data (CSV / JSON)
- Simple consumption models and baseline estimation
- Simulation of conservation strategies (scheduling, device shutdown, efficiency gains)
- Visualization-ready export (CSV/JSON/PNG)
- Basic tests and CI-friendly commands

## Repository layout
- /src — source code (models, processors, CLI)
- /data — sample datasets and schema
- /notebooks — exploratory notebooks (analysis and visualizations)
- /docs — documentation and design notes
- /tests — unit and integration tests
- README.md — this file

Adjust paths if your project uses a different layout.

## Prerequisites
- Git
- A runtime for the implementation language (Node.js, Python, etc.)
- Package manager (npm / pip / poetry) as appropriate
- Optional: Jupyter for notebooks, a plotting library for visualizations

## Installation (example)
Replace commands with the appropriate toolchain for the repository.

1. Clone the repo
    git clone https://github.com/<user>/Taylor-s--Electrecity-saving-project.git
    cd Taylor-s--Electrecity-saving-project

2. Install dependencies (examples)
    - Node.js:
      npm install
    - Python:
      python -m venv .venv
      source .venv/bin/activate
      pip install -r requirements.txt

## Usage
1. Place or convert your consumption data into the data/ directory following the data format below.
2. Run the ingestion step
    - Node:
      npm run ingest -- --input data/yourfile.csv
    - Python:
      python -m src.ingest --input data/yourfile.csv
3. Run analysis or simulation
    - npm run simulate -- --config config/simulation.yaml
    - python -m src.simulate --config config/simulation.yaml
4. Export results
    - Outputs will be written to outputs/ (CSV/JSON and plots)

Include any specific CLI flags and configuration options your implementation supports.

## Configuration
Keep configuration in the /config folder (YAML or JSON). Typical options:
- timeframe: start_date, end_date
- granularity: hourly / daily / minute
- baseline_method: average / rolling
- strategies: list of strategies to evaluate with parameters
- output: outputs/ directory and formats

## Data format
A minimal CSV format example:
timestamp,device_id,power_w
2026-05-01T00:00:00Z,main,1200
2026-05-01T00:01:00Z,fridge,80

Required fields:
- timestamp (ISO 8601)
- device_id (string)
- power_w (numeric, watts)

Provide converters for vendor-specific formats in src/ingest.

## Testing
- Run unit tests:
  - Node: npm test
  - Python: pytest
- Add tests in /tests and name them clearly.

## Contributing
- Fork the project
- Create a feature branch: git checkout -b feat/your-feature
- Write tests and update docs
- Submit a pull request with a clear description of changes
- Follow coding and commit message conventions used in the repo
