## ☆ Dependent Scripts ☆

> "Lonely scripts? Not anymore!"

### **Overview**

This directory contains **Dependent UdonSharp Scripts** developed for VRChat worlds.
Unlike the `Standalone` directory, the scripts within this directory are designed to be **interconnected**. They rely on, reference, or require other custom scripts (often called **Core** or **Manager** scripts) found within the `Dependent` subfolders to function correctly.
The purpose of this directory is to organize larger, more complex systems where multiple scripts work together to achieve a major feature (e.g., a complex game system, a multi-stage puzzle, or a centralized networking handler).

---

### **Directory Structure & Purpose**

Scripts in this directory are organized into **subfolders**. Each subfolder represents a complete, cohesive system or feature set.

---

### **Contribution & Usage**

* **To use a system:** Copy the entire desired **subfolder** (e.g., `/QuestSystem/`) into your Unity project's UdonSharp folder. Ensure all internal script references are correctly linked in the Unity Inspector.
* **To use a script:** Copy the desired `.cs` file OR create a new UdonSharp script then paste the desired script into it. **Warning:** You must ensure its necessary dependencies (usually the Manager or Core script of its system) are also present in your project.
* **Best Practice:** When creating a new dependent system, create a new subfolder and place all related scripts inside. The system's primary entry point (e.g., the main manager script) should be clearly identified.

---

*Aweee~ How romantic! - MelodyHSong*
