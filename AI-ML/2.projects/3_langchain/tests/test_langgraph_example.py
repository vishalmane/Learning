from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def load_build_graph():
    path = Path(__file__).resolve().parents[1] / "examples" / "08_langgraph" / "simple_graph.py"
    spec = spec_from_file_location("simple_graph_example", path)
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_graph


def test_simple_graph_returns_next_step() -> None:
    build_graph = load_build_graph()
    app = build_graph()
    result = app.invoke({"topic": "rag", "next_step": ""})
    assert "embed" in result["next_step"]
