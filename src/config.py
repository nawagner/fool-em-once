from dataclasses import dataclass
from enum import Enum


class Category(Enum):
    HISTORICAL = "historical"
    LITERATURE = "literature"
    SCIENTIFIC = "scientific"
    PERSONAL = "personal"


@dataclass
class Topic:
    id: str
    category: Category
    title: str
    prompt: str


# Model IDs for OpenRouter
MODELS = {
    "gemini-3-flash": "google/gemini-3-flash-preview",
    "gpt-5.2": "openai/gpt-5.2",
}

TOPICS = [
    # Historical (5)
    Topic(
        "hist-01",
        Category.HISTORICAL,
        "Richest Person in History",
        "Write a 500-word high school essay on: Who is really the richest person in history?",
    ),
    Topic(
        "hist-02",
        Category.HISTORICAL,
        "Korean Comfort Women",
        "Write a 500-word high school essay on: The story of Korean comfort women and their impact on modern day Japanese-Korean relations",
    ),
    Topic(
        "hist-03",
        Category.HISTORICAL,
        "American Industrial Espionage",
        "Write a 500-word high school essay on: American industrial espionage in the late 18th and early 19th centuries",
    ),
    Topic(
        "hist-04",
        Category.HISTORICAL,
        "Rosa Parks After Montgomery",
        "Write a 500-word high school essay on: Rosa Parks' contribution to Civil Rights after the Montgomery bus boycott",
    ),
    Topic(
        "hist-05",
        Category.HISTORICAL,
        "Cane Toads in Australia",
        "Write a 500-word high school essay on: The lessons learned from introducing cane toads in Australia",
    ),
    # Literature (5)
    Topic(
        "lit-01",
        Category.LITERATURE,
        "Frankenstein and AI",
        "Write a 500-word high school literary analysis on: Mary Shelley's Frankenstein's relevance to modern debates on artificial intelligence",
    ),
    Topic(
        "lit-02",
        Category.LITERATURE,
        "1984 vs Brave New World",
        "Write a 500-word high school literary analysis on: Between 1984 and Brave New World, which dystopia is more likely to become true and why?",
    ),
    Topic(
        "lit-03",
        Category.LITERATURE,
        "Whitman and Civil War",
        "Write a 500-word high school literary analysis on: How Walt Whitman's experience in the Civil War influenced his poetry",
    ),
    Topic(
        "lit-04",
        Category.LITERATURE,
        "Rumi as Sufi Mystic",
        "Write a 500-word high school literary analysis on: The poet Rumi's role as a Sufi mystic and how his work (like the Masnavi) reflects Islamic mystical tradition",
    ),
    Topic(
        "lit-05",
        Category.LITERATURE,
        "Machiavelli's Prince",
        "Write a 500-word high school literary analysis on: Is Machiavelli's The Prince a genuine guide for tyrants or a satirical critique?",
    ),
    # Scientific (5)
    Topic(
        "sci-01",
        Category.SCIENTIFIC,
        "Geoengineering Water Cycle",
        "Write a 500-word high school science essay on: Methods of geoengineering the water cycle and their potential drawbacks",
    ),
    Topic(
        "sci-02",
        Category.SCIENTIFIC,
        "Earthquake Detectors",
        "Write a 500-word high school science essay on: How do earthquake detectors work?",
    ),
    Topic(
        "sci-03",
        Category.SCIENTIFIC,
        "Eutectics in Metals",
        "Write a 500-word high school science essay on: What are eutectics and why do they matter for metals engineering?",
    ),
    Topic(
        "sci-04",
        Category.SCIENTIFIC,
        "Fermi Paradox",
        "Write a 500-word high school science essay on: What is the Fermi paradox and what are some likely explanations?",
    ),
    Topic(
        "sci-05",
        Category.SCIENTIFIC,
        "Continental Drift Evidence",
        "Write a 500-word high school science essay on: What evidence do we have that Earth's continents were once contiguous?",
    ),
    # Personal (5)
    Topic(
        "pers-01",
        Category.PERSONAL,
        "Mom's Cooking Appreciation",
        "Write a 500-word personal essay from the perspective of a half Chinese and half German-American teenager who was at first ashamed of their Malaysian immigrant mom's cooking but grew to appreciate it and their culture.",
    ),
    Topic(
        "pers-02",
        Category.PERSONAL,
        "Perfect Chill Day",
        "Write a 500-word personal essay describing being a chill person whose perfect day is making a cup of tea, reading a book, getting lunch with friends, playing co-op video games, and watching TV beside their cat.",
    ),
    Topic(
        "pers-03",
        Category.PERSONAL,
        "Social Media Relationship",
        "Write a 500-word personal essay about having a complicated relationship with social media - how it connects to friends and family but also saps attention span and causes jealousy of others' superficial portrayals.",
    ),
    Topic(
        "pers-04",
        Category.PERSONAL,
        "Interview Embarrassment",
        "Write a 500-word personal essay about how completely embarrassing oneself at a high school prep entrance interview showed they were genuine and able to grow.",
    ),
    Topic(
        "pers-05",
        Category.PERSONAL,
        "Bali Healing Journey",
        "Write a 500-word personal essay about how a trip to Bali after a divorce helped heal emotional trauma and reconnect with an authentic self.",
    ),
]


def get_topics_by_category(category: Category) -> list[Topic]:
    return [t for t in TOPICS if t.category == category]
