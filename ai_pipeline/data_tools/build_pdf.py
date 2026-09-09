import os
import sys
import subprocess
import re

def build_pdf_document():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    
    md_path = os.path.join(project_root, "PROJECT_MASTER_DOCUMENT.md")
    html_path = os.path.join(project_root, "PROJECT_MASTER_DOCUMENT.html")
    pdf_path = os.path.join(project_root, "PROJECT_MASTER_DOCUMENT.pdf")
    
    if not os.path.exists(md_path):
        # Read from master_project_document in brain if not in root
        brain_md = r"C:\Users\Administrator\.gemini\antigravity\brain\53fcc2dc-306d-4d56-bf07-91b21deb7d97\master_project_document.md"
        with open(brain_md, "r", encoding="utf-8") as f:
            md_text = f.read()
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_text)
    else:
        with open(md_path, "r", encoding="utf-8") as f:
            md_text = f.read()
            
    # Professional CSS Styling for PDF Print
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Autonomous AI Email & Task Management Assistant - Master Defense Document</title>
<style>
    @page {{
        size: A4;
        margin: 18mm 15mm 18mm 15mm;
        @bottom-right {{
            content: "Page " counter(page);
            font-size: 9pt;
            color: #64748b;
        }}
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.55;
        color: #1e293b;
        background-color: #ffffff;
        margin: 0;
        padding: 10px;
        font-size: 10pt;
    }}
    h1 {{
        color: #0f172a;
        font-size: 20pt;
        border-bottom: 3px solid #2563eb;
        padding-bottom: 6px;
        margin-top: 0;
        page-break-after: avoid;
    }}
    h2 {{
        color: #1e3a8a;
        font-size: 14pt;
        border-bottom: 1.5px solid #cbd5e1;
        padding-bottom: 4px;
        margin-top: 20px;
        page-break-after: avoid;
    }}
    h3 {{
        color: #1d4ed8;
        font-size: 11pt;
        margin-top: 14px;
        page-break-after: avoid;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
        font-size: 8.5pt;
        page-break-inside: avoid;
    }}
    th {{
        background-color: #f1f5f9;
        color: #0f172a;
        font-weight: bold;
        text-align: left;
        padding: 6px 8px;
        border: 1px solid #cbd5e1;
    }}
    td {{
        padding: 5px 8px;
        border: 1px solid #e2e8f0;
    }}
    tr:nth-child(even) {{
        background-color: #f8fafc;
    }}
    code {{
        background-color: #f1f5f9;
        color: #0369a1;
        padding: 1px 4px;
        border-radius: 3px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 8.5pt;
    }}
    pre {{
        background-color: #0f172a;
        color: #f8fafc;
        padding: 10px;
        border-radius: 5px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 8pt;
        overflow-x: auto;
        page-break-inside: avoid;
    }}
    pre code {{
        background-color: transparent;
        color: #38bdf8;
        padding: 0;
    }}
    blockquote {{
        border-left: 4px solid #3b82f6;
        margin: 10px 0;
        padding: 6px 12px;
        background-color: #eff6ff;
        color: #1e40af;
        border-radius: 0 4px 4px 0;
        font-style: italic;
        page-break-inside: avoid;
    }}
    ul, ol {{
        padding-left: 18px;
        margin: 6px 0;
    }}
    li {{
        margin-bottom: 3px;
    }}
    .badge-pass {{
        display: inline-block;
        background-color: #dcfce7;
        color: #166534;
        font-weight: bold;
        padding: 2px 5px;
        border-radius: 3px;
    }}
</style>
</head>
<body>
"""
    lines = md_text.split('\n')
    in_code_block = False
    in_table = False
    table_has_header = False

    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith("```"):
            if in_code_block:
                html_content += "</code></pre>\n"
                in_code_block = False
            else:
                lang = stripped[3:].strip()
                html_content += f"<pre><code class='language-{lang}'>"
                in_code_block = True
            continue
            
        if in_code_block:
            safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            html_content += safe_line + "\n"
            continue

        if "|" in stripped and not stripped.startswith(">"):
            if not in_table:
                in_table = True
                table_has_header = False
                html_content += "<table>\n"
            
            if re.match(r'^\|?\s*:?-+:?\s*\|', stripped):
                continue
                
            cols = [c.strip() for c in stripped.split("|")]
            if cols[0] == "": cols = cols[1:]
            if cols and cols[-1] == "": cols = cols[:-1]
            
            tag = "th" if not table_has_header else "td"
            if not table_has_header:
                table_has_header = True
                
            row_html = "<tr>" + "".join([f"<{tag}>{c}</{tag}>" for c in cols]) + "</tr>\n"
            row_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', row_html)
            row_html = re.sub(r'`(.*?)`', r'<code>\1</code>', row_html)
            row_html = row_html.replace("✅ Passed", "<span class='badge-pass'>✅ Passed</span>")
            html_content += row_html
            continue
        else:
            if in_table:
                html_content += "</table>\n"
                in_table = False

        if not stripped:
            continue

        if stripped.startswith("# "):
            html_content += f"<h1>{stripped[2:]}</h1>\n"
        elif stripped.startswith("## "):
            html_content += f"<h2>{stripped[3:]}</h2>\n"
        elif stripped.startswith("### "):
            html_content += f"<h3>{stripped[4:]}</h3>\n"
        elif stripped.startswith("#### "):
            html_content += f"<h4>{stripped[5:]}</h4>\n"
        elif stripped.startswith("---"):
            html_content += "<hr style='border:0; border-top:1px solid #cbd5e1; margin:16px 0;'>\n"
        elif stripped.startswith("> "):
            quote_text = stripped[2:]
            quote_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', quote_text)
            quote_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', quote_text)
            html_content += f"<blockquote>{quote_text}</blockquote>\n"
        elif stripped.startswith("- ") or stripped.startswith("* "):
            item_text = stripped[2:]
            item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item_text)
            item_text = re.sub(r'`(.*?)`', r'<code>\1</code>', item_text)
            html_content += f"<ul><li>{item_text}</li></ul>\n"
        elif re.match(r'^\d+\.\s', stripped):
            item_text = re.sub(r'^\d+\.\s', '', stripped)
            item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item_text)
            item_text = re.sub(r'`(.*?)`', r'<code>\1</code>', item_text)
            html_content += f"<ol><li>{item_text}</li></ol>\n"
        else:
            p_text = stripped
            p_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', p_text)
            p_text = re.sub(r'`(.*?)`', r'<code>\1</code>', p_text)
            html_content += f"<p>{p_text}</p>\n"

    if in_table:
        html_content += "</table>\n"

    html_content += """
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"HTML written to: {html_path}")

    # Convert to PDF using Edge / Chrome headless
    edge_candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    ]
    browser_exe = next((p for p in edge_candidates if os.path.exists(p)), None)
    
    if browser_exe:
        cmd = [
            browser_exe,
            "--headless",
            "--disable-gpu",
            f"--print-to-pdf={pdf_path}",
            "--no-pdf-header-footer",
            html_path
        ]
        subprocess.run(cmd, check=True)
        if os.path.exists(pdf_path):
            size_kb = os.path.getsize(pdf_path) / 1024.0
            print(f"SUCCESS: Generated PDF at {pdf_path} ({size_kb:.1f} KB)")
            return True
            
    print("Browser engine not found for PDF generation.")
    return False

if __name__ == "__main__":
    build_pdf_document()
