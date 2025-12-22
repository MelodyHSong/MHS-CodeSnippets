/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# Editor Script (Unity)
☆ File Name: AssetScaler.cs
☆ Version: v1.1.1a
☆ Date: 2025-12-16 (Revised with Top 20 List)
☆ Description: Editor tool (Scale!) to scan the scene and calculate the total 
☆              estimated upload size, now listing the top 20 largest assets 
☆              (10 Textures, 10 General) with optimization suggestions.
☆
*/

#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using System.Linq;
using System.IO;

public class AssetScaler : EditorWindow
{
    // Define the structure to hold asset data and its calculated size
    private struct AssetWeight
    {
        public string Path;
        public long SizeBytes; // Use the most relevant size (Memory for textures, Raw for others)
        public string SizeMB => (SizeBytes / (1024f * 1024f)).ToString("F2") + " MB";
        public bool IsTexture;
    }

    private List<AssetWeight> topTenTextures = new List<AssetWeight>();
    private List<AssetWeight> topTenGeneral = new List<AssetWeight>();

    private Vector2 scrollPosTextures;
    private Vector2 scrollPosGeneral;

    private long totalRawSizeBytes = 0;
    private long estimatedTextureMemoryBytes = 0;
    private int assetCount = 0;
    private int textureCount = 0;
    private string scanStatus = "No scan performed.";

    // Display formatted size (MB) for the UI
    private string TotalRawSizeMB => (totalRawSizeBytes / (1024f * 1024f)).ToString("F2") + " MB";
    private string EstimatedTextureMemoryMB => (estimatedTextureMemoryBytes / (1024f * 1024f)).ToString("F2") + " MB";

    public static void ShowWindow()
    {
        GetWindow<AssetScaler>("Scale! Upload Size");
    }

    void OnGUI()
    {
        EditorGUILayout.LabelField("Scale! Upload Size Estimator (Revised)", EditorStyles.boldLabel);
        EditorGUILayout.Space();

        if (GUILayout.Button("Estimate Scene Build Weight (Scan and List Top 20)"))
        {
            ScanAndCalculateTotalWeight();
        }

        EditorGUILayout.Space();

        if (assetCount > 0)
        {
            DrawWeightAnalysis();
            DrawTopAssetList();
        }
        else
        {
            EditorGUILayout.HelpBox(scanStatus, MessageType.None);
        }

        EditorGUILayout.Space();

        EditorGUILayout.LabelField("Note: The actual VRChat upload size (network transfer size) is often smaller due to final archive compression, but this estimate helps target optimization.", EditorStyles.miniLabel);
    }

    private void DrawWeightAnalysis()
    {
        EditorGUILayout.LabelField("Weight Analysis Results:", EditorStyles.boldLabel);

        // Estimated Build Size (The key metric)
        EditorGUILayout.HelpBox(
            $"Estimated Texture Memory Footprint (Build Impact):\n" +
            $"  {EstimatedTextureMemoryMB}\n\n" +
            $"Texture assets are the largest build contributors. This size reflects Unity's imported/compressed texture data.",
            MessageType.Warning
        );

        // Raw Disk Size (For comparison/Debugging)
        EditorGUILayout.HelpBox(
            $"Total Raw Disk File Size (Source Files):\n" +
            $"  {TotalRawSizeMB}",
            MessageType.Info
        );

        EditorGUILayout.LabelField($"Total Assets Scanned: {assetCount} (Textures: {textureCount})", EditorStyles.miniLabel);
        EditorGUILayout.Space();
    }

    private void DrawTopAssetList()
    {
        EditorGUILayout.LabelField("Top 20 Largest Assets (Size descending):", EditorStyles.boldLabel);

        // --- TOP 10 TEXTURES ---
        DrawAssetSection("Top 10 Textures (Memory Size)", topTenTextures, ref scrollPosTextures,
            "Optimization Suggestion: Use the Shrinker! tool to batch-set Max Texture Size (e.g., 2048 or 1024). Ensure texture format is DXT1 or DXT5, not ARGB32.");

        // --- TOP 10 GENERAL ASSETS ---
        DrawAssetSection("Top 10 General Assets (Raw File Size)", topTenGeneral, ref scrollPosGeneral,
            "Optimization Suggestion: Check models for excessive vertex/triangle counts (Reduce polygon count). Ensure audio files are compressed (e.g., Vorbis) and use the right load settings.");
    }

    private void DrawAssetSection(string title, List<AssetWeight> assets, ref Vector2 scrollPos, string suggestion)
    {
        EditorGUILayout.BeginVertical(EditorStyles.helpBox);
        EditorGUILayout.LabelField(title, EditorStyles.boldLabel);

        // Header
        EditorGUILayout.BeginHorizontal(EditorStyles.toolbar);
        EditorGUILayout.LabelField("Size", EditorStyles.boldLabel, GUILayout.Width(90));
        EditorGUILayout.LabelField("Path", EditorStyles.boldLabel);
        EditorGUILayout.EndHorizontal();

        // List Body
        scrollPos = EditorGUILayout.BeginScrollView(scrollPos, GUILayout.Height(150));
        foreach (var asset in assets)
        {
            EditorGUILayout.BeginHorizontal();
            EditorGUILayout.SelectableLabel(asset.SizeMB, GUILayout.Width(90), GUILayout.Height(15));
            EditorGUILayout.SelectableLabel(asset.Path, GUILayout.Height(15));
            EditorGUILayout.EndHorizontal();
        }
        EditorGUILayout.EndScrollView();

        // Suggestion
        EditorGUILayout.HelpBox(suggestion, MessageType.None);

        EditorGUILayout.EndVertical();
        EditorGUILayout.Space();
    }


