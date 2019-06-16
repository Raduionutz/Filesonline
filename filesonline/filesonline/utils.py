import os

import pyAesCrypt

from filesonline.settings import encrypt_password, encrypt_bufferSize

from filesonline.settings import (IMAGE_EXTENSIONS, AUDIO_EXTENSIONS, VIDEO_EXTENSIONS,
    EXCEL_EXTENSIONS, WORD_EXTENSIONS, POWERPOINT_EXTENSIONS, PDF_EXTENSIONS,
    CODING_EXTENSIONS, ARCHIVE_EXTENSIONS)


def get_user_encrypt_password(user):

    e_p = encrypt_password
    u_e_p = user.user_profile.enc_pass

    return ''.join([chr(ord(e_p[i]) + ord(u_e_p[i % len(u_e_p)])) for i in range(len(e_p))])


def encrypt_file(file_path, user):
    new_path = file_path + '.enc'
    pyAesCrypt.encryptFile(file_path, new_path, get_user_encrypt_password(user), encrypt_bufferSize)

    return new_path


def decrypt_file(encrypted_path, user):
    dec_path = encrypted_path[:-4]
    pyAesCrypt.decryptFile(encrypted_path, dec_path, get_user_encrypt_password(user), encrypt_bufferSize)

    return dec_path


def find_good_name(path):
    i = 2

    base, ext = os.path.splitext(path)
    test_name = base + ' ({})'.format(i) + ext
    while os.path.exists(test_name):
        i += 1
        test_name = base + ' ({})'.format(i) + ext
    path = test_name

    return path, i


def get_file_type(ext):

    if ext in AUDIO_EXTENSIONS:
        return 'audio'

    if ext in IMAGE_EXTENSIONS:
        return 'image'

    if ext in VIDEO_EXTENSIONS:
        return 'video'

    if ext in EXCEL_EXTENSIONS:
        return 'excel'

    if ext in WORD_EXTENSIONS:
        return 'word'

    if ext in POWERPOINT_EXTENSIONS:
        return 'power'

    if ext in PDF_EXTENSIONS:
        return 'pdf'

    if ext in CODING_EXTENSIONS:
        return 'code'

    if ext in ARCHIVE_EXTENSIONS:
        return 'archive'

    return 'file'
