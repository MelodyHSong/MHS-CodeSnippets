/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# Editor Script (Unity)
☆ File Name: AssetLister.cs
☆ Version: v1.1.0a
☆ Date: 2025-12-17 (Updated)
☆ Description: Editor tool (Finder!) to scan the scene, list referenced assets, 
☆              and suggest the creator/package name by skipping generic Unity folders.
☆
*/

#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using System.IO;
using System.Linq;

public class AssetLister : EditorWindow
{
    private Vector2 scrollPos;
    private List<(string Path, string Creator)> assetData = new List<(string, string)>();

    // Define a set of common, non-descriptive folder names to skip.
    private static readonly HashSet<string> FOLDERS_TO_SKIP = new HashSet<string>(
        new string[]
        {
            "Assets", "Materials", "Textures", "Models", "Scripts", "Resources",
            "Prefabs", "Animations", "Audio", "Shaders", "Plugins", "Editor",
            "Gizmos", "Standard Assets", "Editor Default Resources", "StreamingAssets",
            "VRCA", "VRChat", "Common", "Packages",
            "Art", "Scenes", "Settings", "ThirdParty", "Tools"
        },
        System.StringComparer.OrdinalIgnoreCase
    );

    // Called by the LibraryHub.cs
    public static void ShowWindow()
    {
        GetWindow<AssetLister>("Finder! Asset Lister");
    }

    void OnGUI()
    {
        EditorGUILayout.LabelField("Finder! Asset List Generator", EditorStyles.boldLabel);
        EditorGUILayout.Space();

        if (GUILayout.Button("Find and Suggest Creators for All Assets"))
        {
            FindAssetsInScene();
        }

        EditorGUILayout.Space();

        if (assetData.Count > 0)
        {
            EditorGUILayout.LabelField($"Found {assetData.Count} Unique Assets:", EditorStyles.miniLabel);

            if (GUILayout.Button("Copy Detailed List to Clipboard (Path | Creator Suggestion)"))
            {
                string copyString = string.Join("\n", assetData.Select(d => $"{d.Path} | Suggested Creator: {d.Creator}").ToArray());
                GUIUtility.systemCopyBuffer = copyString;
                Debug.Log($"☆ {assetData.Count} Asset Paths and Suggestions Copied to Clipboard! ☆");
            }

            // --- Results Table Header ---
            EditorGUILayout.BeginHorizontal(EditorStyles.toolbar);
            EditorGUILayout.LabelField("Suggested Creator", EditorStyles.boldLabel, GUILayout.Width(200));
            EditorGUILayout.LabelField("Asset Path", EditorStyles.boldLabel);
            EditorGUILayout.EndHorizontal();

            // --- Results Table Body ---
            scrollPos = EditorGUILayout.BeginScrollView(scrollPos);
            foreach (var data in assetData)
            {
                EditorGUILayout.BeginHorizontal();
                EditorGUILayout.SelectableLabel(data.Creator, GUILayout.Width(200), GUILayout.Height(15));
                EditorGUILayout.SelectableLabel(data.Path, GUILayout.Height(15));
                EditorGUILayout.EndHorizontal();
            }
            EditorGUILayout.EndScrollView();
        }
    }

    void FindAssetsInScene()
    {
        assetData.Clear();
        string scenePath = UnityEditor.SceneManagement.EditorSceneManager.GetActiveScene().path;

        if (string.IsNullOrEmpty(scenePath))
        {
            Debug.LogError("☆ Error: Current scene is not saved! Please save the scene first. ☆");
            return;
        }

        string[] dependencies = AssetDatabase.GetDependencies(scenePath, true);

        var uniquePaths = dependencies
            .Where(p => p.StartsWith("Assets/") && !p.EndsWith(".cs"))
            .Distinct()
            .OrderBy(p => p)
            .ToList();

        foreach (string path in uniquePaths)
        {
            string suggestedCreator = GetSmartCreatorFromPath(path);
            assetData.Add((path, suggestedCreator));
        }

        Debug.Log($"☆ Finder Scan Complete! Found {assetData.Count} unique assets referenced by the current scene. ☆");
    }

    // Core logic: Extracts a potential creator name by skipping common, non-descriptive folders.
    private string GetSmartCreatorFromPath(string path)
    {
        string[] parts = path.Split('/');

        if (parts.Length <= 1)
        {
            return "N/A (Root Asset)";
        }

        for (int i = 1; i < parts.Length - 1; i++)
        {
            string folderName = parts[i];

            if (!FOLDERS_TO_SKIP.Contains(folderName))
            {
                return folderName;
            }
        }

        return "N/A (Generic Path)";
    }
}
#endif