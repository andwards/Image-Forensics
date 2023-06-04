# Image Forensics

This program aims to determine if an image has been tampered with using Benford's law. Benford's law, also known as the first-digit law, states that in many datasets, the leading digit is more likely to be small (1, 2, 3) than large (8, 9). By applying Benford's law to the Discrete Cosine Transform (DCT) of an image, we can analyze the distribution of the first digits and detect any inconsistencies that may indicate tampering.

## Features

1. **Image Dataset Selection**: The program allows you to select a dataset of natural images for analysis. It is recommened to have five to six images with the same spatial and intensity resolution to form the dataset.
2. **DCT Calculation**: The program utilizes the Discrete Cosine Transform (DCT) on the selected images.
3. **Benford's Law Analysis**: The program applies Benford's law to the DCT of the images. Benford's law states that the leading digit in many datasets follows a specific distribution pattern. By analyzing the distribution of first digits, the program determines if Benford's law holds for the image dataset.
4. **Tampered Image Generation**: The program generates tampered versions of the original images for further analysis. It randomly alters pixel values in the images to simulate tampering. Two types of tampering are supported: partial tampering (changing values for randomly selected pixels) and full tampering (applying blur effects to alter pixel values).
5. **First Digit Occurrence Analysis**: The program calculates the occurrences of the first digits in the DCT of both original and tampered images. This analysis helps identify any deviations from the expected distribution based on Benford's law.
6. **Probability Distribution Visualization**: The program visualizes the probability distribution of the first digits for each image in the dataset. The resulting plots provide a clear representation of the first digit distribution and help detect potential tampering based on deviations from Benford's law.
7. **Debug Mode**: The program includes a debug mode that provides additional output for debugging purposes. By enabling debug mode, you can monitor the intermediate steps of the analysis and gain insights into the calculations and probability computations.
8. **User-Friendly**: The program is user-friendly for executing the analysis. Once the images are selected and placed in the designated folder, running the program displays the analysis results as plots for easy interpretation.

## Contributors

- [Andrew Edwards](https://www.github.com/andwards)