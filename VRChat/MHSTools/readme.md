# ☆ Melody Tools ☆: VRChat Optimization Library

> "The chaos is still here, but at least the assets are sorted."

Welcome to my collection of **C# Editor Scripts** designed specifically to help manage, optimize, and organize assets within the Unity Editor for **VRChat** worlds. These are high-level tools that run *before* you build your world, acting as a personal assistant for your project hygiene!

**Current Version: v1.1.0a**

---

## ☆ Installation

There are two easy ways to install the **`☆ Melody Tools ☆`** library into your Unity project:

### Option 1: Unity Package (Recommended)

1. Navigate to the **`MHS-CodeSnippets/VRChat/_Packages`** directory in this repository.
2. Download the latest **`.unitypackage`** file for the Melody Tools.
3. In your Unity project, simply double-click the downloaded `.unitypackage` file to import all files and scripts automatically.

### Option 2: Manual Drag-and-Drop

1. **Locate Folder:** Ensure the entire **`MHSTools`** folder (which contains the `Editor` subfolder) is placed somewhere within your Unity project's **`Assets`** folder (e.g., `Assets/MyProject/MHSTools`).
2. **Compile:** Once Unity finishes compiling the C# Editor scripts, a new menu item will appear at the top of the Unity Editor.

---

## ☆ The Tools (Accessible via `☆ Melody Tools ☆` Menu)

### 1. Finder! (Asset Lister)

* **Core Function:** Asset Discovery & Attribution
* **Purpose:** Scans the active scene, lists all referenced assets, and intelligently attempts to extract the **Creator/Package Name** from the folder path. Essential for crediting!

### 2. Zapper! (Asset Weight)

* **Core Function:** Raw File Weight Analysis
* **Purpose:** Scans the active scene and lists assets by their **raw file size (MB)**, automatically sorted from largest to smallest. Use this to quickly find your biggest source file sizes.

### 3. Shrinker! (Asset Optimizer)

* **Core Function:** Texture/Material Optimization & Compression
* **Purpose:** Your most powerful tool for shrinking world download size and memory usage. It scans for textures and materials and provides multiple batch fix options:
    * **Max Size Optimization:** Batch-set the **Max Texture Size** (e.g., to 1024, 512, or 256) for selected textures.
    * **Format Optimizer:** Detects textures using uncompressed formats (like ARGB32) and allows you to batch-switch them to compressed formats (DXT1/DXT5).
    * **Shader Checker:** Detects materials using unsupported/legacy shaders and offers a batch replacement fix. It also warns specifically about **Poiyomi** shaders for Android/Quest targets, requiring manual changes.

### 4. Scale! (Upload Size)

* **Core Function:** Estimated Build Weight
* **Purpose:** Calculates the **Estimated Texture Memory Footprint** of your scene, which is far more accurate for VRChat build size than raw file weight. It also lists the **Top 10 Textures** (by memory size) and **Top 10 General Assets** (by file size) for quick optimization targets.

### 5. Maid! (Project Cleaner - DANGER)

* **Core Function:** Project Cleanup & Destructive Removal
* **Purpose:** Scans the **entire project** for assets not referenced by any scene or prefab and permanently moves them off the project. This process uses a **two-step confirmation** to ensure you do not accidentally lose data. Use this tool to keep your project folder tidy and reduce compile times.

---

## ☆ Coding Style & Headers

As with all my code, these C# Editor Scripts follow the same stylish header and clean structure. Please keep these headers intact if you modify or redistribute the source files.

The logic is contained within the C# Editor scripts located in the **`MHSTools/Editor/`** folder.

---

## ☆ License

This code is licensed under the **MIT License**!

A credit to **MelodyHSong** is always appreciated.

---
*Better with cookies. - MelodyHSong*
