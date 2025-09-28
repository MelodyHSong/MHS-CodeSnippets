/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: C# Udon Sharp
☆ File Name: LobbyControlPanel.cs
☆ Date: 2025-09-29
☆ Ver: 1.2
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


/* * --------------------------------------------------------------------------
 * ☆ UDON SHARP WIRING GUIDE (FOR VRC_INTERACT COMPONENTS) ☆
 * ----------------------------------------------------------------------------
 ☆
 * All events are wired from the VRC_Interact -> On Interact event to the 
 * LobbyControlManager GameObject using SendCustomEvent(string).
 ☆
 * * * METHOD: ToggleMirrorA
 * PURPOSE: Toggles the mirror at location A on/off.
 ☆ 
 * * METHOD: ToggleMirrorB
 * PURPOSE: Toggles the mirror at location B on/off.
 ☆
 * * METHOD: ToggleMirrorC
 * PURPOSE: Toggles the mirror at location C on/off.
 ☆
 * * METHOD: ToggleQualityLQ
 * PURPOSE: Switches global quality between HQ (1) and LQ (2). (Default is HQ)
 ☆
 * * METHOD: SetQualityOff
 * PURPOSE: Turns all mirrors off (sets global quality index to 0).
 ☆
 * * METHOD: ToggleBGM
 * PURPOSE: Pauses or plays the BGM AudioSource.
 ☆
 * * METHOD: SetBGMVolume
 * PURPOSE: Reads the Slider value and applies it to the BGM AudioSource volume.
 ☆
 * * METHOD: RunTest
 * PURPOSE: Prints a confirmation message ("✔✔✔ DEBUG BUTTON FIRED! ✔✔✔") to the Console.
 ☆
 * ----------------------------------------------------------------------------
 */
