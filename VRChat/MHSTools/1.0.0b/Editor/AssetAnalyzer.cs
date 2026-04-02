/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# Editor Script (Unity)
☆ File Name: AssetAnalyzer.cs
☆ Date: 2026-04-01
☆
☆ Description: Merged utility for Listing, Scaling, and Zapping. 
☆              Analyzes scene dependencies for weight and origin.
☆
*/

#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using System.IO;
using System.Linq;

public class AssetAnalyzer : EditorWindow
{
    private struct AssetInfo {
        public string Path;
        public string Creator;
        public long RawSize;
        public long BuildSize;
        public bool IsTexture;
        public string SizeMB => (RawSize / (1024f * 1024f)).ToString("F2") + " MB";
    }

    private List<AssetInfo> assets = new List<AssetInfo>();
    private Vector2 scrollPos;
    private string status = "Ready to scan.";

    public static void ShowWindow() => GetWindow<AssetAnalyzer>("Asset Analyzer");

    private void OnGUI() {
        EditorGUILayout.LabelField("Asset Analyzer (Finder + Weight + Scale)", EditorStyles.boldLabel);
        
        if (GUILayout.Button("Scan Scene Dependencies", GUILayout.Height(30))) {
            RunAnalysis();
        }

        if (assets.Count > 0) {
            EditorGUILayout.Space();
            scrollPos = EditorGUILayout.BeginScrollView(scrollPos);
            
            EditorGUILayout.BeginHorizontal(EditorStyles.toolbar);
            EditorGUILayout.LabelField("Size", GUILayout.Width(70));
            EditorGUILayout.LabelField("Creator", GUILayout.Width(120));
            EditorGUILayout.LabelField("Path");
            EditorGUILayout.EndHorizontal();

            foreach (var a in assets) {
                EditorGUILayout.BeginHorizontal();
                EditorGUILayout.LabelField(a.SizeMB, GUILayout.Width(70));
                EditorGUILayout.LabelField(a.Creator, GUILayout.Width(120));
                EditorGUILayout.LabelField(a.Path);
                EditorGUILayout.EndHorizontal();
            }
            EditorGUILayout.EndScrollView();
        } else {
            EditorGUILayout.HelpBox(status, MessageType.Info);
        }
    }

    private void RunAnalysis() {
        assets.Clear();
        string scenePath = UnityEditor.SceneManagement.EditorSceneManager.GetActiveScene().path;
        if (string.IsNullOrEmpty(scenePath)) return;

        string[] deps = AssetDatabase.GetDependencies(scenePath, true);
        foreach (var path in deps.Where(p => p.StartsWith("Assets/") && !p.EndsWith(".cs")).Distinct()) {
            FileInfo info = new FileInfo(Path.Combine(Application.dataPath, path.Substring(7)));
            if (!info.Exists) continue;

            assets.Add(new AssetInfo {
                Path = path,
                RawSize = info.Length,
                Creator = GetCreator(path)
            });
        }
        assets = assets.OrderByDescending(a => a.RawSize).ToList();
        status = $"Scan complete. Found {assets.Count} assets.";
    }

    private string GetCreator(string path) {
        string[] parts = path.Split('/');
        return parts.Length > 2 ? parts[1] : "Generic";
    }
}
#endif
