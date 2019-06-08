import os

import pyAesCrypt

from filesonline.settings import encrypt_password, encrypt_bufferSize


def encrypt_file(file_path):
    new_path = file_path + '.enc'
    pyAesCrypt.encryptFile(file_path, new_path, encrypt_password, encrypt_bufferSize)

    return new_path


def decrypt_file(encrypted_path):
    dec_path = encrypted_path[:-4]
    pyAesCrypt.decryptFile(encrypted_path, dec_path, encrypt_password, encrypt_bufferSize)

    return dec_path
