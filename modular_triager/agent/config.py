from pathlib import Path

def load_prompt_config():
    base = Path(__file__).parent

    system_prompt = (base / "prompts/system.txt").read_text()

    kb_parts = []
    kb_folder = base / "knowledge"

    for f in kb_folder.glob("*.*"):
        kb_parts.append(f"\n\n# {f.name}\n")
        kb_parts.append(f.read_text())

    full_prompt = system_prompt + "\n\n" + "\n".join(kb_parts)
    return full_prompt
