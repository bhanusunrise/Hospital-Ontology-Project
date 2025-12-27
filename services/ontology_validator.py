"""
ontology_validator.py
---------------------

Purpose:
- Validate scheduling requests against the hospital ontology
- Check availability, readiness, and safety rules
- Return a clear decision and explanation

This module represents the ontology-based reasoning layer.
"""

from owlready2 import *
from typing import Dict, Any


# --------------------------------------------------
# Load Ontology
# --------------------------------------------------

ONTOLOGY_PATH = "ontology/hospital_theatre_scheduling.owl"

onto = get_ontology(ONTOLOGY_PATH).load()


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def find_individual_by_name(cls, name: str):
    """
    Find an individual in the ontology by class and name.
    """
    if not name:
        return None

    for individual in cls.instances():
        if individual.name.lower() == name.lower().replace(" ", "_"):
            return individual
    return None


# --------------------------------------------------
# Core Validation Function
# --------------------------------------------------

def validate_schedule(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates extracted scheduling data against the ontology.

    Returns:
    {
        "is_valid": bool,
        "reason": str
    }
    """

    # -----------------------------
    # Extract payload values
    # -----------------------------
    surgeon_name = payload.get("surgeon_name")
    theatre_name = payload.get("theatre_name")
    operation_type = payload.get("operation_type")

    # -----------------------------
    # Grounding: check existence
    # -----------------------------
    surgeon = find_individual_by_name(onto.Surgeon, surgeon_name)
    if not surgeon:
        return {
            "is_valid": False,
            "reason": f"Surgeon '{surgeon_name}' is not registered in the system."
        }

    theatre = find_individual_by_name(onto.Theatre, theatre_name)
    if not theatre:
        return {
            "is_valid": False,
            "reason": f"Theatre '{theatre_name}' is not available in the hospital."
        }

    # -----------------------------
    # Theatre safety checks
    # -----------------------------
    if theatre.isUnderMaintenance and True in theatre.isUnderMaintenance:
        return {
            "is_valid": False,
            "reason": "The selected theatre is currently under maintenance."
        }

    if theatre.isClean and False in theatre.isClean:
        return {
            "is_valid": False,
            "reason": "The selected theatre is not cleaned and ready for surgery."
        }

    # -----------------------------
    # Surgeon availability checks
    # -----------------------------
    if surgeon.isPresent and False in surgeon.isPresent:
        return {
            "is_valid": False,
            "reason": "The assigned surgeon is not currently present in the hospital."
        }

    # -----------------------------
    # Operation priority logic
    # -----------------------------
    if operation_type and "emergency" in operation_type.lower():
        return {
            "is_valid": True,
            "reason": (
                "Emergency surgery detected. "
                "The schedule is allowed as all safety conditions are satisfied."
            )
        }

    # -----------------------------
    # Default approval
    # -----------------------------
    return {
        "is_valid": True,
        "reason": "The theatre and surgeon are available for the requested schedule."
    }
