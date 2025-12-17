/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# Editor Script (Unity)
☆ File Name: ProjectMaid.cs
☆ Version: v1.1.0a
☆ Date: 2025-12-17 (Updated)
☆ Description: Editor tool (Maid!) to scan the entire project for unreferenced assets
☆              (excluding scenes and prefabs) and move them to a desktop backup folder.
☆              Includes strict, two-step confirmation to prevent accidental data loss.
☆
*/

#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System;

public class ProjectMaid : EditorWindow
{
    private int totalAssetCount = 0;
    private int referencedAssetCount = 0;
    private int unreferencedAssetCount = 0;
    private long unreferencedTotalSizeBytes = 0;
    private string scanStatus = "No scan performed. Press Scan to analyze.";
    private bool scanComplete = false;

    // Display formatted size (MB)
    private string UnreferencedSizeMB => (unreferencedTotalSizeBytes / (1024f * 1024f)).ToString("F2") + " MB";

    // Called by the LibraryHub.cs
    public static void ShowWindow()
    {
        GetWindow<ProjectMaid>("Maid! Project Cleaner");
    }

    void OnGUI()
    {
        EditorGUILayout.LabelField("Maid! Project Cleaner (DESTRUCTIVE)", EditorStyles.boldLabel);
        EditorGUILayout.Space();

        GUI.color = Color.yellow;
        if (GUILayout.Button("1. Scan Project for Unreferenced Assets"))
        {
            ScanProjectAssets();
        }
        GUI.color = Color.white;

        EditorGUILayout.Space();

        // --- Scan Results ---
        EditorGUILayout.LabelField("Scan Results:", EditorStyles.miniLabel);

        if (scanComplete)
        {
            EditorGUILayout.HelpBox(
                $"Total Assets in Project: {totalAssetCount}\n" +
                $"Referenced Assets: {referencedAssetCount}\n" +
                $"Unreferenced Assets to Clean: {unreferencedAssetCount}\n" +
                $"Total Unreferenced Weight: {UnreferencedSizeMB}",
                MessageType.Warning
            );

            EditorGUILayout.Space();

            // --- CLEAN UP BUTTON (Enabled only after scan) ---
            GUI.enabled = unreferencedAssetCount > 0;
            GUI.color = Color.red;
            if (GUILayout.Button("2. CLEAN UP PROJECT (Move Unreferenced Assets to Desktop)"))
            {
                AttemptCleanup();
            }
            GUI.color = Color.white;
            GUI.enabled = true;
        }
        else
        {
            EditorGUILayout.HelpBox(scanStatus, MessageType.Info);
        }

        EditorGUILayout.Space();

        EditorGUILayout.LabelField("WARNING: This tool is destructive. It moves files permanently from the project. Always back up your project before use.", EditorStyles.miniLabel);
    }

    // --- Core Scanning Logic ---
    void ScanProjectAssets()
    {
        scanComplete = false;
        totalAssetCount = 0;
        referencedAssetCount = 0;
        unreferencedAssetCount = 0;
        unreferencedTotalSizeBytes = 0;
        scanStatus = "Scanning project dependencies...";

        // 1. Find all scenes and prefabs in the project to check dependencies
        string[] allSceneGuids = AssetDatabase.FindAssets("t:Scene");
        string[] allPrefabGuids = AssetDatabase.FindAssets("t:Prefab");

        // 2. Collect all referenced paths (dependencies)
        var referencedPaths = new HashSet<string>();

        foreach (string guid in allSceneGuids.Concat(allPrefabGuids))
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);

