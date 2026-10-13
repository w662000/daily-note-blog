---
layout: default
title: 技术点 · Experiment Design Patterns
date: 2026-10-10 23:30:00 +0800
---

# 技术点 · Experiment Design Patterns

> 来源：261010_Experiment Design Patterns_handoff.md（项目 handoff 1:1 companion，由 techpoint_flow 新方法提炼；读取编码：utf-8）

## 一、技术选型
（源 handoff 未单列技术选型）

## 二、实施要点与关键技术
（源 handoff 未单列实施要点）

### 关键技术要点（自动抽取）
- ```
workspace/
  experiments/
    run_main.py                # Core experiment runner
    run_baselines.py           # Baseline comparison
    run_ablation.py            # Ablation studies
    strategies.py              # Method implementations
    config.yaml                # Shared configuration
  results/
    <experiment_name>/
      <task_or_problem>/
        <strategy>/
          result.json          # Final metrics
          final_output.md      # Final output artifact
          history.json         # Full trajectory/log
          pass_01/             # Per-iteration artifacts (if iterative)
            intermediate.md
  analysis/
    analyze_results.py         # Statistical analysis
    compute_stats.py           # Significance tests
    make_charts.py             # Visualization
  paper/
    paper.tex                  # LaTeX source
    fig_*.pdf                  # Generated figures
```
- ```
import json, os
from pathlib import Path

def run_experiment(problems, strategies, output_dir):
    for problem in problems:
        for strategy in strategies:
            result_path = Path(output_dir) / problem["id"] / strategy / "result.json"
            if result_path.exists():
                print(f"Skipping {problem['id']}/{strategy} (already done)")
                continue
            
            # Run the experiment
            result = execute_strategy(problem, strategy)
            
            # Save immediately
            result_path.parent.mkdir(parents=True, exist_ok=True)
            with open(result_path, 'w') as f:
                json.dump(result, f, indent=2)
```
- ```
def save_pass_artifacts(output_dir, pass_num, artifacts):
    """Save all artifacts from a single pass of an iterative method."""
    pass_dir = Path(output_dir) / f"pass_{pass_num:02d}"
    pass_dir.mkdir(parents=True, exist_ok=True)
    
    for name, content in artifacts.items():
        with open(pass_dir / f"{name}.md", 'w') as f:
            f.write(content)
```
- ```
# config.yaml
model: anthropic/claude-sonnet-4-20250514
author_temperature: 0.8
judge_temperature: 0.3
max_tokens: 4096
num_judges: 3
max_passes: 15
convergence_k: 2
```
- ```
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)
```
- ```
import random

def run_blind_evaluation(outputs: dict, task_prompt: str, num_judges: int = 7):
    """
    Run blind evaluation of multiple method outputs.
    
    Args:
        outputs: {"method_name": "output_text", ...}
        task_prompt: The original task description
        num_judges: Number of independent judge evaluations
    """
    rankings = []
    
    for judge_i in range(num_judges):
        # Randomize labels and presentation order per judge
        methods = list(outputs.keys())
        random.shuffle(methods)
        labels = {m: chr(65 + i) for i, m in enumerate(methods)}  # A, B, C...
        
        # Present to judge with randomized labels
        prompt = f"Task: {task_prompt}\n\n"
        for method in methods:
            prompt += f"--- Proposal {labels[method]} ---\n{outputs[method]}\n\n"
        prompt += "Rank all proposals from best to worst. Format: RANKING: [best], [second], [worst]"
        
        ranking = call_judge(prompt)
        rankings.append({"labels": labels, "ranking": ranking})
    
    # Aggregate via Borda count
    return compute_borda(rankings)

def compute_borda(rankings, n_methods=3):
    """Borda count: 3/2/1 points for 1st/2nd/3rd."""
    scores = {}
    points = {0: n_methods, 1: n_methods - 1, 2: n_methods - 2}  # Adjust for n_methods
    
    for r in rankings:
        for position, method in enumerate(r["ranking"]):
            scores[method] = scores.get(method, 0) + points.get(position, 0)
    
    return scores
```
- Key design decisions:
- ```
import subprocess

def evaluate_code(solution: str, test_cases: list, timeout: int = 30):
    """Run code solution against test cases with sandboxed execution."""
    results = {"public": [], "private": []}
    
    for test in test_cases:
        try:
            proc = subprocess.run(
                ["python3", "-c", solution],
                input=test["input"],
                capture_output=True,
                timeout=timeout,
                text=True
            )
            actual = proc.stdout.strip()
            expected = test["expected"].strip()
            passed = actual == expected
        except subprocess.TimeoutExpired:
            passed = False
        
        category = "public" if test.get("public") else "private"
        results[category].append(passed)
    
    return {
        "public_pass_rate": sum(results["public"]) / max(len(results["public"]), 1),
        "private_pass_rate": sum(results["private"]) / max(len(results["private"]), 1),
    }
```
- Always compare methods at equal compute budget. If your method uses N API calls, baselines get N calls too:
- ```
Human Evaluation Protocol:
1. Define the evaluation dimensions (fluency, relevance, factual accuracy, etc.)
2. Create annotation guidelines with examples of each score level
3. Run a pilot with 2-3 annotators on 20-30 examples
4. Compute pilot inter-annotator agreement — if low, revise guidelines
5. Run full evaluation
6. Report: annotator count, agreement metrics, compensation, time per item
```
- ```
# Krippendorff's alpha (preferred — handles missing data, any scale)
# pip install krippendorffs-alpha
import krippendorff

# Ratings: rows = annotators, columns = items, values = scores
ratings = [
    [3, 4, 1, 2, 5, None, 3],  # Annotator 1
    [3, 5, 1, 3, 5, 2, 3],     # Annotator 2
    [4, 4, 2, 2, 4, 2, None],  # Annotator 3
]
alpha = krippendorff.alpha(reliability_data=ratings, level_of_measurement="ordinal")
print(f"Krippendorff's alpha: {alpha:.3f}")
# Interpretation: >0.80 good, 0.67-0.80 acceptable, <0.67 questionable
```
- ```
# Cohen's kappa (for exactly 2 annotators, categorical data)
from sklearn.metrics import cohen_kappa_score

annotator_1 = [1, 2, 3, 1, 2, 3, 2]
annotator_2 = [1, 2, 2, 1, 3, 3, 2]
kappa = cohen_kappa_score(annotator_1, annotator_2)
print(f"Cohen's kappa: {kappa:.3f}")
# Interpretation: >0.80 excellent, 0.60-0.80 substantial, 0.40-0.60 moderate
```

## 三、关键产物与命令
（见源 handoff 关键产物字段）

## 四、如何复现 / 重打
（见源 handoff 重打方法字段）

## 五、后续风险
（见源 handoff 后续风险字段）