    void ScanAndCalculateTotalWeight()
    {
        totalRawSizeBytes = 0;
        estimatedTextureMemoryBytes = 0;
        assetCount = 0;
        textureCount = 0;
        topTenTextures.Clear();
        topTenGeneral.Clear();
        scanStatus = "Scanning...";

        string scenePath = UnityEditor.SceneManagement.EditorSceneManager.GetActiveScene().path;

        if (string.IsNullOrEmpty(scenePath))
        {
            Debug.LogError("☆ Error: Current scene is not saved! Please save the scene first. ☆");
            scanStatus = "Error: Current scene is not saved!";
            return;
        }

        string[] dependencies = AssetDatabase.GetDependencies(scenePath, true);

        var textureExtensions = new HashSet<string>(
            new string[] { ".png", ".jpg", ".jpeg", ".tga", ".bmp", ".dds" },
            System.StringComparer.OrdinalIgnoreCase
        );

        // This list will hold ALL relevant assets to be sorted later
        var allAssetWeights = new List<AssetWeight>();

        var uniquePaths = dependencies
            .Where(p => p.StartsWith("Assets/") && !p.EndsWith(".cs") && !p.EndsWith(".meta"))
            .Distinct()
            .ToList();

        foreach (string path in uniquePaths)
        {
            assetCount++;
            string fullPath = Path.Combine(Application.dataPath, path.Substring("Assets/".Length));

            if (!System.IO.File.Exists(fullPath)) continue;

            System.IO.FileInfo info = new System.IO.FileInfo(fullPath);
            long rawSizeBytes = info.Length;
            totalRawSizeBytes += rawSizeBytes;

            bool isTexture = textureExtensions.Contains(System.IO.Path.GetExtension(path));
            long finalSizeBytes = rawSizeBytes; // Default to raw size

            if (isTexture)
            {
                textureCount++;
                TextureImporter importer = AssetImporter.GetAtPath(path) as TextureImporter;

                if (importer != null)
                {
                    long estimatedSize = CalculateTextureMemorySize(importer, path);
                    estimatedTextureMemoryBytes += estimatedSize;
                    finalSizeBytes = estimatedSize; // Use estimated memory size for sorting textures
                }
            }

            allAssetWeights.Add(new AssetWeight
            {
                Path = path,
                SizeBytes = finalSizeBytes,
                IsTexture = isTexture
            });
        }

        // --- SORTING AND TOP 10 SELECTION ---

        // 1. Sort Textures by their estimated memory size (descending)
        topTenTextures = allAssetWeights
            .Where(a => a.IsTexture)
            .OrderByDescending(a => a.SizeBytes)
            .Take(10)
            .ToList();

        // 2. Sort General Assets by their raw file size (descending)
        topTenGeneral = allAssetWeights
            .Where(a => !a.IsTexture)
            .OrderByDescending(a => a.SizeBytes)
            .Take(10)
            .ToList();

        scanStatus = $"Scan Complete! Found {assetCount} unique assets.";

        Debug.Log($"☆ Scale! Scan Complete! Estimated Texture Memory: {EstimatedTextureMemoryMB}. Raw Disk Size: {TotalRawSizeMB}. ☆");
    }

    // This function remains the same as the previous fixed version.
    private long CalculateTextureMemorySize(TextureImporter importer, string assetPath)
    {
        Texture texture = AssetDatabase.LoadAssetAtPath<Texture>(assetPath);
        if (texture == null) return 0;

        int width = texture.width;
        int height = texture.height;

        int maxDim = Mathf.Max(width, height);
        if (maxDim > importer.maxTextureSize)
        {
            float ratio = (float)importer.maxTextureSize / maxDim;
            width = Mathf.RoundToInt(width * ratio);
            height = Mathf.RoundToInt(height * ratio);
            width = Mathf.NextPowerOfTwo(width);
            height = Mathf.NextPowerOfTwo(height);
        }

        // Use GetPlatformTextureSettings, passing an empty string ("") to get the default/Standalone platform settings.
        TextureImporterPlatformSettings platformSettings = importer.GetPlatformTextureSettings("");

        float bpp = 1.0f; // Defaulting to 1 BPP (like DXT5)

        switch (platformSettings.format)
        {
            case TextureImporterFormat.DXT1:
            case TextureImporterFormat.ETC_RGB4:
            case TextureImporterFormat.ETC2_RGB4:
                bpp = 0.5f; // 4 bits per pixel
                break;
            case TextureImporterFormat.DXT5:
            case TextureImporterFormat.ETC2_RGBA8:
                bpp = 1.0f; // 8 bits per pixel
                break;
            case TextureImporterFormat.ARGB32:
            case TextureImporterFormat.RGBA32:
                bpp = 4.0f; // 32 bits per pixel
                break;
            default:
                bpp = 1.0f;
                break;
        }

        long estimatedSize = (long)(width * height * bpp);

        return estimatedSize;
    }
}
#endif
