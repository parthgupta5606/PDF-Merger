from flask import Flask, render_template, request, send_file
from pypdf import PdfReader, PdfWriter
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def parse_pages(page_text, total_pages):
    """Convert input like 1,3,5-7 into page indexes."""

    if not page_text.strip():
        return list(range(total_pages))

    pages = []

    for part in page_text.split(","):
        part = part.strip()

        if "-" in part:
            start, end = map(int, part.split("-"))

            for page in range(start, end + 1):
                if 1 <= page <= total_pages:
                    pages.append(page - 1)

        else:
            page = int(part)

            if 1 <= page <= total_pages:
                pages.append(page - 1)

    return pages


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/merge", methods=["POST"])
def merge_pdfs():

    files = request.files.getlist("pdfs")
    page_inputs = request.form.getlist("pages")

    writer = PdfWriter()

    for i, file in enumerate(files):

        if not file.filename:
            continue

        # Save uploaded PDF temporarily
        filename = f"{uuid.uuid4()}.pdf"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        file.save(filepath)

        reader = PdfReader(filepath)
        total_pages = len(reader.pages)

        # Get pages entered by user
        page_text = page_inputs[i] if i < len(page_inputs) else ""

        selected_pages = parse_pages(page_text, total_pages)

        # Add selected pages to final PDF
        for page_index in selected_pages:
            writer.add_page(reader.pages[page_index])

    # Check whether any pages were actually selected
    if len(writer.pages) == 0:
        return """
        <h2>No pages were selected.</h2>
        <p>Please select at least one page and try again.</p>
        <a href="/">Go Back</a>
        """

    # Create merged PDF
    output_filename = f"merged_{uuid.uuid4()}.pdf"
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)

    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    # Show result page instead of automatically downloading
    return render_template(
        "result.html",
        filename=output_filename
    )


@app.route("/download/<filename>")
def download_file(filename):

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    return send_file(
        filepath,
        as_attachment=True,
        download_name="merged.pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)