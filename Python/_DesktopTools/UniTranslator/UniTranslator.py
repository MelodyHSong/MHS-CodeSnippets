# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: UniTranslator.py
# ☆ Date: 2026-01-19
# ☆
# ☆ Description: A utility to bulk-translate file or folder 
# ☆ names with specific language filtering and dry-run safety.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import os
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

# ☆ Ensures consistent detection results across sessions
DetectorFactory.seed = 0

def universal_translator(root_path, target_lang='en', dry_run=True):
    translator = GoogleTranslator(source='auto', target=target_lang)
    
    if not os.path.exists(root_path):
        print(f"☆ Error: The path '{root_path}' does not exist.")
        return

    # ☆ User configuration prompts
    print("☆ STEP 1: What would you like to translate? (zip, folder, txt, etc.)")
    choice = input("☆ Choice: ").strip().lower().replace(".", "")

    print("\n☆ STEP 2: Which source language should we target?")
    print("☆ Type 'all' or a specific language (e.g., japanese, spanish, german).")
    lang_filter = input("☆ Language Filter: ").strip().lower()

    # ☆ Item discovery logic
    if choice == "folder":
        items_to_process = [f for f in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, f))]
        is_folder_mode = True
    else:
        extension = f".{choice}"
        items_to_process = [f for f in os.listdir(root_path) if f.lower().endswith(extension)]
        is_folder_mode = False

    if not items_to_process:
        print(f"☆ No items found matching '{choice}'.")
        return

    # ☆ Stats counters
    stats = {"processed": 0, "skipped": 0, "errors": 0}
    status_mode = "[DRY RUN MODE]" if dry_run else "[LIVE MODE]"
    
    print(f"\n☆ {status_mode} Filtering for '{lang_filter}' in {len(items_to_process)} items...\n")

    for item in items_to_process:
        try:
            name_part = item if is_folder_mode else os.path.splitext(item)[0]
            ext_part = "" if is_folder_mode else os.path.splitext(item)[1]

            # ☆ Language detection and mapping
            try:
                detected_lang_code = detect(name_part)
                lang_map = {
                    'ja': 'japanese', 
                    'es': 'spanish', 
                    'de': 'german', 
                    'fr': 'french', 
                    'zh-cn': 'chinese',
                    'ko': 'korean'
                }
                detected_lang_full = lang_map.get(detected_lang_code, detected_lang_code)
            except:
                detected_lang_full = "unknown"

            # ☆ Filter validation
            if lang_filter != "all" and lang_filter not in detected_lang_full:
                stats["skipped"] += 1
                continue

            # ☆ Translation and sanitization
            translated_name = translator.translate(name_part)
            clean_name = "".join([c for c in translated_name if c.isalnum() or c in (' ', '-', '_')]).strip()
            new_item_name = f"{clean_name}{ext_part}"
            
            # ☆ Skip if translation yields no change
            if item.lower() == new_item_name.lower():
                stats["skipped"] += 1
                continue

            if dry_run:
                print(f"☆ [PROPOSED] {detected_lang_full.upper()}: '{item}' -> '{new_item_name}'")
                stats["processed"] += 1
            else:
                old_path = os.path.join(root_path, item)
                new_path = os.path.join(root_path, new_item_name)
                
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"☆ [SUCCESS] '{item}' -> '{new_item_name}'")
                    stats["processed"] += 1
                else:
                    print(f"☆ [CONFLICT] '{new_item_name}' already exists.")
                    stats["errors"] += 1

        except Exception as e:
            print(f"☆ [ERROR] processing '{item}': {e}")
            stats["errors"] += 1

    # ☆ Final Report
    print(f"\n{'='*40}")
    print(f"☆ COMPLETED: {status_mode}")
    print(f"☆ Translated: {stats['processed']}")
    print(f"☆ Skipped:    {stats['skipped']}")
    print(f"☆ Conflicts:  {stats['errors']}")
    print(f"{'='*40}")

if __name__ == "__main__":
    # --- CONFIGURATION ---
    target_dir = r"" # Specify your target directory here
    target_language = "en"
    preview_mode = False 
    
    universal_translator(target_dir, target_language, dry_run=preview_mode)
