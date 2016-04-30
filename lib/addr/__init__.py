import cass
import hashlib


def Normalize(mail, city='', statecode='', zipcode='', cursor=None):
    a = cass.Address(mail, city, statecode, zipcode)
    out = a.normalize(cursor)

    if not out:
        return None

    key = []
    if 'mail' in out:
        key.append(out['mail'])
    if 'city' in out:
        key.append(out['city'])
    if 'statecode' in out:
        key.append(out['statecode'])
    keystring = ' '.join(key)
    keyhash = hashlib.sha1(keystring).hexdigest()
    out['key'] = keyhash
    return out
