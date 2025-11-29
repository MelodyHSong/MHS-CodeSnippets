/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# Editor Script (Unity)
☆ File Name: ImageShrinker.cs
☆ Date: 2025-11-28
☆ Description: Editor tool (Shrinker!) to scan the scene, list referenced textures, 
☆              show their file size, allow individual selection, and batch-set Max 
☆              Texture Size for optimization. The list is automatically sorted 
☆              from biggest to smallest file size.
☆
*/

#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using System.Linq;
using System.IO;

public class ImageShrinker : EditorWindow
{
    private struct TextureData
    {
        public string Path;
        public long SizeBytes;
        public string SizeMB => (SizeBytes / (1024f * 1024f)).ToString("F2") + " MB";
        public bool IsSelected;
    }

    private List<TextureData> textureDataList = new List<TextureData>();
    private Vector2 scrollPos;
    private bool selectAll = true;

    // Available optimization sizes
    private readonly int[] SIZES = { 2048, 1024, 512, 256, 128 };
    private int selectedSizeIndex = 1;

    // Called by the LibraryHub.cs
    public static void ShowWindow()
    {
        GetWindow<ImageShrinker>("Shrinker! Texture Resize");
    }

    void OnGUI()
    {
        EditorGUILayout.LabelField("Shrinker! Texture Resize Utility", EditorStyles.boldLabel);
        EditorGUILayout.Space();

        if (GUILayout.Button("Find All Textures in Scene (Scan Weight and Sort)"))
        {
            FindSceneTextures();
        }

        EditorGUILayout.Space();

        if (textureDataList.Count > 0)
        {
            int selectedCount = textureDataList.Count(t => t.IsSelected);

            // --- Resize Controls ---
            EditorGUILayout.BeginHorizontal(EditorStyles.helpBox);

            // Dropdown to select the target size
            selectedSizeIndex = EditorGUILayout.Popup("Target Max Size:", selectedSizeIndex, SIZES.Select(s => s.ToString()).ToArray(), GUILayout.Width(200));
            int targetSize = SIZES[selectedSizeIndex];

            // Apply Button
            GUI.enabled = selectedCount > 0;
            if (GUILayout.Button($"Apply {targetSize} Max Size to {selectedCount} Selected Textures", GUILayout.Height(30)))
            {
                ApplyMaxSize(targetSize);
            }
            GUI.enabled = true;

            EditorGUILayout.EndHorizontal();

            EditorGUILayout.Space();

            // --- Asset List Display Header ---
            EditorGUILayout.BeginHorizontal(EditorStyles.toolbar);

            // Select All Toggle Header
            bool newSelectAll = EditorGUILayout.Toggle(selectAll, GUILayout.Width(20));
            if (newSelectAll != selectAll)
            {
                selectAll = newSelectAll;
                for (int i = 0; i < textureDataList.Count; i++)
                {
                    var data = textureDataList[i];
                    data.IsSelected = selectAll;
                    textureDataList[i] = data;
                }
            }
            EditorGUILayout.LabelField("Weight (MB)", EditorStyles.boldLabel, GUILayout.Width(90));
            EditorGUILayout.LabelField("Texture Path", EditorStyles.boldLabel);
            EditorGUILayout.EndHorizontal();

            // --- Asset List Display Body ---
            scrollPos = EditorGUILayout.BeginScrollView(scrollPos);

            for (int i = 0; i < textureDataList.Count; i++)
            {
                var textureData = textureDataList[i];

                EditorGUILayout.BeginHorizontal();

                // Individual Selection Toggle
                bool newSelection = EditorGUILayout.Toggle(textureData.IsSelected, GUILayout.Width(20));
                if (newSelection != textureData.IsSelected)
                {
                    textureData.IsSelected = newSelection;
                    textureDataList[i] = textureData;
                    // Reset 'Select All' if a single item is deselected
                    if (!newSelection) selectAll = false;
                }

                // Weight Display
                EditorGUILayout.SelectableLabel(textureData.SizeMB, GUILayout.Width(90), GUILayout.Height(15));

                // Path Display
                EditorGUILayout.SelectableLabel(textureData.Path, GUILayout.Height(15));

                EditorGUILayout.EndHorizontal();
            }

            EditorGUILayout.EndScrollView();
        }
    }

    void FindSceneTextures()
    {
        textureDataList.Clear();
        string scenePath = UnityEditor.SceneManagement.EditorSceneManager.GetActiveScene().path;

        if (string.IsNullOrEmpty(scenePath))
        {
            Debug.LogError("☆ Error: Current scene is not saved! Please save the scene first. ☆");
            return;
        }

        string[] dependencies = AssetDatabase.GetDependencies(scenePath, true);

        var textureExtensions = new HashSet<string>(
            new string[] { ".png", ".jpg", ".jpeg", ".tga", ".bmp", ".dds" },
            System.StringComparer.OrdinalIgnoreCase
        );

        var paths = dependencies
            .Where(p => p.StartsWith("Assets/") && textureExtensions.Contains(System.IO.Path.GetExtension(p)))
            .Distinct()
            .ToList(); // Removed OrderBy(p => p) to prepare for size sorting

        // Populate the new list with size and initial selection data
        var tempList = new List<TextureData>();
        foreach (string path in paths)
        {
            string fullPath = Path.Combine(Application.dataPath, path.Substring("Assets/".Length));
            long sizeBytes = 0;
            if (System.IO.File.Exists(fullPath))
            {
                System.IO.FileInfo info = new System.IO.FileInfo(fullPath);
                sizeBytes = info.Length;
            }

            tempList.Add(new TextureData
            {
                Path = path,
                SizeBytes = sizeBytes,
                IsSelected = selectAll
            });
        }

        // ☆ CORE CHANGE: Sort the list by size in descending order (biggest first) ☆
        textureDataList = tempList.OrderByDescending(t => t.SizeBytes).ToList();

        Debug.Log($"☆ Shrinker Scan Complete! Found {textureDataList.Count} unique texture assets, sorted by size. ☆");
    }

    void ApplyMaxSize(int targetSize)
    {
        var selectedTextures = textureDataList.Where(t => t.IsSelected).ToList();

        if (selectedTextures.Count == 0) return;

        if (!EditorUtility.DisplayDialog(
            "Confirm Texture Resize",
            $"Are you sure you want to set the Max Size of {selectedTextures.Count} selected textures to {targetSize}?\n\nThis operation modifies import settings.",
            "Yes, Resize",
            "Cancel"))
        {
            return;
        }

        int appliedCount = 0;

        foreach (var textureData in selectedTextures)
        {
            TextureImporter importer = AssetImporter.GetAtPath(textureData.Path) as TextureImporter;

            if (importer != null)
            {
                if (importer.maxTextureSize > targetSize)
                {
                    importer.maxTextureSize = targetSize;
                    importer.SaveAndReimport();
                    appliedCount++;
                }
            }
        }

        EditorUtility.DisplayDialog("Shrinker! Success",
                                    $"Successfully set Max Texture Size to {targetSize} for {appliedCount} textures out of {selectedTextures.Count} selected.\n\n" +
                                    "Note: Textures that were already smaller or equal were skipped.",
                                    "OK");

        Debug.Log($"☆ Shrinker! Operation Complete. Applied Max Size {targetSize} to {appliedCount} textures. ☆");
    }
}
#endif