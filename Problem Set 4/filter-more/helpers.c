#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // row loop
    for (int i = 0; i < height; i++)
    {
        // column loop
        for (int j = 0; j < width; j++)
        {
            // find average value
            int rgb_avg = round((image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen) / 3.0);

            // set all values equal to average
            image[i][j].rgbtBlue = image[i][j].rgbtRed = image[i][j].rgbtGreen = rgb_avg;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // row loop
    for (int i = 0; i < height; i++)
    {
        // column loop
        for (int j = 0; j < width / 2; j++)
        {
            // create temp array
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // intialize temp array to store orginal
    RGBTRIPLE temp_array[height][width];

    // row loop
    for (int i = 0; i < height; i++)
    {
        // column loop
        for (int j = 0; j < width; j++)
        {
            temp_array[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sumGreen, sumRed, sumBlue;
            sumGreen = sumRed = sumBlue = 0;
            float counter = 0;

            // find neighboring pixels
            for (int x = - 1; x < 2; x++)
            {
                for (int y = - 1; y < 2; y++)
                {

                    if (i + x < 0 || i + x > (height - 1) || j + y < 0 || j + y > (width - 1))
                    {
                        continue;
                    }

                    sumGreen += image[i + x][j + y].rgbtGreen;
                    sumRed += image[i + x][j + y].rgbtRed;
                    sumBlue += image[i + x][j + y].rgbtBlue;

                    counter++;
                }
            }
            // Average of neighboring pixels
            temp_array[i][j].rgbtGreen = round(sumGreen / counter);
            temp_array[i][j].rgbtRed = round(sumRed / counter);
            temp_array[i][j].rgbtBlue = round(sumBlue / counter);

        }
    }

    // row loop
    for (int i = 0; i < height; i++)
    {
        // column loop
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtGreen = temp_array[i][j].rgbtGreen;
            image[i][j].rgbtRed = temp_array[i][j].rgbtRed;
            image[i][j].rgbtBlue = temp_array[i][j].rgbtBlue;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Create temp array
    RGBTRIPLE temp_array_2[height][width];

    // row loop
    for (int i = 0; i < height; i++)
    {
        // column loop
        for (int j = 0; j < width; j++)
        {
            temp_array_2[i][j] = image[i][j];
        }
    }
    // Initialise Sobel arrays
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    // row loop
    for (int i = 0; i < height; i++)
    {
        // column loop
        for (int j = 0; j < width; j++)
        {
            float Gx_red = 0;
            float Gx_green = 0;
            float Gx_blue = 0;
            float Gy_red = 0;
            float Gy_green = 0;
            float Gy_blue = 0;

            for (int x = - 1; x < 2; x++)
            {
                for (int y = - 1; y < 2; y++)
                {

                    if (i + x < 0 || i + x > (height - 1) || j + y < 0 || j + y > (width - 1))
                    {
                        continue;
                    }

                    Gx_red += temp_array_2[i + x][j + y].rgbtRed * Gx[x + 1][y + 1];
                    Gx_green += temp_array_2[i + x][j + y].rgbtGreen * Gx[x + 1][y + 1];
                    Gx_blue += temp_array_2[i + x][j + y].rgbtBlue * Gx[x + 1][y + 1];
                    Gy_red += temp_array_2[i + x][j + y].rgbtRed * Gy[x + 1][y + 1];
                    Gy_green += temp_array_2[i + x][j + y].rgbtGreen * Gy[x + 1][y + 1];
                    Gy_blue += temp_array_2[i + x][j + y].rgbtBlue * Gy[x + 1][y + 1];

                }
            }

            // Calculate Sobel operator
            int red = round(sqrt(Gx_red * Gx_red + Gy_red * Gy_red));
            int green = round(sqrt(Gx_green * Gx_green + Gy_green * Gy_green));
            int blue = round(sqrt(Gx_blue * Gx_blue + Gy_blue * Gy_blue));

            // Cap at 255
            if (red > 255)
            {
                red = 255;
            }

            if (green > 255)
            {
                green = 255;
            }

            if (blue > 255)
            {
                blue = 255;
            }

            // Assign new values to pixels
            image[i][j].rgbtRed = red;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtBlue = blue;

        }
    }
    return;
}
