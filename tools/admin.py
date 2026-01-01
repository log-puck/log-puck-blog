# admin.py
# Mini pannello admin per inserire righe nella tabella "content" del DB mio_lab.db

import sqlite3
from pathlib import Path

from flask import Flask, request, redirect, url_for, render_template_string

# Path al DB: ./db/mio_lab.db
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "mio_lab.db"

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


# Template HTML minimale in-line per la form
CONTENT_FORM_TEMPLATE = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>New Content</title>
    <style>
      body { font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif; margin: 20px; max-width: 900px; }
      label { display: block; margin-top: 10px; font-weight: 600; }
      input[type=text],
      input[type=date],
      textarea,
      select { width: 100%; padding: 6px; margin-top: 4px; box-sizing: border-box; }
      textarea { min-height: 160px; }
      .row { margin-bottom: 8px; }
      .small { width: 48%; display: inline-block; }
      .small + .small { margin-left: 4%; }
      button { margin-top: 16px; padding: 8px 18px; font-size: 14px; }
      .status { margin-top: 10px; padding: 8px; border-radius: 4px; background: #e6ffed; border: 1px solid #b5f2c5; }
      .error { background: #ffecec; border-color: #f5b5b5; }
    </style>
    <script>
      function slugifyTitle() {
        var titleInput = document.getElementById("title");
        var slugInput = document.getElementById("slug");
        if (!titleInput || !slugInput) return;
        var t = titleInput.value || "";
        var slug = t.toLowerCase()
                    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
                    .replace(/[^a-z0-9]+/g, "-")
                    .replace(/^-+|-+$/g, "");
        slugInput.value = slug;
      }
    </script>
  </head>
  <body>
    <h1>New Content</h1>
    {% if message %}
      <div class="status {% if error %}error{% endif %}">
        {{ message }}
      </div>
    {% endif %}
    <form method="post" action="{{ url_for('new_content') }}">
      <div class="row">
        <label for="title">Title</label>
        <input type="text" name="title" id="title" oninput="slugifyTitle()" required>
      </div>

      <div class="row small">
        <label for="type">Type</label>
        <select name="type" id="type">
          <option value="article">article</option>
          <option value="document" selected>document</option>
          <option value="landing">landing</option>
        </select>
      </div>

      <div class="row small">
        <label for="layout">Layout</label>
        <select name="layout" id="layout">
          <option value="session">session</option>
          <option value="archive" selected>archive</option>
          <option value="landing">landing</option>
        </select>
      </div>

      <div class="row small">
        <label for="section">Section</label>
        <select name="section" id="section">
          <option value="OB-Session">OB-Session</option>
          <option value="OB-Archives" selected>OB-Archives</option>
          <option value="OB-Progetti">OB-Progetti</option>
          <option value="OB-AI">OB-AI</option>
        </select>
      </div>

      <div class="row small">
        <label for="subsection">Subsection</label>
        <select name="subsection" id="subsection">
          <option value="">(none)</option>
          <option value="Documents" selected>Documents</option>
          <option value="Giochi MultiAI">Giochi MultiAI</option>
        </select>
      </div>

      <div class="row small">
        <label for="status">Status</label>
        <select name="status" id="status">
          <option value="Draft">Draft</option>
          <option value="Published" selected>Published</option>
          <option value="Archived">Archived</option>
        </select>
      </div>

      <div class="row small">
        <label for="date">Date</label>
        <input type="date" name="date" id="date">
      </div>

      <div class="row">
        <label for="slug">Slug (auto dal Title, modificabile)</label>
        <input type="text" name="slug" id="slug" required>
      </div>

      <div class="row">
        <label for="meta_title">Meta Title</label>
        <input type="text" name="meta_title" id="meta_title">
      </div>

      <div class="row">
        <label for="meta_description">Meta Description</label>
        <textarea name="meta_description" id="meta_description"></textarea>
      </div>

      <div class="row">
        <label for="keywords_seo">Keywords SEO (comma separated)</label>
        <input type="text" name="keywords_seo" id="keywords_seo">
      </div>

      <div class="row">
        <label for="tags">Tags (comma separated)</label>
        <input type="text" name="tags" id="tags">
      </div>

      <div class="row">
        <label for="content_body">Content Body</label>
        <textarea name="content_body" id="content_body"></textarea>
      </div>

      <button type="submit">Save</button>
    </form>
  </body>
</html>
"""


@app.route("/")
def index():
    return redirect(url_for("new_content"))


@app.route("/content/new", methods=["GET", "POST"])
def new_content():
    if request.method == "POST":
        try:
            title = request.form.get("title", "").strip()
            ctype = request.form.get("type", "").strip()
            section = request.form.get("section", "").strip()
            subsection = request.form.get("subsection", "").strip()
            layout = request.form.get("layout", "").strip()
            slug = request.form.get("slug", "").strip()
            status = request.form.get("status", "").strip()
            date_val = request.form.get("date", "").strip()
            meta_title = request.form.get("meta_title", "").strip()
            meta_description = request.form.get("meta_description", "").strip()
            keywords_seo = request.form.get("keywords_seo", "").strip()
            tags = request.form.get("tags", "").strip()
            content_body = request.form.get("content_body", "").strip()

            if not title or not slug:
                raise ValueError("Title and Slug are required.")

            conn = get_db_connection()
            cur = conn.cursor()

            sql = """
                INSERT INTO content (
                    title,
                    type,
                    section,
                    subsection,
                    layout,
                    slug,
                    status,
                    date,
                    meta_title,
                    meta_description,
                    keywords_seo,
                    tags,
                    content_body
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cur.execute(
                sql,
                (
                    title,
                    ctype,
                    section,
                    subsection,
                    layout,
                    slug,
                    status,
                    date_val,
                    meta_title,
                    meta_description,
                    keywords_seo,
                    tags,
                    content_body
                ),
            )
            new_id = cur.lastrowid
            conn.commit()
            conn.close()

            msg = "Content saved with id " + str(new_id)
            return render_template_string(CONTENT_FORM_TEMPLATE, message=msg, error=False)

        except Exception as e:
            err_msg = "Error: " + str(e)
            return render_template_string(CONTENT_FORM_TEMPLATE, message=err_msg, error=True)

    # GET
    return render_template_string(CONTENT_FORM_TEMPLATE, message=None, error=False)

@app.route("/content")
def list_content():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, title, section, subsection, status, date
        FROM content
        ORDER BY date DESC, id DESC
        """
    )
    rows = cur.fetchall()
    conn.close()

    return render_template_string(CONTENT_LIST_TEMPLATE, rows=rows)


if __name__ == "__main__":
    # Avvia il server in modalità sviluppo
    app.run(debug=True)