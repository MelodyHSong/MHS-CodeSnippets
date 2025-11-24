/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# (UdonSharp)
☆ File Name: UdonResetObject.cs
☆ Date: 2025-11-24
☆
*/

using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

public class UdonResetObject : UdonSharpBehaviour
{
    [Header("☆ Target Object to Reset ☆")]
    [Tooltip("Drag the GameObject/Transform that you want to reset back to its starting position here.")]
    public Transform targetObject;

    // ☆ Private fields to store the initial state of the target object.
    private Vector3 initialPosition;
    private Quaternion initialRotation;

    void Start()
    {
        // ☆ The Start method is called when the script initializes.
        // ☆ We capture the object's initial local position and rotation here.
        // ☆ We use 'local' to ensure it resets relative to its parent, if any.
        if (targetObject != null)
        {
            initialPosition = targetObject.localPosition;
            initialRotation = targetObject.localRotation;
            Debug.Log($"☆ UdonResetObject: Initial position stored for {targetObject.name}: {initialPosition} | {initialRotation}");
        }
        else
        {
            Debug.LogError("☆ UdonResetObject Error: Target Object is not assigned! Reset button will not work. ☆");
        }
    }

    // ☆ This method is called when the Collider of the GameObject this script is attached to
    // ☆ is clicked (i.e., when it's set up as a button/interactable in VRChat).
    public override void Interact()
    {
        if (targetObject == null)
        {
            Debug.LogError("☆ UdonResetObject Error: Cannot reset, Target Object is null. ☆");
            return;
        }
        
        // ☆ IMPORTANT: For objects that can be moved by players, you must own the object
        // ☆ before moving it. This sets the local player as the network owner.
        if (!Networking.IsOwner(targetObject.gameObject))
        {
            Networking.SetOwner(Networking.LocalPlayer, targetObject.gameObject);
        }

        // ☆ Perform the reset action by setting the position and rotation
        // ☆ back to the stored initial values.
        targetObject.localPosition = initialPosition;
        targetObject.localRotation = initialRotation;
        
        Debug.Log($"☆ UdonResetObject: Reset {targetObject.name} to starting position: {initialPosition} ☆");
        
        // ☆ If you need this object to be reset for ALL players across the network,
        // ☆ you would need to use a synchronized network event (like SendCustomNetworkEvent)
        // ☆ in a more complex setup. For a simple local reset, this is sufficient.
    }
}
