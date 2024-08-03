import urllib.request
import os
import zipfile


class Extracter:
    def __init__(self, url, project_directory,extract_folder):
        self.url = url
        self.project_directory = project_directory
        self.extract_folder = extract_folder
        self.download_and_extract_zip()


    def download_and_extract_zip(self):
        """
        Download a zip file from a URL and extract its contents to a specified folder.

        :param url: URL of the zip file to be downloaded.
        :param download_folder: Folder where the zip file will be saved (default is current directory).
        :param extract_folder: Folder where the contents of the zip file will be extracted (default is 'extracted').
        """
        # Construct the local filename path
        local_filename = os.path.join(self.project_directory, 'ml-100k.zip')

        try:
            # Download the file
            print(f"Downloading file from {self.url}...")
            urllib.request.urlretrieve(self.url, local_filename)
            print(f"File downloaded successfully as {local_filename}")
            if not os.path.exists(self.extract_folder):
                os.makedirs(self.extract_folder)

            # Extract the zip file
            with zipfile.ZipFile(local_filename, 'r') as zip_ref:
                print(f"Extracting files to {self.extract_folder}...")
                zip_ref.extractall(self.extract_folder)
                print("Extraction complete.")
        except Exception as e:
            print(f"An error occurred: {e}")