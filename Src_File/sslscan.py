import pandas as pd
import OpenSSL
import socket
import tldextract


def get_ssl_info(url):
    tld_parts = tldextract.extract(url)
    top_level_domain = f"{tld_parts.domain}.{tld_parts.suffix}"
    hostname = top_level_domain
    # Create a socket and connect to the host
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, 443))

    # Create an SSL context and wrap the socket with it
    context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_2_METHOD)
    conn = OpenSSL.SSL.Connection(context, s)
    conn.set_tlsext_host_name(hostname.encode())
    conn.set_connect_state()
    conn.do_handshake()

    # Get the SSL information
    peer_cert = conn.get_peer_certificate()
    cipher_used = conn.get_cipher_name()
    tls_version = conn.get_cipher_version()
    subject_name = conn.get_peer_cert_chain()[0].get_subject().CN
    issuer_name = conn.get_peer_cert_chain()[0].get_issuer().CN
    serial_number = conn.get_peer_cert_chain()[0].get_serial_number()
    not_before = conn.get_peer_cert_chain()[0].get_notBefore()
    not_after = conn.get_peer_cert_chain()[0].get_notAfter()
    sig_algorithm = conn.get_peer_cert_chain()[0].get_signature_algorithm()

    # Create a pandas DataFrame with the SSL information
    df = pd.DataFrame({
        'Peer certificate': [peer_cert],
        'Cipher used': [cipher_used],
        'SSL/TLS version': [tls_version],
        'Server subject name': [subject_name],
        'Server issuer name': [issuer_name],
        'Server certificate serial number': [serial_number],
        'Server certificate not valid before': [not_before],
        'Server certificate not valid after': [not_after],
        'Server certificate signature algorithm': [sig_algorithm]
    })

    # Close the SSL connection and the socket
    conn.close()
    s.close()
    print("sslscan")

    return df
