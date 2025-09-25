/*
✰
✰ Author: ✰ MelodyHSong ✰
✰ Language: C#
✰ File Name: xyzRotation.cs
✰ Date: September 24th, 2025
✰
*/

// Description: This script rotates the attached GameObject around the X, Y, and Z axes at the same time! 💖

using UnityEngine;

public class xyzRotation : MonoBehaviour
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
        // owo Rotate around all three axes! ✰
        // Frame-rate independent: speed * Time.deltaTime ✰
        transform.Rotate(new Vector3(xRotationSpeed, yRotationSpeed, zRotationSpeed) * Time.deltaTime);
    }
}

/*
✰
✰ [SerializeField]        : Makes the private variables **visible and editable** in the Unity Inspector. ✰
✰ xRotationSpeed, etc.    : Defines the **speed** (in degrees per second) for each axis. ✰
✰ transform.Rotate(...)   : The core function to apply rotation. ✰
✰ new Vector3(...)        : Creates a new vector to apply rotation to each axis individually. ✰
✰ * Time.deltaTime        : Ensures the rotation is smooth and **frame-rate independent**. ✰ 
✰
*/
