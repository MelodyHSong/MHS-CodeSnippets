/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# Editor Script (Unity)
☆ File Name: LibraryHub.cs
☆ Version: v1.2.0
☆ Date: 2026-04-01
☆
☆ Description: Centralized menu for the Melody Tools suite.
☆
*/

#if UNITY_EDITOR
using UnityEditor;

public class LibraryHub
{
    private const string MENU_ROOT = "☆ Melody Tools ☆/";

    [MenuItem(MENU_ROOT + "Hierarchy Maid (Auto-Sort)", false, 0)]
    public static void ShowSorter() => HierarchyMaid.ShowWindow();

    [MenuItem(MENU_ROOT + "Asset Analyzer (Finder & Weight)", false, 10)]
    public static void ShowAnalyzer() => AssetAnalyzer.ShowWindow();

    [MenuItem(MENU_ROOT + "Shrinker! (Asset Optimizer)", false, 20)]
    public static void ShowShrinker() => ImageShrinker.ShowWindow();

    [MenuItem(MENU_ROOT + "Maid! (Project Cleaner - DANGER)", false, 30)]
    public static void ShowMaid() => ProjectMaid.ShowWindow();
}
#endif
