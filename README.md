# SkillOpt: Executive Strategy for Self-Evolving Agent Skills (Community Fork: No Azure Required)

*This is a community fork of Microsoft's SkillOpt framework. It has been patched to natively support standard OpenAI endpoints (like OpenAI API, DeepSeek via Polza.ai, Ollama, vLLM) without crashing or requiring Azure OpenAI configurations. It also includes fixes for UTF-8 encoding (Russian language support) and simplified model setup.*

*Train agent skills like you train neural networks — with epochs, (mini-)batchsize, learning rates, and validation gates — but without touching model weights.*

[![Project Page](https://img.shields.io/badge/Project%20Page-SkillOpt-8dbb3c)](https://microsoft.github.io/SkillOpt/) [![Paper](https://img.shields.io/badge/Paper-arXiv-b31b1b)](https://arxiv.org/abs/2605.23904) [![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🛠️ What's new in this Fork?

1. **No Azure Lock-in:** The original `azure_openai.py` wrapper has been bypassed. You can now use `api_type: "openai"` to connect to *any* OpenAI-compatible endpoint (Ollama, DeepSeek, standard OpenAI) without setting dummy Azure variables.
2. **UTF-8 Support:** Fixed `UnicodeDecodeError` when reading/writing skill files containing non-ASCII (e.g., Russian) characters on Windows.
3. **Simplified Backend:** A new `simple_openai.py` backend handles direct connections, making local experimentation much faster.

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

Instead of messy environment variables, this fork strongly encourages configuring your models directly in your `config.yaml` file using the standard `endpoint` and `api_key` keys.

Create a `config.yaml` like this:

```yaml
# Core environment settings
env: "searchqa"
split_mode: "split_dir"
split_dir: "data/my_split"

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

skill_init: "configs/initial_skill.md"
out_root: "outputs/my_training"
```

### Run Training

```bash
python scripts/train.py --config config.yaml
```

---

## Data Preparation

SkillOpt expects data in a **split directory** with `train/`, `val/`, `test/` subdirectories, each containing a JSON file (e.g., `items.json` or `data.json`).

```
data/my_split/
├── train/data.json
├── val/data.json
└── test/data.json
```

Each JSON file is an array of task items. Example for QA tasks:

```json
[
  {
    "id": "1",
    "question": "Сколько пользователей зарегистрировано в системе?",
    "answers": ["SELECT COUNT(*) FROM users;"]
  }
]
```

---

## Supported Benchmarks (From Original Repo)

| Benchmark | Type | Config |
|---|---|---|
| SearchQA | QA | `configs/searchqa/default.yaml` |
| ALFWorld | Embodied agent | `configs/alfworld/default.yaml` |
| DocVQA | Document QA | `configs/docvqa/default.yaml` |
| LiveMathematicianBench | Math | `configs/livemathematicianbench/default.yaml` |
| SpreadsheetBench | Code generation | `configs/spreadsheetbench/default.yaml` |
| OfficeQA | Tool-augmented QA | `configs/officeqa/default.yaml` |

---

## Quick Start

### Training

```bash
# Minimal example — train on SearchQA:
python scripts/train.py \
    --config configs/searchqa/default.yaml \
    --split_dir /path/to/your/searchqa_split \
    --azure_openai_endpoint https://your-resource.openai.azure.com/ \
    --optimizer_model gpt-5.5 \
    --target_model gpt-5.5

# Train on LiveMathematicianBench:
python scripts/train.py \
    --config configs/livemathematicianbench/default.yaml \
    --split_dir /path/to/your/livemath_split \
    --azure_openai_endpoint https://your-resource.openai.azure.com/ \
    --optimizer_model gpt-5.5 \
    --target_model gpt-5.5

# Train on ALFWorld:
python scripts/train.py \
    --config configs/alfworld/default.yaml \
    --split_dir /path/to/your/alfworld_split \
    --azure_openai_endpoint https://your-resource.openai.azure.com/ \
    --optimizer_model gpt-5.5 \
    --target_model gpt-5.5
```

Key CLI arguments:

| Argument | Description | Example |
|---|---|---|
| `--config` | Benchmark config YAML | `configs/searchqa/default.yaml` |
| `--split_dir` | Path to data split directory | `/path/to/split` |
| `--azure_openai_endpoint` | Azure OpenAI endpoint URL | `https://your-resource.openai.azure.com/` |
| `--optimizer_model` | Optimizer model deployment name | `gpt-5.5` |
| `--target_model` | Target model deployment name | `gpt-5.5` |
| `--num_epochs` | Number of training epochs | `4` |
| `--batch_size` | Batch size per step | `40` |
| `--workers` | Parallel rollout workers | `8` |
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

