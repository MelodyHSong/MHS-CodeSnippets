# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: scaffold.py
# ☆ Description: Automated project scaffolding and tier-pruning utility for Desktop Tool Template.
# ☆ [Template Meta Utility: Can be removed after project scaffolding]
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import os
import sys
import json
import shutil
import argparse
import re

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST_FILE = os.path.join(BASE_DIR, "template_manifest.json")


def load_manifest():
    if not os.path.exists(MANIFEST_FILE):
        print(f"[!] Error: Manifest not found at {MANIFEST_FILE}")
        sys.exit(1)
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def inspect_template():
    manifest = load_manifest()
    print("=" * 72)
    print("   ⭐ DESKTOP TOOL TEMPLATE — COMPONENT & TIER INSPECTOR 🛸")
    print("=" * 72)

    tiers = manifest.get("tiers", {})
    components = manifest.get("components", [])

    for tier_id, tier_info in tiers.items():
        req_badge = "[MANDATORY]" if tier_info.get("required") else "[OPTIONAL]"
        print(f"\n▶ {tier_info.get('name', tier_id).upper()} {req_badge}")
        print(f"  {tier_info.get('description')}")
        print("  " + "-" * 68)

        tier_components = [c for c in components if c.get("tier") == tier_id]
        if not tier_components:
            print("  (No files registered in this tier)")
            continue

        for comp in tier_components:
            path = comp.get("path")
            full_path = os.path.join(BASE_DIR, path)
            status_icon = "✓" if os.path.exists(full_path) else "✗"
            req_str = "REQ" if comp.get("required") else "OPT"
            print(f"  [{status_icon}] {path:<32} ({req_str}) - {comp.get('description')}")

    print("\n" + "=" * 72)
    print("Available Profiles for Scaffolding:")
    for prof_id, prof_info in manifest.get("profiles", {}).items():
        print(f"  • {prof_id:<18} : {prof_info.get('name')} ({prof_info.get('description')})")
    print("=" * 72 + "\n")


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "_", text)
    return text.strip("_")


def get_profile_files(manifest, profile_name):
    profiles = manifest.get("profiles", {})
    if profile_name not in profiles:
        # Fallback aliases
        alias_map = {
            "core": "minimal",
            "shell": "shell_integrated",
            "binary": "portable_dist",
            "dist": "portable_dist",
            "full": "full_repository",
        }
        profile_name = alias_map.get(profile_name, profile_name)

    if profile_name not in profiles:
        raise ValueError(f"Unknown profile '{profile_name}'. Available: {list(profiles.keys())}")

    prof_data = profiles[profile_name]
    included_tiers = set(prof_data.get("included_tiers", []))

    components = manifest.get("components", [])
    allowed_files = set()

    for comp in components:
        tier = comp.get("tier")
        path = comp.get("path")
        if tier in included_tiers or "all" in included_tiers:
            allowed_files.add(path)

    return allowed_files, profile_name


def create_project(app_name, dest_dir, profile_name="full_repository"):
    manifest = load_manifest()
    allowed_files, resolved_profile = get_profile_files(manifest, profile_name)

    app_slug = slugify(app_name)
    abs_dest = os.path.abspath(dest_dir)

    print("=" * 72)
    print(f"   🚀 SCAFFOLDING NEW DESKTOP TOOL: '{app_name}'")
    print(f"   Profile: {resolved_profile}")
    print(f"   Destination: {abs_dest}")
    print("=" * 72)

    if os.path.exists(abs_dest):
        if os.listdir(abs_dest):
            print(f"[!] Warning: Destination directory is not empty: {abs_dest}")
            choice = input("    Proceed and copy/overwrite into destination? [y/N]: ").strip().lower()
            if choice != "y":
                print("Aborted by user.")
                return

    os.makedirs(abs_dest, exist_ok=True)

    copied_count = 0
    for comp_rel in allowed_files:
        src = os.path.join(BASE_DIR, comp_rel)
        if not os.path.exists(src):
            continue

        dest = os.path.join(abs_dest, comp_rel)
        # Rename spec file to project slug if relevant
        if comp_rel == "desktop_tool.spec":
            dest = os.path.join(abs_dest, f"{app_slug}.spec")

        os.makedirs(os.path.dirname(dest), exist_ok=True)

        if os.path.isdir(src):
            shutil.copytree(src, dest, dirs_exist_ok=True)
        else:
            # Check if text file for string replacement
            try:
                with open(src, "r", encoding="utf-8") as f:
                    content = f.read()

                # Perform standard replacements
                content = content.replace("Desktop Tool Template", app_name)
                content = content.replace("desktop_tool_template", app_slug)
                content = content.replace("desktop_tool.exe", f"{app_slug}.exe")
                content = content.replace("desktop_tool.spec", f"{app_slug}.spec")

                with open(dest, "w", encoding="utf-8") as f:
                    f.write(content)
            except UnicodeDecodeError:
                # Binary file (like icon, png)
                shutil.copy2(src, dest)

        copied_count += 1
        print(f"  [+] Created: {os.path.relpath(dest, abs_dest)}")

    print("-" * 72)
    print(f"✨ Successfully scaffolded '{app_name}' with {copied_count} files!")
    print(f"📁 Project location: {abs_dest}")
    print("👉 Next steps:")
    print(f"   1. cd \"{abs_dest}\"")
    print("   2. Review requirements.txt and app.py")
    print("   3. Run 'run.bat' to launch your new workstation!")
    print("=" * 72 + "\n")


def prune_current(profile_name):
    manifest = load_manifest()
    allowed_files, resolved_profile = get_profile_files(manifest, profile_name)

    print("=" * 72)
    print(f"   ✂️ PRUNING CURRENT REPOSITORY TO PROFILE: '{resolved_profile}'")
    print("=" * 72)

    components = manifest.get("components", [])
    removed_count = 0

    for comp in components:
        path = comp.get("path")
        if path not in allowed_files:
            target = os.path.join(BASE_DIR, path)
            if os.path.exists(target):
                if os.path.isdir(target):
                    shutil.rmtree(target)
                else:
                    os.remove(target)
                print(f"  [-] Removed: {path}")
                removed_count += 1

    # Clean up empty parent directories if any
    for root, dirs, files in os.walk(BASE_DIR, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            if not os.listdir(dir_path) and not d.startswith(".git"):
                try:
                    os.rmdir(dir_path)
                except Exception:
                    pass

    print("-" * 72)
    print(f"✨ Pruning complete! Removed {removed_count} optional components.")
    print("=" * 72 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Desktop Tool Template Scaffolding Utility")
    parser.add_argument("--inspect", action="store_true", help="Inspect template components, tiers, and files")
    parser.add_argument("--create", metavar="APP_NAME", help="Scaffold a new desktop tool project with the given name")
    parser.add_argument("--dest", metavar="PATH", help="Destination folder for the new project")
    parser.add_argument("--profile", default="full_repository", choices=["minimal", "shell", "shell_integrated", "dist", "portable_dist", "full", "full_repository"], help="Project profile (default: full_repository)")
    parser.add_argument("--prune", action="store_true", help="Prune the current directory to match the specified profile")

    args = parser.parse_args()

    if args.inspect:
        inspect_template()
    elif args.create:
        if not args.dest:
            print("[!] Error: --dest PATH is required when using --create")
            sys.exit(1)
        create_project(args.create, args.dest, args.profile)
    elif args.prune:
        prune_current(args.profile)
    else:
        inspect_template()


if __name__ == "__main__":
    main()
