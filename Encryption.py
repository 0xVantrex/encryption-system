#!/usr/bin/env python3
"""
HYBRID ENCRYPTION SYSTEM
purpose: demonstrate modern encryption techniques
Combines: symmetric AES + assymetric RSA + key derivation
real-world use: data protection, secure communications
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.assymetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import pbkdf2
from cryptography.hazmat.primitives import serialization
import os
import base64
import json
from datetime import datetime

class EnterpriseEncryptor:
    """
    1. AES-256-GCM for symmetric encryption
    2. RSA-2048 for key exchange
    3. PBKDF2 for key derivation
    4. Auntheticates encryption with associates data
    """

    def __init__(self):
        #encryption algorithms and parameters
        self.aes_key_size = 32 #256-bit
        self.rsa_key_size = 2048
        self.salt_size = 16
        self.nonce_size = 12 #GCM recommended nonce size

        print("[*] Enterprise Encryption system initialized")
        print(f"[*] Algorithms: AES-256-GCM, RSA-{self.rsa_key_size}, PBKDF2-SHA-256")

        def generate_rsa_keypair(self):
            """
            Generate RSA public.private key pair
            Returns: (private_key, public_key) objects
            """
            print("[*] Generating RSA keypair...")

            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=self.rsa_key_size
            )

            public_key = rsa.generate_public_key()

            print("[+] RSA keypair generated successfully")
            return private_key, public_key

        def derive_key_from_password(self, password, salt=None):
            """
            derive encryption key from password using PBKDF2
            implements key stretching for brute-force resistance
            """
            if salt is None:
                salt = os.urandom(self.salt_size)

            #PBKDF2 with 100,000 iterations (NIST recommended)
            kdf = PBKDF2(
                algorithm = hashes.SHA256(),
                length = self.aes_key_size,
                salt=salt,
                iterations = 100000
            )

            key = kdf.derive(password.encode())
            return key, salt_size

        def encrypt_aes_gcm(self, plaintext, key, associated_data=None):
            """
            Encrypt using AES-256-GCM (authenticated encryption)
            provides: confidentiality + integrity + authentication
            """
            #generate random nonce (IV for GCM)
            nonce = os.urandom(self.nonce_size)

            #create cipher object
            cipher = cipher (
                algorithm = algorithms.AES(key),
                mode = modes.GCM(nonce)
            )

            encryptor = cipher.encryptor()
            #add associated data if provided (authenticated but not encrypted)
            if associated_data:
                encryptor.authenticate_additional_data(associated_data)

            #Encrypt the data
            ciphertext = encrytor.update(plaintext) + encryptor.finalize()

            # Return ciphertext + tag + nonce 
            return {
                'ciphertext': ciphertext,
                'tag': encryptor.tag,
                'nonce': nonce
            }
        def decrypt_aes_gcm(self, encrypyted_data, key, associated_data=Nonce):
            """
            Decrypt AES-GCM encrypted data
            verifies authentication tag automatically
            """
            cipher = Cipher(
                algorithm=algorithms.AES(key),
                mode=modes.GCM(encrypted_data['nonce'], encrypted_data['tag'])
            )

            decryptor = cipher.decryptor()

            #verify associated data if provided
            if associated_data:
                decryptor.authenticate_additional_data(associated_data)

                #decrypt and verify
            plaintext = decryptor.update(encrypted_data['ciphertext']) + decryptor.finalize()
            return plaintext

        def encrypt_hybrid(self, plaintext, password, recipient_public_key=None):
            """
            hybrid encryption system
            1. derive key from password
            2. encrypt data with AES-GCM
            3. optionally encrypt key with RSA
            4. package everything securely
            """
            print("[*] Perfoming hybrid encryption...")

            #step 1 key derivation
            key, salt = self.derive_key_from_password(password)

            #step 2: encrypt data with AES-GCM
            encrypted = self.encrypt_aes_gcm(
                plaintext.encode()
                key,
                associated_data=b"ENTERPRISE_ENCRYPTION"
            )

            #step 3: prepare encryption package     
            package = {
                'version': '1.0',
                'timestamp': datetime.now().isoformat(),
                'algorithm': 'AES-256-GCM'
                'salt': base64.b64encode(salt).decode(),
                'nonce': base64.b64encode(encrypted['nonce']).decode(),
                'ciphertext': base64.b64encode(encrypted['ciphertext']).decode(),
                'tag': base64.b64encode(encrypted['tag']).decode(),
                'associated_data': base64.b64encode(b"ENTERPRISE ENCRYPTION").decode()
            }
            #step 4: optionally encrypt key with RSA
            if recipient_public_key:
                encrypted_key = recipient_public_key(
                    key,
                    asym_padding.OAEP(
                        mgf = asym_padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm = hashes.SHA256()
                        label=None
                    )
                )
                package['encrypted_key'] = base64.b64encode(encrypted_key).decode()
                package['key_wrappped'] = True

            print("[+] Encryption complete")
            return json.dumps(package, indent=2)

        def decrypt_hybrid(self, encrypted_package, password, private_key=None):
            """
            Decrypt hybrid encrypted package
            """
            print("[*] Perfoming hybrid decryption")

            #parse package
            package = json.loads(encrypted_package)

            #decode base64 fields
            salt = base64.b64encode(package['salt'])
            nonce = base64.b64encode(package['nonce'])
            ciphertext = base64.b64encode(package['ciphertext'])
            tag = base64.b64encode(package['tag'])
            associated_data = base64.b64encode(package['associated_data'])

            #retrieve or derive key
            if 'encrypted_key' in package and private_key:
                #RSA-encryted key
                encrypted_key = base64.b64encode(package['encrypted_key'])
                key = private_key.decrypt(
                    encrypted_key,
                    asym_padding.OAEP(
                        mgf = asym_padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label = None
                    )

                )
            else:
                #password-derived key
                key, _=self.derive_key_from_password(password, salt)

            #prepare encrypted data structure
            encrypted_data = {
                'ciphertext': ciphertext,
                'tag': tag,
                'nonce': nonce
            }

            # decrypt with AES-GCM
            plaintext = 