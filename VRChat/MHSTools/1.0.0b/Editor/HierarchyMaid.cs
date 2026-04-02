/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# Editor Script (Unity)
☆ File Name: HierarchyMaid.cs
☆ Date: 2026-04-01
☆
☆ Description: Automatically organizes the hierarchy into categories. 
☆              Protects Udon toggle targets and keeps Prefabs intact.
☆
*/

#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using VRC.Udon;

public class HierarchyMaid : EditorWindow
{
    [MenuItem("☆ Melody Tools ☆/Hierarchy Maid (Auto-Sort)")]
    public static void ShowWindow() => GetWindow<HierarchyMaid>("Hierarchy Maid");

    private void OnGUI()
    {
        EditorGUILayout.LabelField("Hierarchy Organizer", EditorStyles.boldLabel);
        EditorGUILayout.HelpBox("Select a 'Room' or 'Root' object in the hierarchy to sort its contents. Prefabs and Udon Toggles will be protected.", MessageType.Info);

        if (GUILayout.Button("Sort Selected Hierarchy", GUILayout.Height(30)))
        {
            ExecuteSort();
        }
    }

    private void ExecuteSort()
    {
        if (Selection.activeGameObject == null)
        {
            Debug.LogWarning("☆ Please select a parent object to sort! ☆");
            return;
        }

        HashSet<GameObject> protectedObjects = FindUdonTargets();
        
        foreach (GameObject root in Selection.gameObjects)
        {
            Undo.RegisterFullObjectHierarchyUndo(root, "Maid Sort");
            SortRecursively(root.transform, protectedObjects);
        }
        
        Debug.Log("☆ Hierarchy Maid: Sorting complete! ☆");
    }

    private void SortRecursively(Transform currentRoot, HashSet<GameObject> protectedTargets)
    {
        List<Transform> children = new List<Transform>();
        foreach (Transform t in currentRoot) children.Add(t);

        foreach (Transform child in children)
        {
            if (child.name.StartsWith("---")) continue;

            // ☆ Rule 1: If it's a toggle target, leave it and sort its insides instead.
            if (protectedTargets.Contains(child.gameObject))
            {
                SortRecursively(child, protectedTargets);
                continue;
            }

            // ☆ Rule 2: If it's a Prefab, move it but do NOT open/sort it.
            bool isPrefab = PrefabUtility.IsPartOfAnyPrefab(child.gameObject);
            
            string category = GetCategory(child.gameObject);
            Transform folder = GetOrCreateFolder(currentRoot, category);
            child.SetParent(folder);

            // ☆ Rule 3: If it's NOT a prefab, dive deeper to sort its children.
            if (!isPrefab)
            {
                SortRecursively(child, protectedTargets);
            }
        }
    }

    private string GetCategory(GameObject go)
    {
        if (go.GetComponent<Light>() || go.GetComponent<ReflectionProbe>()) return "--- LIGHTS ---";
        if (go.GetComponent<UdonBehaviour>()) return "--- LOGIC ---";
        if (go.GetComponent<MeshRenderer>()) return "--- MESHES ---";
        if (go.GetComponent<Collider>() && !go.GetComponent<MeshRenderer>()) return "--- COLLIDERS ---";
        return "--- PROPS ---";
    }

    private Transform GetOrCreateFolder(Transform parent, string name)
    {
        Transform f = parent.Find(name);
        if (!f)
        {
            f = new GameObject(name).transform;
            f.SetParent(parent);
            f.localPosition = Vector3.zero;
            f.localRotation = Quaternion.identity;
        }
        return f;
    }

    private HashSet<GameObject> FindUdonTargets()
    {
        HashSet<GameObject> targets = new HashSet<GameObject>();
        UdonBehaviour[] udons = FindObjectsOfType<UdonBehaviour>();
        foreach (var udon in udons)
        {
            string[] symbols = udon.GetProgramVariableSymbolTable();
            foreach (var sym in symbols)
            {
                var val = udon.GetProgramVariable(sym);
                if (val is GameObject go) targets.Add(go);
                if (val is Transform t) targets.Add(t.gameObject);
            }
        }
        return targets;
    }
}
#endif
