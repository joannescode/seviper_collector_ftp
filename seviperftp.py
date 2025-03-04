from src.logging import get_logger
from src.seviper import (
    download_extension_kind,
    specify_specific_extension,
    request_credentials,
    initiate_connection,
    scrape_server,
    finalize_connection,
)

log = get_logger()


def main():
    try:
        download_kind = download_extension_kind()
        extension_type = specify_specific_extension(download_kind)
        host, port, username, password = request_credentials()

        ftp = initiate_connection(
            host=host, port=port, username=username, password=password
        )

        scrape_server(
            ftp=ftp,
            download_kind=download_kind,
            extension_type=extension_type,
        )

    except Exception as e:
        log.error("Error while running: %s", e)

    finally:
        finalize_connection(ftp=ftp)


if __name__ == "__main__":
    main()
