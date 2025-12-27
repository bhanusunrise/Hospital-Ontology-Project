from owlready2 import *

# --------------------------------------------------
# Ontology Definition
# --------------------------------------------------
onto = get_ontology(
    "http://www.example.org/hospital_theatre_scheduling.owl"
)

with onto:

    # --------------------------------------------------
    # Core Classes
    # --------------------------------------------------

    class Person(Thing):
        """Any human involved in hospital operations."""
        pass

    class Patient(Person):
        """A person scheduled to undergo a surgical operation."""
        pass

    class Surgeon(Person):
        """A medical professional responsible for performing surgeries."""
        pass

    class Operation(Thing):
        """A surgical procedure planned for a patient."""
        pass

    class Theatre(Thing):
        """A hospital operating theatre."""
        pass

    class TimeSlot(Thing):
        """A defined time period for scheduling surgeries."""
        pass

    class Schedule(Thing):
        """
        A scheduling event that assigns a patient, surgeon,
        operation, theatre, and time slot together.
        """
        pass

    # --------------------------------------------------
    # Object Properties (Relationships)
    # --------------------------------------------------

    class hasPatient(ObjectProperty):
        domain = [Schedule]
        range = [Patient]

    class hasSurgeon(ObjectProperty):
        domain = [Schedule]
        range = [Surgeon]

    class hasOperation(ObjectProperty):
        domain = [Schedule]
        range = [Operation]

    class hasTheatre(ObjectProperty):
        domain = [Schedule]
        range = [Theatre]

    class hasTimeSlot(ObjectProperty):
        domain = [Schedule]
        range = [TimeSlot]

    class surgeonAvailableAt(ObjectProperty):
        """
        Indicates when a surgeon is available to perform surgeries.
        """
        domain = [Surgeon]
        range = [TimeSlot]

    class theatreAvailableAt(ObjectProperty):
        """
        Indicates when a theatre is available for surgery.
        """
        domain = [Theatre]
        range = [TimeSlot]

    class conflictsWith(ObjectProperty):
        """
        Represents overlapping time slots.
        """
        domain = [TimeSlot]
        range = [TimeSlot]
        symmetric = True

    # --------------------------------------------------
    # Data Properties (Attributes)
    # --------------------------------------------------

    class isClean(DataProperty):
        """
        Indicates whether a theatre is cleaned and ready.
        """
        domain = [Theatre]
        range = [bool]

    class isUnderMaintenance(DataProperty):
        """
        Indicates whether a theatre is under maintenance.
        """
        domain = [Theatre]
        range = [bool]

    class isPresent(DataProperty):
        """
        Indicates whether a surgeon is present at the hospital.
        """
        domain = [Surgeon]
        range = [bool]

    class operationDuration(DataProperty):
        """
        Duration of the operation in minutes.
        """
        domain = [Operation]
        range = [int]

    class priorityLevel(DataProperty):
        """
        Priority level of the operation (e.g., emergency, elective).
        """
        domain = [Operation]
        range = [str]

    class maxDailyHours(DataProperty):
        """
        Maximum operating hours per day for a surgeon.
        """
        domain = [Surgeon]
        range = [int]

    # --------------------------------------------------
    # Ontology Constraints (Rules as OWL Restrictions)
    # --------------------------------------------------

    # A schedule must involve exactly one patient
    Schedule.is_a.append(
        hasPatient.exactly(1, Patient)
    )

    # A schedule must involve exactly one surgeon
    Schedule.is_a.append(
        hasSurgeon.exactly(1, Surgeon)
    )

    # A schedule must involve exactly one operation
    Schedule.is_a.append(
        hasOperation.exactly(1, Operation)
    )

    # A schedule must involve exactly one theatre
    Schedule.is_a.append(
        hasTheatre.exactly(1, Theatre)
    )

    # A schedule must involve exactly one time slot
    Schedule.is_a.append(
        hasTimeSlot.exactly(1, TimeSlot)
    )

    # Every surgeon must have at least one available time slot
    Surgeon.is_a.append(
        surgeonAvailableAt.some(TimeSlot)
    )

    # Every theatre must have at least one available time slot
    Theatre.is_a.append(
        theatreAvailableAt.some(TimeSlot)
    )

    # A theatre cannot be under maintenance and usable at the same time
    Theatre.is_a.append(
        Not(isUnderMaintenance.value(True))
    )

    # A theatre must be clean to be usable
    Theatre.is_a.append(
        isClean.value(True)
    )

    # A surgeon must be present to perform a surgery
    Surgeon.is_a.append(
        isPresent.value(True)
    )


# --------------------------------------------------
# Save Ontology
# --------------------------------------------------
onto.save(
    file="hospital_theatre_scheduling.owl",
    format="rdfxml"
)
