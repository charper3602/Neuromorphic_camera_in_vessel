namespace Decoder_app

{
    using System;
    using System.Collections.Generic;
    using System.ComponentModel;
    using System.Data;
    using System.Drawing;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Windows.Forms;
    using Emgu.CV.Structure;
    using Emgu.CV;
    using Emgu.CV.Util;
    using Emgu.CV.Dai;
    using System.Drawing.Imaging;
    using System.Drawing;
    using System.Runtime.InteropServices;
    using Emgu.CV.CvEnum;
    using System.Threading;
    using System.Diagnostics.Metrics;

    public partial class Form1 : Form
    {
        bool streamvideo = false;
        static int cameraIDx = 0;
        int counter = 0;
        VideoCapture capture = new VideoCapture();
        bool _streaming;
        PictureBox Intitial = new PictureBox();
        int[,] coord = new int[10, 2];
        int[,] coord3 = new int[10, 2];
        int[,] coord2 = new int[10, 2];
        int[,] velo = new int[10, 2];
        int count3 = 0;
        int frame_counter = 1;
        int[,] frames = new int[1, 2];
        int frame_count2 = 999999;
        int indicator = 0;
        string frame1 = "";
        int indicator3 = 0;
        string bit_text = "";
        int min_previous = 0;
        int bit_counter = 0;
        int indicator4 = 0;
        VectorOfVectorOfPoint contours = new VectorOfVectorOfPoint();
        VectorOfVectorOfPoint contours2 = new VectorOfVectorOfPoint();
        public Form1()
        {
            InitializeComponent();

        }
        private void Form1_Load(object sender, System.EventArgs e)
        {
            _streaming = false;
            Intitial.Image = pictureBox1.InitialImage;
            frame_count2 = 0;
        }
        public static double[] Reed_Soloman_Correction(double[] code_correct_order, int z1, int z2)
        {
            string output;
            double poly_check_1 = (Math.Pow(z1, 5) * code_correct_order[0]) + (Math.Pow(z1, 4) * code_correct_order[1]) + (Math.Pow(z1, 3) * code_correct_order[2]) + (Math.Pow(z1, 2) * code_correct_order[3]) + (z1 * code_correct_order[4]) + code_correct_order[5];
            double poly_check_2 = (Math.Pow(z2, 5) * code_correct_order[0]) + (Math.Pow(z2, 4) * code_correct_order[1]) + (Math.Pow(z2, 3) * code_correct_order[2]) + (Math.Pow(z2, 2) * code_correct_order[3]) + (z2 * code_correct_order[4]) + code_correct_order[5];
            if ((poly_check_1 == 0) && (poly_check_2 == 0))
            {
                output = "No errors";
                return code_correct_order;
            }
            else
            {
                double k1_z1 = -1 * ((Math.Pow(z1, 4) * code_correct_order[1]) + (Math.Pow(z1, 3) * code_correct_order[2]) + (Math.Pow(z1, 2) * code_correct_order[3]) + (z1 * code_correct_order[4]) + code_correct_order[5]) / (Math.Pow(z1, 5));
                double k1_z2 = -1 * ((Math.Pow(z2, 4) * code_correct_order[1]) + (Math.Pow(z2, 3) * code_correct_order[2]) + (Math.Pow(z2, 2) * code_correct_order[3]) + (z2 * code_correct_order[4]) + code_correct_order[5]) / (Math.Pow(z2, 5));
                if (k1_z1 == -0)
                {
                    k1_z1 = 0;
                }
                if (k1_z2 == -0)
                {
                    k1_z2 = 0;
                }
                if (k1_z1 == k1_z2)
                {
                    code_correct_order[0] = k1_z1;
                }
                double k2_z1 = -1 * ((Math.Pow(z1, 5) * code_correct_order[0]) + (Math.Pow(z1, 3) * code_correct_order[2]) + (Math.Pow(z1, 2) * code_correct_order[3]) + (z1 * code_correct_order[4]) + code_correct_order[5]) / (Math.Pow(z1, 4));
                double k2_z2 = -1 * ((Math.Pow(z2, 5) * code_correct_order[0]) + (Math.Pow(z2, 3) * code_correct_order[2]) + (Math.Pow(z2, 2) * code_correct_order[3]) + (z2 * code_correct_order[4]) + code_correct_order[5]) / (Math.Pow(z2, 4));
                if (k2_z1 == -0)
                {
                    k2_z1 = 0;
                }
                if (k2_z2 == -0)
                {
                    k2_z2 = 0;
                }
                if (k2_z1 == k2_z2)
                {
                    code_correct_order[1] = k2_z1;
                }
                double k3_z1 = -1 * ((Math.Pow(z1, 5) * code_correct_order[0]) + (Math.Pow(z1, 4) * code_correct_order[1]) + (Math.Pow(z1, 2) * code_correct_order[3]) + (z1 * code_correct_order[4]) + code_correct_order[5]) / (Math.Pow(z1, 3));
                double k3_z2 = -1 * ((Math.Pow(z2, 5) * code_correct_order[0]) + (Math.Pow(z2, 4) * code_correct_order[1]) + (Math.Pow(z2, 2) * code_correct_order[3]) + (z2 * code_correct_order[4]) + code_correct_order[5]) / (Math.Pow(z2, 3));
                if (k3_z1 == -0)
                {
                    k3_z1 = 0;
                }
                if (k3_z2 == -0)
                {
                    k3_z2 = 0;
                }
                if (k3_z1 == k3_z2)
                {
                    code_correct_order[2] = k3_z1;
                }
                double k4_z1 = -1 * ((Math.Pow(z1, 5) * code_correct_order[0]) + (Math.Pow(z1, 4) * code_correct_order[1]) + (Math.Pow(z1, 3) * code_correct_order[2]) + (z1 * code_correct_order[4]) + code_correct_order[5]) / (Math.Pow(z1, 2));
                double k4_z2 = -1 * ((Math.Pow(z2, 5) * code_correct_order[0]) + (Math.Pow(z2, 4) * code_correct_order[1]) + (Math.Pow(z2, 3) * code_correct_order[2]) + (z2 * code_correct_order[4]) + code_correct_order[5]) / (Math.Pow(z2, 2));
                if (k4_z1 == -0)
                {
                    k4_z1 = 0;
                }
                if (k4_z2 == -0)
                {
                    k4_z2 = 0;
                }
                if (k4_z1 == k4_z2)
                {
                    code_correct_order[3] = k4_z1;
                }
                double k5_z1 = -1 * ((Math.Pow(z1, 5) * code_correct_order[0]) + (Math.Pow(z1, 4) * code_correct_order[1]) + (Math.Pow(z1, 3) * code_correct_order[2]) + (Math.Pow(z1, 2) * code_correct_order[3]) + code_correct_order[5]) / (Math.Pow(z1, 1));
                double k5_z2 = -1 * ((Math.Pow(z2, 5) * code_correct_order[0]) + (Math.Pow(z2, 4) * code_correct_order[1]) + (Math.Pow(z2, 3) * code_correct_order[2]) + (Math.Pow(z2, 2) * code_correct_order[3]) + code_correct_order[5]) / (Math.Pow(z2, 1));
                if (k5_z1 == -0)
                {
                    k5_z1 = 0;
                }
                if (k5_z2 == -0)
                {
                    k5_z2 = 0;
                }
                if (k5_z1 == k5_z2)
                {
                    code_correct_order[4] = k5_z1;
                }
                double k6_z1 = -1 * ((Math.Pow(z1, 5) * code_correct_order[0]) + (Math.Pow(z1, 4) * code_correct_order[1]) + (Math.Pow(z1, 3) * code_correct_order[2]) + (Math.Pow(z1, 2) * code_correct_order[3]) + (code_correct_order[4] * z1)) / (Math.Pow(z1, 0));
                double k6_z2 = -1 * ((Math.Pow(z2, 5) * code_correct_order[0]) + (Math.Pow(z2, 4) * code_correct_order[1]) + (Math.Pow(z2, 3) * code_correct_order[2]) + (Math.Pow(z2, 2) * code_correct_order[3]) + (code_correct_order[4] * z2)) / (Math.Pow(z2, 0));
                if (k6_z1 == -0)
                {
                    k6_z1 = 0;
                }
                if (k6_z2 == -0)
                {
                    k6_z2 = 0;
                }
                if (k6_z1 == k6_z2)
                {
                    code_correct_order[5] = k6_z1;
                }
                return code_correct_order;
            }





        }
        private void DrawRectangle(PaintEventArgs e, int x, int y)
        {
            System.Drawing.Drawing2D.GraphicsPath gp = new System.Drawing.Drawing2D.GraphicsPath();
            Rectangle rc = new Rectangle(x, y, 5, 5);
            gp.AddRectangle(rc);
            System.Drawing.Region r = new System.Drawing.Region(gp);
            Graphics gr = e.Graphics;
            gr.FillRegion(Brushes.OrangeRed, r);
        }


        private void textBox1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                counter = 1;
                MessageBox.Show(textBox1.Text);
                e.Handled = true;
                using (var g = Graphics.FromImage(pictureBox1.Image))
                {

                    string[] inputs = (textBox1.Text).Split(",");
                    g.DrawRectangle(Pens.Red, Int32.Parse(inputs[0]), Int32.Parse(inputs[1]), 10, 10);
                    SolidBrush redBrush = new SolidBrush(Color.Red);
                    g.FillRectangle(redBrush, Int32.Parse(inputs[0]), Int32.Parse(inputs[1]), 10, 10);
                    pictureBox1.Refresh();
                }

            }
            // int x = 504;
            // int y = 371;
            //textBox1.Text = x.ToString()+","+ y.ToString();

            // counter++;
            // label1.Text = counter.ToString();
            // DrawRectangle(e1);
        }
        private void button1_Click(object sender, EventArgs e)
        {


            string[] code_orginal = textBox2.Text.Split(",");
            double[] code_correct_order = new double[6];
            code_correct_order[0] = Int32.Parse(code_orginal[0]);
            code_correct_order[1] = Int32.Parse(code_orginal[5]);
            code_correct_order[2] = Int32.Parse(code_orginal[1]);
            code_correct_order[3] = Int32.Parse(code_orginal[2]);
            code_correct_order[4] = Int32.Parse(code_orginal[3]);
            code_correct_order[5] = Int32.Parse(code_orginal[4]);
            int z1 = 1;
            int z2 = 2;
            string output1 = String.Join(",", Reed_Soloman_Correction(code_correct_order, z1, z2));

            MessageBox.Show(output1);
            // string output = String.Join(",", code_correct_order);
            // MessageBox.Show(output);
            // counter++;
            // label1.Text = counter.ToString();
        }
        private void pictureBox1_Paint(object sender, PaintEventArgs e)
        {




        }
        public static Bitmap VariableThresholdingLocalProperties(Bitmap image, double a, double b)
        {
            int w = image.Width;
            int h = image.Height;

            BitmapData image_data = image.LockBits(
                new Rectangle(0, 0, w, h),
                ImageLockMode.ReadOnly,
                PixelFormat.Format24bppRgb);

            int bytes = image_data.Stride * image_data.Height;
            byte[] buffer = new byte[bytes];
            byte[] result = new byte[bytes];

            Marshal.Copy(image_data.Scan0, buffer, 0, bytes);
            image.UnlockBits(image_data);

            //Get global mean - this works only for grayscale images
            double mg = 0;
            for (int i = 0; i < bytes; i += 3)
            {
                mg += buffer[i];
            }
            mg /= (w * h);

            for (int x = 1; x < w - 1; x++)
            {
                for (int y = 1; y < h - 1; y++)
                {
                    int position = x * 3 + y * image_data.Stride;
                    double[] histogram = new double[256];

                    for (int i = -1; i <= 1; i++)
                    {
                        for (int j = -1; j <= 1; j++)
                        {
                            int nposition = position + i * 3 + j * image_data.Stride;
                            histogram[buffer[nposition]]++;
                        }
                    }

                    histogram = histogram.Select(l => l / (w * h)).ToArray();

                    double mean = 0;
                    for (int i = 0; i < 256; i++)
                    {
                        mean += i * histogram[i];
                    }

                    double std = 0;
                    for (int i = 0; i < 256; i++)
                    {
                        std += Math.Pow(i - mean, 2) * histogram[i];
                    }
                    std = Math.Sqrt(std);

                    double threshold = a * std + b * mg;
                    for (int c = 0; c < 3; c++)
                    {
                        result[position + c] = (byte)((buffer[position] > threshold) ? 255 : 0);
                    }
                }
            }

            Bitmap res_img = new Bitmap(w, h);
            BitmapData res_data = res_img.LockBits(
                new Rectangle(0, 0, w, h),
                ImageLockMode.WriteOnly,
                PixelFormat.Format24bppRgb);
            Marshal.Copy(result, 0, res_data.Scan0, bytes);
            res_img.UnlockBits(res_data);

            return res_img;
        }
        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void coordinateGridToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Hide();
            FAQ ua = new FAQ();
            ua.ShowDialog();
        }

        private void solomanReedToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Hide();
            FAQ ua = new FAQ();
            ua.ShowDialog();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            var h = Graphics.FromImage(pictureBox1.Image);
            h.Clear(Color.Transparent);
            pictureBox1.ImageLocation = @"C:\Users\charp\OneDrive\Desktop\School\403\Grid_image.png";
            DoubleBuffered = true;
            try
            {
                //Open file dialog, allows you to select an image file
                using (OpenFileDialog ofd = new OpenFileDialog() { Filter = "JPG|*.jpg|PNG|*.png|Bitmap|*.bmp", ValidateNames = true, Multiselect = false })
                {

                    if (ofd.ShowDialog() == DialogResult.OK)
                    {
                        PictureBox PictureBox1 = new PictureBox();
                        PictureBox1.Image = Image.FromFile(ofd.FileName);
                        Bitmap myBitmap = new Bitmap(ofd.FileName);
                        // string[,] values = new string[myBitmap.Width, myBitmap.Height];
                        string values_string = "";
                        for (int x = 0; x < myBitmap.Width; x++)
                        {
                            for (int y = 0; y < myBitmap.Height; y++)
                            {
                                // Get the color of a pixel within myBitmap.
                                Color pixelColor = myBitmap.GetPixel(x, y);
                                string pixelColorStringValue =
                                    pixelColor.R.ToString("D3") + " " +
                                    pixelColor.G.ToString("D3") + " " +
                                    pixelColor.B.ToString("D3") + ", ";
                                if (pixelColorStringValue == "255 255 255, ")
                                {
                                    if ((x == myBitmap.Width - 1) && (y == myBitmap.Height - 1))
                                    {
                                        values_string = values_string + x.ToString() + "|" + y.ToString() + "end";

                                    }
                                    else
                                    {
                                        values_string = values_string + x.ToString() + "|" + y.ToString() + ",";
                                    }
                                    using (var g = Graphics.FromImage(pictureBox1.Image))
                                    {

                                        string[] inputs = (textBox1.Text).Split(",");
                                        g.DrawRectangle(Pens.Red, x + (504 / 2), y + (370 / 2), 1, 1);
                                        SolidBrush redBrush = new SolidBrush(Color.Red);
                                        g.FillRectangle(redBrush, x + (504 / 2), y + (370 / 2), 1, 1);
                                        pictureBox1.Refresh();

                                    }
                                }
                                //values[x, y] = pixelColorStringValue;


                            }

                        }
                        if (!File.Exists("Test_rgb.txt")) // If file does not exists
                        {
                            File.Create("Test_rgb.txt").Close(); // Create file
                            using (StreamWriter sw = File.AppendText("Test_rgb.txt"))
                            {
                                sw.WriteLine(values_string); // Write text to .txt file
                                MessageBox.Show("working");

                            }
                        }
                        else // If file already exists
                        {
                            File.WriteAllText("Test_rgb.txt", String.Empty); // Clear file
                            using (StreamWriter sw = File.AppendText("Test_rgb.txt"))
                            {
                                sw.WriteLine(values_string); // Write text to .txt file
                                MessageBox.Show("working");
                            }
                        }




                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Message", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void button3_Click(object sender, EventArgs e)
        {


            if (!_streaming)
            {
                Application.Idle += streaming;

            }
            else
            {
                Application.Idle -= streaming;
                picOutput.Visible = true;

            }
            _streaming = !_streaming;

        }
        private void streaming(object sender, System.EventArgs e)
        {

            textBox5.WordWrap = true;
            textBox6.WordWrap = true;
            string coord4 = "";
            DoubleBuffered = true;
            var image = capture.QueryFrame().ToImage<Gray, byte>();
            ///Bitmap bmp = image.ToBitmap(); //take a picture
            var imageout = capture.QueryFrame().ToImage<Gray, byte>().ThresholdBinary(new Gray(250), new Gray(255));
            var imageout2 = capture.QueryFrame().ToImage<Gray, byte>().ThresholdBinary(new Gray(252), new Gray(255));
            Mat m = new Mat();
            CvInvoke.FindContours(imageout, contours, m, Emgu.CV.CvEnum.RetrType.External, Emgu.CV.CvEnum.ChainApproxMethod.ChainApproxSimple);

            for (int i = 0; i < contours.Size; i++)
            {
                double perimeter = CvInvoke.ArcLength(contours[i], true);
                VectorOfPoint approx = new VectorOfPoint();
                CvInvoke.ApproxPolyDP(contours[i], approx, .04 * perimeter, true);
                CvInvoke.DrawContours(imageout, contours, i, new MCvScalar(100, 100, 100), 5);
                picOutput.Image = imageout.ToBitmap();
                var moments = CvInvoke.Moments(contours[i]);
                int x = (int)(moments.M10 / moments.M00);
                int y = (int)(moments.M01 / moments.M00);


                if ((i < 10) && (x >= 0) && (y >= 0))
                {
                    using (var g = Graphics.FromImage(pictureBox1.Image))
                    {
                        velo[i, 0] = (x - coord2[i, 0]) * 30;
                        velo[i, 1] = (y - coord2[i, 1]) * 30;
                        if ((contours.Size == 2))
                        {
                            if (indicator < 2)
                            {
                                indicator = indicator + 1;
                                coord3[i, 0] = x;
                                coord3[i, 1] = y;
                                frame_count2 = frame_counter;
                            }

                        }

                        coord2[i, 0] = x;
                        coord2[i, 1] = y;
                        coord[i, 0] = x;
                        coord[i, 1] = y;
                        if ((x >= 0) && (y >= 0) && ((Math.Pow((x - 295), 2) + Math.Pow((y - 230), 2)) < 57600))
                        {
                            g.DrawRectangle(Pens.Red, (int)((x + (150) / 2)), (int)((y + (200) / 2)), 10, 10);
                            SolidBrush redBrush = new SolidBrush(Color.Blue);
                            g.FillRectangle(redBrush, (int)((x + (150) / 2)), (int)((y + (200) / 2)), 10, 10);
                            pictureBox1.Refresh();
                        }


                    }
                }
            }
            if ((frame_counter > frame_count2))
            {
                for (int k = 0; k < 10; k++)
                    for (int j = 0; j < 10; j++)
                    {
                        if ((Math.Pow((coord[k, 0] - coord3[j, 0]), 2) + Math.Pow((coord[k, 1] - coord3[j, 1]), 2)) < 1000)
                        {
                            coord3[j, 0] = coord[k, 0];
                            coord3[j, 1] = coord[k, 1];

                        }
                    }
                {

                }
            }

            if (contours.Size == 0)
            {
                picOutput.Image = imageout.ToBitmap();

            }
            string coord1 = "";
            string velo1 = "";
            for (int j = 0; j < 10; j++)
            {
                if ((coord[j, 0] == coord3[j, 0]) && (coord[j, 1] == coord3[j, 1]) && (frame_counter > frame_count2) && (coord[j, 0] > 0) && (coord3[j, 0] > 0) && (coord[j, 1] > 0) && (coord3[j, 1] > 0) && (j < 2))
                {
                    frames[0, j] = frames[0, j] + 1;
                }
                else if ((coord[j, 0] != coord3[j, 0]) || ((coord[j, 1] != coord3[j, 1])) && (frame_counter > frame_count2) && (coord[j, 0] > 0) && (coord3[j, 0] > 0) && (coord[j, 1] > 0) && (coord3[j, 1] > 0) && (j < 2))
                {
                    frames[0, j] = 0;
                }

                else if ((coord[0, 0] == 0) && (coord[1, 0] == 0) && (frame_counter > frame_count2))
                {
                    frames[0, 1] = 0;
                    frames[0, 0] = 0;
                }
                if (j == 0)
                {
                    coord4 = coord4 + "Ajusted Coord:[" + coord3[j, 0].ToString() + "," + coord3[j, 1].ToString() + "]";
                }
                else
                {
                    coord4 = coord4 + ",[" + coord3[j, 0].ToString() + "," + coord3[j, 1].ToString() + "]";
                }
            }

            ///string frame1 = "";
            for (int i = 0; i < 10; i++)
            {
                if (i == 0)
                {
                    coord1 = "[" + coord[i, 0].ToString() + "," + coord[i, 1].ToString() + "]";
                    velo1 = "[" + velo[i, 0].ToString() + "," + velo[i, 1].ToString() + "]";
                }
                else if (i == 9)
                {
                    coord1 = coord1 + ",[" + coord[i, 0].ToString() + "," + coord[i, 1].ToString() + "]";
                    velo1 = velo1 + ",[" + velo[i, 0].ToString() + "," + velo[i, 1].ToString() + "]";
                }
                else
                {
                    coord1 = coord1 + ",[" + coord[i, 0].ToString() + "," + coord[i, 1].ToString() + "]";
                    velo1 = velo1 + ",[" + velo[i, 0].ToString() + "," + velo[i, 1].ToString() + "]";
                }


            }
            var h = Graphics.FromImage(pictureBox1.Image);
            Point p = new Point(0, 0);
            h.DrawImage(Intitial.Image, p);



            Array.Clear(velo, 0, 20);
            Array.Clear(coord, 0, 20);
            textBox3.Text = coord1;
            textBox4.Text = velo1;
            textBox9.Text = coord4;
            textBox5.Text = textBox5.Text + " First LED " + frames[0, 0].ToString() + " Second LED " + frames[0, 1].ToString() + " ";
            if (frames[0, 0] == 7)
            {
                textBox7.Text = textBox7.Text + "1";
            }
            if (frames[0, 0] == 14)
            {
                textBox7.Text = textBox7.Text + "0";
            }
            ///bmp=maxThresholded.ToBitmap();

            ///CvInvoke.BitwiseNot(image, imageout);
            ///CvInvoke.Threshold(imageout, imageout, 250, 255, ThresholdType.Binary);
            ///CvInvoke.BitwiseNot(imageout, imageout);
            /// CvInvoke.Normalize(image, imageout, 0, 255, NormType.MinMax, DepthType.Cv8U);

            frame_counter++;
        }


        private void textBox4_TextChanged(object sender, EventArgs e)
        {

        }
        unsafe class BmpPixelSnoop : IDisposable
        {
            // A reference to the bitmap to be wrapped
            private readonly Bitmap wrappedBitmap;
            // The bitmap's data (once it has been locked)
            private BitmapData data = null;
            // Pointer to the first pixel
            private readonly byte* scan0;
            // Number of bytes per pixel
            private readonly int depth;
            // Number of bytes in an image row
            private readonly int stride;
            // The bitmap's width
            private readonly int width;
            // The bitmap's height
            private readonly int height;
            /// 

            /// Constructs a BmpPixelSnoop object, the bitmap
            /// object to be wraped is passed as a parameter.
            /// 

            /// The bitmap to snoop
            public BmpPixelSnoop(Bitmap bitmap)
            {
                wrappedBitmap = bitmap ?? throw new ArgumentException("Bitmap parameter cannot be null", "bitmap");
                // Currently works only for: PixelFormat.Format32bppArgb
                if (wrappedBitmap.PixelFormat != PixelFormat.Format32bppArgb)
                    throw new System.ArgumentException("Only PixelFormat.Format32bppArgb is supported", "bitmap");
                // Record the width & height
                width = wrappedBitmap.Width;
                height = wrappedBitmap.Height;
                // So now we need to lock the bitmap so that we can gain access
                // to it's raw pixel data.  It will be unlocked when this snoop is 
                // disposed.
                var rect = new Rectangle(0, 0, wrappedBitmap.Width, wrappedBitmap.Height);
                try
                {
                    data = wrappedBitmap.LockBits(rect, ImageLockMode.ReadWrite, wrappedBitmap.PixelFormat);
                }
                catch (Exception ex)
                {
                    throw new System.InvalidOperationException("Could not lock bitmap, is it already being snooped somewhere else?", ex);
                }
                // Calculate number of bytes per pixel
                depth = Bitmap.GetPixelFormatSize(data.PixelFormat) / 8; // bits per channel
                                                                         // Get pointer to first pixel
                scan0 = (byte*)data.Scan0.ToPointer();
                // Get the number of bytes in an image row
                // this will be used when determining a pixel's
                // memory address.
                stride = data.Stride;
            }
            /// 

            /// Disposes BmpPixelSnoop object
            /// 

            public void Dispose()
            {
                Dispose(true);
                GC.SuppressFinalize(this);
            }
            /// 

            /// Disposes BmpPixelSnoop object, we unlock
            /// the wrapped bitmap.
            /// 

            protected virtual void Dispose(bool disposing)
            {
                if (disposing)
                {
                    if (wrappedBitmap != null)
                        wrappedBitmap.UnlockBits(data);
                }
                // free native resources if there are any.
            }
            /// 

            /// Calculate the pointer to a pixel at (x, x)
            /// 

            /// The pixel's x coordinate
            /// The pixel's y coordinate
            /// A byte* pointer to the pixel's data
            private byte* PixelPointer(int x, int y)
            {
                return scan0 + y * stride + x * depth;
            }
            /// 

            /// Snoop's implemetation of GetPixel() which is similar to
            /// Bitmap's GetPixel() but should be faster.
            /// 

            /// The pixel's x coordinate
            /// The pixel's y coordinate
            /// The pixel's colour
            public System.Drawing.Color GetPixel(int x, int y)
            {
                // Better do the 'decent thing' and bounds check x & y
                if (x < 0 || y < 0 || x >= width || y >= width)
                    throw new ArgumentException("x or y coordinate is out of range");
                int a, r, g, b;
                // Get a pointer to this pixel
                byte* p = PixelPointer(x, y);
                // Pull out its colour data
                b = *p++;
                g = *p++;
                r = *p++;
                a = *p;
                // And return a color value for it (this is quite slow
                // but allows us to look like Bitmap.GetPixel())
                return System.Drawing.Color.FromArgb(a, r, g, b);
            }
            /// 

            /// Sets the passed colour to the pixel at (x, y)
            /// 

            /// The pixel's x coordinate
            /// The pixel's y coordinate
            /// The value to be assigned to the pixel
            public void SetPixel(int x, int y, System.Drawing.Color col)
            {
                // Better do the 'decent thing' and bounds check x & y
                if (x < 0 || y < 0 || x >= width || y >= width)
                    throw new ArgumentException("x or y coordinate is out of range");
                // Get a pointer to this pixel
                byte* p = PixelPointer(x, y);
                // Set the data
                *p++ = col.B;
                *p++ = col.G;
                *p++ = col.R;
                *p = col.A;
            }
            /// 

            /// The bitmap's width
            /// 

            public int Width { get { return width; } }
            // The bitmap's height
            public int Height { get { return height; } }
        }

        private void picOutput_Click(object sender, EventArgs e)
        {

        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void textBox6_TextChanged(object sender, EventArgs e)
        {

        }

        private void button4_Click(object sender, EventArgs e)
        {
            Application.Idle -= streaming;
            picOutput.Visible = false;
            capture.Stop();
            indicator = 0;
            frame_counter = 1;
            frame_count2 = 99999;
            frames[0, 0] = 0;
            frames[0, 1] = 0;
            this.Controls.Clear();
            InitializeComponent();

        }

        private void label4_Click(object sender, EventArgs e)
        {

        }

        private void textBox8_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox9_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox5_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox10_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox7_TextChanged(object sender, EventArgs e)
        {

        }
    }
}

