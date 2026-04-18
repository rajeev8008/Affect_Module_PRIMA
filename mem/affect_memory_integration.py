from typing import TypedDict, Dict

# =====================================================================
# PRIMA - Affective to Memory Integration Schema
# =====================================================================
# This file serves as the strict contract between the Affective Reasoning
# Module (ARM) and the Hierarchical Memory System (HMS) for easy plug-and-play.

class RawUserInputPayload(TypedDict):
    """
    The exact format that the Affective Module receives from the user input.
    This is the first stage of the PRIMA pipeline.
    """
    raw_text: str                   # The exact prompt the user typed (e.g. "I am frustrated.")

class ProcessedMemoryPayload(TypedDict):
    """
    The exact format that the Affective Module outputs and hands over to the 
    Memory Module for storage in the Short-Term/Working Memory.
    """
    raw_text: str                   # The exact prompt the user typed (e.g. "I am frustrated.")
    dominant_emotions: Dict[str, float]  # ONLY the top 5 emotions (filtered). e.g. {"sadness": 0.248, "disgust": 0.211, ...}
    vector_embedding: list[float]   # The mathematical vector embedding from DeBERTa (list of float32s)


# =====================================================================
# Example Payload Generator (For testing integration before modules are merged)
# =====================================================================
def get_mock_payload() -> ProcessedMemoryPayload:
    return {
        "raw_text": "Chefs not counting calories, study finds",
        "dominant_emotions": {
            "sadness": 0.248,
            "disgust": 0.211,
            "joy": 0.199,
            "boredom": 0.100,
            "interest_vigilance": 0.087
        }, # Strictly top 5, rounded to 3 decimal places
        "vector_embedding": [0.120, -0.450, 0.880, 0.010] # Truncated representation of the 768-dim list
    }
