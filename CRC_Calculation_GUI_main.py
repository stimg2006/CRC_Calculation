# -*- coding: utf-8 -*-
"""
@author: FUJIIK
"""
import os
from logging import getLogger, FileHandler, StreamHandler, DEBUG, INFO, Formatter
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, scrolledtext
import customtkinter as ctk
# Locally developed modules
import CRC_calculation as crc_module

Module_version_string = 'CRC Tool - Version 250425_2'
Base_file_name = os.path.basename(__file__)
Font_MainWindow = ('tahoma',11)
Font_SubHelpWindow = ('calibri',11)

def CHECK_SUM_CALCULATION():
    try:
        crc_type = str(combo_box_crc_type.get())
        polynomial_value = int(Entry_polynomial_text.get(),16)
        print(f'polynomial_value = {polynomial_value}')
        initial_value = int(Entry_initial_text.get(),16)
        final_xor_value = int(Entry_final_xor_text.get(),16)
    except Exception as e:
        messagebox.showwarning(title="Error", message=f'Returned Message:{e}')
        print(f'error :{e}')
        return
    
    user_warning_text = ''
    data_index = 0
    list_input_data = []
    texts = ScrolledText_input_data.get('1.0',tk.END)  # Fiterを追加したのでParsing Dataから選択信号のScrolledTextに変更
    list_lines = texts.splitlines()
        
    for i,line in enumerate(list_lines):
        if (line != ''):
            if(',' in str(line)):
                string_list = line.split(',')
                
                for value in string_list:
                    data_index += 1
                    
                    if(value == ''):
                        user_warning_text += f'Warning(data index={data_index}): Empty data"" is automatically ignored.\n'
                    else:
                        try:
                            value = int(value,16)
                            list_input_data.append(value)
                        except Exception as e:
                            user_warning_text += (f'Warning(data index={data_index}):' + str(e) + '\n')
            else:
                try:                
                    value = int(line,16)
                    list_input_data.append(value)
                except Exception as e:
                    user_warning_text += ('Warning:' + str(e) + '\n')
    
    if(user_warning_text != ''):
        user_warning_text += '\n'
    
    CRC_Class = crc_module.CRC(crc_type,polynomial_value, initial_value, final_xor_value)
    # List_look_up_table = []
    # List_look_up_table = crc_module.calculate_crc_look_up_table(0x1D)
    # return_crc_value = crc_module.main_crc_calculation(list_input_data, initial_value, final_xor_value, List_look_up_table)
    List_look_up_table = CRC_Class.calculate_crc_look_up_table(verbose=True)
    return_crc_value = CRC_Class.main_crc_calculation(list_input_data, verbose=True)
    
    if (return_crc_value != 'invalid'):
        print(f'Checksum(decimal):{return_crc_value}')
        print(f'Checksum:0x{str(format(return_crc_value,"02X"))}')
        Entrytext_crc_result.set(f'0x{str(format(return_crc_value,"02X"))}')
        
        scrolled_text_output = (
            user_warning_text
            + CRC_Class.crc_type
            + ' with polynomial '
            + str(CRC_Class.polynomial_value)
            + '\n'
            + CRC_Class.format_lookup_table()
        )
    else:
        Entrytext_crc_result.set('Invalid')
        scrolled_text_output = 'No table created! Non user define function'
    
    
    ScrolledText_used_look_up_table.delete('1.0',tk.END)
    ScrolledText_used_look_up_table.insert('1.0',scrolled_text_output)

def INIT_SUB_WINDOW_CONFIGS():
    global v_help_sub_window
    v_help_sub_window = None           # Help Sub Window用のGlobal宣言


def OPEN_HELP_WINDOW(help_info_type = 'help_text', direct_text_option = 'None'):
    global v_help_sub_window, ScrolledText_help
    
    if v_help_sub_window != None:
        v_help_sub_window.destroy()
    if v_help_sub_window == None or not v_help_sub_window.winfo_exists():
        v_help_sub_window = tk.Toplevel()
        v_help_sub_window.geometry('810x500')
        width_of_scroll_text = 110
        height_of_scroll_text = 23
        
        if help_info_type == 'help_text' :
            v_help_sub_window.title("Help: How to use")
            texts = \
                f'This tool is to calculate CRC. Opens from {Base_file_name}\n'\
                '\n'\
                'Following web page has necessary technical information. \n'\
                '       URL: https://www.sunshine2k.de/coding/javascript/crc/crc_js.html \n'\
                '\n'\
                'Please input your data into "Input Data" box in Hex value. \n'\
                'Each data should be separated by either ","(comma) or line change.\n'\
                '<e.g.>.\n'\
                '  Example 1)\n'\
                '    0xFF, 0xFF, 0xFF\n'\
                '\n'\
                '  Example 2) \n'\
                '    0xFF \n'\
                '    0xFF \n'\
                '    0xFF \n'\
                '\n'\
                '  Example 3) \n'\
                '    0xFF, 0xFF \n'\
                '    0xFF \n'\
                '<Input Rules> \n'\
                '  * If data separate by "," is empty(""), then automatically ignored (With warning message).\n'\
                '  * If data separate by "," is not numeric, then automatically ignored (With warning message).\n'\
                '\n'\
                'This tool usually opens with command prompt at background. \n'\
                f'If you want to open without it, you may change file name ({Base_file_name}) \n'\
                'from *.py file name to *.pyw and restart program. \n'\
                'Then main tool opens without command prompt at background.'\
            
  	    # ヘルプテキスト表示用のラベル        
        ScrolledText_help = scrolledtext.ScrolledText(v_help_sub_window, font=Font_SubHelpWindow, height = height_of_scroll_text,width = width_of_scroll_text,state="normal", relief ="flat" )
        ScrolledText_help.insert(tk.END, texts)
        ScrolledText_help.grid(row=0,column=0, rowspan=3, padx=10, pady=10) 
        ScrolledText_help.configure(state="disabled")
    	# Close File Sub Window用のボタン
        button_close_help_subw = ttk.Button(v_help_sub_window, text='Close', padding = [5,5,5] , command=v_help_sub_window.destroy)
        button_close_help_subw.grid(row=3,column=0,padx=10,pady=5)    
    v_help_sub_window.focus()

