# -*- coding: utf-8 -*-
"""Shared helpers for CRC calculation tools."""

from __future__ import annotations

import re
from typing import List, Tuple


def parse_hex_int(value: str) -> int:
    cleaned = value.strip()
    if cleaned.lower().startswith('0x'):
        cleaned = cleaned[2:]
    return int(cleaned, 16)


def parse_hex_input(text: str) -> Tuple[List[int], str]:
    """Parse comma- or newline-separated hex values."""
    warnings: List[str] = []
    data: List[int] = []
    data_index = 0

    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split(',') if ',' in line else [line]
        for part in parts:
            value = part.strip()
            if not value:
                data_index += 1
                warnings.append(
                    f'Warning(data index={data_index}): Empty data is ignored.'
                )
                continue
            data_index += 1
            try:
                data.append(parse_hex_int(value))
            except ValueError as exc:
                warnings.append(f'Warning(data index={data_index}): {exc}')

    return data, '\n'.join(warnings)


def xor_hex_strings(val1: str, val2: str) -> Tuple[str, str | None]:
    """XOR two equal-length hex strings (nibbles)."""
    s1 = re.sub(r'\s+', '', val1.strip())
    s2 = re.sub(r'\s+', '', val2.strip())
    if len(s1) != len(s2):
        return '', 'Length mismatch. Use the same number of hex digits.'
    try:
        nibbles = [
            format(int(a, 16) ^ int(b, 16), '01X')
            for a, b in zip(s1, s2)
        ]
    except ValueError:
        return '', 'Invalid hex character. Use 0-9 and A-F only.'
    joined = ''.join(nibbles)
    return joined, None
