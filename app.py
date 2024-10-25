import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# Database connection setup (fill in with actual credentials)
DB_URI = os.getenv("DB_URI")
engine = create_engine(DB_URI)


# Helper function to get data from the database
def fetch_review_count():
    query = text("""
    SELECT COUNT(*) FROM records
    WHERE validation_status IS NULL
    """)
    with engine.connect() as conn:
        result = conn.execute(query).fetchone()
    return result[0]

def fetch_records_to_review():
    query = text("""
    SELECT id, image_url, predicted_label FROM records
    WHERE validation_status IS NULL
    """)
    with engine.connect() as conn:
        records = pd.read_sql(query, conn)
    return records

def fetch_class_labels():
    query = text("SELECT label FROM class_labels")
    with engine.connect() as conn:
        labels = pd.read_sql(query, conn)
    return labels['label'].tolist()

def add_new_class_label(new_label):
    query = text("INSERT INTO class_labels (label) VALUES (:new_label)")
    with engine.connect() as conn:
        conn.execute(query, {"new_label": new_label})

def update_record_validation(record_id, correct, corrected_label=None):
    query = text("""
    UPDATE records
    SET validation_status = :correct, corrected_label = :corrected_label
    WHERE id = :record_id
    """)
    with engine.connect() as conn:
        conn.execute(query, {"correct": correct, "corrected_label": corrected_label, "record_id": record_id})

# Streamlit app layout
st.title("Data Validation Dashboard")

# Display the count of records to review
review_count = fetch_review_count()
st.write(f"Records available for review: {review_count}")

# Button to load records for review
if st.button("Start Review"):
    records = fetch_records_to_review()
    class_labels = fetch_class_labels()

    # Loop through records for user to review
    for _, record in records.iterrows():
        st.image(record['image_url'], width=300)
        st.write(f"Predicted Label: {record['predicted_label']}")

        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("✔️ Correct", key=f"correct_{record['id']}"):
                update_record_validation(record['id'], correct=True)
                print("something happens here??")
                st.success("Marked as correct")

        with col2:
            if st.button("❌ Incorrect", key=f"incorrect_{record['id']}"):
                st.warning("Please provide the correct label:")
                selected_label = st.selectbox("Choose the correct label:", class_labels + ["Add New Label..."], key=f"label_{record['id']}")

                if selected_label == "Add New Label...":
                    new_label = st.text_input("Enter new label:")
                    if st.button("Add Label"):
                        if new_label:
                            add_new_class_label(new_label)
                            update_record_validation(record['id'], correct=False, corrected_label=new_label)
                            st.success("New label added and record updated")
                        else:
                            st.error("Please enter a label")
                else:
                    if st.button("Confirm Label", key=f"confirm_{record['id']}"):
                        update_record_validation(record['id'], correct=False, corrected_label=selected_label)
                        st.success("Record updated with corrected label")
