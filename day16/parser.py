SAMPLE_INPUT = '110100101111111000101000'


class InputStream:
    def __init__(self, raw):
        self.raw = raw
        self.pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.pos += 1
        ch = self.raw[self.pos]
        return ch

    def read_one_packet(self):
        version = self.read(3)
        type_id = self.read(3)
        payload = self.read_packet_payload()
        return (version, type_id, payload)

    def read(self, n):
        result = ''.join(self.raw[self.pos:self.pos + n])
        self.pos += n
        return int(result, 2)

    def read_packet_payload(self):
        group = 0b10000
        values = []
        while group & 0b10000:
            group = self.read(5)
            value = group & 0b01111
            values.append(bin(value))
        result = int(''.join(values), 2)
        return result

    def peek(self):
        return self.raw[self.pos]

    def eof(self):
        return self.pos == len(self.raw)


input_stream = InputStream(SAMPLE_INPUT)
print(input_stream.read_one_packet())
