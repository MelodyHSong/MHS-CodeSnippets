# ☆ The Script Library ☆

> "Logic, loops, and a little bit of magic."

This folder contains all the raw **C# (UdonSharp)** files used in my VRChat projects. 

## ☆ How to Use
1. These scripts require **UdonSharp**.
2. Ensure your Unity project has the VRChat Worlds SDK installed.
3. If a script references another script in this folder, make sure both are in your project!

# ✰ World Logic Scripts: UdonSharp Usage ✰

## Overview 

This repository contains C\# scripts written using **UdonSharp**, the preferred scripting language for implementing custom logic in VRChat worlds. These scripts are used to create dynamic, interactive, or animated elements that are safe and network-compatible within the VRChat client environment.

The logic in these scripts (like object rotation, movement, or interaction handling) will **not work** if written as standard `UnityEngine.MonoBehaviour` C\# scripts.

---

## 🛑 Why Standard C# Fails in VRChat

VRChat utilizes a custom, secure runtime environment known as the **Udon Virtual Machine (Udon VM)**.

| Script Type | Status in VRChat | The Reason |
| :--- | :--- | :--- |
| **Standard C# (`MonoBehaviour`)** | **Blocked** ⛔️ | VRChat blocks arbitrary C\# for security and optimization. Any movement logic in a standard `Update()` will be ignored at runtime. |
| **UdonSharp (`UdonSharpBehaviour`)** | **Required** ✅ | UdonSharp scripts are compiled into Udon bytecode, which the VRChat client is designed to safely execute. This is the only way to manage networked behavior and transform changes reliably. |

---

## 🛠️ Script: `xyzRotation_Udon.cs` Usage

### **Description**

This script rotates the attached GameObject around the X, Y, and Z axes simultaneously. It includes networking logic to ensure the rotation is visible and runs correctly for all players in a VRChat instance.

### **Code Snippet**

```csharp
/*
✰
✰ Author: ✰ MelodyHSong ✰
✰ Language: UdonSharp (C# dialect for VRChat)
✰ File Name: xyzRotation_Udon.cs
✰ Date: September 24th, 2025
✰
*/

// Description: This script rotates the attached GameObject around the X, Y, and Z axes at the same time! ✰

using UnityEngine;
using UdonSharp;
using VRC.SDKBase; 
using VRC.Udon;

// CRITICAL: Must inherit from UdonSharpBehaviour!
public class xyzRotationUdon : UdonSharpBehaviour 
{
    // UwU - Editable Speeds in Inspector! ✰
    [SerializeField]
    private float xRotationSpeed = 50f;
    [SerializeField]
    private float yRotationSpeed = 50f;
    [SerializeField]
    private float zRotationSpeed = 50f;

    void Update()
    {
        // 🔑 Ownership Check: Only the client who owns the object can change its transform over the network.
        if (Networking.IsOwner(gameObject))
        {
            // owo Apply rotation! Frame-rate independent: speed * Time.deltaTime ✰
            transform.Rotate(new Vector3(xRotationSpeed, yRotationSpeed, zRotationSpeed) * Time.deltaTime, Space.Self);
        }
        else
        {
            // Request ownership. This ensures the first player to load the object can start the rotation.
            Networking.SetOwner(Networking.LocalPlayer, gameObject);
        }
    }
}
