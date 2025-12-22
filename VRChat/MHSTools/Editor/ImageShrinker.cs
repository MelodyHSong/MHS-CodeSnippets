/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# Editor Script (Unity)
☆ File Name: ImageShrinker.cs
☆ Version: v1.1.1a
☆ Date: 2025-12-21 (Updated)
☆ Description: Editor tool (Shrinker!) for comprehensive asset optimization: 
☆              batch-setting Max Texture Size (Scale Up/Down), batch-setting optimized formats,
☆              and includes a SHADER COMPATIBILITY CHECKER with warnings for 
☆              problematic shaders (like Poiyomi on Android).
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
    // --- Data Structures ---
    private struct TextureData
    {
        public string Path;
        public long SizeBytes;
        public string SizeMB => (SizeBytes / (1024f * 1024f)).ToString("F2") + " MB";
        public bool IsSelected; // Used for Size optimization
        public bool IsUnoptimizedFormat;
        public TextureImporterFormat CurrentFormat;
    }

    private struct MaterialData
    {
        public string Path;
        public string ShaderName;
        public bool IsUnsupportedStandard; // For shaders we can batch-fix (Legacy, etc.)
        public bool IsPoiyomi;             // For Poiyomi shaders (Manual fix only)
        public bool IsSelected;            // Used for Standard Shader batch optimization
    }

    // --- State Variables ---
    private List<TextureData> textureDataList = new List<TextureData>();
    private List<MaterialData> materialDataList = new List<MaterialData>();

    private Vector2 scrollPosWeight;
    private Vector2 scrollPosFormat;
    private Vector2 scrollPosShaders;
    private Vector2 scrollPosPoiyomi;

    private bool selectAllWeight = true;
    private bool selectAllFormat = true;
    private bool selectAllShaders = true;

    // ☆ Toggle to allow resizing smaller images to larger resolutions ☆
    private bool allowUpscaling = false;

    // Keywords that generally indicate a deprecated, unsupported, or problematic standard shader
    private static readonly string[] UNSUPPORTED_KEYWORDS = {
        "Legacy", "Autodesk", "Hidden", "Standard (Specular setup)", "Standard (Metallic setup)", "Mobile"
    };

    // Available optimization sizes
    private readonly int[] SIZE_OPTIONS = { 2048, 1024, 512, 256, 128 };
    private int selectedSizeIndex = 1;

    // Available optimization formats
    private readonly TextureImporterFormat[] FORMAT_OPTIONS = {
        TextureImporterFormat.DXT5,
        TextureImporterFormat.DXT1,
        TextureImporterFormat.Automatic
    };
    private readonly string[] FORMAT_NAMES = {
        "DXT5 (Compressed, Alpha)",
        "DXT1 (Compressed, No Alpha)",
        "Automatic (Platform Default)"
    };
    private int selectedFormatIndex = 0;

    // Shader replacement options
    private readonly string STANDARD_SHADER_NAME = "Standard";

    // A reusable centered label style 
    private GUIStyle centeredLabelStyle;

    // Called by the LibraryHub.cs
    public static void ShowWindow()
    {
        GetWindow<ImageShrinker>("Shrinker! Asset Optimizer");
    }

    void OnEnable()
    {
        // Initialize the safe centered style when the window is enabled
        centeredLabelStyle = new GUIStyle(EditorStyles.boldLabel)
        {
            alignment = TextAnchor.MiddleCenter,
            stretchWidth = true
        };
    }

    void OnGUI()
    {
        EditorGUILayout.LabelField("Shrinker! Asset Optimization Utility", EditorStyles.boldLabel);
        EditorGUILayout.Space();

        if (GUILayout.Button("Find All Assets in Scene (Scan Weight, Format, and Shaders)"))
        {
            FindSceneAssets();
        }

        EditorGUILayout.Space();

        if (textureDataList.Count > 0 || materialDataList.Count > 0)
        {
            // --- Section 1: Max Size Optimizer ---
            DrawSizeOptimizerSection();

            EditorGUILayout.Space();
            EditorGUILayout.Space();

            // --- Section 2: Format Optimizer ---
            DrawFormatOptimizerSection();

            EditorGUILayout.Space();
            EditorGUILayout.Space();

            // --- Section 3: Shader Compatibility Checker ---
            DrawShaderCheckerSection();
        }
    }

    // --- GUI Methods ---

    void DrawSizeOptimizerSection()
    {
        int selectedCount = textureDataList.Count(t => t.IsSelected);

        EditorGUILayout.LabelField("1. Max Texture Size Optimization", centeredLabelStyle);

        EditorGUILayout.BeginVertical(EditorStyles.helpBox);

        EditorGUILayout.BeginHorizontal();
        // Dropdown to select the target size
        selectedSizeIndex = EditorGUILayout.Popup("Target Max Size:", selectedSizeIndex, SIZE_OPTIONS.Select(s => s.ToString()).ToArray(), GUILayout.Width(200));

        // Toggle for upscaling logic
        allowUpscaling = EditorGUILayout.ToggleLeft("Allow Upscaling (Force to Target)", allowUpscaling);
        EditorGUILayout.EndHorizontal();

        // Apply Button
        GUI.enabled = selectedCount > 0;
        string btnLabel = allowUpscaling ? $"Scale to {SIZE_OPTIONS[selectedSizeIndex]}" : $"Shrink to {SIZE_OPTIONS[selectedSizeIndex]}";
        if (GUILayout.Button($"{btnLabel} Max Size for {selectedCount} Selected Textures", GUILayout.Height(30)))
        {
            ApplyMaxSize(SIZE_OPTIONS[selectedSizeIndex]);
        }
        GUI.enabled = true;

        EditorGUILayout.EndVertical();
        EditorGUILayout.Space();

        // Asset List Display Header
        EditorGUILayout.BeginHorizontal(EditorStyles.toolbar);

        // Select All Toggle Header
        bool newSelectAll = EditorGUILayout.Toggle(selectAllWeight, GUILayout.Width(20));
        if (newSelectAll != selectAllWeight)
        {
            selectAllWeight = newSelectAll;
            for (int i = 0; i < textureDataList.Count; i++)
            {
                var data = textureDataList[i];
                data.IsSelected = selectAllWeight;
                textureDataList[i] = data;
            }
        }
        EditorGUILayout.LabelField("Weight (MB)", EditorStyles.boldLabel, GUILayout.Width(90));
        EditorGUILayout.LabelField("Texture Path", EditorStyles.boldLabel);
        EditorGUILayout.EndHorizontal();

        // Asset List Display Body (Sorted by Size)
        scrollPosWeight = EditorGUILayout.BeginScrollView(scrollPosWeight, GUILayout.MinHeight(150), GUILayout.MaxHeight(300));

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
                if (!newSelection) selectAllWeight = false;
            }

            // Weight Display
            EditorGUILayout.SelectableLabel(textureData.SizeMB, GUILayout.Width(90), GUILayout.Height(15));

            // Path Display
            EditorGUILayout.SelectableLabel(textureData.Path, GUILayout.Height(15));

            EditorGUILayout.EndHorizontal();
        }

        EditorGUILayout.EndScrollView();
    }

    void DrawFormatOptimizerSection()
    {
        var unoptimizedTextures = textureDataList.Where(t => t.IsUnoptimizedFormat).ToList();
        int selectedUnoptimizedCount = unoptimizedTextures.Count(t => t.IsSelected);

        EditorGUILayout.LabelField("2. Unoptimized Format Optimizer", centeredLabelStyle);
        EditorGUILayout.HelpBox($"Found {unoptimizedTextures.Count} textures using uncompressed formats (ARGB32/RGBA32). These should be compressed.", MessageType.Warning);

        EditorGUILayout.BeginHorizontal(EditorStyles.helpBox);

        // Dropdown to select the target format
        selectedFormatIndex = EditorGUILayout.Popup("Target Format:", selectedFormatIndex, FORMAT_NAMES, GUILayout.Width(200));
        TextureImporterFormat targetFormat = FORMAT_OPTIONS[selectedFormatIndex];

        // Apply Button
        GUI.enabled = selectedUnoptimizedCount > 0;
        if (GUILayout.Button($"Apply {FORMAT_NAMES[selectedFormatIndex]} to {selectedUnoptimizedCount} Selected Textures", GUILayout.Height(30)))
        {
            ApplyTextureFormat(targetFormat);
        }
        GUI.enabled = true;

        EditorGUILayout.EndHorizontal();
        EditorGUILayout.Space();

        // Asset List Display Header
        EditorGUILayout.BeginHorizontal(EditorStyles.toolbar);

        // Select All Toggle Header
        bool newSelectAll = EditorGUILayout.Toggle(selectAllFormat, GUILayout.Width(20));
        if (newSelectAll != selectAllFormat)
        {
            selectAllFormat = newSelectAll;
            for (int i = 0; i < textureDataList.Count; i++)
            {
                var data = textureDataList[i];
                if (data.IsUnoptimizedFormat)
                {
                    data.IsSelected = selectAllFormat;
                    textureDataList[i] = data;
                }
            }
        }
        EditorGUILayout.LabelField("Current Format", EditorStyles.boldLabel, GUILayout.Width(150));
        EditorGUILayout.LabelField("Texture Path", EditorStyles.boldLabel);
        EditorGUILayout.EndHorizontal();


        // Asset List Display Body (Only Unoptimized Formats)
        scrollPosFormat = EditorGUILayout.BeginScrollView(scrollPosFormat, GUILayout.MinHeight(100), GUILayout.MaxHeight(200));

        for (int i = 0; i < textureDataList.Count; i++)
        {
            var textureData = textureDataList[i];

            if (textureData.IsUnoptimizedFormat)
            {
                EditorGUILayout.BeginHorizontal();

                // Individual Selection Toggle
                bool newSelection = EditorGUILayout.Toggle(textureData.IsSelected, GUILayout.Width(20));
                if (newSelection != textureData.IsSelected)
                {
                    textureData.IsSelected = newSelection;
                    textureDataList[i] = textureData;
                    if (!newSelection) selectAllFormat = false;
                }

                // Format Display
                EditorGUILayout.SelectableLabel(textureData.CurrentFormat.ToString(), GUILayout.Width(150), GUILayout.Height(15));

                // Path Display
                EditorGUILayout.SelectableLabel(textureData.Path, GUILayout.Height(15));

                EditorGUILayout.EndHorizontal();
            }
        }

        EditorGUILayout.EndScrollView();
    }

    void DrawShaderCheckerSection()
    {
        var unsupportedStandardMaterials = materialDataList.Where(m => m.IsUnsupportedStandard).ToList();
        var poiyomiMaterials = materialDataList.Where(m => m.IsPoiyomi).ToList();

        int selectedUnsupportedCount = unsupportedStandardMaterials.Count(m => m.IsSelected);

        EditorGUILayout.LabelField("3. Shader Compatibility Checker", centeredLabelStyle);
        EditorGUILayout.HelpBox($"Found {unsupportedStandardMaterials.Count + poiyomiMaterials.Count} materials using potentially unsupported or deprecated shaders.", MessageType.Error);


        // --- A. POIYOMI SHADER WARNING (MANUAL ONLY) ---
        if (poiyomiMaterials.Any())
        {
            EditorGUILayout.LabelField("☆ Poiyomi Shader Warning (Android/Quest Target)", EditorStyles.boldLabel);
            EditorGUILayout.HelpBox(
                $"Found {poiyomiMaterials.Count} Poiyomi materials. Poiyomi shaders are generally incompatible or problematic on VRChat Quest/Android builds.\n" +
                $"You MUST manually change these materials to a Quest-compatible shader (e.g., VRChat/Mobile/Standard Lite). This tool will NOT batch-fix them due to complexity.",
                MessageType.Warning
            );

            // Header for Poiyomi List
            EditorGUILayout.BeginHorizontal(EditorStyles.toolbar);
            EditorGUILayout.LabelField("Current Shader", EditorStyles.boldLabel, GUILayout.Width(200));
            EditorGUILayout.LabelField("Material Path", EditorStyles.boldLabel);
            EditorGUILayout.EndHorizontal();

            // Poiyomi List Body
            scrollPosPoiyomi = EditorGUILayout.BeginScrollView(scrollPosPoiyomi, GUILayout.MinHeight(50), GUILayout.MaxHeight(150));
            foreach (var materialData in poiyomiMaterials)
            {
                EditorGUILayout.BeginHorizontal();
                EditorGUILayout.SelectableLabel(materialData.ShaderName, GUILayout.Width(200), GUILayout.Height(15));
                EditorGUILayout.SelectableLabel(materialData.Path, GUILayout.Height(15));
                EditorGUILayout.EndHorizontal();
            }
            EditorGUILayout.EndScrollView();
            EditorGUILayout.Space();
        }

        // --- B. STANDARD/LEGACY SHADER BATCH FIX ---
        if (unsupportedStandardMaterials.Any())
        {
            EditorGUILayout.LabelField("Legacy/Unsupported Standard Shader Batch Fix", EditorStyles.boldLabel);

            EditorGUILayout.BeginHorizontal(EditorStyles.helpBox);

            // Display the replacement shader
            EditorGUILayout.LabelField("Target Replacement Shader:", EditorStyles.label, GUILayout.Width(150));
            EditorGUILayout.LabelField(STANDARD_SHADER_NAME, EditorStyles.boldLabel);

            // Apply Button
            GUI.enabled = selectedUnsupportedCount > 0;
            if (GUILayout.Button($"Batch Replace {selectedUnsupportedCount} Selected Shaders with '{STANDARD_SHADER_NAME}'", GUILayout.Height(30)))
            {
                ApplyShaderReplacement(STANDARD_SHADER_NAME);
            }
            GUI.enabled = true;

            EditorGUILayout.EndHorizontal();
            EditorGUILayout.Space();

            // Asset List Display Header (Batch Fix List)
            EditorGUILayout.BeginHorizontal(EditorStyles.toolbar);

            // Select All Toggle Header
            bool newSelectAll = EditorGUILayout.Toggle(selectAllShaders, GUILayout.Width(20));
            if (newSelectAll != selectAllShaders)
            {
                selectAllShaders = newSelectAll;
                for (int i = 0; i < materialDataList.Count; i++)
                {
                    var data = materialDataList[i];
                    if (data.IsUnsupportedStandard)
                    {
                        data.IsSelected = selectAllShaders;
                        materialDataList[i] = data;
                    }
                }
            }
            EditorGUILayout.LabelField("Current Shader", EditorStyles.boldLabel, GUILayout.Width(200));
            EditorGUILayout.LabelField("Material Path", EditorStyles.boldLabel);
            EditorGUILayout.EndHorizontal();


            // Asset List Display Body (Only Unsupported Standard Shaders)
            scrollPosShaders = EditorGUILayout.BeginScrollView(scrollPosShaders, GUILayout.MinHeight(100), GUILayout.MaxHeight(200));

            foreach (var materialData in unsupportedStandardMaterials)
            {
                EditorGUILayout.BeginHorizontal();

                // Individual Selection Toggle
                bool newSelection = EditorGUILayout.Toggle(materialData.IsSelected, GUILayout.Width(20));

                if (newSelection != materialData.IsSelected)
                {
                    int index = materialDataList.FindIndex(m => m.Path == materialData.Path);
                    if (index != -1)
                    {
                        var data = materialDataList[index];
                        data.IsSelected = newSelection;
                        materialDataList[index] = data;
                        if (!newSelection) selectAllShaders = false;
                    }
                }

                // Shader Display
                EditorGUILayout.SelectableLabel(materialData.ShaderName, GUILayout.Width(200), GUILayout.Height(15));

                // Path Display
                EditorGUILayout.SelectableLabel(materialData.Path, GUILayout.Height(15));

                EditorGUILayout.EndHorizontal();
            }

            EditorGUILayout.EndScrollView();
        }
    }

    // --- Logic Methods ---

    void FindSceneAssets()
    {
        textureDataList.Clear();
        materialDataList.Clear();

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
        var materialExtensions = new HashSet<string>(
            new string[] { ".mat" },
            System.StringComparer.OrdinalIgnoreCase
        );

        var texturePaths = dependencies
            .Where(p => p.StartsWith("Assets/") && textureExtensions.Contains(System.IO.Path.GetExtension(p)))
            .Distinct()
            .ToList();

        var materialPaths = dependencies
            .Where(p => p.StartsWith("Assets/") && materialExtensions.Contains(System.IO.Path.GetExtension(p)))
            .Distinct()
            .ToList();


        // 1. Process Textures 
        var tempList = new List<TextureData>();
        foreach (string path in texturePaths)
        {
            string fullPath = Path.Combine(Application.dataPath, path.Substring("Assets/".Length));
            long sizeBytes = 0;
            if (System.IO.File.Exists(fullPath))
            {
                System.IO.FileInfo info = new System.IO.FileInfo(fullPath);
                sizeBytes = info.Length;
            }

            TextureImporter importer = AssetImporter.GetAtPath(path) as TextureImporter;
            TextureImporterFormat currentFormat = TextureImporterFormat.Automatic;
            bool isUnoptimized = false;

            if (importer != null)
            {
                TextureImporterPlatformSettings platformSettings = importer.GetPlatformTextureSettings("");
                currentFormat = platformSettings.format;

                if (currentFormat == TextureImporterFormat.ARGB32 || currentFormat == TextureImporterFormat.RGBA32)
                {
                    isUnoptimized = true;
                }
            }

            tempList.Add(new TextureData
            {
                Path = path,
                SizeBytes = sizeBytes,
                IsSelected = selectAllWeight,
                IsUnoptimizedFormat = isUnoptimized,
                CurrentFormat = currentFormat
            });
        }
        textureDataList = tempList.OrderByDescending(t => t.SizeBytes).ToList();
        selectAllFormat = textureDataList.Any(t => t.IsUnoptimizedFormat);

        // 2. Process Materials 
        var materialTempList = new List<MaterialData>();
        foreach (string path in materialPaths)
        {
            Material material = AssetDatabase.LoadAssetAtPath<Material>(path);
            if (material == null || material.shader == null) continue;

            string shaderName = material.shader.name;
            bool isPoiyomi = shaderName.Contains("Poiyomi");
            bool isUnsupportedStandard = false;

            if (!isPoiyomi)
            {
                isUnsupportedStandard = UNSUPPORTED_KEYWORDS.Any(keyword => shaderName.Contains(keyword));
            }

            materialTempList.Add(new MaterialData
            {
                Path = path,
                ShaderName = shaderName,
                IsUnsupportedStandard = isUnsupportedStandard,
                IsPoiyomi = isPoiyomi,
                IsSelected = isUnsupportedStandard ? selectAllShaders : false
            });
        }
        materialDataList = materialTempList.OrderBy(m => m.ShaderName).ToList();
        selectAllShaders = materialDataList.Any(m => m.IsUnsupportedStandard);

        Debug.Log($"☆ Shrinker Scan Complete! Found {textureDataList.Count} textures, {materialDataList.Count} materials, and {materialDataList.Count(m => m.IsPoiyomi)} Poiyomi shaders. ☆");
    }

    void ApplyMaxSize(int targetSize)
    {
        var selectedTextures = textureDataList.Where(t => t.IsSelected).ToList();

        if (selectedTextures.Count == 0) return;

        string operationName = allowUpscaling ? "Scaling" : "Resizing (Down)";
        if (!EditorUtility.DisplayDialog(
            $"Confirm Texture {operationName}",
            $"Are you sure you want to set the Max Size of {selectedTextures.Count} selected textures to {targetSize}?\n\nThis operation modifies import settings.",
            "Yes, Apply",
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
                TextureImporterPlatformSettings platformSettings = importer.GetPlatformTextureSettings("");

                // ☆ Core Logic: Only scale down normally, or scale freely if allowed ☆
                bool shouldApply = allowUpscaling ? (platformSettings.maxTextureSize != targetSize) : (platformSettings.maxTextureSize > targetSize);

                if (shouldApply)
                {
                    platformSettings.maxTextureSize = targetSize;
                    importer.SetPlatformTextureSettings(platformSettings);
                    importer.SaveAndReimport();
                    appliedCount++;
                }
            }
        }

        EditorUtility.DisplayDialog("Shrinker! Success",
                                    $"Successfully applied {targetSize} Max Size to {appliedCount} textures.\n\n" +
                                    (allowUpscaling ? "Forced all to target size." : "Skipped textures that were already smaller."),
                                    "OK");

        Debug.Log($"☆ Shrinker! Operation Complete. Applied Max Size {targetSize} to {appliedCount} textures. ☆");
        FindSceneAssets();
    }

    void ApplyTextureFormat(TextureImporterFormat targetFormat)
    {
        var selectedTextures = textureDataList.Where(t => t.IsSelected && t.IsUnoptimizedFormat).ToList();

        if (selectedTextures.Count == 0) return;

        if (!EditorUtility.DisplayDialog(
            "Confirm Texture Format Change",
            $"Are you sure you want to change the format of {selectedTextures.Count} selected textures to {targetFormat}?\n\nThis is a major optimization for memory.",
            "Yes, Change Format",
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
                TextureImporterPlatformSettings platformSettings = importer.GetPlatformTextureSettings("");

                if (platformSettings.format != targetFormat)
                {
                    platformSettings.format = targetFormat;
                    importer.SetPlatformTextureSettings(platformSettings);
                    importer.SaveAndReimport();
                    appliedCount++;
                }
            }
        }

        EditorUtility.DisplayDialog("Shrinker! Success",
                                    $"Successfully set Texture Format to {targetFormat} for {appliedCount} textures out of {selectedTextures.Count} selected.\n\n" +
                                    "Note: Ensure textures with transparency use a format that supports it (e.g., DXT5).",
                                    "OK");

        Debug.Log($"☆ Shrinker! Operation Complete. Applied Format {targetFormat} to {appliedCount} textures. ☆");
        FindSceneAssets();
    }

    void ApplyShaderReplacement(string targetShaderName)
    {
        var selectedMaterials = materialDataList.Where(m => m.IsSelected && m.IsUnsupportedStandard).ToList();

        if (selectedMaterials.Count == 0) return;

        if (!EditorUtility.DisplayDialog(
            "Confirm Shader Replacement (RISK)",
            $"WARNING: You are about to replace the shader on {selectedMaterials.Count} material(s) with '{targetShaderName}'.\n\n" +
            "This will destroy material links to custom properties (e.g., textures, colors) that are not present in the target shader. Only proceed if you accept potential visual changes.",
            "Yes, Replace Shaders",
            "Cancel"))
        {
            return;
        }

        Shader targetShader = Shader.Find(targetShaderName);
        if (targetShader == null)
        {
            EditorUtility.DisplayDialog("Error", $"Target shader '{targetShaderName}' could not be found. Aborting.", "OK");
            return;
        }

        int appliedCount = 0;

        foreach (var materialData in selectedMaterials)
        {
            Material material = AssetDatabase.LoadAssetAtPath<Material>(materialData.Path);

            if (material != null && material.shader != targetShader)
            {
                material.shader = targetShader;
                EditorUtility.SetDirty(material);
                AssetDatabase.SaveAssets();
                appliedCount++;
            }
        }

        EditorUtility.DisplayDialog("Shrinker! Success",
                                    $"Successfully replaced shader on {appliedCount} materials with '{targetShaderName}'.\n\n" +
                                    "Please check your scene for any visual errors.",
                                    "OK");

        Debug.Log($"☆ Shrinker! Operation Complete. Applied shader '{targetShaderName}' to {appliedCount} materials. ☆");
        FindSceneAssets();
    }
}
#endif
