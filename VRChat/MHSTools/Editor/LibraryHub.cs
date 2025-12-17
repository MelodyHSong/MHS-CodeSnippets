/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# Editor Script (Unity)
☆ File Name: LibraryHub.cs
☆ Version: v1.1.0a
☆ Date: 2025-12-17 (Updated)
☆ Description: Establishes the main menu header and links all custom editor utilities 
☆              (Finder!, Zapper!, Shrinker!, Scale!, Maid!) into a centralized library hub!
☆
*/

#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;

public class LibraryHub
{
    // Define the main menu path.
    private const string MENU_ROOT = "☆ Melody Tools ☆/";

    [MenuItem(MENU_ROOT + "Tool Library Info", false, 0)]
    public static void ShowLibraryInfo()
    {
        EditorUtility.DisplayDialog(
            "☆ Melody Tools Library v1.1.0a ☆",
            "This is the hub for all custom editor utilities, including Finder!, Zapper!, Shrinker!, Scale!, and Maid!.\n\n" +
            "Scripts are organized under the '☆ Melody Tools ☆' menu.",
            "OK"
        );
    }

    [MenuItem(MENU_ROOT + "Finder! (Asset Lister)", false, 10)]
    public static void ShowAssetListerWindow()
    {
        AssetLister.ShowWindow();
    }

    [MenuItem(MENU_ROOT + "Zapper! (Asset Weight)", false, 20)]
    public static void ShowAssetZapperWindow()
    {
        AssetZapper.ShowWindow();
    }

    [MenuItem(MENU_ROOT + "Shrinker! (Asset Optimizer)", false, 30)]
    public static void ShowImageShrinkerWindow()
    {
        ImageShrinker.ShowWindow();
    }

    [MenuItem(MENU_ROOT + "Scale! (Upload Size)", false, 40)]
    public static void ShowAssetScalerWindow()
    {
        AssetScaler.ShowWindow();
    }

    // ADD THE NEW MAID! TOOL HERE
    [MenuItem(MENU_ROOT + "Maid! (Project Cleaner - DANGER)", false, 50)]
    public static void ShowProjectMaidWindow()
    {
        ProjectMaid.ShowWindow();
    }
}
#endif