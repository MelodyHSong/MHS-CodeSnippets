/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# Udon Sharp
☆ File Name: M_DataTypes.cs
☆ Date: 2025-12-07
☆
*/

using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

// ☆ Description: Defining the essential collectible data: Types and Rarity levels!

// ☆ The enums MUST be public and NOT nested inside the UdonSharp class! ☆

// Possible magical effects of the collected item.
public enum ItemType
{
    None,
    HealthPickup,
    Ammo,
    Currency,
    Experience,
    KeyItem
}

// How rare is this treasure? Only one rarity per object!
public enum ItemRarity
{
    Common,
    Uncommon,
    Rumored,
    Exquisite,
    Treasured,
    Unique
}


public class M_DataTypes : UdonSharpBehaviour
{
    // This script only needs to exist to define the file/script structure.
}