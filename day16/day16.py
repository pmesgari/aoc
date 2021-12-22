"""
620080001611562C8802118E34
1010110010101.....
(+ (+ 10 11) (+ 12 13)))
         +
    +          +
10    11   12    13  

"""


class InputStream:
    def __init__(self, raw):
        self.raw = raw
        self.bits = ''.join(['{0:04b}'.format(int(h, 16)) for h in self.raw])
        # pos holds the position of the next bit to read
        self.pos = 0
        self.expression = ''

    def peek(self):
        if self.pos >= len(self.bits):
            return None
        return self.bits[self.pos]

    def read(self, n):
        result = ''.join(self.bits[self.pos: self.pos + n])
        self.pos += n
        return result

    def read_one_packet(self):
        version = int(self.read(3), 2)
        type_id = int(self.read(3), 2)
        payload = self.read_packet_payload(type_id)
        return (version, type_id, payload)

    def read_packet_payload(self, type_id):
        if type_id == 4:
            return self.read_literal_payload()
        return self.read_operator_payload()

    def read_count_based_operator_payload(self):
        count = int(self.read(11), 2)
        payload = [self.read_one_packet() for _ in range(count)]
        return payload

    def read_size_based_operator_payload(self):
        size = int(self.read(15), 2)
        end = self.pos + size

        packets = []
        while self.pos < end:
            packets.append(self.read_one_packet())

        return packets

    def read_operator_payload(self):
        if self.read(1) == '1':
            return self.read_count_based_operator_payload()
        return self.read_size_based_operator_payload()

    def read_literal_payload(self):
        values = []
        prefix = '1'
        while prefix == '1':
            group = self.read(5)
            values.append(group[1:])
            prefix = group[0]
        return int(''.join(values), 2)


class LiteralValue:
    def __init__(self, version, type_id, val):
        self.version = version
        self.type_id = type_id
        self.val = val

    def display(self):
        print(self.val)


OPERATOR_LABEL = {
    0: '+',
    1: '*',
    2: 'min',
    3: 'max',
    5: '>',
    6: '<',
    7: '='
}


class Operator:
    def __init__(self, version, type_id, payload):
        self.version = version
        self.type_id = type_id
        self.payload = payload
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def display(self):
        for ch in self.children:
            ch.display()
        print(OPERATOR_LABEL.get(self.type_id, 'UNDEFINED'))


def to_tree(packet, parent=None):
    version, type_id, payload = packet
    if type_id == 4:
        return LiteralValue(version, type_id, payload)

    if parent is None and type_id != 4:
        parent = Operator(version, type_id, payload)
    else:
        parent = Operator(version, type_id, payload)

    for p in payload:
        parent.add_child(to_tree(p, parent))
    return parent


def sum_versions(exp_tree):
    total = 0

    Q = [exp_tree]
    while Q:
        node = Q.pop()
        total += node.version
        if node.type_id != 4:
            for ch in node.children:
                Q.append(ch)

    return total


def evaluate(exp_tree):
    total = 0

    if exp_tree.type_id == 4:
        return exp_tree.val

    if exp_tree.type_id == 0:
        for ch in exp_tree.children:
            total += evaluate(ch)

    elif exp_tree.type_id == 1:
        total = 1
        for ch in exp_tree.children:
            total *= evaluate(ch)

    elif exp_tree.type_id == 2:
        values = [evaluate(exp) for exp in exp_tree.children]
        return min(values)

    elif exp_tree.type_id == 3:
        values = [evaluate(exp) for exp in exp_tree.children]
        return max(values)

    elif exp_tree.type_id == 5:
        lhs, rhs = exp_tree.children
        if evaluate(lhs) > evaluate(rhs):
            return 1
        return 0

    elif exp_tree.type_id == 6:
        lhs, rhs = exp_tree.children
        if evaluate(lhs) < evaluate(rhs):
            return 1
        return 0

    elif exp_tree.type_id == 7:
        lhs, rhs = exp_tree.children
        if evaluate(lhs) == evaluate(rhs):
            return 1
        return 0

    return total


input_stream = InputStream('805311100469800804A3E488ACC0B10055D8009548874F65665AD42F60073E7338E7E5C538D820114AEA1A19927797976F8F43CD7354D66747B3005B401397C6CBA2FCEEE7AACDECC017938B3F802E000854488F70FC401F8BD09E199005B3600BCBFEEE12FFBB84FC8466B515E92B79B1003C797AEBAF53917E99FF2E953D0D284359CA0CB80193D12B3005B4017968D77EB224B46BBF591E7BEBD2FA00100622B4ED64773D0CF7816600B68020000874718E715C0010D8AF1E61CC946FB99FC2C20098275EBC0109FA14CAEDC20EB8033389531AAB14C72162492DE33AE0118012C05EEB801C0054F880102007A01192C040E100ED20035DA8018402BE20099A0020CB801AE0049801E800DD10021E4002DC7D30046C0160004323E42C8EA200DC5A87D06250C50015097FB2CFC93A101006F532EB600849634912799EF7BF609270D0802B59876F004246941091A5040402C9BD4DF654967BFDE4A6432769CED4EC3C4F04C000A895B8E98013246A6016CB3CCC94C9144A03CFAB9002033E7B24A24016DD802933AFAE48EAA3335A632013BC401D8850863A8803D1C61447A00042E3647B83F313674009E6533E158C3351F94C9902803D35C869865D564690103004E74CB001F39BEFFAAD37DFF558C012D005A5A9E851D25F76DD88A5F4BC600ACB6E1322B004E5FE1F2FF0E3005EC017969EB7AE4D1A53D07B918C0B1802F088B2C810326215CCBB6BC140C0149EE87780233E0D298C33B008C52763C9C94BF8DC886504E1ECD4E75C7E4EA00284180371362C44320043E2EC258F24008747785D10C001039F80644F201217401500043A2244B8D200085C3F8690BA78F08018394079A7A996D200806647A49E249C675C0802609D66B004658BA7F1562500366279CCBEB2600ACCA6D802C00085C658BD1DC401A8EB136100')
packet = input_stream.read_one_packet()
exp_tree = to_tree(packet)

# print(sum_versions(exp_tree))
print('----Stack Operations----\n')
# exp_tree.display()
print(evaluate(exp_tree))
