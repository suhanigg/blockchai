import streamlit as st
import hashlib

# Initialize hospital ledger
def get_hospital_ledger():
    if "hospital_ledger" not in st.session_state:
        st.session_state.hospital_ledger = {}
    return st.session_state.hospital_ledger

# Function to generate a hash for data integrity
def generate_hash(patient_name, treatment, cost, date_of_visit):
    data = f"{patient_name}{treatment}{cost}{date_of_visit}"
    return hashlib.sha256(data.encode()).hexdigest()

# Function to add a patient visit
def add_patient_visit(patient_name, treatment, cost, date_of_visit):
    ledger = get_hospital_ledger()
    visit_hash = generate_hash(patient_name, treatment, cost, date_of_visit)
    visit = {
        "treatment": treatment,
        "cost": cost,
        "date_of_visit": date_of_visit,
        "visit_hash": visit_hash,
    }
    if patient_name not in ledger:
        ledger[patient_name] = []
    ledger[patient_name].append(visit)
    st.success(f"Visit added for {patient_name} on {date_of_visit} for treatment {treatment} costing ${cost}.")
    return visit_hash

# Streamlit UI
st.title("🏥 Hospital Ledger System")

# Add patient visit
st.header("Add Patient Visit")
patient_name = st.text_input("Enter patient name").strip().lower()
treatment = st.text_input("Enter treatment received").strip()
cost = st.number_input("Enter cost of treatment ($)", min_value=0.0, format="%.2f")
date_of_visit = st.date_input("Enter date of visit").strftime("%Y-%m-%d")

if st.button("Add Visit"):
    if patient_name and treatment and cost:
        visit_hash = add_patient_visit(patient_name, treatment, cost, date_of_visit)
        st.write(f"Visit hash: {visit_hash}")
    else:
        st.error("Please fill in all fields correctly.")

# Search for a patient
st.header("Search Patient Records")
search_patient = st.text_input("Enter patient name to search").strip().lower()

if st.button("Search"):
    ledger = get_hospital_ledger()
    if search_patient in ledger:
        st.subheader(f"Visit records for {search_patient}")
        for visit in ledger[search_patient]:
            st.write(f"- Treatment: {visit['treatment']}, Cost: ${visit['cost']}, Date: {visit['date_of_visit']}, Hash: {visit['visit_hash']}")
    else:
        st.error(f"Patient {search_patient} not found in the ledger.")
