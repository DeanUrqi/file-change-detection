# Change Detection 

For the snippet I've chosen the change detection requirement to demonstrate my solution design.
It includes a basic outline of the local stored manifest and how it checks for changes, for uploading files to the server. 
 Doesn't include the mentioned chunked uploads or checking if files already exist on the server.

Upon running it will check what files have changed and are to upload and output what is "uploaded", and the new manifest created.

NOTE
- I used Python 3.12 - All modules are apart of the standard library
- I used jpgs and a text file for the example, but any file should work
- In my example:
    - Example1 and Example3 both are new files, but were previously in the manifest
    - Example4 and Example5 are new and not present in manifest
