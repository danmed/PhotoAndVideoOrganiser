# Photo & Video Sorter GUI

A Python script with a graphical user interface (GUI) to organize your photos and videos from a source folder into year and month subfolders in a destination folder.

![image](https://github.com/user-attachments/assets/cffbb06c-2340-486d-adfe-131a74fa8f80)


## Description

This script provides an easy way to sort large collections of photos and videos. It reads the creation or modification date of each media file and then copies or moves it into a structured folder hierarchy (`YYYY/MM`) in your chosen destination. It also allows you to save and load preset source/destination folder pairs for quick access.

## Features

* **Graphical User Interface:** Easy-to-use interface built with Tkinter.
* **Source & Destination Selection:** Browse and select your source (input) and destination (output) folders.
* **Year/Month Organization:** Automatically creates folders named by year (e.g., `2025`) and subfolders named by month (e.g., `06` for June) in the destination.
* **Move or Copy:**
    * Choose to **move** files (originals are deleted from the source). This is the default.
    * Choose to **copy** files (originals are kept in the source).
* **Overwrite Control:** Option to overwrite files in the destination if they already exist.
* **Conflict Resolution:** If not overwriting, files with duplicate names in the target month folder will be automatically renamed by appending a number (e.g., `image.jpg` becomes `image (1).jpg`).
* **Preset Management:**
    * Save frequently used source and destination folder pairs as named presets.
    * Load presets to quickly populate folder paths.
    * Delete unneeded presets.
    * Presets are stored in a `photo_sorter_presets.json` file in the script's directory.
* **File Type Support:** Supports a wide range of common photo and video file extensions.
    * **Photos:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.tif`, `.heic`, `.heif`, `.raw`, `.nef`, `.cr2`, `.orf`, `.sr2`, `.arw`, `.dng`
    * **Videos:** `.mp4`, `.mov`, `.avi`, `.mkv`, `.wmv`, `.flv`, `.webm`, `.mpg`, `.mpeg`, `.m4v`, `.3gp`
* **Progress Logging:** A log area displays the actions being performed, files processed, and any errors encountered.
* **Cross-platform (Python):** As a Python script, it should run on Windows, macOS, and Linux where Python and Tkinter are available.

## Requirements

* **Python 3.6 or newer:** The script uses f-strings and other modern Python features.
* **Tkinter:** This is usually included with standard Python installations. If not (e.g., on some Linux minimal installs), you may need to install it separately (e.g., `sudo apt-get install python3-tk`).

## How to Use

1.  **Download:**
    * Clone this repository: `git clone https://github.com/danmed/PhotoAndVideoOrganiser.git`
    * Or, download the `photo_video_sorter.py` script directly.

2.  **Run the Script:**
    * Open a terminal or command prompt.
    * Navigate to the directory where you saved the script: `cd path/to/script`
    * Execute the script: `python photo_video_sorter.py`
    * (On some systems, you might use `python3` instead of `python`).

3.  **Using the Application:**
    * **Source Folder:** Click "Browse..." to select the folder containing the photos and videos you want to organize.
    * **Destination Folder:** Click "Browse..." to select the folder where the organized `YYYY/MM` subfolders will be created.
    * **Presets (Optional):**
        * To save the current source/destination as a preset, click "Save Current", enter a name, and click OK.
        * To load a preset, select it from the dropdown menu.
        * To delete a preset, select it and click "Delete Selected".
    * **Options:**
        * **Move files:** Ticked by default. Untick to copy files instead of moving them.
        * **Overwrite existing files:** Tick if you want files in the destination to be replaced if a new file with the same name is processed for that location. If unticked, name conflicts are resolved by appending numbers.
    * **Process Files:** Click this button to start the organization process.
    * Monitor the **Log** area for progress and any messages.

**IMPORTANT:** It is highly recommended to **test the script with sample source and destination folders first** before using it on your main photo and video collection. This will help you understand its behavior and ensure it works as expected.

## Configuration

* **Presets:** User-defined presets for source and destination folders are stored in a JSON file named `photo_sorter_presets.json`. This file is automatically created and managed in the same directory as the script.

## Troubleshooting

* **GUI Not Opening / Errors on Start:**
    * Ensure you have Python 3.6+ installed and that Tkinter is available.
    * Run the script from a command line/terminal to see any error messages.
    * If you downloaded the script, ensure it wasn't corrupted.
* **Permission Errors:**
    * The script needs read permissions for the source folder and its contents.
    * It needs read and write permissions for the destination folder (to create subfolders and write files).
    * It also needs permission to write the `photo_sorter_presets.json` file in its own directory.
* **Incorrect Dates:** The script uses file system metadata (creation or modification time) to determine the year and month. If this metadata is incorrect for your files (e.g., due to how they were copied or downloaded), the sorting might not reflect the actual "date taken". For more accurate photo dates, EXIF data reading would be needed (a potential future enhancement).

## Future Enhancements (Ideas)

* Read EXIF data for photos to get the "Date Taken" for more accurate sorting.
* Option to customize the output folder structure (e.g., `YYYY/YYYY-MM-DD`).
* Progress bar for long operations.
* Option to specify file types to include/exclude.
* Ability to undo the last operation (complex).
* Package as a standalone executable (e.g., using PyInstaller).

## Contributing

Contributions are welcome! If you have suggestions for improvements or bug fixes, please feel free to:
1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourAmazingFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some amazing feature'`).
5.  Push to the branch (`git push origin feature/YourAmazingFeature`).
6.  Open a Pull Request.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details (you'll need to create this file if you choose this license).