def INIT_MENU():
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    # "File"メニュー設定
    menu_file = tk.Menu(menubar,tearoff=False,font=Font_MainWindow)
    menubar.add_cascade(label='File', menu=menu_file)
    menu_file.add_command(label='Close', command = root.destroy) # Previous :root.destroy :Post runを追加した。
    # "Help"メニュー設定
    menu_help = tk.Menu(menubar,tearoff=False,font=Font_MainWindow)
    menubar.add_cascade(label='Help', menu=menu_help)
    menu_help.add_command(label='How-Tos', command = lambda help_type = 'help_text', add_opt = 'None':OPEN_HELP_WINDOW(help_type,add_opt))

def COMBO_CRC_TYPE_CHANGE(choice):
    if(choice == 'CRC8'):
        Entrytext_polynomial.set('0x1D')
    elif (choice == 'CRC16'):
        Entrytext_polynomial.set('0x1021')
    # else:
    #     Entrytext_polynomial.set('no value defined')

def IS_NUM_FUNCTION(num):
    try:
        float(num)
    except ValueError:
        return False
    else:
        return True

if __name__ == '__main__': # Create a Tkinter window
    global root
# Loggerの準備
    Logger = getLogger(__name__)
    Logger.setLevel(DEBUG)
    Streamhandler = StreamHandler()
    Streamhandler.setLevel(DEBUG)
    Filehandler = FileHandler('CRC_Tool_log.txt')
    Filehandler.setLevel(INFO)
    Logger_file_out_formatter = Formatter('[%(levelname)s] %(asctime)s - %(message)s [%(filename)s]')
    Filehandler.setFormatter(Logger_file_out_formatter)
    Logger.addHandler(Streamhandler)    
    Logger.addHandler(Filehandler)

# Tkinter Applicationの土台(root object)を準備
    root = tk.Tk()
    root.title(Module_version_string)
    root.geometry('500x600') # 'Hrizontal size x Vertical Size' in pixcel (Arg Example: '800x600').
    INIT_MENU()
    INIT_SUB_WINDOW_CONFIGS()
    root_row_num = 0
    frame_row_num = 0
    
    Parameter_frame = ctk.CTkFrame(root)
    InOut_frame = ctk.CTkFrame(root)
    Parameter_frame.propagate(False) # フレームサイズの自動調整ONを明示する
    InOut_frame.propagate(False) # フレームサイズの自動調整ONを明示する
    
    Parameter_frame.grid(row=root_row_num,column=0,sticky='nsew', padx=0, pady = 0)
    root_row_num +=1
    InOut_frame.grid(row=root_row_num,column=0,sticky='nsew', padx=0, pady = 0)
    
