# ☆ Melody Tools ☆: VRChat Optimization Library

> "The chaos is still here, but at least the assets are sorted."

Welcome to the updated collection of **C# Editor Scripts** designed specifically to help manage, optimize, and organize assets within the Unity Editor for **VRChat** worlds and avatars. These tools act as your personal project hygiene assistant!

> Current Version: v1.2.0 (Streamlined Edition)

---

## ☆ Installation

1. **Folder Setup:** Ensure the scripts are placed within a folder named `Editor` inside your Unity `Assets` directory (e.g., `Assets/MelodyTools/Editor/`).
2. **Compilation:** Once Unity finishes compiling, a new menu labeled **`☆ Melody Tools ☆`** will appear in your top menu bar.

---

## ☆ The Tools (Accessible via `☆ Melody Tools ☆` Menu)

### 1. Hierarchy Maid (Auto-Sort)

* **Core Function:** Intelligent Scene Organization.
* **Purpose:** Automatically sorts your hierarchy into clean categories like `--- MESHES ---` and `--- LIGHTS ---`.
* **VRC-Safe:** Identifies **Udon Toggles** and **Nested Room Logic** to ensure "SetActive" chains never break.
* **Prefab Protection:** Treats **Prefabs** as sealed units, moving them without unpacking or breaking their internal structure.[cite: 1]

### 2. Asset Analyzer (Finder & Weight)

* **Core Function:** Dependency & Size Intelligence.[cite: 1]
* **Purpose:** Merges the functionality of the old *Finder!*, *Zapper!*, and *Scale!*.[cite: 1]
  * Lists all referenced assets in the scene.[cite: 1]
  * Suggests the **Creator/Package Name** based on folder paths.[cite: 1]
  * Displays **Raw File Weight** and identifies large texture memory contributors.[cite: 1]

### 3. Shrinker! (Asset Optimizer)

* **Core Function:** Texture & Shader Compression.[cite: 1]
* **Purpose:** Your primary tool for reducing download size.[cite: 1]
  * **Batch Resizing:** Set Max Texture Size for multiple assets at once.[cite: 1]
  * **Format Fixer:** Switches unoptimized formats (ARGB32) to VRC-friendly compression (DXT5).[cite: 1]
  * **Shader Checker:** Flags problematic shaders (like Poiyomi on Quest) and offers batch-replacement for legacy materials.[cite: 1]

### 4. Maid! (Project Cleaner - DANGER)

* **Core Function:** Global Project Cleanup.[cite: 1]
* **Purpose:** Scans for assets not referenced by *any* scene or prefab and moves them to a backup folder on your Desktop.[cite: 1]
* **Safety:** Features a **two-step confirmation** to prevent accidental data loss.[cite: 1]

---

## ☆ License

This library is licensed under the **MIT License**.
A credit to **MelodyHSong** is always appreciated!

---

> *Better with cookies. - MelodyHSong*
