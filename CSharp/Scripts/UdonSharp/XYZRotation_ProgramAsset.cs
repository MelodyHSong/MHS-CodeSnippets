// ✰
// ✰ Author: ✰ MelodyHSong ✰
// ✰ Language: UdonSharp (C# dialect for VRChat)
// ✰ File Name: xyzRotation_Udon.cs
// ✰ Date: September 24th, 2025
// ✰

// Required using statements for VRChat networking
using UnityEngine;
using UdonSharp;
using VRC.SDKBase;
using VRC.Udon;

// The class must inherit from UdonSharpBehaviour!
public class XYZRotation_ProgramAsset : UdonSharpBehaviour
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
        // 🔑 CHECK 1: Ensure the script is only running on the client who owns the object.
        if (Networking.IsOwner(gameObject))
        {
            // owo Rotate around all three axes! ✰
            // VRChat will respect the transform change because the owner is doing it.
            transform.Rotate(new Vector3(xRotationSpeed, yRotationSpeed, zRotationSpeed) * Time.deltaTime, Space.Self);
        }
        else
        {
            // 🔑 CHECK 2: If we are not the owner, we request ownership every frame!
            // This is a simple but effective way to ensure the first person to load 
            // the object or enter the scene starts the rotation.
            Networking.SetOwner(Networking.LocalPlayer, gameObject);
        }
    }
}