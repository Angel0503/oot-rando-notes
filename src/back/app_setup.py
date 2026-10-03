"""First-run setup for the packaged (.exe) version.

The exe carries the tracker template inside itself. At startup we:
  1. create a `data` folder next to the exe (or in %LOCALAPPDATA%\\OOTR-AutoTracker if the
     exe's folder is read-only),
  2. copy the bundled template into data/oot-tracker/ (refreshed on every launch),
  3. create data/generated/ for the generated file,
  4. point patch_tracker at those real, writable locations.

When running from source (python launcher.py) nothing changes.
"""
import os
import shutil
import sys

APP_FOLDER = "OOTR-AutoTracker"
TEMPLATE_REL = os.path.join("oot-tracker", "track-oot-template.json")
GENERATED_REL = os.path.join("generated", "track-oot-generated.json")


def _can_write(folder):
    try:
        os.makedirs(folder, exist_ok=True)
        probe = os.path.join(folder, ".write_test")
        with open(probe, "w") as f:
            f.write("ok")
        os.remove(probe)
        return True
    except OSError:
        return False


def get_data_dir():
    next_to_exe = os.path.join(os.path.dirname(sys.executable), "data")
    if _can_write(next_to_exe):
        return next_to_exe
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    fallback = os.path.join(base, APP_FOLDER, "data")
    os.makedirs(fallback, exist_ok=True)
    return fallback


def prepare(patch_module):
    """Set up folders/files and redirect patch_module's paths. Returns the data dir (or None)."""
    if not getattr(sys, "frozen", False):
        return None

    data_dir = get_data_dir()

    template = os.path.join(data_dir, TEMPLATE_REL)
    os.makedirs(os.path.dirname(template), exist_ok=True)
    bundled = os.path.join(sys._MEIPASS, "data", TEMPLATE_REL)
    if os.path.exists(bundled):
        shutil.copyfile(bundled, template)
    else:
        print(f"[-] Bundled template not found ({bundled}). Was the exe built with --add-data for data/oot-tracker?")

    output = os.path.join(data_dir, GENERATED_REL)
    os.makedirs(os.path.dirname(output), exist_ok=True)

    # patch_tracker joins these to its own folder with os.path.join; an absolute path wins.
    patch_module.INPUT_PATH = template
    patch_module.OUTPUT_PATH = output

    print(f"[+] Data folder ready: {data_dir}")
    return data_dir