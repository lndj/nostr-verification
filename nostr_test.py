from nostr.key import PublicKey
from replit import db

pb = PublicKey.from_npub('npub10dnanfsan5y8q59y5gpv0jpgdntwjkrra0rukctpe3u2wvngfd5s2e7z9g')
print(pb.hex())


# del db['master']
# del db[pb.hex()]

print(db.get('master'))