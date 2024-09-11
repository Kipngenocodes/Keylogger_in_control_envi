'''
the code above conduct a Brute-Force Password Cracking

'''
# itertools is used for generating cobinations of characters
# string provides constants like ascii_letters punctuation, and digits to create a character set
# time to calculate the time taken to crack the password

import itertools
import string
import time

def bforce_password_cracker(password_target, pass_max_length= 6):
    
    # character definitions to be used in brute-force attack
    chars = string.ascii_letters + string.punctuation + string.digits
    
    print(f"Starting brute-force password cracking... (max length: {pass_max_length})")
    start_time = time.time()   # record the start time
    
    # conductions all combinations of chars upto max_length
    for len in range(1, pass_max_length+1 ):
        # generating all combination possible for the entere length
        for guessing in itertools.product(chars, repeat=len):
            # convert the combination to string
            password_guessed = ''.join(guessing)
            
            # printing guessed password
            print(f"Guessed password: {guessing}")
            
            # checking if gussed password matches the password target
            if password_guessed == password_target:
                time_taken = time.time() - start_time
                print(f"Password cracked: {password_guessed}")
                print(f'Time taken is: {time_taken:.2f} seconds') 
                
                return
            
            
    print("Password not found within the given length limit.") 
    
if __name__ =='__main__':
    password_target = 'kipnge'
    
    
    pass_max_length = 6
    
    bforce_password_cracker(password_target, pass_max_length
                            )