/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: Markdown
☆ File Name: README.md
☆ Date: 2025-09-29
☆ Ver: 1.1
☆
*/

# 🌟 VRChat Lobby Control Panel (SDK3/Udon Sharp) 🌟

This document details the configuration and troubleshooting steps for a robust, performance-optimized mirror and audio control system built for VRChat using Unity 2022 and Udon Sharp (U#).

The **LobbyControlPanel.cs** script manages three mirror locations (A, B, C) with toggles for High Quality (HQ) or Low Quality (LQ) modes, individual on/off switches for each location, and BGM audio controls.

---

## 🛠️ Required Setup Summary

For the system to function correctly, the following components **must** be used and wired to the **`LobbyControlManager`** object (the one holding the Udon Behaviour):

1.  **UI Elements:** Use **VRChat-specific UI components** (e.g., `Button - TextMeshPro (VRC)`).
2.  **Interaction Method:** All buttons **must** use the `VRC_Interact` component, *not* the standard `Button.OnClick()` event.
3.  **Assignments:** All 6 mirror GameObjects, the AudioSource, and the Slider **must** be assigned in the Inspector.

---

## 🚨 Critical Troubleshooting Issues & Solutions

The majority of issues were caused by conflicts in Unity's Input System, which prevents VRChat clicks from reaching the Udon script.

### 1. The Clicks Do Not Register (Buttons Are Unresponsive)

| Problem | Cause | Definitive Fix |
| :--- | :--- | :--- |
| **Input Conflict** | The Unity project contained a hidden or duplicate `EventSystem` or `StandaloneInputModule`, which interferes with VRChat's `InputSystemUIInputModule`. | **Execute a Clean Sweep:** 1. Delete all `EventSystem` objects from the Hierarchy. 2. Create a new `Canvas` (to generate a new, clean EventSystem). 3. If the new EventSystem still shows the `StandaloneInputModule` warning, click **"Replace with InputSystemUIInputModule"**. |
| **Faulty Button Components** | Custom-created VRC buttons were somehow corrupted or missing key VRChat raycast components (like `VRC_Interact`). | **Use Working Prefabs:** Delete the custom buttons and **copy/duplicate** buttons from a known working VRChat SDK Example scene (like the Udon Example Scene) to guarantee a working component structure. |
| **Missing Interact Script (The SDK3 Fix)** | The SDK3 standard `Button.OnClick()` is unreliable with Udon. | **Use VRC\_Interact:** For every single control button, manually add a **Box Collider** (set to **`Is Trigger`**) and the **`VRC_Interact`** component. Wire the `On Interact` event to call the Udon method (`SendCustomEvent`). |

### 2. Volume Slider Does Not Change Volume

| Problem | Cause | Definitive Fix |
| :--- | :--- | :--- |
| **Script Crash (Start-up)** | The `bgmAudioSource` or `bgmVolumeSlider` variables were unassigned (`None`) in the Inspector, causing the `Start()` function to crash silently before button logic could run. | **Assign All Variables:** Ensure both the **AudioSource** and the **Slider GameObject** are dragged into their corresponding slots on the `LobbyControlManager` Udon Behaviour. |
| **Invalid Volume Range** | The standard Unity `AudioSource.volume` property only accepts values from 0.0 to 1.0. | **Set Max Value to 1:** On the **Slider (Script)** component, set the **Max Value** to **1**. (If this value is $> 1$, the volume will be maxed out but will not change visually/perceptibly in the 0-1 range). |

### 3. All Mirrors Start On/State Resets

| Problem | Cause | Definitive Fix |
| :--- | :--- | :--- |
| **State Conflict** | The mirror GameObjects were not physically disabled in the editor, or the script didn't reset the internal state. | **Physical Disable + Code Reset:** Ensure all 6 `VRCMirror` GameObjects are **disabled** in the Hierarchy before entering Play Mode. The `Start()` function is now coded to force the mirror toggles to `false` and the quality to HQ (index 1) for a clean start. |

---

## ⚙️ Udon Sharp Wiring Guide

All events are wired from the **`VRC_Interact` $\rightarrow$ `On Interact`** event to the **`LobbyControlManager`** GameObject.

| Control | Function Name (Case Sensitive) | Purpose |
| :--- | :--- | :--- |
| **Volume Slider** (`On Value Changed`) | `SetBGMVolume` | Reads slider value and applies it to the AudioSource. |
| **BGM Play/Pause Button** | `ToggleBGM` | Pauses or plays the BGM. |
| **Quality Toggle (HQ/LQ)** | `ToggleQualityLQ` | Switches global quality between HQ (1) and LQ (2). |
| **Mirrors OFF Button** | `SetQualityOff` | Turns all mirrors off (global setting). |
| **Location A Toggle** | `ToggleMirrorA` | Toggles the mirror at location A on/off. |
