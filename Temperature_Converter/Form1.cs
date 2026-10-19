using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Temperature_Converter
{
    public partial class Form1 : Form
    {
        int fahrenheit, celcius;


        public Form1()
        {
            InitializeComponent();
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void label4_Click(object sender, EventArgs e)
        {

        }

        private void vsbTemperature_Scroll(object sender, ScrollEventArgs e)
        {

        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            DialogResult iExit;

            iExit = MessageBox.Show("Are you sure you want to exit", "Confirm exit", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);

            if (iExit == DialogResult.No)
            {
                e.Cancel = true;
            }
        }

        private void vsbTemperature_ValueChanged(object sender, EventArgs e)
        {
            fahrenheit = Convert.ToInt32(vsbTemperature.Value);
            lblFahrenheit.Text = fahrenheit.ToString()+"°F";
            celcius = (fahrenheit - 32) * 5 / 9;
            lblCelcius.Text = celcius.ToString()+"°C";
        }
    }
}
