import cv2 as cv2
import numpy as np
import os
import random
from matplotlib import pyplot as plt
import math

# Read images from folder images
def read_images():
    images = []
    for file in os.listdir('/content/drive/MyDrive/images/'):
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
    
    digits = np.log10(dct).astype(int).astype('float32')
    first_digits = dct / np.power(10, digits)
    first_digits[(first_digits < 1.0) & (first_digits > 0.9)] = 1  # Handle edge case.
    first_digits = first_digits.astype(int)

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
            return False

        pastValue = probability[value - 1]
    
    return True

def partial_tamper_image(img, k=5):
    newImg = cv2.GaussianBlur(img,(k,k),0)
    return newImg

def full_tamper_image(img, k=31):
    newImg = cv2.medianBlur(img, k)
    return newImg

images = read_images()

debugMode = False

print('--Benford\'s Law Analysis--')
for img in images:
    image = cv2.imread('/content/drive/MyDrive/images/' + img, cv2.IMREAD_GRAYSCALE)

    unq, counts = compute_first_digits_counts(image, debugMode)
    probability = compute_probability(unq, counts, debugMode)

    plt.bar(unq, probability, color='silver')

    plt.plot(unq, probability, color='black', linestyle='dashed', linewidth=2, marker='x', label='Original Benford\'s Analysis')
    
    partialTamper = partial_tamper_image(image)
    unq, counts = compute_first_digits_counts(partialTamper, debugMode)
    probability = compute_probability(unq, counts, debugMode)
  
    plt.plot(unq, probability, color='green', linestyle='dashed', linewidth=2, marker='x', label='Partially Modifed Analysis')

    fullTamper = full_tamper_image(image)
    unq, counts = compute_first_digits_counts(fullTamper, debugMode)
    probability = compute_probability(unq, counts, debugMode)
    
    plt.plot(unq, probability, color='red', linestyle='dashed', linewidth=2, marker='x', label='Fully Modifed Analysis')

    plt.legend(loc='best')
    plt.ylabel('Probability')
    plt.xlabel('First Digit')
    plt.title(img)    
    plt.show(block=False)