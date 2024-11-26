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
    using System.Timers;
    using System.Timers;
    using static System.Windows.Forms.VisualStyles.VisualStyleElement.TaskbarClock;
    using System.Diagnostics;
    using OpenTK.Graphics.ES30;
    using System.Diagnostics.Eventing.Reader;
    using System.Text.RegularExpressions;
    using ZedGraph;

    public partial class Form1 : Form
    {
        int frame_initial = 0;
        String[] Line_raw = new string[3];
        bool streamvideo = false;
        static int cameraIDx = 0;
        int counter = 0;
        string bit_text1 = "";
        VideoCapture capture = new VideoCapture();

        bool _streaming;
        PictureBox Intitial = new PictureBox();
        PictureBox Intitial2 = new PictureBox();
        int[,] coord = new int[10, 2];
        int[,,] coord_total = new int[10000, 2, 2];
        int[,] coord3 = new int[10, 2];
        int[,] coord2 = new int[10, 2];
        int[,] velo = new int[10, 2];
        int count3 = 0;
        int indicator10 = 0;
        int frame_counter = 1;
        int[,] frames = new int[1, 10];
        int frame_count2 = 999999;
        int indicator = 0;
        int indicator7 = 0;
        int[,] array_coord = new int[2, 10];
        int[,] array_coord2 = new int[2, 10];
        int[,] array_coord_master = new int[2, 10];
        string frame1 = "";
        double frame_inter = 0;
        int indicator3 = 0;
        string bit_text = "";
        int min_previous = 0;
        int bit_counter = 0;
        int indicator4 = 0;
        int indicator5 = 0;
        int indicator6 = 0;
        int indicator8 = 0;
        int indicator9 = 0;
        string[] coord_x_inter = new string[2];
        string[] coord_y_inter = new string[2];
        VectorOfVectorOfPoint contours = new VectorOfVectorOfPoint();
        VectorOfVectorOfPoint contours2 = new VectorOfVectorOfPoint();
        int counter_blinker = 0;
        int counter_black = 0;
        static System.Windows.Forms.Timer t = new System.Windows.Forms.Timer();
        static System.Windows.Forms.Timer t2 = new System.Windows.Forms.Timer();
        static System.Windows.Forms.Timer t3 = new System.Windows.Forms.Timer();
        static System.Windows.Forms.Timer t4 = new System.Windows.Forms.Timer();
        static System.Windows.Forms.Timer t5 = new System.Windows.Forms.Timer();
        static System.Windows.Forms.Timer t6 = new System.Windows.Forms.Timer();
        static System.Windows.Forms.Timer t7 = new System.Windows.Forms.Timer();
        static System.Windows.Forms.Timer t8 = new System.Windows.Forms.Timer();
        System.Diagnostics.Stopwatch FrameStopWatch1 = new System.Diagnostics.Stopwatch();
        System.Diagnostics.Stopwatch FrameStopWatch2 = new System.Diagnostics.Stopwatch();
        VideoCapture videocap = new VideoCapture(@"C:\Users\charp\OneDrive\Desktop\School\403\output1_1_mov.mp4");
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



        private void button1_Click(object sender, EventArgs e)
        {


            string[] code_orginal = new string[5];
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

                                        string[] inputs = (textBox4.Text).Split(",");
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

        private void button1_Click_1(object sender, EventArgs e)
        {


            if (!_streaming)
            {
                Application.Idle += streaming;

            }
            else
            {

                Application.Idle -= streaming;
                /// picOutput.Visible = true;

            }
            _streaming = !_streaming;

        }
        private void streaming(object sender, System.EventArgs e)
        {
            //frame_inter = frame_counter;
            //textBox11.Text = (frame_inter * .033).ToString();
            ////if(frame_counter< frame_count2)
            ////{
            ////    FrameStopWatch1.Reset();
            ////    FrameStopWatch2.Reset();
            ////}
            ////if (frame_counter > frame_count2)
            ////{


            ////    if ((FrameStopWatch1.Elapsed.TotalMilliseconds > 3000))
            ////    {
            ////        FrameStopWatch1.Reset();


            ////    }
            ////    if ((FrameStopWatch2.Elapsed.TotalMilliseconds > 3000))
            ////    {
            ////        FrameStopWatch2.Reset();

            ////    }
            ////}


            /////  if (counter_blinker < 41)
            ///// {
            ///// .



            ///// }
            ////      counter_blinker++;
            ///// }
            ////else if ((counter_black < 11) && (counter_blinker == 40))
            ////{


            ////    if ((counter_black == 10))
            ////    {

            ////        counter_blinker = 0;
            ////    }

            ////    counter_black++;

            ////}
            ////if ((counter_black == 10) && (counter_blinker == 0))
            ////{
            ////    counter_blinker = 0;
            ////    counter_black = 0;
            ////}










            //textBox5.WordWrap = true;

            //string coord4 = "";
            //DoubleBuffered = true;

            ///  var image = capture.QueryFrame().ToImage<Gray, byte>();
            /// picOutput.Image = image.ToBitmap();




            ///Bitmap bmp = image.ToBitmap(); //take a picture
            ///var imageout = capture.QueryFrame().ToImage<Gray, byte>().ThresholdBinary(new Gray(250), new Gray(255));

            //Mat m = new Mat();
            //CvInvoke.FindContours(imageout, contours, m, Emgu.CV.CvEnum.RetrType.External, Emgu.CV.CvEnum.ChainApproxMethod.ChainApproxSimple);
            //Rectangle rect = new Rectangle();

            //for (int i = 0; i < contours.Size; i++)
            //{
            //    double perimeter = CvInvoke.ArcLength(contours[i], true);
            //    VectorOfPoint approx = new VectorOfPoint();
            //    CvInvoke.ApproxPolyDP(contours[i], approx, .04 * perimeter, true);
            //    CvInvoke.DrawContours(imageout, contours, i, new MCvScalar(100, 100, 100), 5);
            //    picOutput.Image = imageout.ToBitmap();
            //    var moments = CvInvoke.Moments(contours[i]);
            //    int x = (int)(moments.M10 / moments.M00);
            //    int y = (int)(moments.M01 / moments.M00);


            //    if ((i < 10) && (x >= 0) && (y >= 0))
            //    {
            //        using (var g = Graphics.FromImage(pictureBox1.Image))
            //        {
            //            velo[i, 0] = (x - coord2[i, 0]) * 30;
            //            velo[i, 1] = (y - coord2[i, 1]) * 30;
            //            if ((contours.Size == 2))
            //            {
            //                if (indicator < 2)
            //                {
            //                    indicator = indicator + 1;
            //                    coord3[i, 0] = x;
            //                    coord3[i, 1] = y;
            //                    frame_counter = 0;
            //                }

            //            }

            //            coord2[i, 0] = x;
            //            coord2[i, 1] = y;
            //            if (((coord[i, 0] < 0) || ((coord[i, 1] < 0))))
            //            {
            //                coord[i, 0] = 0;
            //                coord[i, 1] = 0;
            //            }
            //            else
            //            {
            //                coord[i, 0] = x;
            //                coord[i, 1] = y;
            //            }

            //            if ((x >= 0) && (y >= 0) && ((Math.Pow((x - 295), 2) + Math.Pow((y - 230), 2)) < 57600))
            //            {
            //                g.DrawRectangle(Pens.Red, (int)((x + (150) / 2)), (int)((y + (200) / 2)), 10, 10);
            //                SolidBrush redBrush = new SolidBrush(Color.Blue);
            //                g.FillRectangle(redBrush, (int)((x + (150) / 2)), (int)((y + (200) / 2)), 10, 10);
            //                pictureBox1.Refresh();
            //            }


            //        }
            //    }
            //}
            //if ((contours.Size == 2))
            //{
            //    frames[0, 0] = frames[0, 0] + 1;
            //    frames[0, 1] = frames[0, 1] + 1;

            //    for (int k = 0; k < 10; k++)
            //        for (int j = 0; j < 10; j++)
            //        {

            //            if (((Math.Pow((coord[k, 0] - coord3[j, 0]), 2) + Math.Pow((coord[k, 1] - coord3[j, 1]), 2)) < 1000) && (coord[k, 0] > 0) && (coord[k, 1] > 0))
            //            {
            //                coord3[j, 0] = coord[k, 0];
            //                coord3[j, 1] = coord[k, 1];


            //            }


            //        }

            //}

            //else if ((contours.Size == 0))
            //{
            //    if (1 == 1)
            //    {
            //        picOutput.Image = imageout.ToBitmap();
            //        for (int y = 0; y < 10; y++)
            //        {
            //            frames[0, y] = 0;

            //        }
            //    }
            //    ///  FrameStopWatch1.Reset();
            //    ///  FrameStopWatch2.Reset();

            //}
            //else if (contours.Size == 1)
            //{
            //    picOutput.Image = imageout.ToBitmap();
            //    if (1 == 1)
            //    {
            //        for (int y = 0; y < 10; y++)
            //        {
            //            if ((coord[y, 0] == 0) && (coord[y, 1] == 0) && (y < 2))
            //            {
            //                frames[0, y] = 0;
            //            }
            //            else
            //            {
            //                frames[0, y] = 0;
            //            }

            //            if ((coord[1, 0] != coord3[1, 0]) || (coord[1, 1] != coord3[1, 1]))
            //            {
            //                ///FrameStopWatch2.Reset();

            //            }
            //            if ((coord[0, 0] != coord3[0, 0]) || (coord[0, 1] != coord3[0, 1]))
            //            {
            //                /// FrameStopWatch1.Reset();

            //            }



            //        }
            //    }


            //}
            //else
            //{
            //    frames[0, 0] = 0;
            //    frames[0, 1] = 0;
            //}
            //string coord1 = "";
            //string velo1 = "";
            //for (int j = 0; j < 2; j++)
            //{

            //    if (j == 0)
            //    {
            //        coord4 = coord4 + "Ajusted Coord:[" + coord3[j, 0].ToString() + "," + coord3[j, 1].ToString() + "]";
            //    }
            //    else
            //    {
            //        coord4 = coord4 + ",[" + coord3[j, 0].ToString() + "," + coord3[j, 1].ToString() + "]";
            //    }
            //}

            /////string frame1 = "";
            //for (int i = 0; i < 10; i++)
            //{
            //    if (i == 0)
            //    {
            //        coord1 = "[" + coord[i, 0].ToString() + "," + coord[i, 1].ToString() + "]";
            //        velo1 = "[" + velo[i, 0].ToString() + "," + velo[i, 1].ToString() + "]";
            //    }
            //    else if (i == 9)
            //    {
            //        coord1 = coord1 + ",[" + coord[i, 0].ToString() + "," + coord[i, 1].ToString() + "]";
            //        velo1 = velo1 + ",[" + velo[i, 0].ToString() + "," + velo[i, 1].ToString() + "]";
            //    }
            //    else
            //    {
            //        coord1 = coord1 + ",[" + coord[i, 0].ToString() + "," + coord[i, 1].ToString() + "]";
            //        velo1 = velo1 + ",[" + velo[i, 0].ToString() + "," + velo[i, 1].ToString() + "]";
            //    }


            //}
            //var h = Graphics.FromImage(pictureBox1.Image);
            //Point p = new Point(0, 0);
            //h.DrawImage(Intitial.Image, p);

            //Array.Clear(velo, 0, 20);
            //Array.Clear(coord, 0, 20);
            //textBox3.Text = coord1;
            //textBox4.Text = velo1;



            //if (frames[0, 0] == 0)
            //{
            //    indicator3 = 0;
            //    indicator4 = 0;

            /////textBox5.Text = textBox5.Text + " First LED " + frames[0, 0].ToString() + " Second LED " + frames[0, 1].ToString() + " ";
            //if ((indicator3 == 0) && (frames[0, 0] > 4) && (frames[0, 0] < 8) && (indicator4 == 0))
            //{
            //    bit_text = bit_text + "1";
            //    textBox7.Text = bit_text;
            //    indicator3 = 1;
            //}
            //else if ((frames[0, 0] > 8) && ((frames[0, 0] < 12)))
            //{
            //    if (indicator3 == 1)
            //    {
            ///        bit_text = bit_text.Substring(0, bit_text.Length - 1);
            //    }
            //    bit_text = bit_text + "0";
            //    textBox7.Text = bit_text;
            //    indicator4 = 1;
            //}

            ///textBox10.Text = textBox10.Text + contours.Size.ToString();

            /////bmp=maxThresholded.ToBitmap();

            /////CvInvoke.BitwiseNot(image, imageout);
            /////CvInvoke.Threshold(imageout, imageout, 250, 255, ThresholdType.Binary);
            /////CvInvoke.BitwiseNot(imageout, imageout);
            ///// CvInvoke.Normalize(image, imageout, 0, 255, NormType.MinMax, DepthType.Cv8U);
            //frame_counter++;

            //  textBox11.Text = textBox11.Text + " LED1:Seconds  " + FrameStopWatch1.Elapsed.Seconds.ToString() + " Mili: " + FrameStopWatch1.Elapsed.Milliseconds.ToString();
            // textBox12.Text = textBox12.Text + " LED2:Seconds " + FrameStopWatch2.Elapsed.Seconds.ToString() + " Mili: " + FrameStopWatch2.Elapsed.Milliseconds.ToString();
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
                if (wrappedBitmap.PixelFormat != 0)
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
            ///picOutput.Visible = false;
            capture.Stop();
            videocap.Stop();
            indicator = 0;
            frame_counter = 1;
            frame_count2 = 99999;
            frames[0, 0] = 0;
            frames[0, 1] = 0;
            indicator3 = 0;
            indicator4 = 0;
            counter_black = 0;
            counter_blinker = 0;
            bit_text = "";
            coord_total = new int[10000, 2, 2];
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

        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void button2_Click_1(object sender, EventArgs e)
        {

            int indicator_l = 0;
            // while (indicator_l<100)
            // {

            //while (indicator_l == 0)
            // {

            t.Interval = 500; // specify interval time as you want
            t.Tick += new EventHandler(timer_Tick_light);
            t.Start();


            //}

            /// indicator_l = 0;

            //while (indicator_l == 0)
            // {
            MessageBox.Show("Error Message");
            t2.Interval = 500; // specify interval time as you want
            t2.Tick += new EventHandler(timer_Tick_dark);
            t2.Start();
            MessageBox.Show("Error Message");
            t3.Interval = 500; // specify interval time as you want
            t3.Tick += new EventHandler(timer_Tick_light);
            t3.Start();


            //     indicator_l = 1;
            ///}






            //}

        }

        private void pictureBox2_Click(object sender, EventArgs e)
        {


        }
        void timer_Tick_light(object sender, EventArgs e)
        {


        }
        void timer_Tick_dark(object sender, EventArgs e)
        {


        }

        private void textBox11_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox12_TextChanged(object sender, EventArgs e)
        {

        }

        private void button5_Click(object sender, EventArgs e)
        {

            String line;
            int x = 0;
            int y = 0;
            const Int32 BufferSize = 128;
            indicator = 0;



            using (var fileStream = File.OpenRead(@"C:\Users\charp\OneDrive\Desktop\School\403\coordfile2_mov.txt"))
            using (var streamReader = new StreamReader(fileStream, Encoding.UTF8, true, BufferSize))
            {
                //Pass the file path and file name to the StreamReader constructor

                //Read the first line of text
                while ((line = streamReader.ReadLine()) != null)
                {



                    //write the line to console window
                    Line_raw = line.Split(" ");
                    if (indicator == 0)
                    {
                        frame_initial = Int32.Parse(Line_raw[0]);
                        indicator = 1;
                    }


                    if ((frame_counter == Int32.Parse(Line_raw[0])) && (indicator == 1))
                    {
                        coord_total[frame_counter, 0, 0] = x;
                        coord_total[frame_counter, 0, 1] = y;
                        coord_total[frame_counter, 1, 0] = Int32.Parse(Line_raw[1].Split(":")[1]);
                        coord_total[frame_counter, 1, 1] = Int32.Parse(Line_raw[2].Split(":")[1]);
                    }
                    else if ((frame_counter == Int32.Parse(Line_raw[0]) - 1) && (indicator == 1))
                    {
                        coord_total[frame_counter, 1, 0] = Int32.Parse(Line_raw[1].Split(":")[1]);
                        coord_total[frame_counter, 1, 1] = Int32.Parse(Line_raw[2].Split(":")[1]);
                    }














                    coord_x_inter = Line_raw[1].Split(":");
                    coord_y_inter = Line_raw[2].Split(":");

                    x = Int32.Parse(coord_x_inter[1]);
                    y = Int32.Parse(coord_y_inter[1]);
                    frame_counter = Int32.Parse(Line_raw[0]);
                    //Read the next line

                }
                string coord1 = "";
                string velo1 = "";
                for (int j = frame_initial + 1; j < Int32.Parse(Line_raw[0]); j++)
                {

                    for (int LED1 = 0; LED1 < 2; LED1++)
                    {
                        if ((coord_total[j, LED1, 0] == 0) && (coord_total[j, LED1, 1] == 0))
                        {
                            frames[0, LED1] = 0;
                        }
                        else if ((coord_total[j, 0, 0] == 0) && (coord_total[j, 0, 1] == 0) && (coord_total[j, 1, 0] == 0) && (coord_total[j, 1, 1] == 0))
                        {
                            frames[0, 0] = 0;
                            frames[0, 1] = 0;
                        }
                        else
                        {
                            if ((coord_total[j - 1, LED1, 0] == 0) && (coord_total[j - 1, LED1, 1] == 0) && (coord_total[j, 0, 0] > 0) && (coord_total[j, 0, 1] > 0) && (coord_total[j, 1, 0] > 0) && (coord_total[j, 1, 1] > 0))
                            {


                                frames[0, LED1] = frames[0, LED1] + 1;



                            }
                            else if ((coord_total[j - 1, LED1, 0] == 0) && (coord_total[j - 1, LED1, 1] == 0) && (coord_total[j, 0, 0] > 0) && (coord_total[j, 0, 1] > 0) && (coord_total[j, 1, 0] == 0) && (coord_total[j, 1, 1] == 0))
                            {
                                if ((((Math.Pow((coord_total[j - 1, LED1, 0] - coord_total[j, 0, 0]), 2) + Math.Pow((coord_total[j - 1, LED1, 1] - coord_total[j, 0, 1]), 2) < 1000))))
                                {

                                    velo[0, 0] = (coord_total[j - 1, LED1, 0] - coord_total[j, 0, 0]) * 30;
                                    velo[0, 1] = (coord_total[j - 1, LED1, 1] - coord_total[j, 0, 1]) * 30;
                                    frames[0, LED1] = frames[0, LED1] + 1;



                                }
                            }
                            else if ((coord_total[j - 1, LED1, 0] == 0) && (coord_total[j - 1, LED1, 1] == 0) && (coord_total[j, 1, 0] > 0) && (coord_total[j, 1, 1] > 0) && (coord_total[j, 0, 0] == 0) && (coord_total[j, 0, 1] == 0))
                            {
                                if ((((Math.Pow((coord_total[j - 1, LED1, 0] - coord_total[j, 1, 0]), 2) + Math.Pow((coord_total[j - 1, LED1, 1] - coord_total[j, 1, 1]), 2) < 1000))))
                                {

                                    velo[0, 0] = (coord_total[j - 1, LED1, 0] - coord_total[j, 1, 0]) * 30;
                                    velo[0, 1] = (coord_total[j - 1, LED1, 1] - coord_total[j, 1, 1]) * 30;
                                    frames[0, LED1] = frames[0, LED1] + 1;



                                }
                            }
                            else
                            {
                                for (int LED2 = 0; LED2 < 2; LED2++)
                                {

                                    if ((((Math.Pow((coord_total[j - 1, LED1, 0] - coord_total[j, LED2, 0]), 2) + Math.Pow((coord_total[j - 1, LED1, 1] - coord_total[j, LED2, 1]), 2) < 1000) && (coord_total[j - 1, LED1, 0] > 0) && (coord_total[j - 1, 1, 1] > 0))))
                                    {
                                        if (indicator3 == 0)
                                        {
                                            velo[0, 0] = (coord_total[j - 1, LED1, 0] - coord_total[j, LED2, 0]) * 30;
                                            velo[0, 1] = (coord_total[j - 1, LED1, 1] - coord_total[j, LED2, 1]) * 30;
                                            frames[0, LED1] = frames[0, LED1] + 1;
                                            indicator3 = 1;
                                        }

                                    }

                                }
                                if ((indicator3 == 0) && indicator4 == 0)
                                {
                                    frames[0, LED1] = 0;
                                }
                                if ((indicator3 == 1))
                                {
                                    indicator3 = 0;
                                }
                            }

                        }

                        if ((x >= 0) && (y >= 0) && ((Math.Pow((x - 295), 2) + Math.Pow((y - 230), 2)) < 57600))
                        {
                            using (var g = Graphics.FromImage(pictureBox1.Image))
                            {
                                g.DrawRectangle(Pens.Red, (int)((coord_total[j, LED1, 0] + (150) / 2)), (int)((coord_total[j, LED1, 1] + (200) / 2)), 10, 10);
                                SolidBrush redBrush = new SolidBrush(Color.Blue);
                                g.FillRectangle(redBrush, (int)((coord_total[j, LED1, 0] + (150) / 2)), (int)((coord_total[j, LED1, 1] + (200) / 2)), 10, 10);
                                pictureBox1.Refresh();
                                for (int i = 0; i < 10; i++)
                                {
                                    if (i == 0)
                                    {
                                        coord1 = "[" + coord_total[j, LED1, 0].ToString() + "," + coord_total[j, LED1, 1].ToString() + "]";
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
                            }
                        }

                    }
                    textBox3.Text = coord1;
                    textBox4.Text = velo1;
                    var h = Graphics.FromImage(pictureBox1.Image);
                    Point p = new Point(0, 0);
                    h.DrawImage(Intitial.Image, p);
                    if (frames[0, 0] == 0)
                    {
                        indicator5 = 0;
                        indicator6 = 0;
                    }
                    textBox5.Text = textBox5.Text + " First LED " + frames[0, 0].ToString() + " Second LED " + frames[0, 1].ToString() + " ";
                    if ((indicator5 == 0) && (frames[0, 0] > 7) && (frames[0, 0] < 18) && (indicator5 == 0))
                    {
                        bit_text = bit_text + "1";
                        textBox7.Text = bit_text;
                        indicator5 = 1;
                    }
                    else if ((frames[0, 0] > 25) && ((frames[0, 0] < 33)) && (indicator5 == 1) && (indicator6 == 0))
                    {
                        if (indicator5 == 1)
                        {
                            bit_text = bit_text.Substring(0, bit_text.Length - 1);
                        }
                        bit_text = bit_text + "0";
                        textBox7.Text = bit_text;
                        indicator6 = 1;
                    }
                    if (frames[0, 1] == 0)
                    {
                        indicator8 = 0;
                        indicator9 = 0;
                    }
                    if ((indicator8 == 0) && (frames[0, 1] > 7) && (frames[0, 1] < 18))
                    {
                        bit_text1 = bit_text1 + "1";
                        textBox10.Text = bit_text1;
                        indicator8 = 1;
                    }
                    else if ((frames[0, 1] > 20) && ((frames[0, 1] < 33)) && (indicator8 == 1) && (indicator9 == 0))
                    {
                        if (indicator8 == 1)
                        {
                            bit_text1 = bit_text1.Substring(0, bit_text1.Length - 1);
                        }
                        bit_text1 = bit_text1 + "0";
                        textBox10.Text = bit_text1;
                        indicator9 = 1;
                    }
                    if ((bit_text.Contains("11011100") || (bit_text1.Contains("11011100")))||bit_text1.Contains("11001101"))
                    {
                        textBox8.Text = textBox8.Text + " ID Tag 1 Indentified Frame: " + j.ToString() + " ";
                    }
                    if ((bit_text1.Contains("11001100") || (bit_text.Contains("11001100"))))
                    {
                        textBox8.Text = textBox8.Text + " ID Tag 2 Indentified  Frame: " + j.ToString() + " ";
                    }
                    wait(30);

                }


                //close the file
            }
        }
        public void wait(int milliseconds)
        {
            var timer1 = new System.Windows.Forms.Timer();
            if (milliseconds == 0 || milliseconds < 0) return;

            // Console.WriteLine("start wait timer");
            timer1.Interval = milliseconds;
            timer1.Enabled = true;
            timer1.Start();

            timer1.Tick += (s, e) =>
            {
                timer1.Enabled = false;
                timer1.Stop();
                // Console.WriteLine("stop wait timer");
            };

            while (timer1.Enabled)
            {
                Application.DoEvents();
            }
        }


    }
}

