using System;
using System.Drawing;
using System.Windows.Forms;
using System.Linq;

class program
{
	static void Main()
	{
		Application.Run(new Form_test());
	}

	class Form_test:Form
	{
		public Label Label_polynomial;
		public Label Label_initial_value;
		public Label Label_final_xor_value;
		public Label Label_input_data;
		public Label Label_output;
		public Button Button_Run;
		public TextBox TextBox_polynomial;
		public TextBox TextBox_initial_value;
		public TextBox TextBox_final_xor_value;
		public RichTextBox TextBox_input_data_array;
		public TextBox TextBox_output;
		byte generator_polynomial;
		/*NG
		public byte[] crc8_look_up_table;
		new byte[256] crc8_look_up_table;
		OK */
		byte[] crc8_look_up_table = new byte[256];
	
		public Form_test()
		{
			this.Text = "CRC8 calculation";

			// Polynomial
			Label_polynomial = new Label();
			Label_polynomial.Text = "polynomial value";
			Label_polynomial.Location = new System.Drawing.Point(25,25);
			this.Controls.Add(Label_polynomial);
			TextBox_polynomial = new TextBox();
			TextBox_polynomial.Location = new System.Drawing.Point(125,25);
			TextBox_polynomial.Size = new System.Drawing.Size(100,70);
			TextBox_polynomial.Text = "0x1D";
			this.Controls.Add(TextBox_polynomial);
			
			// Initial value
			Label_initial_value = new Label();
			Label_initial_value.Text = "Initial value";
			Label_initial_value.Location = new System.Drawing.Point(25,50);
			this.Controls.Add(Label_initial_value);
			TextBox_initial_value = new TextBox();
			TextBox_initial_value.Location = new System.Drawing.Point(125,50);
			TextBox_initial_value.Size = new System.Drawing.Size(100,70);
			TextBox_initial_value.Text = "0xFF";
			this.Controls.Add(TextBox_initial_value);

			// Final XOR value
			Label_final_xor_value = new Label();
			Label_final_xor_value.Text = "Final XOR value";
			Label_final_xor_value.Location = new System.Drawing.Point(25,75);
			this.Controls.Add(Label_final_xor_value);
			TextBox_final_xor_value = new TextBox();
			TextBox_final_xor_value.Location = new System.Drawing.Point(125,75);
			TextBox_final_xor_value.Size = new System.Drawing.Size(100,70);
			TextBox_final_xor_value.Text = "0xFF";
			this.Controls.Add(TextBox_final_xor_value);

			// Input data value
			Label_input_data = new Label();
			Label_input_data.Text = "Input data";
			Label_input_data.Location = new System.Drawing.Point(25,100);
			this.Controls.Add(Label_input_data);
			TextBox_input_data_array = new RichTextBox();
			TextBox_input_data_array.Location = new System.Drawing.Point(25,125);
			TextBox_input_data_array.Size = new System.Drawing.Size(200,50);
			TextBox_input_data_array.Text = "0x11, 0x22, 0x33, 0x44";
			this.Controls.Add(TextBox_input_data_array);

			// Output
			Label_output = new Label();
			Label_output.Text = "Checksum value:";
			Label_output.Location = new System.Drawing.Point(25,190);
			this.Controls.Add(Label_output);
			TextBox_output = new TextBox();
			TextBox_output.Location = new System.Drawing.Point(125,190);
			TextBox_output.Size = new System.Drawing.Size(75,75);
			TextBox_output.Text = "Result";
			this.Controls.Add(TextBox_output);
			
			Button_Run = new Button();
			Button_Run.Text = "Run";
			Button_Run.Size = new System.Drawing.Size(75,25);
			Button_Run.Location = new System.Drawing.Point(50,225);
			Button_Run.Click += new EventHandler(Button_Pressed);
			this.Controls.Add(Button_Run);
		}
		
		public void Button_Pressed(object sender, EventArgs e)
		{
			byte check_sum_result;
			calculate_crc_table();
			check_sum_result = calculate_crc8();

		 //TextBox_output.Text = String.Format("index {0}",crc8_look_up_table[1]);
		 TextBox_output.Text = String.Format("0x{0:X2}",check_sum_result);
		}
		
		public void calculate_crc_table()
		{
		 //crc8_look_up_table = new byte[256]; Define moved to public.
		 generator_polynomial = Convert.ToByte(TextBox_polynomial.Text,16);
		    /* Repeat for all byte values of 0 - 255 */
			for (int dividend = 0; dividend < 256; dividend++)
			{
				byte current_Byte = (byte)dividend;
				/* calculate the CRC-8 value for current byte */
				for (byte bit = 0; bit < 8; bit++)
				{
					if ((current_Byte & 0x80) != 0)
					{
						current_Byte <<= 1;
						current_Byte ^= generator_polynomial;
					}
					else
					{
						current_Byte <<= 1;
					}
				}
				/* 256 current_byte remainder values are matching with 256 patterns of XOR calculation result in CRC calculation) */
				crc8_look_up_table[dividend] = current_Byte;
			}			
		}
		
		public byte calculate_crc8()
		{
			byte Checksum = 0;
			string inputString; 
			inputString = TextBox_input_data_array.Text; //= "0x01, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99";
			
			// カンマで区切って各16進数値を取得し、前後のスペースを削除
            string[] hexValues = inputString.Split(',')
                .Select(value => value.Trim())
                .ToArray();
			
			// 各16進数値を整数に変換
            byte[] byteValues = hexValues.Select(value => Convert.ToByte(value, 16)).ToArray();
			
			// バイト配列を作成
            byte[] Message_Data = new byte[byteValues.Length];
            Array.Copy(byteValues, Message_Data, byteValues.Length);
			
			//int data_size = 5;
			//byte[] Message_Data = new byte[data_size];
			//byte[] Message_Data = { 0x01, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,0x88,0x99 };
			
			int length = Message_Data.Length;
			byte Initial_Value;
			byte Final_XOR_Value;
			
			Initial_Value = Convert.ToByte(TextBox_initial_value.Text,16);
			Final_XOR_Value = Convert.ToByte(TextBox_final_xor_value.Text,16);
			
			Checksum = Initial_Value;

			for (int i = 0; i < length; i++)
			{
				Checksum = crc8_look_up_table[Checksum ^ Message_Data[i]];
			}

			Checksum = (byte)(Checksum ^ Final_XOR_Value);
			return Checksum;
		}
		
	}
}
