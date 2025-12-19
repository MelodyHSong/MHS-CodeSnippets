## ☆ Standalone Scripts ☆

> "What do we call a lonely script?"

### **Overview**

This directory contains **Standalone UdonSharp Scripts** developed for VRChat worlds.

The scripts within this directory are designed to be **self-contained** and function without referencing or requiring other custom scripts from the `_Scripts` folder (though they may reference built-in Udon or Unity components).

---

### **Directory Structure & Purpose**

Each file in this directory represents a single, independent UdonSharp script, usually tackling one specific task or feature.

| Script Type | Description |
| :--- | :--- |
| **Standalone Scripts** | Scripts that only rely on their own logic and built-in components (e.g., a simple button toggle, a basic timer, a local movement controller). |
| **Helper Classes** | Any small, highly independent utility classes that don't directly control a VRChat feature but are used across multiple standalone scripts (e.g., simple mathematical functions, common string manipulation, if necessary). |

---

### **Contribution & Usage**

* **To use a script:** Simply copy the desired `.cs` file into your Unity project's UdonSharp folder, attach it to a GameObject, and configure the public variables in the Inspector as needed. OR create a new UdonSharp scropt then paste the desired scropt into it. 
* **Best Practice:** When creating a new standalone script, ensure it does not create a dependency on any other script *within* the `MHS-CodeSnippets` directory structure. If a script requires another custom script to function, it should be placed in the appropriate non-`Standalone` directory.

---
*Why so lonley? - MelodyHSong* 
