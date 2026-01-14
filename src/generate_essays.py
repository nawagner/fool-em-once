import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

from config import MODELS, Topic, Category, get_topics_by_category

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "essays" / "original"

# Load environment variables from .env.local
load_dotenv(BASE_DIR / ".env.local")


def get_api_key() -> str:
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER-API-KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Add it to .env.local or the environment."
        )
    return api_key


def request_chat_completion(
    *,
    model_id: str,
    messages: list[dict],
    api_key: str,
    base_url: str = "https://openrouter.ai/api/v1",
    max_retries: int = 3,
    retry_sleep=time.sleep,
    timeout: int = 60,
) -> str:
    url = f"{base_url}/chat/completions"
    payload = {
        "model": model_id,
        "messages": messages,
        "max_tokens": 800,
        "temperature": 0.7,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    last_error = None
    for attempt in range(max_retries):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=timeout,
            )
            if response.status_code >= 500:
                response.raise_for_status()
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except requests.RequestException as exc:
            last_error = exc
            if attempt >= max_retries - 1:
                break
            retry_sleep(2 ** attempt)

    if last_error:
        raise last_error
    raise RuntimeError("Failed to request chat completion.")


def generate_essay(topic: Topic, model_key: str) -> dict:
    """Generate a single essay using OpenRouter."""
    model_id = MODELS[model_key]
    api_key = get_api_key()

    content = request_chat_completion(
        model_id=model_id,
        api_key=api_key,
        messages=[
            {
                "role": "system",
                "content": "You are a high school student writing an essay for class. Write naturally and authentically as a student would. Do not use overly sophisticated vocabulary or perfect structure.",
            },
            {"role": "user", "content": topic.prompt},
        ],
    )
    word_count = len(content.split())

    return {
        "id": f"{model_key}_{topic.id}",
        "topic_id": topic.id,
        "topic_title": topic.title,
        "category": topic.category.value,
        "model": model_key,
        "content": content,
        "word_count": word_count,
    }


def generate_essays_for_category(category: Category, models: list[str] = None):
    """Generate essays for a single category (for pilot testing)."""
    if models is None:
        models = list(MODELS.keys())

    topics = get_topics_by_category(category)
    essays = []

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for model_key in models:
        for topic in topics:
            essay_id = f"{model_key}_{topic.id}"
            print(f"Generating: {essay_id} - {topic.title}")

            # Save individual text file for easy copy/paste
            txt_path = OUTPUT_DIR / f"{essay_id}.txt"
            if txt_path.exists():
                content = txt_path.read_text()
                essay = {
                    "id": essay_id,
                    "topic_id": topic.id,
                    "topic_title": topic.title,
                    "category": topic.category.value,
                    "model": model_key,
                    "content": content,
                    "word_count": len(content.split()),
                }
                essays.append(essay)
                continue

            essay = generate_essay(topic, model_key)
            essays.append(essay)
            txt_path.write_text(essay["content"])

            # Rate limiting
            time.sleep(1)

    # Save manifest
    manifest_path = OUTPUT_DIR / f"manifest_{category.value}.json"
    with open(manifest_path, "w") as f:
        json.dump(essays, f, indent=2)

    print(f"\nGenerated {len(essays)} essays for {category.value}")
    print(f"Individual files saved to: {OUTPUT_DIR}/")
    print(f"Manifest saved to: {manifest_path}")

    return essays


def generate_all_essays():
    """Generate all 40 essays."""
    all_essays = []

    for category in Category:
        essays = generate_essays_for_category(category)
        all_essays.extend(essays)
        time.sleep(2)  # Pause between categories

    # Save complete manifest
    manifest_path = OUTPUT_DIR / "manifest_all.json"
    with open(manifest_path, "w") as f:
        json.dump(all_essays, f, indent=2)

    print(f"\nTotal essays generated: {len(all_essays)}")
    return all_essays


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Pilot mode: generate for specific category
        category_name = sys.argv[1].upper()
        category = Category[category_name]
        generate_essays_for_category(category)
    else:
        # Full generation
        generate_all_essays()
