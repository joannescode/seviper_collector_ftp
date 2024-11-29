from ftplib import FTP


def start_connection():
    ftp = FTP(host="ftp.us.debian.org", timeout=5, encoding="utf-8")
    # start connection and check if was success
    if ftp.login():
        print("Connection OK!")
        return ftp


def download_files_with_x_extension(extension, ftp):
    # list all files in direction and write file endswith extension selected
    files = []

    def _collect_line(line):
        files.append(line)

    ftp.dir(_collect_line)

    for output in files:
        part = output.split()
        if part[0].startswith("-r") and part[-1].endswith(extension):
            filename = part[-1]
            print(f"File with {extension} extension found: {filename}")
            with open(filename, "wb") as local_file:
                ftp.retrbinary(f"RETR {filename}", local_file.write)


def download_all_files_founded(ftp):
    # write all files founded, no exception
    files = []

    def _collect_line(line):
        files.append(line)

    ftp.dir(_collect_line)

    for output in files:
        part = output.split()
        if part[0].startswith("-r"):
            filename = part[-1]
            print(f"File found: {filename}")
            with open(filename, "wb") as local_file:
                ftp.retrbinary(f"RETR {filename}", local_file.write)


def list_dirs(ftp):
    # List all dirs with parameter "d"
    dirs = []

    def _collect_line(output_line):
        if output_line.startswith("d"):
            dir_name = output_line.split()[-1]
            dirs.append(dir_name)

    ftp.dir(_collect_line)
    return dirs


def ftp_navigation(ftp):
    # Navigation with list saved in list_dirs
    while True:
        print("Current dir: ", ftp.pwd())

        dirs = list_dirs(ftp)
        if not dirs:
            print("Root not contain dirs.")
            break

        print("Dirs founded:")
        for i, dir_name in enumerate(dirs):
            print(f"[{i}] {dir_name}")
        print("[q] Sair")

        choice = input("\n Choice one dir for navigation (or 'q' for exit): ")
        if choice.lower() == "q":
            break

        try:
            choice_id = int(choice)
            if 0 <= choice_id < len(dirs):
                ftp.cwd(dirs[choice_id])
                return True

            else:
                print("Invalid choice. Try again.")

        except ValueError:
            print("Invalid input. Please, type a number or 'q'.")


def close_connection(ftp):
    # close connection and check if was success
    if ftp.quit():
        print("Connection closed!")
