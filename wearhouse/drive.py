from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def upload_to_drive(filename):
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    archivo = drive.CreateFile()
    archivo.SetContentFile(filename)
    archivo.Upload()
    print("{} subido".format(archivo['title']))
