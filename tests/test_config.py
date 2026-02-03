from src.config_loader import load_config

def test_dev_config():
    cfg = load_config("configs/dev.yaml")
    assert cfg["env"] == "dev"
    assert "cluster" in cfg
