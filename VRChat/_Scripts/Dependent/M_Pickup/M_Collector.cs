/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# Udon Sharp
☆ File Name: M_Collector.cs
☆ Date: 2025-12-07
☆
*/

using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

// ☆ Description: A secret agent collectible! Destroyed locally, sends item data to the PointCounter.

public class M_Collector : UdonSharpBehaviour
{
    // Link to the main score keeper.
    public M_PointCounter PointCounter; // Reference to the other UdonSharp class.

    [Header("Item Data")]
    // Use an array of the public enum type.
    public ItemType[] ItemTypes;

    // Use the public enum type.
    public ItemRarity Rarity = ItemRarity.Common;

    // The official UdonSharp event for when a player bumps into this trigger!
    public override void OnPlayerTriggerEnter(VRCPlayerApi player)
    {
        // Check if the collector is the local user (aka, YOU!).
        if (player.isLocal)
        {
            // 1. Send the item's point value to the counter.
            if (PointCounter != null)
            {
                // Pass the Rarity index (0, 1, 2, etc.) to the counter script.
                PointCounter.AddPoints((int)Rarity);
            }

            // 2. Report what was collected for the debug console!
            string typesString = "";
            foreach (ItemType type in ItemTypes)
            {
                typesString += type.ToString() + " ";
            }
            Debug.Log($"☆ Shhh... {player.displayName} secretly collected a {Rarity.ToString()} item! Types: {typesString}");

            // 3. Poof! Destroy the object just for this client (memory saved locally).
            Destroy(gameObject);
        }
    }
}