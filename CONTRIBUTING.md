# ☆ Contributing to Melody's CodeSnippets Repository ☆

> "Every code block should sparkle a little bit."

Thank you for your interest in contributing to my personal library of code blocks, algorithms, and logic patterns! Your contributions help maintain and expand this resource.

Before submitting any contribution, please review these general guidelines and the specific requirements for the language folder you are working in.

---

## 💖 How to Contribute

We welcome contributions in three primary forms:

1.  **Reporting Bugs:** If you find an issue in a snippet (incorrect logic, compile error, etc.), please open a new Issue describing the file location and the problem.
2.  **Suggesting Features:** Suggest a new algorithm, pattern, or code block you think would be useful to add to a specific language directory.
3.  **Submitting Code:** Provide new code snippets or fixes via a Pull Request (PR), adhering to the style guidelines below.

---

## ☆ General Submission Process

1.  **Fork** the repository to your personal GitHub account.
2.  **Clone** your fork locally and create a new branch for your work (e.g., `feat/java-sort-algorithm` or `fix/vrchat-asset-lister`).
3.  **Test** your code thoroughly in its respective environment (e.g., VRChat, standard Java runtime, etc.).
4.  **Open a Pull Request** targeting the `main` branch of the original repository.

---

## ☆ Language-Specific Coding Guidelines (Mandatory)

All submitted code **must** adhere to the standard conventions of the target language, AND follow the custom styling rules below.

### 1. `VRChat/` and Udon Sharp (U#)

This folder includes specialized code for VRChat worlds (Udon Sharp runtime scripts, Unity Editor Tools).

* **File Headers (MANDATORY):** All new or modified files must include the specific custom ASCII header block found in the repository's `README.md`. Replace `☆ Author: ☆ MelodyHSong ☆` with `☆ Author: ☆ [Your GitHub Handle] ☆`.
- Here is an example of what my code looks like:

```csharp
/*
☆
☆ Author: ☆ MelodyHSong ☆
☆ Language: Udon Sharp (C#)
☆ File Name: ExampleToggle.cs
☆ Date: 2025-11-22
☆
*/

using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

public class ExampleToggle : UdonSharpBehaviour
{
    // Magic happens here...
}

``` 
* **Editor Tools:** Files intended to run only in the Unity Editor must be correctly placed inside the **`VRChat/MHSTools/Editor/`** sub-directory.
* **Comments:** If you want to decorate your code, use `☆` and other ASCII symbols. **DO NOT USE EMOJIS** within C# comments. It may cause errors for other users.

### 2. `CPlusPlus/`, `CSharp/`, and `Java/`

For general algorithms and standard code blocks:

* **File Headers:** While the full custom header is preferred, a clear comment at the top identifying the author is required.
* **Style:** Follow the established best practices for the target language (e.g., camelCase for Java/C#, snake\_case for C++ variables, proper indentation, etc.).
* **Comments:** Use the already mentioned style for any complex logic explanation.

---

## ⭐️ Review Process

I will review all contributions for:

1.  **Functionality:** Does the code work as intended and pass tests?
2.  **Performance:** Is the code efficient?
3.  **Style Compliance:** Does the code meet the mandatory header and commenting requirements for its directory? 

Please be prepared to make minor revisions based on feedback. Thank you again for your time and effort!

---
*I know, I know. This is weird. - MelodyHSong* 
