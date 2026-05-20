# -*- coding: utf-8 -*-
"""CRC Calculation Tool — Streamlit web app."""

from __future__ import annotations

import streamlit as st

import CRC_calculation as crc_module
from crc_utils import parse_hex_input, parse_hex_int, xor_hex_strings

APP_VERSION = 'CRC Tool Web - Version 250521'
CRC_PRESETS = {
    'CRC8': {
        'polynomial': '0x1D',
        'initial': '0x00',
        'final_xor': '0x00',
        'example_input': '0xFF, 0xFF, 0xFF',
        'example_note': '例: 0xFF×3 → Checksum **0x8B**（poly=0x1D, init/xor=0x00）',
    },
    'CRC16': {
        'polynomial': '0x1021',
        'initial': '0x00',
        'final_xor': '0x00',
        'example_input': (
            '0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39'
        ),
        'example_note': (
            '例: ASCII "123456789" → Checksum **0x31C3**'
            '（poly=0x1021, init/xor=0x00）'
        ),
    },
}
HELP_URL = 'https://www.sunshine2k.de/coding/javascript/crc/crc_js.html'


def apply_crc_preset(crc_type: str) -> None:
    preset = CRC_PRESETS[crc_type]
    st.session_state.polynomial = preset['polynomial']
    st.session_state.initial = preset['initial']
    st.session_state.final_xor = preset['final_xor']
    st.session_state.input_data = preset['example_input']


def on_crc_type_change() -> None:
    apply_crc_preset(st.session_state.crc_type)

st.set_page_config(
    page_title='CRC Calculation Tool',
    page_icon='🔢',
    layout='wide',
)

st.title('CRC Calculation Tool')
st.caption(APP_VERSION)

tab_crc, tab_xor, tab_help = st.tabs(['CRC 計算', '2値 XOR', '使い方'])

with tab_crc:
    col_params, col_result = st.columns([1, 1])

    with col_params:
        if 'crc_type' not in st.session_state:
            st.session_state.crc_type = 'CRC8'
            apply_crc_preset('CRC8')

        crc_type = st.selectbox(
            'CRC Type',
            ['CRC8', 'CRC16'],
            key='crc_type',
            on_change=on_crc_type_change,
        )
        st.caption(CRC_PRESETS[crc_type]['example_note'])

        st.text_input('Polynomial Value', key='polynomial')
        st.text_input('Initial Value', key='initial')
        st.text_input('Final XOR Value', key='final_xor')
        st.text_area('Input Data (Hex)', height=220, key='input_data')

        run = st.button(
            'Run Calculation',
            type='primary',
            use_container_width=True,
        )

    with col_result:
        st.subheader('Calculation Result')
        result_placeholder = st.empty()
        st.subheader('Used look-up table')
        lut_placeholder = st.empty()

    if run:
        polynomial = st.session_state.polynomial
        initial = st.session_state.initial
        final_xor = st.session_state.final_xor
        input_data = st.session_state.input_data
        try:
            poly_val = parse_hex_int(polynomial)
            init_val = parse_hex_int(initial)
            xor_val = parse_hex_int(final_xor)
        except ValueError as exc:
            st.error(f'Parameter error: {exc}')
        else:
            parsed, warnings = parse_hex_input(input_data)
            if not parsed:
                st.warning('No valid input data. Enter at least one hex value.')
            else:
                crc = crc_module.CRC(crc_type, poly_val, init_val, xor_val)
                crc.calculate_crc_look_up_table()
                crc_value = crc.main_crc_calculation(parsed)

                if crc_value == 'invalid':
                    result_placeholder.error('Invalid CRC type.')
                else:
                    width = 2 if crc_type == 'CRC8' else 4
                    hex_result = f'0x{format(crc_value, f"0{width}X")}'
                    result_placeholder.metric('Checksum', hex_result)
                    result_placeholder.caption(f'Decimal: {crc_value}')

                    lut_text = (
                        (warnings + '\n\n' if warnings else '')
                        + f'{crc_type} with polynomial {polynomial}\n'
                        + crc.format_lookup_table()
                    )
                    lut_placeholder.text_area(
                        'Look-up table',
                        lut_text,
                        height=400,
                        label_visibility='collapsed',
                    )

with tab_xor:
    st.markdown('2つの16進文字列を、同じ桁数でニブル単位に XOR します。')
    c1, c2 = st.columns(2)
    with c1:
        val1 = st.text_input('First value (hex)', placeholder='A1B2')
    with c2:
        val2 = st.text_input('Second value (hex)', placeholder='C3D4')

    if st.button('XOR', type='primary'):
        joined, err = xor_hex_strings(val1, val2)
        if err:
            st.error(err)
        else:
            st.success(f'Result: `{joined}`')
            st.json({'nibbles': list(joined), 'joined': joined})

with tab_help:
    st.markdown(
        f"""
### CRC 計算
- 入力データは **16進** で、カンマまたは改行で区切ります。
- **CRC Type** を変更すると、多項式・初期値・Final XOR・入力例が自動で切り替わります。
- 空のカンマ区切りや不正な値は警告として無視されます。

**例**
```
0xFF, 0xFF, 0xFF
```
```
0xFF
0xFF
0xFF
```

### 参考
技術的な背景は次のページを参照してください。  
[{HELP_URL}]({HELP_URL})

### デスクトップ版
従来の Tkinter GUI は `CRC_Calculation_GUI_main.py` から起動できます（要: customtkinter）。
"""
    )
