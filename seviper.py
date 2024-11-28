from ftplib import FTP

ftp = FTP(host="ftp.us.debian.org", timeout=5, encoding="utf-8")


def start_connection():
    # start connection and check if was success
    if ftp.login():
        print("Connection OK!")
        return True


def download_files_with_x_extension(extension=str):
    # list all files in direction and write file endswith extension selected
    files = []
    ftp.retrlines("NLST", files.append)
    for filename in files:
        if filename.endswith(extension):
            print(f"File with {extension} extension found: {filename}")
            with open(filename, "wb") as local_file:
                ftp.retrbinary(f"RETR {filename}", local_file.write)


def close_connection():
    # close connection and check if was success
    if ftp.quit():
        print("Connection closed!")
