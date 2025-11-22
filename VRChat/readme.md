# ☆ Melody's VRChat Workshop ☆

> "Code, Coffee, and a little bit of Chaos."

Welcome to my personal collection of **Udon Sharp (U#)** scripts, prefabs, and logic blocks for VRChat! This repository is where I store the magical bits and bobs used to bring worlds to life. Whether you are looking for simple toggles or complex game logic, you might find something useful here.

## ☆ What's Inside?

Here is a breakdown of the folders you'll find in this repo:

* **`_Scripts/`** - The brainy stuff! C# scripts compatible with Udon Sharp.
* **`_Prefabs/`** - Drag-and-drop Unity objects ready for your scene.
* **`_Assets/`** - Materials, sounds, and textures that support the scripts.
* **`_Docs/`** - Notes on how to use the more complex systems.
* **`_Misc/`** - Other files I want to share. 

## ☆ Requirements

To use these scripts, ensure your Unity project is set up with:
* Unity 2022.3.22f1 (or current VRChat supported version)
* VRChat SDK3 (Worlds)
* UdonSharp (via VRChat Creator Companion)

## ☆ Coding Style & Attribution

I believe code should be as cute as it is functional! You will notice all my scripts follow a specific format. If you use my code, please keep the headers intact!

Here is an example of what my code looks like:

```csharp
/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: Udon Sharp (C#)
☆ File Name: ExampleToggle.cs
☆ Date: 2025-11-22
☆
*/

using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

public class ExampleToggle : UdonSharpBehaviour
{
    // Magic happens here...
}
