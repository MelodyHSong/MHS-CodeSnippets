/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# Udon Sharp
☆ File Name: LobbyControlPanel.cs
☆ Date: 2025-09-29
☆ Ver: 1.4
☆
*/

using UdonSharp;
using UnityEngine;
using UnityEngine.UI;
using VRC.SDKBase;
using VRC.Udon;

public class LobbyControlPanel : UdonSharpBehaviour
{
    // --- Mirror Configuration ---

    [Header("Mirror Configuration (6 GameObjects Total)")]
    // Mirror Location A (e.g., Wall 1)
    [Tooltip("Index 0: HQ Mirror. Index 1: LQ Mirror.")]
    public GameObject[] mirrorsA = new GameObject[2];
    // Mirror Location B (e.g., Standalone)
    [Tooltip("Index 0: HQ Mirror. Index 1: LQ Mirror.")]
    public GameObject[] mirrorsB = new GameObject[2];
    // Mirror Location C (e.g., Wall 2)
    [Tooltip("Index 0: HQ Mirror. Index 1: LQ Mirror.")]
    public GameObject[] mirrorsC = new GameObject[2];

    [Header("Current States")]
    // 0 = Off, 1 = HQ, 2 = LQ
    private int currentQualityIndex = 0; 
    private bool mirrorAIsOn = false;
    private bool mirrorBIsOn = false;
    private bool mirrorCIsOn = false;

    // --- Audio Control Targets ---
    
    [Header("Audio Controls")]
    [Tooltip("The AudioSource component for the Background Music (BGM).")]
    public AudioSource bgmAudioSource;
    
    [Tooltip("The slider UI component for BGM volume.")]
    public Slider bgmVolumeSlider;
    
    // --- NEW GENERIC TOGGLES ---
    
    [Header("☆ Generic Toggles (10x) ☆")]
    [Tooltip("Generic Toggle 01 - Used for general object visibility.")]
    public GameObject genericToggleTarget01;
    [Tooltip("Generic Toggle 02 - Used for general object visibility.")]
    public GameObject genericToggleTarget02;
    [Tooltip("Generic Toggle 03 - Used for general object visibility.")]
    public GameObject genericToggleTarget03;
    [Tooltip("Generic Toggle 04 - Used for general object visibility.")]
    public GameObject genericToggleTarget04;
    [Tooltip("Generic Toggle 05 - Used for general object visibility.")]
    public GameObject genericToggleTarget05;
    [Tooltip("Generic Toggle 06 - Used for general object visibility.")]
    public GameObject genericToggleTarget06;
    [Tooltip("Generic Toggle 07 - Used for general object visibility.")]
    public GameObject genericToggleTarget07;
    [Tooltip("Generic Toggle 08 - Used for general object visibility.")]
    public GameObject genericToggleTarget08;
    [Tooltip("Generic Toggle 09 - Used for general object visibility.")]
    public GameObject genericToggleTarget09;
    [Tooltip("Generic Toggle 10 - Used for general object visibility.")]
    public GameObject genericToggleTarget10;


    // --- Core Functions ---

    void Start()
    {
        // Reset local toggle states to OFF
        mirrorAIsOn = false;
        mirrorBIsOn = false;
        mirrorCIsOn = false;
        
        // SET DEFAULT QUALITY: 1 (HQ)
        currentQualityIndex = 1; 
        
        // Ensure all 6 mirror GameObjects start disabled.
        _SetAllMirrorsInactive();
        
        // Set the initial volume slider value
        if (bgmAudioSource != null && bgmVolumeSlider != null)
        {
            bgmVolumeSlider.value = bgmAudioSource.volume;
        }

        // Check for null generic toggles and throw error if they are missing
        CheckGenericToggleAssignments();
    }
    
    // Helper function to check all 10 generic assignments
    private void CheckGenericToggleAssignments()
    {
        // We use a list to make iterating and reporting errors cleaner
        GameObject[] targets = new GameObject[]
        {
            genericToggleTarget01, genericToggleTarget02, genericToggleTarget03, genericToggleTarget04, genericToggleTarget05,
            genericToggleTarget06, genericToggleTarget07, genericToggleTarget08, genericToggleTarget09, genericToggleTarget10
        };

        for (int i = 0; i < targets.Length; i++)
        {
            if (targets[i] == null)
            {
                // This logs the error if the target is NULL, as requested.
                // Note: The logic handles null gracefully if the button is never clicked,
                // but this error fulfills the requirement to notify the user in the editor.
                Debug.LogError("☆ GENERIC TOGGLE " + (i + 1).ToString("00") + " ☆ is unassigned (NULL)! Please assign a GameObject or remove the button wiring.");
            }
        }
    }
    

