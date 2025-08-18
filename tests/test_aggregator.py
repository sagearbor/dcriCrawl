import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.aggregator.aggregator import aggregate_by_domain, save_aggregated_csv


def test_aggregate_by_domain_and_save(tmp_path):
    input_file = tmp_path / "analysis.jsonl"
    records = [
        {
            "url": "https://example.com/a",
            "keywords": {"ai": ["ai"], "policy": []},
        },
        {
            "url": "https://example.com/b",
            "keywords": {"ai": [], "policy": ["privacy"]},
        },
        {
            "url": "https://other.com",
            "keywords": {"ai": ["artificial intelligence"], "policy": []},
        },
    ]
    with input_file.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    aggregated = aggregate_by_domain(str(input_file))
    assert aggregated["example.com"]["pages"] == 2
    assert aggregated["example.com"]["ai_keywords"] == ["ai"]
    assert aggregated["example.com"]["policy_keywords"] == ["privacy"]
    assert aggregated["other.com"]["pages"] == 1
    assert "artificial intelligence" in aggregated["other.com"]["ai_keywords"]

    filtered = aggregate_by_domain(str(input_file), min_pages=2)
    assert "other.com" not in filtered
    assert filtered["example.com"]["pages"] == 2

    output_file = tmp_path / "report.csv"
    save_aggregated_csv(aggregated, str(output_file))
    content = output_file.read_text(encoding="utf-8").splitlines()
    assert content[0].startswith("domain,")
    assert any("example.com" in line for line in content)
