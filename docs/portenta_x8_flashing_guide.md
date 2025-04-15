# Portenta X8 Flashing Guide

This guide provides step-by-step instructions for flashing your Arduino Portenta X8 board using the Universal Update Utility (UUU) tool.

## Prerequisites

- Arduino Portenta X8 board
- USB-C cable
- Image files for the Portenta X8 (typically in a directory structure like `image-latest/881/`)
- UUU (Universal Update Utility) flash tool

## Flashing Instructions

### 1. Prepare Your Portenta X8 Board

1. Disconnect the board from your computer
2. Power off the board completely
3. Press and hold the BOOT/RECOVERY button (this may be labeled differently on your specific model)
4. While holding the button, connect the board to your computer via USB
5. Release the button after a few seconds

### 2. Navigate to the UUU Tool Directory

Open PowerShell or Command Prompt and navigate to the directory containing the UUU tool and flashing scripts:

```powershell
cd "C:\path\to\image-files\mfgtool-files-portenta-x8"
```

For example:
```powershell
cd "C:\Users\dvir\Downloads\image-latest (4)\881\mfgtool-files-portenta-x8"
```

### 3. Check if Your Device is Detected

Run the following command to check if your Portenta X8 board is detected by the UUU tool:

```powershell
.\uuu.exe -lsusb
```

You should see your Portenta X8 board listed with a protocol (SDP or FB).

### 4. Flash the Board

You can flash the board in one step using the full_image.uuu script:

```powershell
.\uuu.exe full_image.uuu
```

Alternatively, you can flash in stages:

1. Flash the bootloader first:
   ```powershell
   .\uuu.exe bootloader.uuu
   ```

2. Then flash the full image:
   ```powershell
   .\uuu.exe full_image.uuu
   ```

### 5. Wait for the Process to Complete

- The flashing process may take several minutes, especially when writing the main image
- Do not disconnect your board during this process
- You should see progress indicators in the terminal window

### 6. Verify the Flashing was Successful

- After the flashing process completes, disconnect your board
- Power it off, then power it on normally
- It should boot with the new image

## Troubleshooting

If you encounter any issues during the flashing process:

- Make sure your board is properly in recovery/download mode
- Check that all the required files are present in the correct directories
- Try using a different USB port or cable
- Ensure your computer doesn't go to sleep during the flashing process
- Try running the UUU tool with verbose output for more information:
  ```powershell
  .\uuu.exe -v full_image.uuu
  ```

## File Structure

The image files for the Portenta X8 typically include:

- `imx-boot-portenta-x8`: Bootloader image
- `lmp-partner-arduino-image-portenta-x8.wic`: Main system image
- `u-boot-portenta-x8.itb`: U-Boot image
- `sit-portenta-x8.bin`: System Information Table
- `mfgtool-files-portenta-x8/`: Directory containing the UUU tool and flashing scripts

## References

- [Arduino Portenta X8 Documentation](https://docs.arduino.cc/hardware/portenta-x8/)
- [UUU Tool GitHub Repository](https://github.com/nxp-imx/mfgtools)
