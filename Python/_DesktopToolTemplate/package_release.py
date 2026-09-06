# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: package_release.py
# ☆ Description: Automated build, packaging, and checksum generation for Desktop Tool Template releases.
# ☆ [Template Tier: Tier 3 (Optional - Portable Binary & Release Packaging)]
# ☆ Safe to delete if: This tool is not distributed as compiled .exe / zipped releases.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import os
import sys
import shutil
import zipfile
import hashlib
import subprocess

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")

# ==============================================================================
# ☆ RELEASE CONFIGURATION (Update for your project)
# ==============================================================================
APP_NAME = "Desktop-Tool"
VERSION = "1.0.0"
DIST_EXE_NAME = "desktop_tool.exe"
SPEC_FILE_NAME = "desktop_tool.spec"

# Attempt dynamic detection from setup_integration.py if available
try:
    import setup_integration as si
    if hasattr(si, "DIST_EXE_NAME"):
        DIST_EXE_NAME = si.DIST_EXE_NAME
    if hasattr(si, "SPEC_FILE"):
        SPEC_FILE_NAME = si.SPEC_FILE
    if hasattr(si, "APP_TITLE"):
        APP_NAME = si.APP_TITLE.replace(" ", "-")
except Exception:
    pass


def calculate_sha256(filepath):
    """Calculate SHA-256 hash of a file."""
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()


def step(msg):
    print(f"\n[+] {msg}")


def build_icon():
    """Generate multi-resolution icons if generate_icon.py exists."""
    icon_script = os.path.join(BASE_DIR, "generate_icon.py")
    if os.path.exists(icon_script):
        step("Generating multi-resolution cosmic icon asset...")
        res = subprocess.run([sys.executable, icon_script], cwd=BASE_DIR)
        if res.returncode != 0:
            print("[!] Warning: Icon generation exited with non-zero code. Proceeding with existing icon if available.")


def build_executable():
    """Compile standalone executable using PyInstaller."""
    step("Compiling standalone executable with PyInstaller...")
    spec_path = os.path.join(BASE_DIR, SPEC_FILE_NAME)
    if not os.path.exists(spec_path):
        # Fallback to finding any .spec file
        specs = [f for f in os.listdir(BASE_DIR) if f.endswith(".spec")]
        if specs:
            spec_path = os.path.join(BASE_DIR, specs[0])
        else:
            raise FileNotFoundError(f"PyInstaller spec file not found: {SPEC_FILE_NAME}")

    res = subprocess.run([sys.executable, "-m", "PyInstaller", "--noconfirm", spec_path], cwd=BASE_DIR)
    if res.returncode != 0:
        raise RuntimeError(f"PyInstaller build failed with exit code {res.returncode}.")

    exe_path = os.path.join(DIST_DIR, DIST_EXE_NAME)
    if not os.path.exists(exe_path) or os.path.getsize(exe_path) == 0:
        raise FileNotFoundError(f"Executable missing or empty: {exe_path}")
    print(f"    Executable verified: {exe_path} ({os.path.getsize(exe_path):,} bytes)")
    return exe_path


def create_zip_package():
    """Package standalone portable release archive."""
    step("Packaging standalone portable release archive...")
    zip_v_name = f"{APP_NAME}-v{VERSION}-Windows-x64.zip"
    zip_name = f"{APP_NAME}-Windows-x64.zip"

    zip_v_path = os.path.join(DIST_DIR, zip_v_name)
    zip_path = os.path.join(DIST_DIR, zip_name)

    # Temporary staging directory for clean zip structure
    stage_dir = os.path.join(DIST_DIR, f"{APP_NAME}-v{VERSION}")
    if os.path.exists(stage_dir):
        shutil.rmtree(stage_dir)
    os.makedirs(stage_dir, exist_ok=True)

    # Core release files to include
    root_files = [
        "run.bat",
        "install.bat",
        "uninstall.bat",
        "setup_integration.py",
        "setup_context_menu.py",
        "config.json",
        "README.md",
        "LICENSE",
        "CHANGELOG.md",
    ]
    for rf in root_files:
        src = os.path.join(BASE_DIR, rf)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(stage_dir, rf))

    # Standalone executable
    exe_src = os.path.join(DIST_DIR, DIST_EXE_NAME)
    if os.path.exists(exe_src):
        shutil.copy2(exe_src, os.path.join(stage_dir, DIST_EXE_NAME))

    # Assets directory (icon & resources, excluding screenshot working files)
    assets_src = os.path.join(BASE_DIR, "assets")
    if os.path.exists(assets_src):
        assets_dest = os.path.join(stage_dir, "assets")
        shutil.copytree(assets_src, assets_dest, ignore=shutil.ignore_patterns("screenshots*"))

    # Create versioned zip archive
    with zipfile.ZipFile(zip_v_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(stage_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, stage_dir)
                zf.write(full_path, rel_path)

    # Copy to non-versioned alias zip
    shutil.copy2(zip_v_path, zip_path)

    # Clean up staging directory
    shutil.rmtree(stage_dir)

    print(f"    Archive created: {zip_v_path} ({os.path.getsize(zip_v_path):,} bytes)")
    print(f"    Archive alias:   {zip_path} ({os.path.getsize(zip_path):,} bytes)")
    return [zip_v_path, zip_path]


def generate_checksums(files):
    """Generate SHA-256 checksums file."""
    step("Generating SHA-256 checksums...")
    checksums_path = os.path.join(DIST_DIR, "SHA256SUMS.txt")
    lines = []
    for filepath in files:
        filename = os.path.basename(filepath)
        sha = calculate_sha256(filepath)
        size = os.path.getsize(filepath)
        lines.append(f"{sha}  {filename}")
        print(f"    {filename:<42}  {size:>10,} bytes  SHA256: {sha}")

    with open(checksums_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"    Checksums saved to: {checksums_path}")
    return checksums_path


def main():
    print("=" * 70)
    print(f"   ⭐ {APP_NAME.upper()} v{VERSION} — RELEASE PACKAGING SEQUENCE 🛸")
    print("=" * 70)

    os.makedirs(DIST_DIR, exist_ok=True)
    build_icon()
    exe_path = build_executable()
    zip_paths = create_zip_package()

    all_artifacts = [exe_path] + zip_paths
    checksums_path = generate_checksums(all_artifacts)

    print("\n" + "=" * 70)
    print("   ✨ ALL RELEASE FILES COMPILED AND VERIFIED SUCCESSFULLY! ✨")
    print("=" * 70)
    for f in all_artifacts + [checksums_path]:
        print(f"   * dist/{os.path.basename(f)}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
