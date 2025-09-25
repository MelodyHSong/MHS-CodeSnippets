/*
✰
✰ Author: ✰ MelodyHSong ✰
✰ Language: C#
✰ File Name: yRotation.cs
✰ Date: September 24th, 2025
✰
*/

// Description: 

using UnityEngine;

public class yRotation : MonoBehaviour
{
    // UwU - Editable Speed in Inspector! ✰
    [SerializeField]
    private float rotationSpeed = 50f;

    void Update()
    {
        // owo Rotate around the Y-axis! ✰
        // Frame-rate independent: speed * Time.deltaTime ✰
        transform.Rotate(Vector3.up * rotationSpeed * Time.deltaTime);
    }
}

/*
✰
✰ [SerializeField]        : Makes the private variable **visible and editable** in the Unity Inspector. ✰
✰ rotationSpeed = 50f     : Defines the **speed** (in degrees per second) that you can adjust in the editor. ✰
✰ transform.Rotate(...)   : The core function to apply rotation. ✰
✰ Vector3.up              : Specifies the rotation axis as the **Y-axis**. ✰
✰ * Time.deltaTime        : Ensures the rotation is smooth and **frame-rate independent**. ✰ 
✰
*/
