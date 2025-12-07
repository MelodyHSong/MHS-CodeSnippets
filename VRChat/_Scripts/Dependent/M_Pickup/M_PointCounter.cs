/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# Udon Sharp
☆ File Name: M_PointCounter.cs
☆ Date: 2025-12-07
☆
*/

// ☆ 



using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

// ☆ Description: The official score keeper! It tracks total points and syncs the score for everyone.
// ☆ This Udon Behaviour MUST be set to SYNCHRONIZED.

public class M_PointCounter : UdonSharpBehaviour
{
    // The display text (UI) for showing off the current score.
    public UnityEngine.UI.Text ScoreDisplay;

    [UdonSynced]
    // The player's grand total score, shared across the network.
    private int totalScore = 0;

    // ☆ Point values defined by rarity. Index must match the ItemRarity enum!
    public int[] RarityPointValues = new int[]
    {
        10,  // Common points (easiest to find!)
        50,  // Uncommon
        100, // Rumored
        500, // Exquisite
        1000,// Treasured
        5000 // Unique (Big points!)
    };

    void Start()
    {
        // Set the score display when the world starts.
        UpdateScoreDisplay();
    }

    // ☆ Update the UI display (Local Only) after a score change.
    private void UpdateScoreDisplay()
    {
        if (ScoreDisplay != null)
        {
            ScoreDisplay.text = $"Score: {totalScore}";
        }
    }

    // ☆ The M_Collector calls this! We receive the item's rarity as an index.
    public void AddPoints(int rarityIndex)
    {
        // We only allow the Master to update the synced variable (for stability!).
        if (!Networking.IsOwner(gameObject))
        {
            Networking.SetOwner(Networking.LocalPlayer, gameObject);
        }

        // Double-check the rarity index is valid before adding points.
        if (rarityIndex >= 0 && rarityIndex < RarityPointValues.Length)
        {
            int pointsGained = RarityPointValues[rarityIndex];
            totalScore += pointsGained;

            // CORRECTED LINE: Using UnityEngine.Debug to resolve the ambiguity.
            UnityEngine.Debug.Log($"⭐ Score updated! Gained {pointsGained} for a {((ItemRarity)rarityIndex).ToString()} item. Total: {totalScore}");

            // Tell the network the score has changed!
            RequestSerialization();
        }
    }

    // ☆ VRChat calls this when the synced data changes from another client.
    public override void OnDeserialization()
    {
        // Gotta keep that display up-to-date!
        UpdateScoreDisplay();
    }
}