"""Class-level patch of the Guizhan Slimefun core jar: replace the compiled formatter-fix classes and bump the plugin.yml marker.
usage: python tools/sf_patch_jar.py <original.jar> <classes-dir> <out.jar> <old-marker> <new-marker>
Fails if a replacement class is not in the original (no half-patched output); unchanged entries are copied byte for byte."""
import hashlib
import sys
import zipfile
from pathlib import Path

src, out_dir, dst, old, new = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4], sys.argv[5]
repl = {p.relative_to(out_dir).as_posix(): p.read_bytes() for p in out_dir.rglob("*.class")}
zin = zipfile.ZipFile(src)
changed = []
with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
    for i in zin.infolist():
        data = zin.read(i.filename)
        if i.filename in repl:
            data = repl.pop(i.filename)
            changed.append(i.filename)
        elif i.filename == "plugin.yml":
            t = data.decode("utf-8")
            n = t.replace(old, new)
            assert n != t, "version marker not found in plugin.yml"
            data = n.encode("utf-8")
            changed.append("plugin.yml")
        zi = zipfile.ZipInfo(i.filename, date_time=i.date_time)
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = i.external_attr
        zout.writestr(zi, data)
if repl:
    dst.unlink()
    raise SystemExit(f"classes not present in the original jar: {sorted(repl)}")
print("entries changed:", changed)
print("sha256 in:", hashlib.sha256(src.read_bytes()).hexdigest()[:16], "out:", hashlib.sha256(dst.read_bytes()).hexdigest()[:16], "size", dst.stat().st_size)
print("zip test:", zipfile.ZipFile(dst).testzip())
