"""The zippee-ki-yay module provides the Python interfaces to extract namelist from a zip archive without the need to download it first.
 Acknowledgements for inspiration goes to https://betterprogramming.pub/how-to-know-zip-content-without-downloading-it-87a5b30be20a

"""

__author__ = ("Bernhard Lehner <https://github.com/berni-lehner>")


import io
import struct
import requests
from zipfile import ZipFile
from pathlib import Path

#_RESPONSE_STATUS_OK = 200
_RESPONSE_PARTIAL_CONTENT = 206
#_RESPONSE_RANGE_NOT_SATISFIABLE = 416

#from https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
_ZIP_EOCD_RECORD_SIZE = 22
_ZIP64_EOCD_LOCATOR_SIZE = 20
_ZIP64_EOCD_RECORD_SIZE = _ZIP_EOCD_RECORD_SIZE + _ZIP64_EOCD_LOCATOR_SIZE + 56


def _decode_little_endian(le_bytes) -> int:
    assert len(le_bytes) == 4
    
    result = struct.unpack("<" + "i", le_bytes)[0]
    
    return result


def _decode_little_endian64(le_bytes) -> int:
    assert len(le_bytes) == 8

    result = struct.unpack("<" + "q", le_bytes)[0]
    
    return result


def _fetch_partial(url, from_: int, to_: int):
    response = requests.get(url, headers={'Range': f'bytes={from_}-{to_}'})

    assert response.status_code == _RESPONSE_PARTIAL_CONTENT

    return response.content


def _fetch_filesize(url) -> int:
    file_size = int(requests.head(url).headers['Content-Length'])
    
    return file_size


def _get_zip_info(url) -> ZipFile:
    file_size = _fetch_filesize(url)

    cd_size = -1
    cd_start = -1
    meta_info = None
    zip_eocd_record = None
    zip64_eocd_locator = None
    zip64_eocd_record = _fetch_zip64_eocd_record(url, file_size)
    
    # let's see if the signature of the record indicates a zip64 format
    if _is_zip64(zip64_eocd_record):
        zip64_eocd_locator = _fetch_zip64_eocd_locator(url, file_size)
        cd_size = _decode_little_endian64(zip64_eocd_record[40:48])
        cd_start = _decode_little_endian64(zip64_eocd_record[48:56])
        meta_info = zip64_eocd_record + zip64_eocd_locator
    else:
        zip64_eocd_record = None
        zip_eocd_record = _fetch_zip_eocd_record(url, file_size)
        cd_size = _decode_little_endian(zip_eocd_record[12:16])
        cd_start = _decode_little_endian(zip_eocd_record[16:20])
        meta_info = zip_eocd_record
 
    # fetch central directory (CD) entry
    from_ = cd_start
    to_ = from_ + cd_size - 1
    cd = _fetch_partial(url, from_, to_)

    # open CD+EOCD bytes as an empty zip file
    zfile_info = ZipFile(io.BytesIO(cd + meta_info))

    return zfile_info


# Signature values begin with the two byte constant marker of 0x4b50, representing the characters "PK".
def _check_signature(signature) -> bool:
    assert len(signature) == 2, "signature needs to be two bytes long"

    codecs = ["utf-8"]

    signature_ok = False
    def try_decode(text):
        for codec in codecs:
            try:
                return text.decode(codec)
            except UnicodeError:
                continue
    
    signature_ok = try_decode(signature) == 'PK'

    return signature_ok


def _fetch_zip_eocd_record(url, file_size: int) -> bytes:
    #end of central directory (EOCD) record is located at the end of the zip        
    from_ = file_size - _ZIP_EOCD_RECORD_SIZE
    to_ = file_size - 1
    eocd_record = _fetch_partial(url, from_, to_)
    
    assert len(eocd_record) == _ZIP_EOCD_RECORD_SIZE

    return eocd_record


def _fetch_zip64_eocd_record(url, file_size: int) -> bytes:
    from_ = file_size - _ZIP64_EOCD_RECORD_SIZE
    to_ = file_size - 1

    zip64_eocd_record = _fetch_partial(url, from_, to_)

    assert len(zip64_eocd_record) == _ZIP64_EOCD_RECORD_SIZE
    
    return zip64_eocd_record


def _fetch_zip64_eocd_locator(url, file_size: int) -> bytes:
    from_ = file_size - (_ZIP_EOCD_RECORD_SIZE + _ZIP64_EOCD_LOCATOR_SIZE)
    to_ = from_ + _ZIP64_EOCD_LOCATOR_SIZE - 1
    zip64_eocd_locator = _fetch_partial(url, from_, to_)
    
    assert len(zip64_eocd_locator) == _ZIP64_EOCD_LOCATOR_SIZE
    
    return zip64_eocd_locator
    


def _is_zip64(zip64_eocd_record) -> bool:
    is_zip64 = _check_signature(zip64_eocd_record[0:2])

    return is_zip64


def namelist(url: Path):
    nl = _get_zip_info(url).namelist()

    return nl
