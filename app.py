
from flask import Flask, render_template, request, redirect, url_for, flash
from database import (
    get_documents,
    add_document,
    get_document,
    update_document,
    delete_document
)
from datetime import date

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-private-value"


# Calculate expiry status
def get_status(expiry_date):
    today = date.today()

    if isinstance(expiry_date, date):
        expiry = expiry_date
    else:
        expiry = date.fromisoformat(str(expiry_date)[:10])

    remaining_days = (expiry - today).days

    if remaining_days < 0:
        status = "Expired"
    elif remaining_days == 0:
        status = "Expires Today"
    elif remaining_days <= 7:
        status = "Urgent"
    elif remaining_days <= 30:
        status = "Expiring Soon"
    else:
        status = "Valid"

    return remaining_days, status


# Home page
@app.route("/")
def index():
    documents = get_documents()

    document_list = []

    for doc in documents:
        remaining, status = get_status(doc["expiry_date"])

        document_list.append({
            "id": doc["id"],
            "document_name": doc["document_name"],
            "document_type": doc["document_type"],
            "issue_date": doc["issue_date"],
            "expiry_date": str(doc["expiry_date"])[:10],
            "notes": doc["notes"],
            "remaining_days": remaining,
            "status": status
        })

    total = len(document_list)

    expired = sum(
        d["status"] == "Expired"
        for d in document_list
    )

    upcoming = sum(
        d["status"] in ["Urgent", "Expiring Soon"]
        for d in document_list
    )

    valid = sum(
        d["status"] == "Valid"
        for d in document_list
    )

    return render_template(
        "index.html",
        documents=document_list,
        total=total,
        expired=expired,
        upcoming=upcoming,
        valid=valid
    )


# Add document
@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("document_name", "").strip()
    doc_type = request.form.get("document_type", "").strip()
    issue_date = request.form.get("issue_date", "")
    expiry_date = request.form.get("expiry_date", "")
    notes = request.form.get("notes", "").strip()

    if not name or not doc_type or not expiry_date:
        return "Please fill in all required fields.", 400

    try:
        expiry = date.fromisoformat(expiry_date)

        if issue_date:
            issue = date.fromisoformat(issue_date)

            if issue > expiry:
                return "Issue date cannot be after expiry date.", 400

    except ValueError:
        return "Please enter valid dates.", 400

    add_document(
        name,
        doc_type,
        issue_date,
        expiry_date,
        notes
    )

    return redirect(url_for("index"))


# Edit document
@app.route("/edit/<int:document_id>", methods=["GET", "POST"])
def edit(document_id):
    document = get_document(document_id)

    if document is None:
        return "Document not found.", 404

    if request.method == "POST":
        name = request.form.get("document_name", "").strip()
        doc_type = request.form.get("document_type", "").strip()
        issue_date = request.form.get("issue_date", "")
        expiry_date = request.form.get("expiry_date", "")
        notes = request.form.get("notes", "").strip()

        if not name or not doc_type or not expiry_date:
            return "Please fill in all required fields.", 400

        try:
            expiry = date.fromisoformat(expiry_date)

            if issue_date:
                issue = date.fromisoformat(issue_date)

                if issue > expiry:
                    return "Issue date cannot be after expiry date.", 400

        except ValueError:
            return "Please enter valid dates.", 400

        update_document(
            document_id,
            name,
            doc_type,
            issue_date,
            expiry_date,
            notes
        )

        return redirect(url_for("index"))

    return render_template(
        "edit.html",
        document=document
    )


# Delete document
@app.route("/delete/<int:document_id>", methods=["POST"])
def delete(document_id):
    delete_document(document_id)

    return redirect(url_for("index"))


# Run application
if __name__ == "__main__":
    app.run(debug=True)
