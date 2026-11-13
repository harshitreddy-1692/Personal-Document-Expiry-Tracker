
import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

# Check Supabase credentials
if not SUPABASE_URL or not SUPABASE_SECRET_KEY:
    raise RuntimeError(
        "Supabase settings are missing. Check your .env file."
    )

# Connect to Supabase
supabase = create_client(
    SUPABASE_URL.strip(),
    SUPABASE_SECRET_KEY.strip()
)


# Get all documents
def get_documents():
    response = (
        supabase.table("documents")
        .select("*")
        .order("expiry_date")
        .execute()
    )
    return response.data


# Add a document
def add_document(name, doc_type, issue_date, expiry_date, notes):
    response = supabase.table("documents").insert({
        "document_name": name,
        "document_type": doc_type,
        "issue_date": issue_date or None,
        "expiry_date": expiry_date,
        "notes": notes
    }).execute()

    return response.data


# Get one document
def get_document(document_id):
    response = (
        supabase.table("documents")
        .select("*")
        .eq("id", document_id)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


# Update a document
def update_document(
    document_id,
    name,
    doc_type,
    issue_date,
    expiry_date,
    notes
):
    response = (
        supabase.table("documents")
        .update({
            "document_name": name,
            "document_type": doc_type,
            "issue_date": issue_date or None,
            "expiry_date": expiry_date,
            "notes": notes
        })
        .eq("id", document_id)
        .execute()
    )

    return response.data


# Delete a document
def delete_document(document_id):
    response = (
        supabase.table("documents")
        .delete()
        .eq("id", document_id)
        .execute()
    )

    return response.data
