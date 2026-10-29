"""Reúne as duas partes, extrai o CSV oficial e verifica SHA-256."""
from pathlib import Path
import gzip
import hashlib
import tempfile
import shutil

root = Path(__file__).resolve().parent
output = root / "APOSENTADOS_082025_FULL.csv"
expected = "cd7aeaf871cbbe006ae7ced659bbf6bb94107aa5ff943eeb2eeded53b884bdec"
if output.exists():
    with output.open("rb") as existing:
        if hashlib.file_digest(existing, "sha256").hexdigest() != expected:
            raise SystemExit("O CSV já existe com conteúdo diferente; mova-o antes de extrair.")
    print(f"CSV já extraído e verificado: {output}")
else:
    with tempfile.TemporaryFile() as compressed:
        for name in ("APOSENTADOS_082025_FULL.csv.gz.part01", "APOSENTADOS_082025_FULL.csv.gz.part02"):
            with (root / name).open("rb") as part:
                shutil.copyfileobj(part, compressed)
        compressed.seek(0)
        with gzip.GzipFile(fileobj=compressed) as source, tempfile.NamedTemporaryFile(dir=root, delete=False) as target:
            temporary = Path(target.name)
            shutil.copyfileobj(source, target)
    with temporary.open("rb") as result:
        digest = hashlib.file_digest(result, "sha256").hexdigest()
    if digest != expected:
        temporary.unlink()
        raise SystemExit("Falha na verificação SHA-256.")
    temporary.replace(output)
    print(f"CSV extraído e SHA-256 verificado: {output}")
