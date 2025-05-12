<div align="center">
  <h1>
    CC4 to ARKit Renamer with Jaw Open <img src="./assets/fig/Hi.gif" width="40px">
  </h1>
  <p>
    Blender add-on for converting CC4 shape keys to ARKit naming conventions
  </p>
  <p>
    <img src="https://img.shields.io/badge/Blender-3.6+-brightgreen?style=flat-square" alt="Blender Version" />
    <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="License" />
  </p>
</div>

## Key Features
- 🚀 **User-Selectable Inputs:**  
  Easily select the Armature, Base Mesh, and Jaw Bone via the UI panel.
- 🔄 **Jaw Open Process:**  
  Automatically rotates the selected jaw bone to capture a "jaw open" state and creates a driven shape key.
- 🔀 **Shape Key Conversion:**  
  Renames CC4 shape keys to their corresponding ARKit names.
- 😃 **Teeth/Tongue Merging & Separation:**  
  If objects named `CC_Base_Teeth` and/or `CC_Base_Tongue` exist, the add-on merges them into the base mesh using vertex groups and (upon revert) separates and renames them accordingly.
- 🔒 **Revert Functionality (Disabled):**  
  The revert operator remains in the code but its UI button is disabled.
- ↩️ **Jaw Bone Reset:**  
  After conversion, the jaw bone is automatically rotated back to its original position.

## Installation

1. **Download the Add-on:**
   - Clone or download the repository as a ZIP file from GitHub.

2. **Install in Blender:**
   - Open Blender.
   - Go to **Edit > Preferences > Add-ons**.
   - Click **Install…**.
   - Navigate to and select the downloaded ZIP file.
   - Click **Install Add-on from File**.
   - In the Add-ons list, search for **CC4 to ARKit Renamer with Jaw Open**.
   - Enable the add-on by checking its box.

3. **Save Preferences (Optional):**
   - Click **Save Preferences** to keep the add-on enabled for future sessions.

## Usage

1. **Prepare Your Scene:**
   - Ensure your scene contains:
     - A Base Mesh with CC4 shape keys.
     - An Armature controlling the mesh.
     - A Jaw Bone (e.g., `CC_Base_JawRoot`).
     - Optionally, teeth and tongue objects named `CC_Base_Teeth` and `CC_Base_Tongue`.

2. **Open the Panel:**
   - In the 3D Viewport, press **N** to open the Sidebar.
   - Click on the **CC4 ARKit** tab.

3. **Select Required Objects:**
   - Choose the **Base Mesh**.
   - The UI will indicate if your selection is valid.

4. **Convert CC4 to ARKit:**
   - Click the **Convert CC4 to ARKit** button.

## Troubleshooting

- **"Mesh already converted" Message:**  
  Verify that your Base Mesh still contains the original CC4 shape keys.
- **Vertex Count Mismatch:**  
  Ensure the Base Mesh has applied modifiers and is correctly evaluated.
- **Teeth/Tongue Merging Issues:**  
  Confirm that teeth and tongue objects are named exactly `CC_Base_Teeth` and `CC_Base_Tongue`.

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions, issues, and feature requests are welcome! Please open an issue on GitHub for more details.

## Acknowledgements

- Inspired by the need to integrate CC4 and ARKit facial rig workflows.
- Thanks to the Blender community for feedback and testing.
