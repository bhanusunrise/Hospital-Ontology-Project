import streamlit as st
from services.data_validator import extract_schedule_data
from services.ontology_validator import (
    validate_schedule,
    check_theatre_availability,
    create_schedule_record
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Hospital Theatre Scheduling System",
    page_icon="🏥",
    layout="wide"
)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("🏥 Hospital Theatre Scheduling System")
st.subheader("Ontology-Guided Surgery Scheduling Assistant")

st.markdown("""
This system supports **safe and conflict-free hospital theatre scheduling**.

You may:
- Check **theatre availability**
- Validate **surgery scheduling requests**
- Confirm and **store schedules in the ontology**
""")

st.markdown("---")

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.header("📋 System Overview")
    st.info(
        "The system uses an ontology as its knowledge base and "
        "validates all scheduling decisions against hospital rules."
    )

# --------------------------------------------------
# Main Layout
# --------------------------------------------------
left_col, right_col = st.columns([2, 1])

# --------------------------------------------------
# Input Section
# --------------------------------------------------
with left_col:
    st.markdown("## 📝 Enter Request")

    user_query = st.text_area(
        "Describe what you want to do:",
        placeholder="Example: Is Theatre A available?",
        height=140
    )

    validate_btn = st.button("🔍 Process Request")
    reset_btn = st.button("🔄 Reset")

# --------------------------------------------------
# Helper: Detect Availability-Only Query
# --------------------------------------------------


def is_availability_query(payload: dict) -> bool:
    return (
        payload.get("theatre_name") is not None
        and payload.get("surgeon_name") is None
        and payload.get("operation_type") is None
    )


# --------------------------------------------------
# Right Panel – Processing
# --------------------------------------------------
with right_col:
    st.markdown("## 📌 System Status")

    if validate_btn and user_query.strip():

        with st.spinner("⏳ Processing your request..."):
            extracted = extract_schedule_data(user_query)

        st.markdown("### 🔍 Extracted Information")
        st.json(extracted)

        # ------------------------------
        # Availability Query
        # ------------------------------
        if is_availability_query(extracted):

            available, reason = check_theatre_availability(
                extracted["theatre_name"]
            )

            if available:
                st.success("✅ Theatre is available")
                st.info(reason)

                st.session_state["pending_schedule"] = extracted

                if st.button("📅 Schedule Surgery"):
                    result = create_schedule_record(
                        st.session_state["pending_schedule"]
                    )

                    if result["success"]:
                        st.success("✅ Surgery scheduled and saved in ontology")
                    else:
                        st.error(result["reason"])

            else:
                st.error("❌ Theatre not available")
                st.info(reason)

        # ------------------------------
        # Scheduling Request
        # ------------------------------
        else:
            with st.spinner("🧠 Validating against hospital rules..."):
                validation = validate_schedule(extracted)

            if validation["is_valid"]:
                st.success("✅ Schedule is valid")

                if st.button("📅 Confirm and Save Schedule"):
                    result = create_schedule_record(extracted)

                    if result["success"]:
                        st.success("✅ Surgery scheduled and saved in ontology")
                    else:
                        st.error(result["reason"])
            else:
                st.error("❌ Scheduling not allowed")
                st.info(validation["reason"])

    else:
        st.info("Enter a request and click **Process Request**")

# --------------------------------------------------
# Reset
# --------------------------------------------------
if reset_btn:
    st.session_state.clear()
    st.experimental_rerun()

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.caption(
    "Academic Prototype | Ontology-Guided Decision Support System"
)
