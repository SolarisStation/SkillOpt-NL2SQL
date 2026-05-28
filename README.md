# SkillOpt: NL2SQL Local Trainer

*A streamlined, community-optimized fork of Microsoft's SkillOpt, stripped of all extra benchmarks and hard-coded to train your local models (like Qwen via Ollama) to become PostgreSQL experts using text-space optimization.*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🛠️ What is this Fork?

This repository takes the powerful SkillOpt engine (which automatically rewrites system prompts to improve model performance) and turns it into a **dedicated NL2SQL (Natural Language to SQL) trainer**.

1. **No Azure Lock-in:** The original `azure_openai.py` wrapper has been bypassed. You can use standard OpenAI endpoints (like DeepSeek via Polza.ai, Ollama, vLLM).
2. **Pure SQL Focus:** All other heavy benchmarks (ALFWorld, SweBench, etc.) have been removed. The evaluator is hard-coded to compare SQL syntax accurately.
3. **UTF-8 Support:** Fixed `UnicodeDecodeError` when reading/writing skill files containing non-ASCII (e.g., Russian) characters.

---

## Install

**Requirements:** Python 3.10+

```bash
git clone https://github.com/SolarisStation/SkillOpt-wthout-asure.git
cd SkillOpt-wthout-asure
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

---

## Quick Start Configuration

All configuration is done in `configs/nl2sql/default.yaml`. 

```yaml
# Core environment settings
env: "nl2sql"
split_mode: "split_dir"
split_dir: "data/nl2sql"

# Target Model (e.g., Local Ollama student)
target_model:
  model: "qwen3.5:2b"
  api_type: "openai"
  endpoint: "http://localhost:11434/v1"
  api_key: "ollama"
  auth_mode: "api_key"
  temperature: 0.0

# Optimizer Model (e.g., DeepSeek cloud teacher)
optimizer_model:
  model: "deepseek/deepseek-v4-flash"
  api_type: "openai"
  endpoint: "https://api.polza.ai/v1" # Or https://api.deepseek.com/v1
  api_key: "YOUR_API_KEY"
  auth_mode: "api_key"
  temperature: 0.1

# Training parameters
num_epochs: 3
batch_size: 5
accumulation: 1
seed: 42
merge_batch_size: 5
edit_budget: 4
min_edit_budget: 2
validation_interval: 1

# Evaluation parameters
sel_env_num: 2
test_env_num: 1
eval_val: true
eval_test: true

skill_init: "configs/nl2sql/initial_skill.md"
out_root: "outputs/nl2sql"
```

### Run Training

```bash
python scripts/train.py --config configs/nl2sql/default.yaml
```

---

## Data Preparation

Provide your NL2SQL examples in `data/nl2sql/train`, `val`, and `test` directories using this JSON schema:

```json
[
  {
    "id": "1",
    "question": "Сколько пользователей зарегистрировано в системе?",
    "answers": ["SELECT COUNT(*) FROM users;"]
  }
]
```


| `--out_root` | Output directory | `outputs/my_run` |

### Eval Only

Evaluate a trained skill on specific data splits without training:

```bash
# Evaluate on test set only:
python scripts/eval_only.py \
  --config configs/searchqa/default.yaml \
  --skill outputs/my_run/best_skill.md \
  --split valid_unseen \
  --split_dir /path/to/searchqa_split \
  --azure_openai_endpoint https://your-resource.openai.azure.com/

# Evaluate on all splits (train + val + test):
python scripts/eval_only.py \
  --config configs/searchqa/default.yaml \
  --skill outputs/my_run/best_skill.md \
  --split all \
  --split_dir /path/to/searchqa_split \
  --azure_openai_endpoint https://your-resource.openai.azure.com/
```

| Split | Description |
|---|---|
| `valid_unseen` | Test set |
| `valid_seen` | Validation set |
| `train` | Training set |
| `all` | All splits combined (default) |

### Output Structure

Each run writes to a structured output directory:

```
outputs/<run_name>/
├── config.json              # Flattened runtime config
├── history.json             # Per-step training history
├── runtime_state.json       # Resume checkpoint
├── best_skill.md            # Best validated skill document
├── skills/skill_vXXXX.md   # Skill snapshot per step
├── steps/step_XXXX/        # Per-step artifacts (patches, evals)
├── slow_update/epoch_XX/   # Slow update logs
└── meta_skill/epoch_XX/    # Meta skill logs
```

Re-running the same command auto-resumes from the last completed step.

---

## WebUI

Launch the monitoring dashboard (optional):

```bash
pip install -e ".[webui]"
python -m skillopt_webui.app
```

| Flag | Default | Description |
|---|---|---|
| `--port` | 7860 | Server port |
| `--host` | `0.0.0.0` | Bind address |
| `--share` | off | Create a public Gradio share link |

```bash
# With public share link (useful for remote servers)
python -m skillopt_webui.app --share
```

---

## Citation

```bibtex
@misc{yang2026skilloptexecutivestrategyselfevolving,
      title={SkillOpt: Executive Strategy for Self-Evolving Agent Skills}, 
      author={Yifan Yang and Ziyang Gong and Weiquan Huang and Qihao Yang and Ziwei Zhou and Zisu Huang and Yan Li and Xuemei Gao and Qi Dai and Bei Liu and Kai Qiu and Yuqing Yang and Dongdong Chen and Xue Yang and Chong Luo},
      year={2026},
      eprint={2605.23904},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2605.23904}
}
```

