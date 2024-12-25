import os
import win32com.client
from flask import Flask, request, jsonify
from PIL import Image, ImageDraw


app = Flask(__name__)

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


def generate_colored_icon(folder_path, color):
    """
    Generate a colored folder icon and save it as an .ico file.
    """
    print(f"Generating icon for color: {color}")

    # Convert color from hex to RGB
    color = color.lstrip("#")
    rgb_color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    print(f"RGB color: {rgb_color}")

    # Create an image for the icon
    icon_size = (256, 256)  # Icon size
    img = Image.new("RGB", icon_size, rgb_color)

    # Save the image as an .ico file
    icon_path = os.path.join(folder_path, "folder_icon.ico")
    try:
        img.save(icon_path, format="ICO")
        print(f"Icon saved at: {icon_path}")
    except Exception as e:
        print(f"Error saving icon: {e}")

    return icon_path



if __name__ == '__main__':
    app.run(debug=True)
