import cv2 as cv2
import numpy as np
import os
import random
from matplotlib import pyplot as plt

# Read images from folder images
def read_images():
    images = []
    for file in os.listdir('./images'):
        if file.endswith(".jpg"):
            images.append(file)
    return images

# Calculate the first digits
def compute_first_digits(img, debug):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    dct = cv2.dct(np.float32(img) / 255.0)
    dct = np.abs(dct)

    min_val = dct.min()
    if min_val < 1:
        dct = np.power(10, -np.floor(np.log10(min_val)) + 1) * dct

    # if not (dct >= 1.0).all():
    #     raise ValueError("Error")
    
    digits = np.log10(dct).astype(int).astype('float32')
    first_digits = dct / np.power(10, digits)
    first_digits[(first_digits < 1.0) & (first_digits > 0.9)] = 1  # Handle edge case.
    first_digits = first_digits.astype(int)

    # if not (first_digits >= 1).all() and (first_digits <= 9).all():
    #     raise ValueError("Error")

    # if debug:
    #     print(first_digits)

    return first_digits

# Calculate the occurrences of the first digits
def compute_first_digits_counts(img, debug):
    first_digits = compute_first_digits(img, debug)
    unq, counts = np.unique(first_digits, return_counts=True)
    if debug:
        print(unq, counts)
    return unq, counts

# Calculate the probability of the first digits
def compute_probability(unq, counts, debug):
    probability = []
    for i in unq:
        probability.append(counts[i - 1] / np.sum(counts))
    if debug:
        print(probability)
    return probability

# Checks to see if Benford's law is satisfied
def benford_law_check(first_digits, probability, debug):
    pastValue = probability[first_digits[0] - 1]   

    for value in first_digits:
        if debug:
            print('Checking value: ', probability[value - 1])
            
        if probability[value - 1] > pastValue and value != 1:
            # print(probability[value - 1], ' > ', pastValue)
            return False

        pastValue = probability[value - 1]
    
    return True

def tamper_image(img, k=31):
    newImg = cv2.medianBlur(img, k)
    return newImg

images = read_images()
tamper_images = []

debugMode = False

# Default images
print('--Default images--')
for img in images:
    image = cv2.imread('./images/' + img, cv2.IMREAD_GRAYSCALE)

    unq, counts = compute_first_digits_counts(image, debugMode)
    probability = compute_probability(unq, counts, debugMode)
    isBenford = benford_law_check(unq, probability, debugMode)

    title = img
    if isBenford:
        print('Original: ' + img + ' satisfies Benford\'s Law!')
        title = 'Benford\'s Law: ' + img + ' (Original)'
    else:
        print('Original: ' + img + ' does not satisfy Benford\'s Law!')
        title = 'Fraud Detected: ' + img + ' (Original)'

    # yaxis = yaxis / yaxis.sum()
    plt.bar(unq, probability, label='Original')
    plt.ylabel('Probability')
    plt.xlabel('First Digit')
    plt.title(title)    
    plt.show(block=False)



# 10 Percent Tampered images
print('--10 Percent Tampered images--')
for img in images:
    image = cv2.imread('./images/' + img, cv2.IMREAD_GRAYSCALE)
    rows,cols = image.shape

    # Select a random pixel in the image
    randompixel = np.random.choice(image[0], replace=False)

    if debugMode:
        print('Pixel Intensity Replaced: ', randompixel)
    
    for i in range(rows):
        for j in range(cols):
            if image[i][j] == randompixel:
                image[i][j] = 0

    unq, counts = compute_first_digits_counts(image, debugMode)
    probability = compute_probability(unq, counts, debugMode)
    isBenford = benford_law_check(unq, probability, debugMode)

    if isBenford:
        print('Partially Tampered: ' + img + ' satisfies Benford\'s Law!')
        title = 'Benford\'s Law: ' + img + ' (Partially Tampered)'
    else:
        print('Partially Tampered: ' + img + ' does not satisfy Benford\'s Law!')
        title = 'Fraud Detected: ' + img + ' (Partially Tampered)'

    plt.bar(unq, probability, label='Partially Tampered')
    plt.show(block=False)

# # Full Tamper images
print('--Tamper images--')
for img in images:
    image = cv2.imread('./images/' + img, cv2.IMREAD_GRAYSCALE)
    # tamper_images.append(tamper_image(image))
    tamperImg = tamper_image(image)

    unq, counts = compute_first_digits_counts(tamperImg, debugMode)
    probability = compute_probability(unq, counts, debugMode)
    isBenford = benford_law_check(unq, counts, debugMode)
    
    if isBenford:
        print('Fully Tampered: ' + img + ' satisfies Benford\'s Law!')
        title = 'Benford\'s Law: ' + img + ' (Fully Tampered)'
    else:
        print('Fully Tampered:' + img + ' does not satisfy Benford\'s Law!')
        title = 'Fraud Detected: ' + img + ' (Fully Tampered)'

    plt.bar(unq, counts, label='Fully Tampered')
    plt.ylabel('Probability of Occurrence')        
    plt.xlabel('First digit')
    plt.legend()
    plt.show()

    # cv2.imshow('Img', tamperImg)
    # cv2.waitKey(0)