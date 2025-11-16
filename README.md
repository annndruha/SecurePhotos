# <img src="https://raw.githubusercontent.com/Annndruha/SecurePhotos/main/src/img/icon.svg" width="32px"> SecurePhotos

![version](https://img.shields.io/github/v/release/Annndruha/SecurePhotos)
[![GitHub license](https://img.shields.io/github/license/Annndruha/SecurePhotos.svg)](https://github.com/Annndruha/SecurePhotos/blob/master/LICENSE)
[![python lint](https://github.com/Annndruha/SecurePhotos/actions/workflows/flake8.yml/badge.svg)](https://github.com/Annndruha/SecurePhotos/actions/workflows/flake8.yml/badge.svg)

SecurePhotos - Gallery for photos with encryption for your photos or any files. Also, it's faster than windows default gallery!

### Screenshots:

![image](https://github.com/annndruha/SecurePhotos/assets/51162917/5fb7e01c-fed6-4ab7-8777-9eace9cf5ea8)


### Features

* Encrypt/Decrypt files and folders on disk
* Encrypted image preview without decrypt on disk
* Rotate and delete images
* Infinite photos zoom

### Install and usage:

##### Pre-build exe for Windows:
* Go to [release section](https://github.com/annndruha/SecurePhotos/releases)
* Download `SecurePhotos.exe` from release assets

##### Manual run from sources:
Install Python and execute in terminal:
```bash
git clone https://github.com/annndruha/SecurePhotos
cd SecurePhotos
pip install -r requirements.txt
python -m src
```

### Algorithm:


When you click `Encrypt 🔒`:

```mermaid

flowchart TD
    PW["Password<br/>Not stored in RAM or anywhere"] --> SHA[SHA-256]
    SHA --> HASH["Password HASH<br/>Stored in RAM (while open)"]
    
    DATA["Image/video file on disk<br/>(png | jpg | mp4 | mkv | etc.)"] --> BYTES["Bytes"]
    BYTES --> PADDING["Padding up to block size 16"]

    subgraph AES-256
        HASH --> CHIPPER
        PADDING --> CHIPPER["Ciphertext"]
    end

    CHIPPER --> NEW_FILE["Encrypted image or folder on disk<br/>with ext (.aes/.aes_zip)"]
    NEW_FILE --> DELETE_FILE["Delete old file<br/>or folder"]
    
    style PW fill:#e6e6fa
    style SHA fill:#e6e6fa
    style DATA fill:#b3d9ff
    style BYTES fill:#b3d9ff
    style PADDING fill:#b3d9ff
    style HASH fill:#e6e6fa
    style CHIPPER fill:#fffc5e
    style NEW_FILE fill:#ccffcc
    style DELETE_FILE fill:#ffcccc
    
```

### Contact
Feel free to report bugs and suggest improvements on [annndruha.github@gmail.com](mailto:annndruha.github@gmail.com)
