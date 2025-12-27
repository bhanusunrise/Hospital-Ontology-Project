import streamlit as st
from services.data_validator import extract_schedule_data
from services.ontology_validator import validate_schedule



# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Hospital Theatre Scheduling System",
    page_icon="🏥",
    layout="wide"
)

# --------------------------------------------------
# Header Section
# --------------------------------------------------
st.title("🏥 Hospital Theatre Scheduling System")
st.subheader("Safe and Reliable Surgery Scheduling Support")

st.markdown(
    """
    This system helps you **plan and review surgery schedules** for hospital theatres.
    
    It checks surgeon availability, theatre usage, and time conflicts,
    and clearly explains whether a scheduling request is acceptable or not.
    
    The goal is to support **safe, organised, and conflict-free theatre scheduling**.
    """
)

st.markdown("---")

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.header("📋 System Information")

    st.markdown("### 🏥 What This System Does")
    st.info(
        "Supports daily hospital theatre scheduling by checking availability, "
        "detecting conflicts, and explaining scheduling decisions in a clear way."
    )

    st.markdown("### ✅ System Status")
    st.success("Scheduling System Ready")
    st.caption(
        "The system is aware of:\n"
        "- Surgeons and their working times\n"
        "- Operation types and durations\n"
        "- Operating theatres\n"
        "- Available time slots\n"
        "- Scheduling rules and conflicts"
    )

    st.markdown("### 💡 Example Requests")
    st.markdown(
        """
        • Schedule Dr. Silva for a knee surgery at 10:00 AM  
        • Check if Theatre A is free tomorrow morning  
        • Why was this surgery not allowed at this time?  
        """
    )

    st.markdown("### ℹ️ Notes")
    st.caption(
        "This system supports decision-making.\n"
        "Final scheduling decisions remain with hospital staff."
    )

# --------------------------------------------------
# Main Layout
# --------------------------------------------------
left_col, right_col = st.columns([2, 1])

# --------------------------------------------------
# Scheduling Request Input
# --------------------------------------------------
with left_col:
    st.markdown("## 📝 Enter Scheduling Request")

    user_query = st.text_area(
        label="Describe the surgery schedule you want to create or check:",
        placeholder=(
            "Example:\n"
            "Schedule Dr. Silva to perform a knee surgery in Theatre A at 9:00 AM"
        ),
        height=140
    )

    btn_col1, btn_col2, btn_col3 = st.columns(3)

    with btn_col1:
        validate_btn = st.button("🔍 Check Schedule")

    with btn_col2:
        explain_btn = st.button("🧠 View Explanation")

    with btn_col3:
        reset_btn = st.button("🔄 Clear Request")

# --------------------------------------------------
# Scheduling Status Panel
# --------------------------------------------------
with right_col:
    st.markdown("## 📌 Scheduling Status")

    if validate_btn and user_query.strip():
        extracted_data = extract_schedule_data(user_query)

        st.warning("⏳ Checking schedule...")

        st.markdown("### 🔍 Extracted Scheduling Details")
        st.json(extracted_data)

        validation_result = validate_schedule(extracted_data)

        st.markdown("## 📄 Scheduling Result")

        if validation_result["is_valid"]:
            st.success(validation_result["reason"])
        else:
            st.error(validation_result["reason"])

    else:
        st.info(
            "Enter a scheduling request and click **Check Schedule** "
            "to see whether it can be safely scheduled."
        )

# --------------------------------------------------
# System Response Section
# --------------------------------------------------
st.markdown("## 📄 Scheduling Result")

st.text_area(
    label="System Decision:",
    value=(
        "The scheduling decision will appear here.\n\n"
        "If the request is valid, the system will confirm it.\n"
        "If not, the system will clearly explain the reason."
    ),
    height=170,
    disabled=True
)

# --------------------------------------------------
# Explanation Section
# --------------------------------------------------
st.markdown("## 🧩 Explanation")

with st.expander("See how the decision was made"):
    st.markdown(
        """
        **How the system checks a schedule:**
        
        1. Identifies the surgeon, operation, theatre, and time requested  
        2. Checks whether the surgeon is available at that time  
        3. Confirms the theatre is free and suitable  
        4. Looks for overlapping surgeries or time conflicts  
        5. Ensures hospital scheduling rules are followed  
        6. Provides a clear decision with reasons
        
        This helps ensure **patient safety**, **staff wellbeing**, and **efficient theatre use**.
        """
    )

# --------------------------------------------------
# Reset Handling
# --------------------------------------------------
if reset_btn:
    st.experimental_rerun()

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.caption(
    "This system is designed to assist hospital staff with theatre scheduling. "
    "It provides guidance and explanations to support safe and informed decisions."
)
