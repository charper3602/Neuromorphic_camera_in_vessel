namespace Decoder_app
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            pictureBox1 = new PictureBox();
            menuStrip1 = new MenuStrip();
            settingsToolStripMenuItem = new ToolStripMenuItem();
            debugModeToolStripMenuItem = new ToolStripMenuItem();
            fAQToolStripMenuItem = new ToolStripMenuItem();
            coordinateGridToolStripMenuItem = new ToolStripMenuItem();
            solomanReedToolStripMenuItem = new ToolStripMenuItem();
            label2 = new Label();
            textBox3 = new TextBox();
            textBox4 = new TextBox();
            textBox5 = new TextBox();
            button4 = new Button();
            textBox7 = new TextBox();
            label4 = new Label();
            textBox8 = new TextBox();
            textBox10 = new TextBox();
            button5 = new Button();
            ((System.ComponentModel.ISupportInitialize)pictureBox1).BeginInit();
            menuStrip1.SuspendLayout();
            SuspendLayout();
            // 
            // pictureBox1
            // 
            pictureBox1.Image = (Image)resources.GetObject("pictureBox1.Image");
            pictureBox1.InitialImage = (Image)resources.GetObject("pictureBox1.InitialImage");
            pictureBox1.Location = new Point(759, 216);
            pictureBox1.Name = "pictureBox1";
            pictureBox1.Size = new Size(767, 686);
            pictureBox1.TabIndex = 2;
            pictureBox1.TabStop = false;
            pictureBox1.Click += pictureBox1_Click;
            pictureBox1.Paint += pictureBox1_Paint;
            // 
            // menuStrip1
            // 
            menuStrip1.ImageScalingSize = new Size(20, 20);
            menuStrip1.Items.AddRange(new ToolStripItem[] { settingsToolStripMenuItem, debugModeToolStripMenuItem, fAQToolStripMenuItem });
            menuStrip1.Location = new Point(0, 0);
            menuStrip1.Name = "menuStrip1";
            menuStrip1.Size = new Size(3014, 24);
            menuStrip1.TabIndex = 3;
            menuStrip1.Text = "menuStrip1";
            // 
            // settingsToolStripMenuItem
            // 
            settingsToolStripMenuItem.Name = "settingsToolStripMenuItem";
            settingsToolStripMenuItem.Size = new Size(61, 20);
            settingsToolStripMenuItem.Text = "Settings";
            // 
            // debugModeToolStripMenuItem
            // 
            debugModeToolStripMenuItem.Name = "debugModeToolStripMenuItem";
            debugModeToolStripMenuItem.Size = new Size(88, 20);
            debugModeToolStripMenuItem.Text = "Debug Mode";
            // 
            // fAQToolStripMenuItem
            // 
            fAQToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] { coordinateGridToolStripMenuItem, solomanReedToolStripMenuItem });
            fAQToolStripMenuItem.Name = "fAQToolStripMenuItem";
            fAQToolStripMenuItem.Size = new Size(41, 20);
            fAQToolStripMenuItem.Text = "FAQ";
            // 
            // coordinateGridToolStripMenuItem
            // 
            coordinateGridToolStripMenuItem.Name = "coordinateGridToolStripMenuItem";
            coordinateGridToolStripMenuItem.Size = new Size(158, 22);
            coordinateGridToolStripMenuItem.Text = "Coordinate Grid";
            coordinateGridToolStripMenuItem.Click += coordinateGridToolStripMenuItem_Click;
            // 
            // solomanReedToolStripMenuItem
            // 
            solomanReedToolStripMenuItem.Name = "solomanReedToolStripMenuItem";
            solomanReedToolStripMenuItem.Size = new Size(158, 22);
            solomanReedToolStripMenuItem.Text = "Soloman Reed";
            solomanReedToolStripMenuItem.Click += solomanReedToolStripMenuItem_Click;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Segoe UI", 30F);
            label2.Location = new Point(876, 9);
            label2.Name = "label2";
            label2.Size = new Size(499, 54);
            label2.TabIndex = 5;
            label2.Text = "Event Camera Visualization";
            label2.Click += label2_Click;
            // 
            // textBox3
            // 
            textBox3.Location = new Point(1527, 189);
            textBox3.Name = "textBox3";
            textBox3.Size = new Size(532, 23);
            textBox3.TabIndex = 11;
            textBox3.Text = "Live Coord";
            // 
            // textBox4
            // 
            textBox4.Location = new Point(1527, 218);
            textBox4.Name = "textBox4";
            textBox4.Size = new Size(532, 23);
            textBox4.TabIndex = 12;
            textBox4.Text = "Live Velocity";
            textBox4.TextChanged += textBox4_TextChanged;
            // 
            // textBox5
            // 
            textBox5.Font = new Font("Segoe UI", 15F);
            textBox5.Location = new Point(1527, 247);
            textBox5.Multiline = true;
            textBox5.Name = "textBox5";
            textBox5.Size = new Size(535, 315);
            textBox5.TabIndex = 13;
            textBox5.Text = "Frames";
            textBox5.TextChanged += textBox5_TextChanged;
            // 
            // button4
            // 
            button4.Location = new Point(461, 299);
            button4.Name = "button4";
            button4.Size = new Size(255, 79);
            button4.TabIndex = 15;
            button4.Text = "Reset";
            button4.UseVisualStyleBackColor = true;
            button4.Click += button4_Click;
            // 
            // textBox7
            // 
            textBox7.Location = new Point(1532, 580);
            textBox7.Multiline = true;
            textBox7.Name = "textBox7";
            textBox7.Size = new Size(530, 30);
            textBox7.TabIndex = 16;
            textBox7.Text = "Decoded Binary LED1";
            textBox7.TextChanged += textBox7_TextChanged;
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Location = new Point(759, 905);
            label4.Name = "label4";
            label4.Size = new Size(71, 15);
            label4.TabIndex = 17;
            label4.Text = "Stream Data";
            label4.Click += label4_Click;
            // 
            // textBox8
            // 
            textBox8.Location = new Point(921, 112);
            textBox8.Margin = new Padding(3, 2, 3, 2);
            textBox8.Multiline = true;
            textBox8.Name = "textBox8";
            textBox8.Size = new Size(403, 99);
            textBox8.TabIndex = 18;
            textBox8.Text = "Final Output ID Tag";
            textBox8.TextAlign = HorizontalAlignment.Center;
            textBox8.TextChanged += textBox8_TextChanged;
            // 
            // textBox10
            // 
            textBox10.Location = new Point(1532, 632);
            textBox10.Multiline = true;
            textBox10.Name = "textBox10";
            textBox10.Size = new Size(530, 30);
            textBox10.TabIndex = 20;
            textBox10.Text = "Decoded Binary LED2";
            textBox10.TextChanged += textBox10_TextChanged;
            // 
            // button5
            // 
            button5.Location = new Point(461, 189);
            button5.Margin = new Padding(3, 2, 3, 2);
            button5.Name = "button5";
            button5.Size = new Size(255, 88);
            button5.TabIndex = 26;
            button5.Text = "File Stream";
            button5.UseVisualStyleBackColor = true;
            button5.Click += button5_Click;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            AutoScroll = true;
            ClientSize = new Size(3014, 1044);
            Controls.Add(button5);
            Controls.Add(textBox10);
            Controls.Add(textBox8);
            Controls.Add(label4);
            Controls.Add(textBox7);
            Controls.Add(button4);
            Controls.Add(textBox5);
            Controls.Add(textBox4);
            Controls.Add(textBox3);
            Controls.Add(label2);
            Controls.Add(pictureBox1);
            Controls.Add(menuStrip1);
            Icon = (Icon)resources.GetObject("$this.Icon");
            MainMenuStrip = menuStrip1;
            Name = "Form1";
            StartPosition = FormStartPosition.WindowsDefaultBounds;
            Text = "Calibration Screen";
            Load += Form1_Load;
            ((System.ComponentModel.ISupportInitialize)pictureBox1).EndInit();
            menuStrip1.ResumeLayout(false);
            menuStrip1.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion
        private PictureBox pictureBox1;
        private MenuStrip menuStrip1;
        private ToolStripMenuItem settingsToolStripMenuItem;
        private ToolStripMenuItem debugModeToolStripMenuItem;
        private ToolStripMenuItem fAQToolStripMenuItem;
        private Label label2;
        private ToolStripMenuItem coordinateGridToolStripMenuItem;
        private ToolStripMenuItem solomanReedToolStripMenuItem;
        private TextBox textBox3;
        private TextBox textBox4;
        private TextBox textBox5;
        private Button button4;
        private TextBox textBox7;
        private Label label4;
        private TextBox textBox8;
        private TextBox textBox10;
        private Button button5;
    }
}