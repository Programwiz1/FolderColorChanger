// Onboarding Popup
document.addEventListener("DOMContentLoaded", () => {
  const popup = document.getElementById("onboarding-popup");
  const closePopup = document.getElementById("close-popup");

  // Show popup on first load
  popup.classList.add("show");

  closePopup.addEventListener("click", () => {
    popup.classList.remove("show");
  });
});

// Folder Preview Logic
const colorPicker = document.getElementById("color-picker");
const folderPreview = document.getElementById("folder-preview");

colorPicker.addEventListener("input", () => {
  const selectedColor = colorPicker.value;
  // Update the overlay color
  folderPreview.style.setProperty("--overlay-color", selectedColor);
});

// Apply Button
document.getElementById("apply-button").addEventListener("click", async () => {
  const folderPath = document.getElementById("folder-path").value;
  const selectedColor = colorPicker.value;

  if (folderPath.trim()) {
    try {
      // Send POST request to the backend
      const response = await fetch("http://127.0.0.1:5000/set-folder-color", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          folder_path: folderPath,
          color: selectedColor,
        }),
      });

      // Handle response from the backend
      const result = await response.json();
      if (response.ok) {
        alert(result.message || "Color applied successfully!");
      } else {
        alert(result.error || "An error occurred while applying the color.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to communicate with the backend.");
    }
  } else {
    alert("Please enter a valid folder path.");
  }
});

// Reset Button
document.getElementById("reset-button").addEventListener("click", () => {
  document.getElementById("folder-path").value = "";
  colorPicker.value = "#ff0000";
  folderPreview.style.setProperty("--overlay-color", "#ff0000"); // Reset to default red
  alert("Settings reset to default.");
});

// Browse Button Functionality
const browseButton = document.getElementById("browse-button");
const folderPathInput = document.getElementById("folder-path");

// When the Browse button is clicked, allow folder selection
browseButton.addEventListener("click", async () => {
  if (window.showDirectoryPicker) {
    try {
      const directoryHandle = await window.showDirectoryPicker();
      folderPathInput.value = directoryHandle.name; // Set folder name as path
      console.log(`Folder selected: ${directoryHandle.name}`);
    } catch (error) {
      console.error("Folder selection was canceled or failed", error);
    }
  } else {
    alert("Folder browsing is not supported in this browser.");
  }
});