    // ☆ DEBUG/TEST FUNCTION (Keep this name for your test button!) ☆
  
    public void RunTest()
    {
        // This function confirms the click event fired successfully.
        Debug.Log("✔✔✔ DEBUG BUTTON FIRED! ✔✔✔");
    }
    
    // --- Individual Mirror Toggle Methods (Called via VRC_Interact) ---

    public void ToggleMirrorA()
    {
        mirrorAIsOn = !mirrorAIsOn;
        _UpdateMirrorStates();
    }
    
    public void ToggleMirrorB()
    {
        mirrorBIsOn = !mirrorBIsOn;
        _UpdateMirrorStates();
    }
    
    public void ToggleMirrorC()
    {
        mirrorCIsOn = !mirrorCIsOn;
        _UpdateMirrorStates();
    }
    
    // --- NEW GENERIC TOGGLE METHODS (Called via VRC_Interact) ---

    // Note: These methods are designed to fail silently if the target is NULL, 
    // relying on the CheckGenericToggleAssignments() in Start() to report the error.
    public void ToggleGeneric01() { if (genericToggleTarget01 != null) genericToggleTarget01.SetActive(!genericToggleTarget01.activeSelf); }
    public void ToggleGeneric02() { if (genericToggleTarget02 != null) genericToggleTarget02.SetActive(!genericToggleTarget02.activeSelf); }
    public void ToggleGeneric03() { if (genericToggleTarget03 != null) genericToggleTarget03.SetActive(!genericToggleTarget03.activeSelf); }
    public void ToggleGeneric04() { if (genericToggleTarget04 != null) genericToggleTarget04.SetActive(!genericToggleTarget04.activeSelf); }
    public void ToggleGeneric05() { if (genericToggleTarget05 != null) genericToggleTarget05.SetActive(!genericToggleTarget05.activeSelf); }
    public void ToggleGeneric06() { if (genericToggleTarget06 != null) genericToggleTarget06.SetActive(!genericToggleTarget06.activeSelf); }
    public void ToggleGeneric07() { if (genericToggleTarget07 != null) genericToggleTarget07.SetActive(!genericToggleTarget07.activeSelf); }
    public void ToggleGeneric08() { if (genericToggleTarget08 != null) genericToggleTarget08.SetActive(!genericToggleTarget08.activeSelf); }
    public void ToggleGeneric09() { if (genericToggleTarget09 != null) genericToggleTarget09.SetActive(!genericToggleTarget09.activeSelf); }
    public void ToggleGeneric10() { if (genericToggleTarget10 != null) genericToggleTarget10.SetActive(!genericToggleTarget10.activeSelf); }


    // --- Global Quality Setter Methods (Called via VRC_Interact) ---

    public void ToggleQualityLQ() // Renamed for clarity on the single button's purpose
    {
        // If currently HQ (1), switch to LQ (2). If currently LQ (2), switch to HQ (1).
        // If currently OFF (0), switch to HQ (1) as a sensible default.
        if (currentQualityIndex == 2)
        {
            currentQualityIndex = 1; // Switch to HQ
        } 
        else if (currentQualityIndex == 1)
        {
            currentQualityIndex = 2; // Switch to LQ
        }
        else // Must be OFF (0)
        {
            currentQualityIndex = 1; // Default to HQ
        }
        
        _UpdateMirrorStates();
    }

    // New, dedicated OFF button
    public void SetQualityOff()
    {
        currentQualityIndex = 0; // Off state
        _UpdateMirrorStates();
    }
    
    // --- Core Mirror Logic ---

    private void _UpdateMirrorStates()
    {
        // If quality is Off (index 0), shut everything down
        if (currentQualityIndex == 0)
        {
            _SetAllMirrorsInactive();
            return;
        }

        // Get the array index for the selected quality (1=HQ -> 0, 2=LQ -> 1)
        int qualityArrayIdx = currentQualityIndex - 1;

        // Update all three mirror locations
        _SetMirrorGroupActivity(mirrorsA, qualityArrayIdx, mirrorAIsOn);
        _SetMirrorGroupActivity(mirrorsB, qualityArrayIdx, mirrorBIsOn);
        _SetMirrorGroupActivity(mirrorsC, qualityArrayIdx, mirrorCIsOn);
    }