# Parameter Frame >>>    
    # CRC Type用Widget
    Label_crc_type = ctk.CTkLabel(Parameter_frame, text = 'CRC Type selection:',anchor='w')
    Label_crc_type.grid(row=frame_row_num,column=0, padx=10, pady=2)
    List_crc_type = ['CRC8','CRC16']
    combo_box_crc_type = ctk.CTkComboBox(Parameter_frame,values=List_crc_type, width = 100, command=COMBO_CRC_TYPE_CHANGE)
    combo_box_crc_type.grid(row=frame_row_num,column=1,padx=15,pady=5)
    combo_box_crc_type.set('CRC8')
    frame_row_num += 1
    
    # Polynomial Value用Widget
    Entrytext_polynomial = tk.StringVar()
    Entrytext_polynomial.set('0x1D')    
    Label_polynomial = ctk.CTkLabel(Parameter_frame, text = 'Polynomial Value:',anchor='w')
    Label_polynomial.grid(row=frame_row_num,column=0, padx=10, pady=2)
    Entry_polynomial_text = ctk.CTkEntry(Parameter_frame,textvariable=Entrytext_polynomial, width = 100)
    Entry_polynomial_text.grid(row=frame_row_num,column=1,padx=10,pady=2)    
    frame_row_num += 1
    
    # Initial Value用Widget
    Entrytext_initial = tk.StringVar()
    Entrytext_initial.set('0x00')
    Label_initial = ctk.CTkLabel(Parameter_frame, text = 'Initial Value:',anchor='w')
    Label_initial.grid(row=frame_row_num,column=0, padx=10, pady=2)
    Entry_initial_text = ctk.CTkEntry(Parameter_frame,textvariable=Entrytext_initial, width = 100)
    Entry_initial_text.grid(row=frame_row_num,column=1,padx=10,pady=2)
    frame_row_num += 1
    
    # Final XOR Value用Widget
    Entrytext_final_xor = tk.StringVar()
    Entrytext_final_xor.set('0x00')
    Label_final_xor = ctk.CTkLabel(Parameter_frame, text = 'Final XOR Value:',anchor='w')
    Label_final_xor.grid(row=frame_row_num,column=0, padx=10, pady=2)
    Entry_final_xor_text = ctk.CTkEntry(Parameter_frame,textvariable=Entrytext_final_xor, width = 100)
    Entry_final_xor_text.grid(row=frame_row_num,column=1,padx=10,pady=2)
    frame_row_num += 1
    
    separator = ttk.Separator(Parameter_frame, orient='horizontal')
    separator.grid(row=frame_row_num,column=0,columnspan=3,padx=10,pady=10,sticky='we') 
    frame_row_num += 1
    
    # 結果表示用Widget
    Entrytext_crc_result = tk.StringVar()
    Entrytext_crc_result.set('-')
    Label_calc_result_value = ctk.CTkLabel(Parameter_frame, text = 'Calculation Result:',anchor='w')
    Label_calc_result_value.grid(row=frame_row_num,column=0, padx=10, pady=2)
    Entry_final_calc_result_text = ctk.CTkEntry(Parameter_frame, textvariable=Entrytext_crc_result, width = 100)
    Entry_final_calc_result_text.grid(row=frame_row_num,column=1,padx=10,pady=2)
    
    # 実行ボタン
    button_run_calculation = ttk.Button(Parameter_frame, text='Run Calculation', padding = [3,3,3], width = 20, command=CHECK_SUM_CALCULATION)
    button_run_calculation.grid(row=frame_row_num,column=2,padx=7,pady=2,ipady=7)
    frame_row_num += 1
# Parameter Frame <<<

# Input Output Frame >>>
    frame_row_num = 0
    separator = ttk.Separator(InOut_frame, orient='horizontal')
    separator.grid(row=frame_row_num,column=0,columnspan=3,padx=10,pady=10,sticky='we')
    frame_row_num += 1


    label_left = ctk.CTkLabel(InOut_frame, text = 'Input Data (Hex)')
    label_left.grid(row=frame_row_num,column=0, padx=10, pady=0)
    label_right = ctk.CTkLabel(InOut_frame, text = 'Used look up table')
    label_right.grid(row=frame_row_num,column=1, padx=10, pady=0)
    frame_row_num += 1

    # Input Data用のScrolledText        
    ScrolledText_input_data = ctk.CTkTextbox(InOut_frame, width = 200, height = 200, state="normal", activate_scrollbars=False)
    ScrolledText_input_data.grid(row=frame_row_num,column=0, sticky='news', padx=20, pady=10, ipady=50)
    ScrolledText_input_data.configure(state="normal")

    scrollbar_text_input_data = ctk.CTkScrollbar(ScrolledText_input_data, command=ScrolledText_input_data.yview)
    scrollbar_text_input_data.grid(row=0,column=1, sticky='ns')
    ScrolledText_input_data.configure(yscrollcommand=scrollbar_text_input_data.set) # スクロールバーのWidgetへの接続

    # Look up table出力用のScrolledText              
    ScrolledText_used_look_up_table = ctk.CTkTextbox(InOut_frame, width = 200, height = 200, state="normal", activate_scrollbars=False)
    ScrolledText_used_look_up_table.grid(row=frame_row_num,column=1, sticky='news', padx=20, pady=10, ipady=50)
    ScrolledText_used_look_up_table.configure(state="normal")
    
    scrollbar_text_lut = ctk.CTkScrollbar(ScrolledText_used_look_up_table, command=ScrolledText_used_look_up_table.yview)
    scrollbar_text_lut.grid(row=0,column=1, sticky='ns')
    ScrolledText_used_look_up_table.configure(yscrollcommand=scrollbar_text_lut.set) # スクロールバーのWidgetへの接続
    frame_row_num += 1
# Input Output Frame <<<

    InOut_frame.grid_columnconfigure(0, weight=10)
    InOut_frame.grid_columnconfigure(1, weight=10)
    InOut_frame.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=10)
    root.grid_columnconfigure(0, weight=1)
    
# Run the Tkinter main loop
    root.mainloop()
