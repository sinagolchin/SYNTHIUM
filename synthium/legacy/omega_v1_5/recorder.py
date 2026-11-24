import json
import os
from datetime import datetime
from .vectors import SynthiumVector

LEXICON_PATH = os.path.join("data", "lexicon.json")

class Recorder:
    def __init__(self):
        self._ensure_lexicon_exists()

    def _ensure_lexicon_exists(self):
        if not os.path.exists(LEXICON_PATH):
            os.makedirs("data", exist_ok=True)
            with open(LEXICON_PATH, "w") as f:
                json.dump({
                    "meta": {"version": "1.5", "created": datetime.now().isoformat()},
                    "discovered_units": []
                }, f, indent=2)

    def find_entry(self, name: str):
        with open(LEXICON_PATH, "r") as f:
            data = json.load(f)
        for entry in data["discovered_units"]:
            if entry["term"].lower() == name.lower():
                return entry
        return None

    def save_discovery(self, name: str, vector: SynthiumVector, formula: str):
        with open(LEXICON_PATH, "r") as f:
            data = json.load(f)

        # Check for existing
        for i, entry in enumerate(data["discovered_units"]):
            if entry["term"].lower() == name.lower():
                data["discovered_units"][i] = self._create_entry(name, vector, formula)
                action = "UPDATED"
                break
        else:
            data["discovered_units"].append(self._create_entry(name, vector, formula))
            action = "RECORDED"

        with open(LEXICON_PATH, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"[LEXICON]: {action} '{name}'")

    def _create_entry(self, name, vector, formula):
        return {
            "term": name,
            "vector": {"v": vector.v, "R": vector.R, "r": vector.r, "C": vector.C, "S": vector.S},
            "formula": formula,
            "timestamp": datetime.now().isoformat(),
            "category": "Psychological" if vector.S > 0.3 else "Physical"
        }

    def get_statistics(self):
        with open(LEXICON_PATH, "r") as f:
            data = json.load(f)
        return {
            "total_entries": len(data["discovered_units"]),
            "last_modified": data["meta"].get("last_modified", "N/A")
        }
