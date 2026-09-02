#Provide a small code snippet demonstrating your approach to one of the core requirements, and why you chose this component
    #Change Detection: Only files that have been created or modified since the last successful sync should be transferred.

import hashlib
import os
import time
from datetime import datetime

manifest = [
    {
        "filepath": "folder\\Example1.jpg",
        "file_size": 50000,
        "last_modified": 1000000000.9654553, #OLD
        "file_hash": "eqewqeqd85549c212491b2912ed315d41aasdasdsa95ff2f7b77a88032131233", #OLD
        "last_synced": 1000000000.9654553
    },
    {
        "filepath": "folder\\Example2.jpg",
        "file_size": 48705,
        "last_modified": 1788173306.76063,
        "file_hash": "5fd1d0715ed0ce04400092769488930fa144cea5fc1c6e00a7b95d751b8d8b5e",
        "last_synced": 1788173306.76063
    },
    {
        "filepath": "folder\\Example3.jpg",
        "file_size": 31332,
        "last_modified": 31232133.710917, #OLD
        "file_hash": "3eq23efasdfsdfg342wdfsdfawedfew3242332423f23f23f3212dwedfasddsad", #OLD
        "last_synced": 31232133.710917
    } 
    #etc
]

def generate_sha256_hash(filepath):
    with open(filepath, "rb") as f:
        sha256_hash = hashlib.file_digest(f, "sha256").hexdigest()
    return sha256_hash

def create_file_metadata(filepath, file_size=None, last_modified=None, file_hash=None):
    file_metadata = {
        "filepath": filepath,
        "file_size": file_size or os.path.getsize(filepath),
        "last_modified": last_modified or os.path.getmtime(filepath),
        "file_hash": file_hash or generate_sha256_hash(filepath),
    }
    return file_metadata

def compare_files_by_metadata(file, file_metadata):
    new_file_size = os.path.getsize(file.path)
    new_last_modified = os.path.getmtime(file.path)

    if new_file_size == file_metadata["file_size"] and new_last_modified == file_metadata["last_modified"]:
        return
    
    new_sha256_hash = generate_sha256_hash(file.path)

    if new_sha256_hash != file_metadata["file_hash"]:
        return create_file_metadata(filepath=file.path, file_size=new_file_size, last_modified=new_last_modified, file_hash=new_sha256_hash)
    return

def check_file_with_manifest(manifest_by_filepath):
    directory_path = "folder"
    files_to_sync = []

    with os.scandir(directory_path) as entries:
        for entry in entries:
            if entry.is_file():
                # print(f"File name: {entry.name} | Full path: {entry.path}")
                if entry.path in manifest_by_filepath:
                    new_file_metadata = compare_files_by_metadata(entry, manifest_by_filepath[entry.path])
                    if new_file_metadata:
                        files_to_sync.append(new_file_metadata)
                else:
                    files_to_sync.append(create_file_metadata(entry.path))

    return files_to_sync

def sync_files_to_server(files_to_sync):
    synced_files = []
    for file in files_to_sync:
        try:
            #~~~~~~~~~UPLOAD file TO SERVER~~~~~~~~~#
            updated_timestamp = time.time()
            file.update({"last_synced": time.time()})
            synced_files.append(file)
        except Exception as e:
            print(f"Unable to transfer file {files_to_sync[0]["filepath"]}")
            continue
        print(f"UPLOADED FILE {file} TO SERVER")

    return synced_files

def update_manifest_with_uploaded_files(synced_files, manifest_by_filepath): #Only update if sync is successful
    for file in synced_files:
        if file["filepath"] in manifest_by_filepath:
            manifest_by_filepath[file["filepath"]] = file
        else:
            manifest_by_filepath.update({file["filepath"]: file})

    manifest = list(manifest_by_filepath.values())
    print(f"\nNEW MANIFEST = {manifest}")

manifest_by_filepath = {
    file["filepath"]: file for file in manifest
}

files_to_sync = check_file_with_manifest(manifest_by_filepath)
synced_files = sync_files_to_server(files_to_sync)
update_manifest_with_uploaded_files(synced_files, manifest_by_filepath)
