#!/usr/bin/env python3

import os
import shutil
import re
import boto3

# Use Amazon S3
# Write your Amazon access_key_id and secret_access_key
session = boto3.Session(
    aws_access_key_id='',
    aws_secret_access_key=''
)

s3 = session.resource('s3')

# Write the name of the bucket where you're going to save the backups
bucket = s3.Bucket('')

# Path to directory that you will back up
basepath = ''

# path to any directory where the script can create the mirror directory
basemirror = ''

# Name for the backup in S3
S3_backup_name = ''

# Start

mirror_path = ''

# Source -> Amazon S3

for dirpath, dirnames, filenames in os.walk(basepath):
    # Upload files
    for file_x in filenames:
        # On Mac avoid .DS_Store file
        if file_x != '.DS_Store':
            source_path = dirpath + '/' + file_x

            mirror_path = source_path.replace(basepath, basemirror)

            # get modification time for source file
            mod_time = os.path.getmtime(source_path)

            # check modification time. If it changed upload to S3
            if os.path.exists(mirror_path):
                with open(mirror_path, 'r') as value:
                    time = value.readline()
                    if time != str(mod_time):
                        # Upload file to Amazon S3
                        S3_dest_path = source_path.replace(basepath, S3_backup_name)
                        bucket.upload_file(source_path, S3_dest_path)
                        # update modification time for the mirror file
                        with open(mirror_path, 'w') as file_mod_time:
                            file_mod_time.write(str(mod_time))
            else:
                # Upload file to Amazon S3 because the file is new
                S3_dest_path = source_path.replace(basepath, S3_backup_name)
                bucket.upload_file(source_path, S3_dest_path)

                # update modification time for that file
                # if it's a new file it will create it
                # Maybe in a new release later, change extension to .txt
                with open(mirror_path, 'w') as file_mod_time:
                    file_mod_time.write(str(mod_time))

    # create directories if they don't exist in the mirror directory
    mirror_path_dir = dirpath.replace(basepath, basemirror)
    for dir_name in dirnames:
        directory = mirror_path_dir + '/' + dir_name
        # check if directory already exists
        if not os.path.exists(directory):
            os.makedirs(directory)


# Function to remove files in S3
def remove_keys(list_keys):
    bucket.delete_objects(
        Delete={
            'Objects': list_keys
        }
    )


# This function get all the keys for a directory and remove them in S3
def remove_directory_keys(_directory):
    keys = []
    for dir_path, dir_names, file_names in os.walk(_directory):
        for file_w in file_names:
            path = dir_path + '/' + file_w
            s3_dest_path = path.replace(basemirror, S3_backup_name)
            keys.append({'Key': s3_dest_path})

            # The delete_object function doesn't accept an object with more than 1000 keys
            if len(keys) == 1000:
                remove_keys(keys)
                # clear list
                keys = []

    # List is not empty
    if keys:
        remove_keys(keys)


# Amazon S3 ->  Source

keys_to_remove = []

for dirpath, dirnames, filenames in os.walk(basemirror):

    for file_y in filenames:
        mirror_path = dirpath + '/' + file_y

        source_path = mirror_path.replace(basemirror, basepath)

        # if path doesn't exist on the source. Delete file on the mirror and in S3
        if not os.path.exists(source_path):
            os.remove(mirror_path)
            # replace path for S3
            S3_dest_path = source_path.replace(basepath, S3_backup_name)
            keys_to_remove.append({'Key': S3_dest_path})

            # The delete_object function doesn't accept an object with more than 1000 keys
            if len(keys_to_remove) == 1000:
                remove_keys(keys_to_remove)
                # clear list
                keys_to_remove = []

    # List is not empty
    if keys_to_remove:
        remove_keys(keys_to_remove)

    # Remove mirror directories if they don't exist in the source
    # the above code remove the files the in mirror directory but no the folders
    # No need to do this on S3
    source_path_dir = dirpath.replace(basemirror, basepath)
    for dir_name in dirnames:
        source_directory = source_path_dir + '/' + dir_name
        # check if directory already exists in the source
        if not os.path.exists(source_directory):
            mirror_directory = dirpath + '/' + dir_name
            # Remove all the keys in S3 for that directory
            remove_directory_keys(mirror_directory)
            # remove mirror directory
            shutil.rmtree(mirror_directory)
