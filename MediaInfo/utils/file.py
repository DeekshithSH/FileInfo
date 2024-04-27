from exiftool import ExifTool

def split_text(value):
    return value[0].split(":", maxsplit=1), value[1]

def get_metadata(file_path) -> str:
    with ExifTool() as et:
        metadata : dict= (et.execute_json(file_path))[0]
    keys_to_remove = [
    "SourceFile",
    "File:Directory",
    "File:FileAccessDate",
    "File:FileInodeChangeDate",
    "ExifTool:Warning",
    "File:FileModifyDate",
    "File:FileName",
    "File:FilePermissions",
    "File:FileSize",
    "ExifTool:ExifToolVersion"
    ]

    metadata = {key: value for key, value in metadata.items() if key not in keys_to_remove}
    metadata=map(split_text, metadata.items())
    curt=""
    text=""
    for x in metadata:
        try:
            if x[0][0] != curt:
                curt=x[0][0]
                text+=f"<br><b>{curt}</b>"

            text+=f"<br>&nbsp&nbsp{x[0][1]}: {' '.join(x[1]) if (isinstance(x[1], list)) else x[1]}"
        except IndexError:
            text+="<br>"+str(x)

    return text
