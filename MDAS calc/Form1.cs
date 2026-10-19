using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;


namespace MDAS_calc
{
    public partial class Form1 : Form
    {
        double firstNum, secondNum, result;
        public Form1()
        {
            InitializeComponent();
        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void btnSub_Click(object sender, EventArgs e)
        {
            try
            {
                firstNum = double.Parse(txtFirstNum.Text);
                secondNum = double.Parse(txtSecondNum.Text);


                result = firstNum - secondNum;


                txtResult.Text = result.ToString();
            }
            catch
            {
                MessageBox.Show("Enter a valid number", "MDAS error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                txtFirstNum.Text = string.Empty;
                txtSecondNum.Text = string.Empty;
                txtResult.Text = string.Empty;
                txtFirstNum.Focus();
            }
        }

        private void btnMul_Click(object sender, EventArgs e)
        {
            try
            {
                firstNum = double.Parse(txtFirstNum.Text);
                secondNum = double.Parse(txtSecondNum.Text);


                result = firstNum * secondNum;


                txtResult.Text = result.ToString();
            }
            catch
            {
                MessageBox.Show("Enter a valid number", "MDAS error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                txtFirstNum.Text = string.Empty;
                txtSecondNum.Text = string.Empty;
                txtResult.Text = string.Empty;
                txtFirstNum.Focus();
            }
        }

        private void btnDiv_Click(object sender, EventArgs e)
        {
            try
            {
                firstNum = double.Parse(txtFirstNum.Text);
                secondNum = double.Parse(txtSecondNum.Text);


                result = firstNum / secondNum;


                txtResult.Text = result.ToString();
            }
            catch
            {
                MessageBox.Show("Enter a valid number", "MDAS error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                txtFirstNum.Text = string.Empty;
                txtSecondNum.Text = string.Empty;
                txtResult.Text = string.Empty;
                txtFirstNum.Focus();
            }
        }

        private void btnReset_Click(object sender, EventArgs e)
        {
            txtFirstNum.Text = string.Empty;
            txtSecondNum.Text = string.Empty;
            txtResult.Text = string.Empty;
            txtFirstNum.Focus();
        }

        private void btnExit_Click(object sender, EventArgs e)
        {
            DialogResult iExit = MessageBox.Show("Are you sure you want to exit?", "Exit MDAS calc", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
            if (iExit == DialogResult.Yes) {
                Application.Exit();
            }

        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            try
            {
                firstNum = double.Parse(txtFirstNum.Text);
                secondNum = double.Parse(txtSecondNum.Text);


                result = firstNum + secondNum;


                txtResult.Text = result.ToString();
            }
            catch
            {
                MessageBox.Show("Enter a valid number", "MDAS error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                txtFirstNum.Text = string.Empty;
                txtSecondNum.Text = string.Empty;
                txtResult.Text = string.Empty;
                txtFirstNum.Focus();
            }
        }
    }
}
