import os
import pythoncom
import win32com.client
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageDraw


app = Flask(__name__)
CORS(app)
# Test route
@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Backend is working!"})

# Route to change folder color
@app.route('/set-folder-color', methods=['POST'])
def set_folder_color():

    data = request.json
    folder_path = data.get("folder_path")
    color = data.get("color")

    print(f"Request received with folder_path: {data.get('folder_path')} and color: {data.get('color')}")

    if not folder_path or not os.path.exists(folder_path):
        return jsonify({"error": "Invalid folder path."}), 400

    if not color:
        return jsonify({"error": "Color value is missing."}), 400

    # Change folder icon logic
    try:
        apply_folder_color(folder_path, color)
        return jsonify({"message": f"Color {color} applied to folder {folder_path}!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def apply_folder_color(folder_path, color):
    """
    Change the folder icon color by generating a desktop.ini file
    and setting a custom folder icon.
    """
    print(f"Applying folder color. Folder path: {folder_path}, Color: {color}")
    pythoncom.CoInitialize() 
    
    shell = win32com.client.Dispatch("WScript.Shell")
    desktop_ini_path = os.path.join(folder_path, "desktop.ini")
    icon_path = generate_colored_icon(folder_path, color)

    print(f"Generated icon path: {icon_path}")
    print(f"Desktop.ini path: {desktop_ini_path}")

    # Write desktop.ini to change the folder icon
    try:
        with open(desktop_ini_path, "w") as desktop_ini:
            desktop_ini.write(f"[.ShellClassInfo]\nIconResource={icon_path},0\n")
            print("Desktop.ini file written successfully.")
    except Exception as e:
        print(f"Error writing desktop.ini: {e}")

    # Set the folder as a system folder to apply the icon
    os.system(f"attrib +s \"{folder_path}\"")
    os.system(f"attrib +h \"{desktop_ini_path}\"")
    print("Folder attributes updated.")


def generate_colored_icon(folder_path, color_hex):
    """
    Generate a tinted folder icon from folder_template.png
    and save it as an .ico file.
    """
    import os
    from PIL import Image
    # Convert color from hex (#RRGGBB) to an (R, G, B) tuple
    color_hex = color_hex.lstrip("#")
    rgb_color = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    print(f"RGB color: {rgb_color}")

    # Build a path to the PNG template relative to this file
    base_path = os.path.join(
        os.path.dirname(__file__),  # backend/
        "..",                       # up one level => FolderColorChanger/
        "frontend", "assets", "folder_template.png"
    )
    print(f"Loading base folder icon from: {base_path}")

    # Load the base PNG as RGBA (so we keep transparency)
    base_img = Image.open(base_path).convert("RGBA")

    # Create an overlay in the chosen color, same size as base
    # giving full opacity (255 in alpha channel)
    overlay = Image.new("RGBA", base_img.size, rgb_color + (255,))

    # Alpha-composite: overlay color onto the original image
    # This tints the folder shape with your chosen color
    tinted_img = Image.alpha_composite(base_img, overlay)

    # Now save it as an .ICO file in the target folder
    # The multiple sizes param ensures the .ico has several resolutions
    icon_path = os.path.join(folder_path, "folder_icon.ico")
    tinted_img.save(icon_path, format="ICO",
                    sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
    print(f"Icon saved at: {icon_path}")

    return icon_path




if __name__ == '__main__':
    app.run(debug=True)
