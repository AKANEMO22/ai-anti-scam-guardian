import os

def get_base_data_dir() -> str:
    """Returns the absolute path to the data directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    data_dir = os.path.join(project_root, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir
