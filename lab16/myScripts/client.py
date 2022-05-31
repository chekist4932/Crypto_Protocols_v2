import json
import socket


def fragmentation(data_to_send):
    if type(data_to_send) is dict:
        return [json.dumps(data_to_send).encode()[x:x + 1024] for x in
                range(0, len(json.dumps(data_to_send).encode()), 1024)]
    elif type(data_to_send) is bytes:
        return [data_to_send[x:x + 1024] for x in
                range(0, len(data_to_send), 1024)]


def client(data_to_send: dict or bytes):
    result = b""
    package_blocks = fragmentation(data_to_send)

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(("localhost", 50544))

    for block in package_blocks:
        client_sock.sendall(block)
        data = client_sock.recv(1024)
        if data.decode() == str(len(package_blocks) - 1):
            client_sock.sendall(b"DataPut")
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                result += data
    client_sock.close()

    return result


r = {'CMSVersion': '1',
     'DigestAlgorithmIdentifiers': 'SHA256',
     'EncapsulatedContentInfo': {'ContentType':
                                'text',
                                'OCTET STRING': '7b22526563697069656e744964223a20323630352c202253657373696f6e4b6579223a202266663236383138333636333634666633313431343465346464336639333735333937623363363734306333623739376565616264323536613138346234323135222c202254696d654d61726b223a202232322d30352d32372d31342d35332d3230227d'},
    'CertificateSet': {
                'publicExponent': 9510135329540294581567159115573253600370920033954789323114548833422489485610968595642667792532204721113834358948539537744450187169533703699614997052280698480995131281751636732001535081616032184947473675441941694457398873324306155406531613817099312382633834835000454552353010046680637870593999843839411665877,
                'N': 57791657265261907410482995972282059695863614691847675687946256832395893048318592333395900045241861519383343301197312886748888972932736978980960744677044194327975193741278993626005021817560452242489851191726475911926922209748236470214500777033716687018430644716945747182230254395995965744533401891221526957027},
 'RevocationInfoChoises': 'NULL',
 'SignerInfos': {'CMSVersion': '1', 'SignerIdentifier': 'Цой Георгий', 'DigestAlgorithmIdentifier': 'SHA256',
                 'SignedAttributes': 'NULL', 'SignatureAlgorithmIdentifier': 'RSAdsi',
                 'SignatureValue': '04c1dc33091f8a47400c5bc0aab1b8051407a511e3df30b32eedcd2a58abd201fc44be8b18364dcad969375f6903a8df49df32e55e710e313e2826a55ed2d086ba98b32b3552aa6647f72423e390a9d833cda329aaeadd2e60509bc64ec7c24ed5209c3cc26a44c33cbfc24c7784de55f6c8f29d0f3f8da8ee4354ebb89beb59',
                 'UnsignedAttributes': {'OBJECT IDENTIFIER': 'signature-time-stamp', 'SET OF AttributeValue': ' '}}}
