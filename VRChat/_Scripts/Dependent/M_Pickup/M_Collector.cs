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

// ☆ Description: A secret agent collectible! Finds the PointCounter automatically, adds score, and destroys itself locally.

public class M_Collector : UdonSharpBehaviour
{
    // Link to the main score keeper, found automatically in Start().
    private M_PointCounter PointCounter;

    [Header("Item Data")]
    // Use an array of the public enum type.
    public ItemType[] ItemTypes;

    // Use the public enum type.
    public ItemRarity Rarity = ItemRarity.Common;

    // ☆ We use Start() to find the PointCounter object automatically!
    void Start()
    {
        // 1. Attempt to find the M_PointCounter via GameObject name.
        if (PointCounter == null)
        {
            // NOTE: The Game Object hosting M_PointCounter MUST be named "ScoreManager" for this to work.
            GameObject scoreObject = GameObject.Find("ScoreManager");

            if (scoreObject != null)
            {
                // Get the component from the found GameObject.
                PointCounter = scoreObject.GetComponent<M_PointCounter>();
            }
        }

        // 2. Log a warning if it still couldn't be found (safety check).
        if (PointCounter == null)
        {
            Debug.LogError("☆ M_Collector: Could not find the M_PointCounter! Check object name is 'ScoreManager' and M_PointCounter is attached.");
        }
    }

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
            else
            {
                // Log warning if the counter is missing.
                Debug.LogWarning($"☆ PointCounter reference is missing on {gameObject.name}. Skipping point addition.");
            }

            // 2. Report what was collected for the debug console!
            string typesString = "";
            foreach (ItemType type in ItemTypes)
            {
                typesString += type.ToString() + " ";
            }
            Debug.Log($"☆ {player.displayName} collected a {Rarity.ToString()} item! Types: {typesString}");

            // 3. Poof! Destroy the object just for this client (memory saved locally).
            Destroy(gameObject);
        }
    }
}
