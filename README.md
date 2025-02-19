# Auto Outliner

Auto Outliner is a Blender add-on that automatically resets the scale of selected objects, removes any existing materials assigned to the objects, adds a solidify modifier, and assigns materials with customizable properties.

## Features

- Resets the scale of selected objects
- Removes any existing materials assigned to the objects
- Adds a solidify modifier with customizable thickness, flip normals, and material offset
- Assigns fill and outline materials with customizable colors
- Enables backface culling for the outline material

## Installation

1. Download the `auto_outliner.py` file.
2. Open Blender and go to `Edit > Preferences`.
3. In the Preferences window, go to the `Add-ons` tab.
4. Click the `Install...` button at the top right.
5. Select the downloaded `auto_outliner.py` file and click `Install Add-on`.
6. Enable the add-on by checking the box next to `Auto Outliner`.

## Usage

1. Select the objects you want to apply the auto outline setup to.
2. Open the `Auto Outliner` panel in the `View3D > Sidebar > Tools` tab.
3. Customize the properties as needed:
   - Outline Thickness
   - Flip Normals
   - Material Offset
   - Fill Color
   - Outline Color
   - Backface Culling
4. Click the `Auto Outliner` button to apply the setup to the selected objects.

## Properties

- **Outline Thickness**: Thickness of the solidify modifier.
- **Flip Normals**: Option to flip the normals of the solidify modifier.
- **Material Offset**: Material offset for the solidify modifier.
- **Fill Color**: Color for the fill material.
- **Outline Color**: Color for the outline material.
- **Backface Culling**: Enable backface culling for the outline material.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

- Michal Uchwat
- Email: uchwatmichal@gmail.com

## Support

For any issues or questions, please contact the author at the email provided above.
