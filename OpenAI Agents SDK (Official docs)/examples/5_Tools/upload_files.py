import sys
from pathlib import Path
import rich
from openai import OpenAI
from g_config import create_openai_config, create_gemini_config

# Use an absolute path
file = Path("D:/2025_practice/AI-Agents/OpenAI Agents SDK (Official docs)/examples/5_Tools/Aqeel Shahzad Engineer.pdf")

client = OpenAI()

def from_disk() -> None:
    print("Uploading file from disk")
    upload = client.uploads.upload_file_chunked(
        file=file,
        mime_type="application/pdf",
        purpose="batch",
    )
    rich.print(upload)

def from_in_memory() -> None:
    print("Uploading file from memory")
    data = file.read_bytes()
    filename = "Aqeel Shahzad Engineer.pdf"
    upload = client.uploads.upload_file_chunked(
        file=data,
        filename=filename,
        bytes=len(data),
        mime_type="txt",
        purpose="batch",
    )
    rich.print(upload)

if "memory" in sys.argv:
    from_in_memory()
else:
    from_disk()

"""
# Example output when running the script
(agentic_env) D:\2025_practice\AI-Agents\OpenAI Agents SDK (Official docs)\examples\5_Tools>python upload_files.py
Uploading file from disk
Upload(
    id='upload_6883d14993d48191941ff72344721c71',
    bytes=97288,
    created_at=1753469257,
    expires_at=1753472857,
    filename='Aqeel Shahzad Engineer.pdf',
    object='upload',
    purpose='batch',
    status='completed',
    file=FileObject(
        id='file-Vw1Kd4UJ88b341e4F8Zqqt',
        bytes=97288,
        created_at=1753469257,
        filename='Aqeel Shahzad Engineer.pdf',
        object='file',
        purpose='batch',
        status='processed',
        expires_at=None,
        status_details=None
    )
)
"""