import subprocess
from config import LLAMA_PATH, MODEL_PATH, MMPROJ_PATH, MAX_TOKENS

def describe_image_with_qwen(image_path, prompt):
    command = [
        LLAMA_PATH,
        "-m", MODEL_PATH,
        "--mmproj", MMPROJ_PATH,
        "--image", image_path,
        "-p", prompt,
        "-n", str(MAX_TOKENS),
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return result.stdout.strip()