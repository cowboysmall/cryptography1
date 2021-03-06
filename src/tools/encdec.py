from gmpy2         import mul, invert, powmod
from Crypto.Cipher import AES
from Crypto.Util   import Counter
from collections   import defaultdict

import http
import common


def many_time_pad_crack(cypher_texts, key_length):
    hits = [defaultdict(int) for _ in range(key_length)]
    key  = [0] * key_length

    for i in range(len(cypher_texts) - 1):
        for j in range(i + 1, len(cypher_texts)):

            count = 0
            for (x, y) in zip(cypher_texts[i][:key_length], cypher_texts[j][:key_length]):

                result = x ^ y
                if result in range(65, 91) + range(97, 123):

                    temp_key = y ^ 32
                    hits[count][temp_key] += 1
                    if key[count] not in hits[count] or hits[count][key[count]] < hits[count][temp_key]:
                        key[count] = temp_key

                    temp_key = x ^ 32
                    hits[count][temp_key] += 1
                    if key[count] not in hits[count] or hits[count][key[count]] < hits[count][temp_key]:
                        key[count] = temp_key

                count += 1

    return key


def aes_decrypt(cypher_text, key, counter_mode = False):
    if counter_mode:
        ctr = Counter.new(128, initial_value = long(cypher_text[:16].encode('hex'), 16))
        aes = AES.new(key, AES.MODE_CTR, counter = ctr)
    else:
        aes = AES.new(key, AES.MODE_CBC, cypher_text[:16])

    return aes.decrypt(cypher_text[16:])


def rsa_decrypt(number, exponent, p, q, N):
    phi_N   = mul(p - 1, q - 1)
    inverse = invert(exponent, phi_N)
    decrypt = powmod(number, inverse, N)

    return hex(decrypt).split('00')[1].decode('hex')


def padding_oracle_decrypt(cypher_text, url, key, block_size = 16):
    cypher_text = common.hex_to_ascii(cypher_text)

    length      = len(cypher_text)
    count       = length // block_size
    D           = [0] * length

    def clear(block):
        return D[:block * block_size] + [0] * (length - (block * block_size))

    def padding(index, pad):
        return [0] * index + [pad] * pad + [0] * block_size

    for block in xrange(count - 1, 0, -1):
        for byte in xrange(block_size - 1, -1, -1):

            index = ((block - 1) * block_size) + byte
            for current in xrange(256):
                D[index] = current

                cleared  = clear(block)
                padded   = padding(index, block_size - byte)
                result   = common.three_xor(cypher_text, cleared, padded)

                if http.make_request(url, key, common.ascii_to_string(result)):
                    break

                if current == 255:
                    D[index] = block_size - byte

    return common.ascii_to_string(D)

