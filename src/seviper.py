from ftplib import FTP
from src.logging import get_logger
import os

current_path = os.path.dirname(os.path.realpath(__file__))
log = get_logger()


def download_extension_kind():
    """
    Prompts the user to specify if they wish to download a specific extension kind.

    The function asks the user to input either '0' (for no) or '1' (for yes).
    If the user inputs '1', it indicates that they wish to download a specific extension kind.
    If the user inputs any other value, it indicates that no specific extension is selected.

    Returns:
        str: The user's input, either '0' or '1'.

    Raises:
        Exception: If there is an error during the input process.
    """
    try:
        download_kind = input(
            "Which extension kind for download you wish? Type 0 (for no) or 1 (for yes):"
        )

        if download_kind != "1":
            log.info("No specific extension selected.\n")
            return download_kind
        return download_kind
    except Exception as e:
        log.error(f"Error in download type input: {e}")
        raise


def specify_specific_extension(download_kind):
    """Prompts the user to specify a file extension type based on the provided download kind.

    Parameters:
    download_kind (str): A string indicating the type of download. If the value is "1",
                         the function will prompt the user to enter a desired file extension.

    Returns:
    str: The user-specified file extension if download_kind is "1".
    None: If download_kind is not "1".

    Raises:
    Exception: If there is an error during the input process, it logs the error and raises the exception."""
    try:
        if download_kind == "1":
            log.info("Please specify the desired extension type. Available examples:\n")
            log.info(
                """
            .txt  - Plain text file.
            .jpg  - JPEG image file.
            .pdf  - PDF document (Portable Document Format).
            .docx - Microsoft Word document.
            .xlsx - Microsoft Excel spreadsheet.
            .mp3  - MP3 audio file.
            .mp4  - MP4 video file.
            .zip  - ZIP compressed file.
            .html - HTML file for web pages.
            .exe  - Executable file for Windows systems.
            """
            )
            extension_type = input("\nEnter the desired extension (e.g., .txt):")
            log.info(f"You chose the extension: {extension_type}\n")
            return extension_type
        elif download_kind != "1":
            extension_type = None
            return extension_type
    except Exception as e:
        log.error(f"Error in extension type input: {e}")
        raise


def request_credentials():
    """
    Prompts the user to input FTP connection details and credentials.

    The function requests the following information from the user:
    - Host address (mandatory)
    - Connection port (default is 21)
    - Access username (optional)
    - Access password (optional)

    If the host address is not provided, the function will prompt the user again.
    If the port is not a valid number, the default port (21) will be used.

    Returns:
        tuple: A tuple containing the host address (str), port (int), username (str or None), and password (str or None).

    Raises:
        Exception: If an error occurs during the credential request process.
    """
    try:
        log.info("Fill in the following information to initiate the connection:")

        host = input("Host address (e.g., ftp.example.com):").strip()
        if not host:
            log.info("Host address is mandatory.")
            return request_credentials()

        port = input("Connection port (default is 21):").strip()
        if not port:
            port = 21
        else:
            try:
                port = int(port)
            except ValueError:
                log.info("Port must be a number. Using default (21)")

        log.info("\nFill in credentials, leave blank if not applicable:")

        username = input("Access username:").strip()
        if not username:
            username = None

        password = input("Access password:").strip()
        if not password:
            password = None

        return host, port, username, password
    except Exception as e:
        log.error(f"Error during access credentials request: {e}")
        raise


def initiate_connection(host, port=21, username=None, password=None):
    """
    Initiates an FTP connection to the specified host and port.

    Parameters:
    host (str): The hostname or IP address of the FTP server.
    port (int, optional): The port number to connect to. Defaults to 21.
    username (str, optional): The username for FTP login. Defaults to None for anonymous login.
    password (str, optional): The password for FTP login. Defaults to None for anonymous login.

    Returns:
    FTP: An instance of the FTP connection.

    Raises:
    Exception: If there is an error initiating the connection.

    Logs:
    - Connection establishment details.
    - Login details and current directory.
    - Error details if connection initiation fails.
    """
    try:
        ftp = FTP(timeout=5, encoding="utf-8")
        ftp.connect(host=host, port=port)
        log.info("\n\nConnection established with %s on port %s.", host, port)

        if username or password:
            ftp.login(user=username, passwd=password)
            log.info(f"Logged in as user: {username}. Current directory: %s", ftp.pwd())
        else:
            ftp.login()
            log.info("Anonymous login. Current directory: %s", ftp.pwd())

        return ftp
    except Exception as e:
        log.error("Error initiating connection: %s", e)
        finalize_connection(ftp)
        raise


def _add_information(parts, letter_type, full_directory, navigated_directories, queue):
    """
    Adds directory information to the queue and navigated directories set if the first part
    starts with the specified letter type and the directory has not been navigated yet.

    Args:
        parts (list): A list of parts where the first element is checked against the letter_type.
        letter_type (str): The letter type to check the first part against.
        full_directory (str): The full directory path to be added.
        navigated_directories (set): A set of directories that have already been navigated.
        queue (list): A list representing the queue to which the directory will be added.

    Returns:
        bool: True if the directory was added to the queue and navigated directories, False otherwise.
    """
    if parts[0].startswith(letter_type):
        if full_directory not in navigated_directories:
            queue.append(full_directory)
            navigated_directories.add(full_directory)
            log.info(f"Check performed, information added: type: {letter_type}.")
            return True
    return False


