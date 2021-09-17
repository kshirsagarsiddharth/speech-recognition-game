#recognizer = sr.Recognizer()
#microphone = sr.Microphone()
import speech_recognition as sr 

def recognize_speech_from_mic(recognizer,microphone):
    
    """
    Transcribe speech recorded from microphone
    Returns a dectonary with three keys 
    "success":a boolean indicating weather the api request was successful 

    "error":`None` if no error occured, otherwise a string containing an error message 
            if the api could not be reached or speech was unrecognizable 
    
    "transcription": `None` if the speech could not be transcribed otherwise a string containing the 
                    transcribed text 
    """

    if not isinstance(recognizer,sr.Recognizer): 
        raise TypeError("`recognizer` should be a `recognizer` instance")
    if not isinstance(microphone,sr.Microphone):
        raise TypeError("`microphone` should be a `Microphone` object")

    # adjsut the recognizer sensitivity to ambient noise and record audio from microphone 
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source) 

    response = {
        'success':True,
        'error':None,
        'transcription':None
    }

    # try recognizing the speech in the recording 
    # if a RequestError or UnknownValueError exception is caught 
    # update the response object accordingly 

    try:
        response['transcription'] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # google api was unreachable or unresponsive 
        response['success'] = False 
        response['error'] = 'The API is unavailable'
    except sr.UnknownValueError:
        #the speech was unintelligible or unrecognizable 
        response['error'] = "Unable to recognize speech"
    
    return response 

import random 
import time 
import IPython

IPython.display.Audio("eye_tiger.mp3")
WORDS = ['apple','banana','grape','orange','mango','lemon'] 
NUM_GUSSES = 3 
PROMPT_LIMIT = 5 # number of times we will allow our guests to play this game 

recognizer = sr.Recognizer()
microphone = sr.Microphone() 

word = random.choice(WORDS) 


# formatting the instruction string 
instructions = f"I'm thinking of one of these words: {WORDS} You have {NUM_GUSSES} tries to guess which one."  

# show the instructions and wait for three seconds to start the game 
print(instructions)
time.sleep(4) 

for i in range(NUM_GUSSES): 
    """
    get the guess from the user 
    if a transcription is returned, break out of loop and continuse 
    
    if no transcription is returned, and API request is failed break 
    out of the for loop 
    
    if api request succeeded but no transcription was returned, 
        reprompt the user to guess again. Do this PROMPT_LIMIT times
    """
    for j in range(PROMPT_LIMIT): 
        print(f"Guess {i + 1}. Speak!") 
        guess = recognize_speech_from_mic(recognizer,microphone)
        if guess['transcription']:
            break
        if guess['success'] != True:
            break
        print(f"I didn't catch that. Please will you repete? \n")
        print("\n")
    # even after prompt limit the error persists break out of the game 
    if guess['error']:
        print(f"ERROR: {guess['error']}")
        
    # show user the transcription
    print(f"You Said: {guess['transcription']}") 
    # determine if guess is correct and user has guesses remaining 
    guess_is_correct = guess['transcription'].lower() == word
    user_has_more_tries = i < NUM_GUSSES - 1 
    
    if guess_is_correct:
        print("Correct! You Win!.")
        break
    elif user_has_more_tries: 
        print('Incorrect. Try again.\n')
    else:
        print(f"Sorry, you lose!\nI was thinking of {word}")
        break
        
    
            

