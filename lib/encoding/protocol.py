import mrjob.protocol


class PostgresProtocol(mrjob.protocol.RawProtocol):

    def read(self, line):
        key, value = mrjob.protocol.RawProtocol.read(self, line)
        # keys are always hex sha1
        value = value.decode('unicode_escape').encode('utf_8')
        return (key, value)

    def write(self, key, value):
        # keys are always hex sha1
        value = value.decode('utf_8').encode('unicode_escape')
        return mrjob.protocol.RawProtocol.write(self, key, value)
