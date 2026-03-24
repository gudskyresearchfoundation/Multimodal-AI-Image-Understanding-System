import argparse
from vlm_engine import describe_image_with_qwen
from llm_engine import reason_from_description


def run_pipeline(image_path: str, question: str | None = None):
    print("\n[1/2] Generating scene description with LLaVA...\n")
    description = describe_image_with_qwen(image_path, question)

    print("=== SCENE DESCRIPTION ===")
    print(description)

    print("\n[2/2] Generating final response with Llama 3...\n")
    final_response = reason_from_description(description, question)

    print("=== FINAL RESPONSE ===")
    print(final_response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--question", default=None)
    args = parser.parse_args()

    run_pipeline(args.image, args.question)