# Dropbox Conexion
# Author: Blanca Cano

import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

from _config import TOKEN

# Name of the local file to upload and their dropbox file name

# LOCALFILE = 'photo.png'
# BACKUPPATH = '/photo.png'

# Uploads contents of LOCALFILE to Dropbox


def backup(LOCALFILE, BACKUPPATH, dbx):

    print(f"El fichero que se va a subir es {LOCALFILE}")
    with open(LOCALFILE, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print(f"Uploading {LOCALFILE} to Dropbox as {BACKUPPATH} ...")
        try:
            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()

# Change the text string in LOCALFILE to be new_content
# @param new_content is a string


def change_local_file(new_content, LOCALFILE):
    print("Changing contents of " + LOCALFILE + " on local machine...")
    with open(LOCALFILE, 'w') as f:  # HE CAMBIADO WB
        f.write(new_content)


# Restore the local and Dropbox files to a certain revision
def restore(LOCALFILE, BACKUPPATH, dbx, rev=None):
    # Restore the file on Dropbox to a certain revision
    print("Restoring " + BACKUPPATH + " to revision " + rev + " on Dropbox...")
    dbx.files_restore(BACKUPPATH, rev)

    # Download the specific revision of the file at BACKUPPATH to LOCALFILE
    msg = (f"Downloading current {BACKUPPATH} from Dropbox,"
           f" overwriting {LOCALFILE}...")
    print(msg)
    dbx.files_download_to_file(LOCALFILE, BACKUPPATH, rev)


# Look at all of the available revisions on Dropbox, and return the oldest one
def select_revision(BACKUPPATH, dbx):

    # Get the revisions for a file (and sort by the datetime object,
    # "server_modified")

    entries = dbx.files_list_revisions(BACKUPPATH, limit=30).entries
    revisions = sorted(entries, key=lambda entry: entry.server_modified)

    for revision in revisions:
        print(revision.rev, revision.server_modified)

    # Return the oldest revision (first entry, because revisions was sorted
    # oldest:newest)

    return revisions[0].rev


def upload_to_dropbox(_LOCALFILE, _BACKUPPATH):

    LOCALFILE = _LOCALFILE
    BACKUPPATH = _BACKUPPATH
    # Check for an access token

    if (len(TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token. ")

    # Create an instance of a Dropbox class,
    # which can make requests to the API.

    print("Creating a Dropbox object...")
    dbx = dropbox.Dropbox(TOKEN)

    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an "
                 "access token from the app console on the web.")

    # Create a backup of the current settings file
    backup(LOCALFILE, BACKUPPATH, dbx)

    # Change the user's file, create another backup
    change_local_file("updated", LOCALFILE)
    backup(LOCALFILE, BACKUPPATH, dbx)

    # Restore the local and Dropbox files to a certain revision
    to_rev = select_revision(BACKUPPATH, dbx)
    restore(LOCALFILE, BACKUPPATH, dbx, to_rev)
    print("Done!")
