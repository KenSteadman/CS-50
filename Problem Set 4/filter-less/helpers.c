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

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // row loop
    for (int i = 0; i < height; i++)
    {
        // column loop
        for (int j = 0; j < width; j++)
        {

            int original_Red = image[i][j].rgbtRed;
            int original_Green = image[i][j].rgbtGreen;
            int original_Blue = image[i][j].rgbtBlue;


            int sepiaRed = round(.393 * original_Red + .769 * original_Green + .189 * original_Blue);
            int sepiaGreen = round(.349 * original_Red + .686 * original_Green + .168 * original_Blue);
            int sepiaBlue = round(.272 * original_Red + .534 * original_Green + .131 * original_Blue);

            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }

            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }

            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
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
