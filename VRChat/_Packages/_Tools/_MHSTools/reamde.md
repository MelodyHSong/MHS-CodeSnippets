# ☆ Melody Tools ☆: Tool Library v1.1.1a

> "Keep your projects clean, your textures small, and your cookies fresh."

Welcome to the **v1.1.1a** update of Melody Tools! This version focuses on giving the **Shrinker!** tool even more control over your world assets, allowing you to not just optimize, but fine-tune resolutions exactly how you need them.

---

## ☆ What's New in v1.1.1a

### 1. Shrinker! Update: Forced Resolution Scaling
* **Forced Scaling:** Added a new toggle in the **Shrinker! (Asset Optimizer)** tool: **"Allow Upscaling (Force to Target)"**.
* **Flexibility:** Previously, the tool would only scale textures *down* to the target size. Now, if the toggle is enabled, it will force all selected textures to the chosen resolution (e.g., forcing a 128px icon to 512px for consistency).
* **Smart Logic:** When the toggle is off, it reverts to "Shrink Only" mode, ensuring you don't accidentally increase the memory footprint of smaller assets.

### 2. UI Polishing & Optimization
* Updated the **Shrinker!** layout for better clarity when managing multiple batch-fix sections (Size, Format, and Shaders).
* Improved internal scan logic to maintain performance even as the tool library grows.

---

## ☆ Current Toolset Summary

* **Finder! (Asset Lister):** Smart creator attribution based on project paths.
* **Zapper! (Asset Weight):** Raw file weight analysis with interactive sorting.
* **Shrinker! (Asset Optimizer):** Batch resolution scaling (Now with Upscaling!), texture format compression, and shader compatibility checking.
* **Scale! (Upload Size):** Real-time estimation of your scene's VRChat upload weight.
* **Maid! (Project Cleaner):** Destructive asset cleanup with two-step safety confirmation.

---

## ☆ Installation

1. **Delete Old Version:** To ensure a clean update, it is recommended to delete your existing `MHSTools` folder.
2. **Import Package:** Double-click the `MelodyTools_v1.1.1a.unitypackage` and click **Import**.
3. **Enjoy:** Access the hub via the **`☆ Melody Tools ☆`** menu at the top of your Unity Editor.

---
*Cookies make the code run faster. - MelodyHSong*