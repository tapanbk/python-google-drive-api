
## python examples for google drive API
#### Installation and setup Steps

1. ##### Generate and download **credentials.json** file from  [Google Developer Console](https://console.developers.google.com/apis/library)

2. ##### Create new folder **.credentials** and move that json file into **.credentials** folder

3. ##### Install pip using command

    <code>sudo apt-get install python3-pip</code>
  
3. ##### Install Virtualenv package used for creating virtual environment for python using command

    <code>sudo pip3 install virtualenv using command</code>
  
4. ##### Create new virtualenv named venv using command

    <code>virtualenv venv</code> 
  
5. ##### Activate venv using command

    <code>source venv/bin/activate</code>
  
6. ##### Install dependencies using command

    <code>pip install -r requirements.txt</code>

7. ##### Create **files** directory and move files to upload in the files directory
 
8. ##### Run main.py file
  - Please mention proper file name in file upload function as parameter

    <code>python main.py</code>
    

#### Currently available python examples for google drive API
1. Upload file to a root path of the drive
1. Download file from root path of the drive
1. Create folder in the drive
1. Upload file to folder
1. Search file in all folder of drive
1. Search file inside a folder
1. Delete file
1. Empty files from trash
