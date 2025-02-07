from jwt import decode, InvalidTokenError, DecodeError, get_unverified_header
from tqdm import tqdm

# Define the JWT and dictionary file path within the script
jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZ3Vlc3QifQ.KimmF-GuaVVyqXUm4pqvFrnQFkxnin5qwkrtgQUX4iE"
# path to the password list
dictionary_file_path = "../rockyou.txt"

def is_jwt(jwt):
    parts = jwt.split(".")
    if len(parts) != 3:
        return False

    return True


def read_jwt(jwt):
    if not is_jwt(jwt):
        with open(jwt) as fp:
            jwt = fp.read().strip()

    if not is_jwt(jwt):
        raise RuntimeError("Parameter %s is not a valid JWT" % jwt)

    return jwt


def crack_jwt(jwt, dictionary):
    header = get_unverified_header(jwt)
    with open(dictionary, encoding="utf-8", errors="ignore") as fp:
        for secret in tqdm(fp, desc="Trying secrets"):
            secret = secret.rstrip()

            try:
                decode(jwt, secret, algorithms=[header["alg"]])
                return secret
            except DecodeError:
                # Signature verification failed
                pass
            except InvalidTokenError:
                # Signature correct, something else failed
                return secret


def signature_is_supported(jwt):
    header = get_unverified_header(jwt)
    return header["alg"] in ["HS256", "HS384", "HS512"]


def main():
    jwt_value = read_jwt(jwt)
    if not signature_is_supported(jwt_value):
        print("Error: This JWT does not use a supported signing algorithm")
        return

    print("Cracking JWT %s" % jwt_value)
    result = crack_jwt(jwt_value, dictionary_file_path)
    if result:
        print("Found secret key:", result)
    else:
        print("Key not found")


if __name__ == "__main__":
    main()
