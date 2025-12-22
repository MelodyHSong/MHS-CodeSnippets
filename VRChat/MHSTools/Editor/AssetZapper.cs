/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# Editor Script (Unity)
☆ File Name: AssetZapper.cs
☆ Version: v1.1.1a
☆ Date: 2025-12-17 (Updated)
☆ Description: Editor tool (Zapper!) to scan the scene, list referenced assets, 
☆              and calculate their raw file size/weight for optimization. Includes 
☆              sorting and total size calculation.
☆
*/

#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using System.Linq;
using System.IO;

public class AssetZapper : EditorWindow
{
    // Define the structure to hold asset data and its calculated size
    private struct AssetWeight
    {
        public string Path;
        public long SizeBytes;
        public string Creator;

        public string SizeMB => (SizeBytes / (1024f * 1024f)).ToString("F2") + " MB";
    }

    private List<AssetWeight> weightedAssets = new List<AssetWeight>();
    private Vector2 scrollPos;
    private bool sortDescending = true;
    private long totalSizeBytes = 0;

    private enum SortBy { Size, Path, Creator }
    private SortBy currentSort = SortBy.Size;

    // Called by the LibraryHub.cs
    public static void ShowWindow()
    {
        GetWindow<AssetZapper>("Zapper! Asset Weight");
    }

    void OnGUI()
    {
        EditorGUILayout.LabelField("Zapper! Asset Weight Analyzer", EditorStyles.boldLabel);
        EditorGUILayout.Space();

        if (GUILayout.Button("Scan Scene and Calculate Asset Weights"))
        {
            ScanAndCalculateWeights();
        }

        if (weightedAssets.Count > 0)
        {
            EditorGUILayout.Space();

            // --- Total Size Display ---
            float totalSizeMB = totalSizeBytes / (1024f * 1024f);
            EditorGUILayout.HelpBox($"Total Scanned Assets: {weightedAssets.Count}\nTotal Weight: {totalSizeMB:F2} MB", MessageType.Info);
            EditorGUILayout.Space();

            // --- Header Bar with Sorting Controls ---
            EditorGUILayout.BeginHorizontal(EditorStyles.toolbar);

            // Size Column Header (Interactive Button for Sorting)
            if (GUILayout.Button(GetSortHeader("Size (MB)", SortBy.Size, 70), EditorStyles.toolbarButton, GUILayout.Width(70)))
            {
                ToggleSort(SortBy.Size);
            }

            // Creator Column Header
            if (GUILayout.Button(GetSortHeader("Creator", SortBy.Creator, 150), EditorStyles.toolbarButton, GUILayout.Width(150)))
            {
                ToggleSort(SortBy.Creator);
            }

            // Path Column Header
            if (GUILayout.Button(GetSortHeader("Path", SortBy.Path, 0), EditorStyles.toolbarButton))
            {
                ToggleSort(SortBy.Path);
            }

            EditorGUILayout.EndHorizontal();

            // --- Asset List Display ---
            scrollPos = EditorGUILayout.BeginScrollView(scrollPos);
            foreach (var asset in weightedAssets)
            {
                EditorGUILayout.BeginHorizontal();
                EditorGUILayout.SelectableLabel(asset.SizeMB, GUILayout.Width(70), GUILayout.Height(15));
                EditorGUILayout.SelectableLabel(asset.Creator, GUILayout.Width(150), GUILayout.Height(15));
                EditorGUILayout.SelectableLabel(asset.Path, GUILayout.Height(15));
                EditorGUILayout.EndHorizontal();
                // Optional: Draw a separator line between items
                Rect rect = EditorGUILayout.GetControlRect(false, 1);
                rect.height = 1;
                EditorGUI.DrawRect(rect, new Color(0.5f, 0.5f, 0.5f, 0.2f));
            }
            EditorGUILayout.EndScrollView();
        }
    }

    // Helper function to create the header text with a sorting indicator
    private string GetSortHeader(string label, SortBy sortType, int width)
    {
        string indicator = "";
        if (currentSort == sortType)
        {
            indicator = sortDescending ? " ▼" : " ▲";
        }
        return label + indicator;
    }

    // Function to handle the sorting toggle logic
    private void ToggleSort(SortBy newSort)
    {
        if (currentSort == newSort)
        {
            sortDescending = !sortDescending;
        }
        else
        {
            currentSort = newSort;
            sortDescending = true; // Default to descending when changing columns
        }
        SortAssets();
    }

    // Core sorting logic based on currentSort and sortDescending flags
    private void SortAssets()
    {
        IOrderedEnumerable<AssetWeight> sortedList = null;

        switch (currentSort)
        {
            case SortBy.Size:
                sortedList = sortDescending
                    ? weightedAssets.OrderByDescending(a => a.SizeBytes)
                    : weightedAssets.OrderBy(a => a.SizeBytes);
                break;
            case SortBy.Path:
                sortedList = sortDescending
                    ? weightedAssets.OrderByDescending(a => a.Path)
                    : weightedAssets.OrderBy(a => a.Path);
                break;
            case SortBy.Creator:
                sortedList = sortDescending
                    ? weightedAssets.OrderByDescending(a => a.Creator)
                    : weightedAssets.OrderBy(a => a.Creator);
                break;
        }

        if (sortedList != null)
        {
            weightedAssets = sortedList.ToList();
        }
    }


    void ScanAndCalculateWeights()
    {
        weightedAssets.Clear();
        totalSizeBytes = 0;

        string scenePath = UnityEditor.SceneManagement.EditorSceneManager.GetActiveScene().path;

        if (string.IsNullOrEmpty(scenePath))
        {
            Debug.LogError("☆ Error: Current scene is not saved! Please save the scene first. ☆");
            return;
        }

        string[] dependencies = AssetDatabase.GetDependencies(scenePath, true);
        var uniquePaths = dependencies
            .Where(p => p.StartsWith("Assets/") && !p.EndsWith(".cs") && !p.EndsWith(".asset"))
            .Distinct()
            .ToList();

        foreach (string path in uniquePaths)
        {
            // Note: Application.dataPath points to the Assets folder in the project.
            string fullPath = Path.Combine(Application.dataPath, path.Substring("Assets/".Length));

            if (!System.IO.File.Exists(fullPath)) continue;

            System.IO.FileInfo info = new System.IO.FileInfo(fullPath);
            long sizeBytes = info.Length;
            totalSizeBytes += sizeBytes; // Accumulate total raw size

            // Simple creator suggestion based on the first folder name
            string creatorSuggestion = path.Split('/').Length > 2 ? path.Split('/')[1] : "N/A";

            weightedAssets.Add(new AssetWeight
            {
                Path = path,
                SizeBytes = sizeBytes,
                Creator = creatorSuggestion
            });
        }

        // Always sort by the default criteria (Size, Descending) after scanning
        currentSort = SortBy.Size;
        sortDescending = true;
        SortAssets();

        Debug.Log($"☆ Zapper Scan Complete! Total weight of {weightedAssets.Count} assets: {(totalSizeBytes / (1024f * 1024f)):F2} MB. ☆");
    }
}
#endif