            // GetDependencies finds everything referenced by the asset at 'path'
            string[] dependencies = AssetDatabase.GetDependencies(path, true);
            foreach (var dep in dependencies)
            {
                referencedPaths.Add(dep);
            }
            // The scene/prefab itself is also considered referenced
            referencedPaths.Add(path);
        }

        referencedAssetCount = referencedPaths.Count;

        // 3. Find ALL assets in the Assets folder (excluding scripts and meta files)
        string[] allAssetGuids = AssetDatabase.FindAssets(""); // Finds all assets
        List<string> projectAssetPaths = new List<string>();

        foreach (string guid in allAssetGuids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            // Ignore scripts (.cs), meta files, and .unity scene files (handled as dependencies above)
            if (path.StartsWith("Assets/") && !path.EndsWith(".cs") && !path.EndsWith(".meta") && !path.EndsWith(".unity"))
            {
                projectAssetPaths.Add(path);
            }
        }
        totalAssetCount = projectAssetPaths.Count;

        // 4. Determine Unreferenced Assets
        List<string> unreferencedPaths = new List<string>();
        foreach (string path in projectAssetPaths)
        {
            // If an asset path is NOT found in our referenced set, it's unreferenced.
            if (!referencedPaths.Contains(path))
            {
                unreferencedPaths.Add(path);

                // Calculate size of the unreferenced file
                string fullPath = Path.Combine(Application.dataPath, path.Substring("Assets/".Length));
                if (File.Exists(fullPath))
                {
                    System.IO.FileInfo info = new System.IO.FileInfo(fullPath);
                    unreferencedTotalSizeBytes += info.Length;
                }
            }
        }

        unreferencedAssetCount = unreferencedPaths.Count;
        scanStatus = $"Scan completed. Found {unreferencedAssetCount} unreferenced assets.";
        scanComplete = true;

        Debug.Log($"☆ Maid! Scan Complete. Found {unreferencedAssetCount} unreferenced assets, total size: {UnreferencedSizeMB}. ☆");

        // Store the list for the cleanup step
        EditorPrefs.SetString("Maid_UnreferencedPaths", string.Join(";", unreferencedPaths));
    }

    // --- Confirmation and Cleanup Logic ---

    void AttemptCleanup()
    {
        string pathsString = EditorPrefs.GetString("Maid_UnreferencedPaths", "");
        if (string.IsNullOrEmpty(pathsString))
        {
            Debug.LogError("Maid! Error: No unreferenced assets found in the last scan. Please scan again.");
            return;
        }

        // --- CONFIRMATION 1: Yes/No Dialog ---
        bool confirmed = EditorUtility.DisplayDialog(
            "MAID! FINAL WARNING: DESTRUCTIVE ACTION",
            $"This will move {unreferencedAssetCount} assets ({UnreferencedSizeMB}) to your Desktop. This CANNOT be undone by Unity.\n\n" +
            "Are you absolutely certain you want to proceed?",
            "Yes, I understand the risk",
            "Cancel Cleanup"
        );

        if (!confirmed) return;

        // --- CONFIRMATION 2: Second Warning Dialog (Equivalent of typing 'CLEAN') ---
        bool secondConfirmed = EditorUtility.DisplayDialog(
            "MAID! SECOND CONFIRMATION (Equivalent of typing 'CLEAN')",
            "You have confirmed the cleanup. This action is irreversible within Unity. \n\nClick 'PROCEED' to permanently move the assets to your Desktop.",
            "PROCEED",
            "Cancel"
        );

        if (!secondConfirmed)
        {
            Debug.LogWarning("Maid! Cleanup cancelled by user (second confirmation skipped).");
            return;
        }

        // Re-get paths string after the simulated double confirmation
        pathsString = EditorPrefs.GetString("Maid_UnreferencedPaths", "");
        if (string.IsNullOrEmpty(pathsString)) return; // Safety check

        // EXECUTE CLEANUP
        ExecuteCleanup(pathsString.Split(';').ToList());
    }


    void ExecuteCleanup(List<string> unreferencedPaths)
    {
        if (unreferencedPaths == null || unreferencedPaths.Count == 0) return;

        // Create the backup folder path on the desktop
        string desktopPath = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
        string projectName = Path.GetFileNameWithoutExtension(Application.dataPath);
        string folderName = $"{projectName}_RemovedAssets_{DateTime.Now:yyyyMMdd_HHmmss}";
        string backupPath = Path.Combine(desktopPath, folderName);

        Directory.CreateDirectory(backupPath);

        int movedCount = 0;

        // Disable refresh during the file moving process for better performance
        AssetDatabase.StartAssetEditing();

        foreach (string projectRelativePath in unreferencedPaths)
        {
            // Convert "Assets/..." path to absolute project path
            string projectFullPath = Path.GetFullPath(projectRelativePath);

            // Find the file name
            string fileName = Path.GetFileName(projectRelativePath);
            string destinationPath = Path.Combine(backupPath, fileName);

            try
            {
                // Attempt to move the main asset file
                if (File.Exists(projectFullPath))
                {
                    File.Move(projectFullPath, destinationPath);
                    movedCount++;
                }

                // Also attempt to move the associated .meta file
                string metaProjectFullPath = projectFullPath + ".meta";
                string metaDestinationPath = destinationPath + ".meta";

                if (File.Exists(metaProjectFullPath))
                {
                    File.Move(metaProjectFullPath, metaDestinationPath);
                }
            }
            catch (Exception e)
            {
                Debug.LogError($"Maid! Error moving asset {projectRelativePath}: {e.Message}");
            }
        }

        // Re-enable refresh and let Unity see the changes
        AssetDatabase.StopAssetEditing();
        AssetDatabase.Refresh();

        EditorUtility.DisplayDialog("Maid! Cleanup Complete",
            $"Successfully moved {movedCount} asset(s) to the backup folder:\n\n{backupPath}\n\n" +
            "Please delete this folder manually if you are satisfied with the cleanup.",
            "OK");

        // Reset state
        scanComplete = false;
        scanStatus = "Cleanup complete. Rescan required.";
        unreferencedAssetCount = 0;

        Debug.Log($"☆ Maid! Cleanup SUCCESS. Moved {movedCount} assets to {backupPath}. ☆");
    }
}
#endif