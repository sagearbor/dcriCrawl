import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.analyzer.pipeline import analyze_crawled_data


def test_analyze_crawled_data(tmp_path):
    input_file = tmp_path / "crawled.jsonl"
    output_file = tmp_path / "analysis.jsonl"
    html = "<html><body>AI is used. See our privacy policy.</body></html>"
    record = {"url": "https://example.com", "html": html, "timestamp": "2024-01-01T00:00:00"}
    input_file.write_text(json.dumps(record) + "\n", encoding="utf-8")

    analyze_crawled_data(str(input_file), str(output_file))

    lines = output_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    result = json.loads(lines[0])
    assert result["url"] == "https://example.com"
    assert "ai" in result["keywords"]["ai"]
    assert "policy" in result["keywords"]["policy"]
