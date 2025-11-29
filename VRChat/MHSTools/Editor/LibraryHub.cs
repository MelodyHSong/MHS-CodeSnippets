/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# Editor Script (Unity)
☆ File Name: LibraryHub.cs
☆ Date: 2025-11-28
☆ Description: Establishes the main menu header and links all custom editor utilities 
☆              (Finder! and Zapper!) into a centralized library.
☆
*/

#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;

public class LibraryHub
{
    // Define the main menu path, now with the closing asterisk.
    private const string MENU_ROOT = "☆ Melody Tools ☆/";

    [MenuItem(MENU_ROOT + "Tool Library Info", false, 0)]
    public static void ShowLibraryInfo()
    {
        EditorUtility.DisplayDialog(
            "☆ Melody Tools Library ☆",
            "This is the hub for all custom editor utilities, including Finder! and Zapper!.\n\n" +
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

    [MenuItem(MENU_ROOT + "Shrinker! (Image Resizer)", false, 30)]
    public static void ShowImageShrinkerWindow()
    {
        ImageShrinker.ShowWindow();
    }
}
#endif