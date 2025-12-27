from owlready2 import *
from datetime import datetime
import os

# --------------------------------------------------
# Resolve ontology path safely (CRITICAL FIX)
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
ONTOLOGY_PATH = os.path.join(
    PROJECT_ROOT,
    "ontology",
    "hospital_theatre_scheduling.owl"
)

# Load ontology using absolute path
onto = get_ontology(ONTOLOGY_PATH).load()


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------
def find_by_name(cls, name: str):
    if not name:
        return None

    for inst in cls.instances():
        if hasattr(inst, "hasName"):
            for n in inst.hasName:
                if n.lower() == name.lower():
                    return inst
    return None


# --------------------------------------------------
# Availability Check
# --------------------------------------------------
def check_theatre_availability(theatre_name: str):
    theatre = find_by_name(onto.Theatre, theatre_name)

    if not theatre:
        return False, "Theatre does not exist in the system."

    if False in theatre.isClean:
        return False, "Theatre is not cleaned."

    if True in theatre.isUnderMaintenance:
        return False, "Theatre is under maintenance."

    return True, "Theatre is clean and ready for surgery."


# --------------------------------------------------
# Scheduling Validation
# --------------------------------------------------
def validate_schedule(payload: dict):
    surgeon = find_by_name(onto.Surgeon, payload.get("surgeon_name"))
    theatre = find_by_name(onto.Theatre, payload.get("theatre_name"))

    if not surgeon:
        return {"is_valid": False, "reason": "Surgeon not found."}

    if not theatre:
        return {"is_valid": False, "reason": "Theatre not found."}

    if False in surgeon.isPresent:
        return {"is_valid": False, "reason": "Surgeon is not present."}

    if False in theatre.isClean:
        return {"is_valid": False, "reason": "Theatre is not clean."}

    if True in theatre.isUnderMaintenance:
        return {"is_valid": False, "reason": "Theatre is under maintenance."}

    return {
        "is_valid": True,
        "reason": "All conditions satisfied. Scheduling allowed."
    }


# --------------------------------------------------
# Create Schedule Record
# --------------------------------------------------
def create_schedule_record(payload: dict):
    try:
        surgeon = find_by_name(onto.Surgeon, payload.get("surgeon_name"))
        theatre = find_by_name(onto.Theatre, payload.get("theatre_name"))

        if not surgeon or not theatre:
            return {
                "success": False,
                "reason": "Required entities not found."
            }

        schedule_id = f"Schedule_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        schedule = onto.Schedule(schedule_id)
        schedule.hasSurgeon = [surgeon]
        schedule.hasTheatre = [theatre]

        # Save using the SAME resolved path
        onto.save(file=ONTOLOGY_PATH, format="rdfxml")

        return {"success": True}

    except Exception as e:
        return {"success": False, "reason": str(e)}