def _download_file(ftp, full_directory):
    """
    Downloads a file from an FTP server and saves it locally.

    Args:
        ftp (ftplib.FTP): An instance of the FTP connection.
        full_directory (str): The full path of the file on the FTP server.

    Raises:
        FileExistsError: If the directory already exists.
        Exception: For any other exceptions that occur during the download process.

    Logs:
        Info: When the file is downloaded successfully.
        Warning: If there is an error during the download process.
    """
    filename = full_directory.split("/")[-1]
    try:
        os.makedirs(os.path.join(current_path, "files"), exist_ok=True)

        with open(os.path.join(current_path, "files", filename), "wb") as local_file:
            ftp.retrbinary(f"RETR {full_directory}", local_file.write)
        log.info(f"File downloaded successfully: {filename}")
    except FileExistsError:
        pass
    except Exception as e:
        log.warning(f"Error downloading file {filename}: {e}")


def _download_file_with_specific_extension(ftp, parts, full_directory, extension_type):
    """
    Downloads a file from an FTP server if it has a specific extension.

    Args:
        ftp (ftplib.FTP): The FTP connection object.
        parts (list): A list of parts of the file path.
        full_directory (str): The full directory path of the file on the FTP server.
        extension_type (str): The file extension to check for.

    Returns:
        None
    """
    if parts[-1].endswith(extension_type):
        _download_file(ftp, full_directory)


def _max_depth():
    """
    Prompts the user to enter the navigation depth level for the application.

    The function provides a default depth level of 3 if no input is given.
    If the user inputs a depth level greater than 15, a confirmation is requested.
    If the user confirms, the entered depth level is returned.
    If the user declines or provides invalid input, the function prompts again or defaults to 3.

    Returns:
        int: The navigation depth level.

    Raises:
        Exception: If an unexpected error occurs during the input process.
    """
    try:
        log.info(
            """\n\nPlease enter the navigation depth level (default is level 3). 
            \nWARNING: Higher numbers increase the risk of connection overload and storage usage."""
        )

        input_depth = input("Please enter the depth level of navigation: ")

        if not input_depth:
            return 3

        max_depth = int(input_depth)

        if max_depth > 15:
            confirm_response = input(
                "Are you sure about this level? Greater than 15? Type '1' for Yes, '2' for No."
            )

            depth_confirmation = int(confirm_response)
            if depth_confirmation == 1:
                return max_depth
            elif depth_confirmation == 2:
                log.info("Please enter a depth level again.")
                return _max_depth()
            else:
                log.info("Invalid input. Depth set to 3 (default).")

            return max_depth
    except ValueError:
        log.info("Invalid input, please respond with a valid number.")
        return _max_depth()
    except Exception as e:
        log.error(f"Error during navigation depth request: {e}")
        raise


def scrape_server(
    ftp,
    download_kind=False,
    extension_type=None,
):
    """
    Scrapes the FTP server directory structure and downloads files based on the specified criteria.

    Args:
        ftp (ftplib.FTP): An active FTP connection object.
        download_kind (bool or str, optional): Determines the type of files to download.
            If False, all files are downloaded. If "1", only files with the specified extension are downloaded.
        extension_type (str, optional): The file extension to filter by when download_kind is "1".

    Raises:
        Exception: If there is an error navigating or collecting server information.

    Logs:
        Various stages of processing, including directory levels, entries checked, and files or directories found.
    """
    max_depth = _max_depth()
    try:
        navigated_directories = set()
        directory_depth = 0
        queue = [""]
        while queue and directory_depth != max_depth:
            log.info(
                f"Processing level {directory_depth}. Directories in queue: {len(queue)}"
            )
            current_path = queue.pop(0)
            try:
                directory_content = []
                ftp.dir(current_path, directory_content.append)

                for info in directory_content:
                    log.info(f"Checking entry: {info}")
                    parts = info.split()
                    name = parts[-1]
                    full_directory = f"{current_path}/{name}".strip("/")
                    if _add_information(
                        parts=parts,
                        letter_type="d",
                        full_directory=full_directory,
                        navigated_directories=navigated_directories,
                        queue=queue,
                    ):
                        log.info(f"Directory found and added: {full_directory}")

                    elif _add_information(
                        parts=parts,
                        letter_type="l",
                        full_directory=full_directory,
                        navigated_directories=navigated_directories,
                        queue=queue,
                    ):
                        log.info(f"Symbolic link found and added: {full_directory}")

                    elif parts[0].startswith("-"):
                        if download_kind != "1":
                            log.info(f"File found: {full_directory}")
                            _download_file(ftp, full_directory)
                        elif download_kind == "1":
                            log.info(f"File found: {full_directory}")
                            _download_file_with_specific_extension(
                                ftp, parts, full_directory, extension_type
                            )

            except Exception as e:
                log.error(f"Error processing {current_path}: {e}")

            directory_depth += 1

        log.info("Processing completed.")
    except Exception as e:
        log.error(f"Error attempting to navigate/collect server information: {e}")


def finalize_connection(ftp):
    """
    Finalizes the FTP connection by quitting the session.

    This function attempts to close the given FTP connection gracefully by calling the `quit` method.
    If an error occurs during this process, it logs an error message.

    Args:
        ftp (ftplib.FTP): The FTP connection object to be closed.

    Raises:
        Exception: If an error occurs while trying to close the connection.
    """
    try:
        if "ftp" in locals():
            ftp.quit()
            log.info("Connection closed successfully!")
    except Exception as e:
        log.error("Error trying to close the connection %s", e)
