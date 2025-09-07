from core.src.ai_collaboration.grok_adapter import MultiModelOrchestrator


def mock_heavy(prompt: str) -> str:
    return f"Heavy prediction: {prompt}"


def mock_light(prompt: str) -> str:
    return f"Light response: {prompt}"


def test_heavy_training_populates_dataset():
    orch = MultiModelOrchestrator(mock_heavy, mock_heavy, mock_light)
    res = orch.run_heavy_training("TrainX")

    # both heavy results present and are lists of 5 iterations
    assert 'heavy_1' in res and 'heavy_2' in res
    assert isinstance(res['heavy_1'], list) and len(res['heavy_1']) == 5
    assert isinstance(res['heavy_2'], list) and len(res['heavy_2']) == 5

    # shared dataset should have 10 entries (5 from each heavy model)
    assert len(orch.dataset) == 10
    assert orch.dataset[0].startswith("Heavy prediction: TrainX - iteration 0")


def test_light_pull_returns_response_using_dataset():
    orch = MultiModelOrchestrator(mock_heavy, mock_heavy, mock_light)
    orch.run_heavy_training("TrainY")
    out = orch.run_light_pull("Summarize the training")

    assert isinstance(out, str)
    # light response should be produced and include the query
    assert out.startswith("Light response:")
    assert "Summarize the training" in out
    assert "based on:" in out


def test_light_pull_no_dataset():
    orch = MultiModelOrchestrator(mock_heavy, mock_heavy, mock_light)
    out = orch.run_light_pull("Q")
    assert out == "No dataset available from heavy models."
