# Reasoner_Agent

Reasoner Agent combining LLM and MILP sources.

## Objective

Compare two implementations of a reasoner agent — an LLM-based reasoner and an optimization-based (MILP) reasoner — that generate placement plans matching services to nodes according to user intentions, when possible.

Given a JSON file describing:
- Intents concerning services and their specifics
- Services and their requirements
- Nodes and their capabilities
- Network latencies

(see examples in the `datasets/` directory)

## Optimization (MILP solver)

- Implemented in Python using the PuLP library and solved using the CBC open-source mixed-integer linear programming solver.
- Runs on Google Colab.

## LLM Model

- Calls the OpenAI API with a strict prompt.
- Prints back only the mapping lines.
- Output format: `Service <id> -> Node <id>`

### Setup

```bash
pip install openai
export OPENAI_API_KEY="sk-xxxx..."   # macOS/Linux
setx OPENAI_API_KEY "sk-xxxx..."     # Windows
```

### Run

```bash
python placement.py --json_path problem.json
```

Optional:

```bash
python placement.py --json_path problem.json --model gpt-4o-mini
```

## Input JSON Format

The input JSON file describes a placement problem with four main sections:

### `services`
List of services to be placed, each with:
- `id`: unique identifier (e.g. `"s1"`)
- `name`: human-readable name
- `resources`: base resource requirements — `CPU`, `MEM`, `DISK`, `BW`

### `nodes`
List of candidate nodes for placement, each with:
- `id`: unique identifier (e.g. `"n1"`, `"g1"`)
- `type`: `"gateway"` or `"computing"`
- `capacity`: available resources (same fields as `services.resources`)

### `latency`
Network latency (in ms) from each node to the reference point (e.g. the end user or gateway), keyed by node id. Each value is a single-element list (reserved for potential multi-path/multi-source latency in future versions).

### `intentions`
List of user intentions to satisfy, each with:
- `id`: unique identifier
- `description`: human-readable description of the intent
- `services`: list of service ids involved in this intention
- `QoS`: required quality of service — `latency` (max acceptable, in ms), `bandwidth` (min required)
- `extra_resources`: additional resource requirements specific to this intention (added on top of the service's base `resources`)
- `weight`: priority of the intention, used to arbitrate in case of resource conflicts (higher = more important)

Example dataset: see `datasets/` directory.

## Repository Structure

- `datasets/` → four datasets for testing (JSON files)
- `llm_model/` → LLM-based reasoner (`llm_reasoner_gpt.py`)
- `milp_solver/` → MILP solver model notebook (`Adaptive_service_placement_using_mathematical_optimization_for_intent_aware_QoS.ipynb`)
- `results/` → LLM-based and MILP solver model outputs (text files, one per dataset)