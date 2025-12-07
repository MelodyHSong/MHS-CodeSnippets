# ☆ Melody's UdonSharp Collectible System ☆

This repository contains a set of UdonSharp scripts designed for VRChat worlds to implement a robust, locally-tracked collectible system with a global, synchronized scoring mechanic. Collectibles disappear only for the player who picks them up, ensuring every user can experience the collection, while the points they gain are added to a universally visible score.

## 💾 Scripts

- `M_DataTypes.cs` - Defines the global `ItemType` (e.g., Ammo, Currency) and `ItemRarity` (e.g., Common, Unique) enums used for categorization and point calculation. 

- `M_Collector.cs` - The core script attached to every collectible item. It locally destroys the item upon player collision and notifies the `M_PointCounter` to update the score. 

- `M_PointCounter.cs` - The central score keeper. It manages the synced total points and updates the world's score display. 

---
