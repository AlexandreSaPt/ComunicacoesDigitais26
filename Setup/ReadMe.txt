# Setup Instructions

## 1. Prerequisites
Ensure WSL is installed on your system. If not, open PowerShell as Administrator and run:
```cmd
wsl --install
```

## 2. Import the Environment - Zip link:https://drive.google.com/file/d/1xCQ-Stxlf8JBt6WwDQlNNj0OhCsxTnzn/view?usp=sharing
1. Download and extract the `.zip` file to get the `.tar` archive.
2. Open Command Prompt (`cmd`) or PowerShell.
3. Import the distribution by running:
   ```cmd
   wsl --import <DistroName> C:\WSL\<DistroName> <AbsolutePathToTarFile>
   ```
   *(Example: `wsl --import SDR-Legacy C:\WSL\SDR-Legacy C:\Users\YourName\Downloads\SDR-Legacy.tar`)*

## 3. Verify Installation
Check that the distribution was imported successfully:
```cmd
wsl -l -v
```
You should see `<DistroName>` listed in the output.

## 4. Launch
To start using the environment:
```cmd
wsl -d <DistroName>
```