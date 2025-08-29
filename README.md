# Reasoner_Agent
Reasoner Agent combining LLM and MILP sources.


Objective:
Given a JSON file describing services and requirements (see examples in the data/ directory), the models generate a placement plan, when possible, to match services to nodes.


Optimization:
- Implemented in Python using IBM DOcplex.
- Runs on Google Colab.


LLM-model:
- Calls the OpenAI API with a strict prompt.
- Prints back only the mapping lines.
- Output format: Service <id> -> Node <id>
- Setup
pip install openai
export OPENAI_API_KEY="sk-xxxx..."   # macOS/Linux
setx OPENAI_API_KEY "sk-xxxx..."    # Windows
- Run
python placement.py --json_path problem.json
- Optional:
python placement.py --json_path problem.json --model gpt-4o-mini


Repository Structure
- data/ → three small datasets for testing
- optimization/ → MILP model notebook (Adaptive_service_placement_using_mathematical_optimization_for_intent_aware_QoS.ipynb)
- llm_model/ → LLM-based reasoner (llm_reasoner_gpt.py)
- evaluation.pdf → contains the evaluation results and discussion