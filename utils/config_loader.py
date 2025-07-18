import os
import json

def load_extraction_config(customer_id: str, config_folder="config") -> dict:
    """
    Load the GPT entity extraction config JSON for a given customer_id.
    Falls back to an empty dict if file not found or invalid.
    
    Expects config files named like: extraction_config_<customer_id>.json
    in the `config_folder` directory.
    """
    filename = f"extraction_config_{customer_id}.json"
    path = os.path.join(config_folder, filename)
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"⚠️ Extraction config file not found for customer: {customer_id}")
        return {}
    except json.JSONDecodeError as e:
        print(f"⚠️ Extraction config JSON decode error for {customer_id}: {e}")
        return {}
