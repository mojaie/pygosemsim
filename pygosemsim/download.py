
import urllib.request
from pathlib import Path


resource_dir = Path(__file__).resolve().parent / "_resources"


def initialize():
    """Initialize downloaded resource directory
    """
    if not resource_dir.exists():
        resource_dir.mkdir()
        print(f"Resource directory created: {resource_dir}")


def clear():
    """Remove all downloaded resources
    """
    initialize()
    for p in resource_dir.glob("*"):
        p.unlink()
    print(f"Resource directory is now empty: {resource_dir}")


def download(filename, url, decode="utf-8"):
    """Download resources via HTTP
    """
    initialize()
    chunk_size = 1024 * 1024  # 1 MB
    print(f"Download started: {url}")
    with urllib.request.urlopen(url) as res:
        contlen = res.info().get("Content-Length")
        total_size = int(contlen.rstrip())
        downloaded_bytes = 0
        chunks = []
        while True:
            chunk = res.read(chunk_size)
            downloaded_bytes += len(chunk)
            if not chunk:
                break
            chunks.append(chunk)
            progress = round(downloaded_bytes / total_size * 100, 1)
            dl = round(downloaded_bytes / (1024 * 1024), 1)
            tot = round(total_size / (1024 * 1024), 1)
            print(f"Downloaded {dl}MB of {tot}MB ({progress} %)", end="\r")
        if decode:
            data = b"".join(chunks).decode(decode)
            mode = "wt"
        else:
            data = b"".join(chunks)
            mode = "wb"
        print("")
    with open(resource_dir / filename, mode) as f:
        f.write(data)
    tot = round(total_size / (1024 * 1024), 1)
    print(f"Download finished: {filename} ({tot}) MB")


def obo(name="go-basic"):
    filename = f"{name}.obo"
    go_obo_url = f"http://purl.obolibrary.org/obo/go/{filename}"
    dest = resource_dir / filename
    if dest.exists():
        raise ValueError(
            f"{filename} already exists in the resource directory")
    download(filename, go_obo_url)


def gaf(name="goa_human"):
    filename = f"{name}.gaf.gz"
    go_obo_url = f"http://geneontology.org/gene-associations/{filename}"
    dest = resource_dir / filename
    if dest.exists():
        raise ValueError(
            f"{filename} already exists in the resource directory")
    download(filename, go_obo_url, decode=False)
