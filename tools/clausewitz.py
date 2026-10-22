"""Small lossless-enough reader for static inspection; not an engine validator."""
import re
from dataclasses import dataclass

TOKEN = re.compile(r'#[^\n]*|"(?:\\.|[^"\\])*"|[{}]|[<>!=]=?|[^\s{}=<>!#"]+')

@dataclass
class Entry:
    key: str
    op: str
    value: object

def parse(text):
    tokens = [m.group() for m in TOKEN.finditer(text.lstrip('\ufeff')) if not m.group().startswith('#')]
    pos = 0
    def block(nested=False):
        nonlocal pos
        out = []
        while pos < len(tokens):
            key = tokens[pos]; pos += 1
            if key == '}':
                if not nested: raise ValueError('Unexpected closing brace')
                return out
            if key == '{': raise ValueError('Unexpected opening brace')
            if pos < len(tokens) and tokens[pos] in ('=', '<', '>', '<=', '>=', '!=', '=='):
                op = tokens[pos]; pos += 1
                if pos >= len(tokens): raise ValueError('Missing value')
                val = tokens[pos]; pos += 1
                if val == '{': val = block(True)
                elif val == '}': raise ValueError('Missing value before brace')
                out.append(Entry(key, op, val))
            else:
                out.append(Entry(key, '', None))
        if nested: raise ValueError('Unclosed brace')
        return out
    return block()

def get(entries, key, default=None):
    return next((e.value for e in entries if e.key == key), default)

def dump(entries, depth=0):
    lines = []
    for e in entries:
        prefix = '\t' * depth + e.key
        if isinstance(e.value, list):
            lines += [prefix + ' ' + e.op + ' {', dump(e.value, depth + 1), '\t' * depth + '}']
        else:
            lines.append(prefix + (' ' + e.op + ' ' + str(e.value) if e.op else ''))
    return '\n'.join(lines)

def walk(entries):
    for e in entries:
        yield e
        if isinstance(e.value, list): yield from walk(e.value)