    private void _SetMirrorGroupActivity(GameObject[] mirrorGroup, int activeIndex, bool isLocationOn)
    {
        if (mirrorGroup == null || mirrorGroup.Length < 2) return;

        for (int i = 0; i < 2; i++)
        {
            GameObject mirror = mirrorGroup[i];
            if (mirror != null)
            {
                // Active if: 1. Location is toggled ON AND 2. The global quality matches this mirror's slot.
                bool isActive = isLocationOn && (i == activeIndex);
                mirror.SetActive(isActive);
            }
        }
    }

    private void _SetAllMirrorsInactive()
    {
        // Pass an invalid index (-1) to ensure no mirror group is activated
        _SetMirrorGroupActivity(mirrorsA, -1, false); 
        _SetMirrorGroupActivity(mirrorsB, -1, false);
        _SetMirrorGroupActivity(mirrorsC, -1, false);
    }
    
    // --- Audio Control Methods (Called via VRC_Interact) ---

    public void ToggleBGM()
    {
        if (bgmAudioSource != null)
        {
            if (bgmAudioSource.isPlaying)
            {
                bgmAudioSource.Pause();
            }
            else
            {
                bgmAudioSource.Play();
            }
        }
    }

    // Called by the Slider's On Value Changed event
    public void SetBGMVolume()
    {
        if (bgmAudioSource != null && bgmVolumeSlider != null)
        {
            bgmAudioSource.volume = bgmVolumeSlider.value;
        }
    }
}
/* * ----------------------------------------------------------------------------
 * ☆ UDON SHARP WIRING GUIDE (FOR VRC_INTERACT COMPONENTS) ☆
 * ----------------------------------------------------------------------------
 * All events are wired from the VRC_Interact -> On Interact event to the 
 * LobbyControlManager GameObject using SendCustomEvent(string).
 * * * METHOD: ToggleMirrorA
 * PURPOSE: Toggles the mirror at location A on/off.
 * * METHOD: ToggleMirrorB
 * PURPOSE: Toggles the mirror at location B on/off.
 * * METHOD: ToggleMirrorC
 * PURPOSE: Toggles the mirror at location C on/off.
 * * * METHOD: ToggleQualityLQ
 * PURPOSE: Switches global quality between HQ (1) and LQ (2). (Default is HQ)
 * * METHOD: SetQualityOff
 * PURPOSE: Turns all mirrors off (sets global quality index to 0).
 * * * METHOD: ToggleBGM
 * PURPOSE: Pauses or plays the BGM AudioSource.
 * * METHOD: SetBGMVolume
 * PURPOSE: Reads the Slider value and applies it to the BGM AudioSource volume.
 * * * METHOD: RunTest
 * PURPOSE: Prints a confirmation message ("✔✔✔ DEBUG BUTTON FIRED! ✔✔✔") to the Console.
 * * * --- GENERIC TOGGLES ---
 * * METHOD: ToggleGeneric01
 * PURPOSE: Toggles the active state of genericToggleTarget01.
 * * METHOD: ToggleGeneric02
 * PURPOSE: Toggles the active state of genericToggleTarget02.
 * * METHOD: ToggleGeneric03
 * PURPOSE: Toggles the active state of genericToggleTarget03.
 * * METHOD: ToggleGeneric04
 * PURPOSE: Toggles the active state of genericToggleTarget04.
 * * METHOD: ToggleGeneric05
 * PURPOSE: Toggles the active state of genericToggleTarget05.
 * * METHOD: ToggleGeneric06
 * PURPOSE: Toggles the active state of genericToggleTarget06.
 * * METHOD: ToggleGeneric07
 * PURPOSE: Toggles the active state of genericToggleTarget07.
 * * METHOD: ToggleGeneric08
 * PURPOSE: Toggles the active state of genericToggleTarget08.
 * * METHOD: ToggleGeneric09
 * PURPOSE: Toggles the active state of genericToggleTarget09.
 * * METHOD: ToggleGeneric10
 * PURPOSE: Toggles the active state of genericToggleTarget10.
 * ----------------------------------------------------------------------------
 */
