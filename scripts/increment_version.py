from pathlib import Path
import re

version_file = Path("version.txt")
current = version_file.read_text().strip()
major, minor = map(int, current.split("."))

new_version = f"{major}.{minor + 1}"
version_file.write_text(new_version)
print(f"Incrémentation : {current} ➜ {new_version}")
