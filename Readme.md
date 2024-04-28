# File Info
I planned to create a Media Info Website but Built a File Metadata Project

# Requirements
- libmagic1 exiftool
    If your on Ubuntu You can install them by running the below Command
    ```sh
    apt install libmagic1 exiftool
    ```
- python3

# How to Deploy
1. Clone this repo `git clone https://github.com/DeekshithSH/FileInfo.git` and open `FileInfo` Folder
2. Install Required python library
    ```
    pip3 install -r requirements.txt
    ```
3. create .env file with content
    ```
    PORT=8080
    ```
    replace `8080` with port number you want the WebApp to start on. If you don't create .env file WebApp will start in Port 8080
4. Start the WebApp by Running command below
    ```
    python3 -m MediaInfo
    ```