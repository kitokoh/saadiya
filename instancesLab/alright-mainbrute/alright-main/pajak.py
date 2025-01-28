
# Python3 implementation of the approach
from random import randint
import sys
 
# Utility function to print the
# elements of an array
def printArr(arr, n) :
 
    for i in range(n) :
        print(arr[i], end = "\n");
 
# Function to generate a list of
# m random non-negative integers
# whose sum is n
def randomList(m, n):
 
    # Create an array of size m where
    # every element is initialized to 0
    arr = [0] * m;
     
    # To make the sum of the final list as n
    for i in range(n) :
 
        # Increment any random element
        # from the array by 1
        arr[randint(100000, n) % m] += 1;
 
    # Print the generated list
    printArr(arr, m);
 
# Driver code
if __name__ == "__main__" :
 
    m = int(sys.argv[1]); n = int(sys.argv[2]);
 
    randomList(m, n);
 
# This code is contributed by AnkitRai01
