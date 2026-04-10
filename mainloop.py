import pygame
import pygame_menu
import time
import csv
import os
from PIL import Image, ImageDraw, ImageFont
from fillpdf import fillpdfs
from typing import Tuple
import re


gender_height_misattributions_adjustment = 4
height_misattributions_adjustment = 4
gender_addition = 177
page2GraphStart = 209       # Moved to outside function for easier debugging
happygraphstarty = 513     # Moved to outside function for easier debugging
widthmisattributions = 284
heightmisattributions = 14

expInfo = {}
expInfo['date'] = time.strftime(("%Y_%m_%d-%H_%M"))
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
pygame.font.init() # you have to call this at the start if you want to use the module
clock = pygame.time.Clock()
padding = 100
# Setup the display
surface = pygame.display.set_mode()
displayX, displayY = surface.get_size()
surface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)# (displayX-10, displayY-10),pygame.RESIZABLE,display=0)
x, y = surface.get_size()
surfaceRectangle = surface.get_rect()

## Let's set up everything for the text
font1 = pygame.font.Font(pygame.font.match_font('sans'), 50)
font2 = pygame.font.Font(pygame.font.match_font('sans.bold'), 70)
my_font = pygame.font.Font('freesansbold.ttf', 55)
fontslist=[font1,font1,font1,font1,font1]
black = (0,0,0)
textTopPadding = 200
menuPadding = 100 # value in pixels
background_color = (200,200,200)


### Boolean Values go here ###  TODO: move all boolean values here
textDrawn = False
run = True
stimShow = False
displayStimuli = False
showInstructions = False
stimClear = False
displayMainMenu = True
stimuliPlayed = False
acceptAnswer = False
audioStarted = False
volumeAdjusted = False
waitForVolumeSet = True
display_buttons = False

## Here's how we work with our time stuff
trialDict = {}
trialResponses = {}
dictIndex = 0
trialIndex = 0
danvasubtest = 'Adult' # The default test if no selection is made, gets altered when drop select is changed
data_dict = {}
stimsList = {}
correctAnswers = {}
incorrectAnswers = {}
errorList = []
NamesCorrectAnswers = {}
intensity = ''
gender = ''
genderOfAnswer = ''
intensityOfAnswer = ''
correctAnswerForString = ''
currentAnswer = 0

highIntensityErrors = 0
lowIntensityErrors = 0
errorList = []
skippedErrors = 0
errorsByMisjudgement = 0
totalErrors = 0
happyHighIntensityErrors = 0
happyLowIntensityErrors = 0
sadHighIntensityErrors = 0
sadLowIntensityErrors = 0
angryHighIntensityErrors = 0
angryLowIntensityErrors = 0
fearfulHighIntensityErrors = 0
fearfulLowIntensityErrors = 0
happyErrors = 0
sadErrors = 0
angryErrors = 0
fearfulErrors = 0
lowIntensityErrors = 0
misattributedHappySad = 0
misattributedHappyAngry = 0
misattributedHappyFearful = 0
misattributedSadHappy = 0
misattributedSadAngry = 0
misattributedSadFearful = 0
misattributedAngryHappy = 0
misattributedAngrySad = 0
misattributedAngryFearful = 0
misattributedFearfulHappy = 0
misattributedFearfulSad = 0
misattributedFearfulAngry = 0
maleHappyErrors = 0
maleSadErrors = 0
maleAngryErrors = 0
maleFearfulErrors = 0
maleTotalErrors = 0
femaleHappyErrors = 0
femaleSadErrors = 0
femaleAngryErrors = 0
femaleFearfulErrors = 0
femaleTotalErrors = 0
stimuliEndTime = 0

dictionaryloop = 0
dictionaryloop2 = 0

stimuliStart = 0
displayTime = 2  # NOTE: Not sure if this is what I changed
stimuliEndTime = 1
# This is to set the number of the trial for scoring the right data

dictionarydefinitions = ["participant","age","skippedErrors","totalErrors","totalerrors","happyHighIntensityErrors","happyLowIntensityErrors",
                         "sadHighIntensityErrors","sadLowIntensityErrors","angryHighIntensityErrors",
                         "angryLowIntensityErrors","fearfulHighIntensityErrors","fearfulLowIntensityErrors",
                         "happyErrors","sadErrors","angryErrors","fearfulErrors","lowIntensityErrors",
                         "highIntensityErrors","misattributedHappySad","misattributedHappyAngry",
                         "misattributedHappyFearful","misattributedSadHappy","misattributedSadAngry",
                         "misattributedSadFearful","misattributedAngryHappy","misattributedAngrySad",
                         "misattributedAngryFearful","misattributedFearfulHappy","misattributedFearfulSad",
                         "misattributedFearfulAngry","errorsByMisjudgement","danvasubtest","maleHappyErrors",
                         "maleSadErrors","maleAngryErrors","maleFearfulErrors","maleTotalErrors",
                         "femaleHappyErrors","femaleSadErrors","femaleAngryErrors","femaleFearfulErrors","femaleTotalErrors",
                         "totalErrors1","totalErrors2","happyErrors2","sadErrors2","angryErrors2","fearfulErrors2",]


file = ('src/stimFiles/adult.csv')

def sanitize_filename(filename):
    # Define a regular expression pattern to match illegal characters
    illegal_chars_pattern = r'[<>:"/\\|?*\x00-\x1F\x7F-\x9F]'  # Windows illegal characters
    
    # Replace illegal characters with underscores
    sanitized_filename = re.sub(illegal_chars_pattern, '_', filename)
    
    return sanitized_filename

def testConditions(testIndex):
    global dictIndex, file, danvasubtest
    if testIndex == 0:
        file = ('src/stimFiles/'+ 'adultFaces.csv')
        danvasubtest = 'Adult Faces'
    if testIndex == 1:
        file = ('src/stimFiles/'+ 'adultPostures.csv')
        danvasubtest = 'Adult Postures'
    if testIndex == 2:
        file = ('src/stimFiles/'+ 'childFaces.csv')
        danvasubtest = 'Child Faces'
    if testIndex == 3:
        file = ('src/stimFiles/'+ 'adultVoices.csv')
        danvasubtest = 'Adult Voices'
    if testIndex == 4:
        file = ('src/stimFiles/'+ 'childVoices.csv')
        danvasubtest = 'Child Voices'

    with open(file, newline='') as csvfile:
        trialSetupConditions = csv.DictReader(csvfile)
        for lines in trialSetupConditions:
            trialDict[dictIndex] = (lines)
            dictIndex = dictIndex + 1
            
testConditions(0)

def showStim(showStim):
    
    global displayStimuli, stimShow
    if showStim == True:
        displayStimuli = True
        
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    global textDrawn
    rect = rect
    y = pygame.Rect(rect).top
    lineSpacing = -2
    # get the height of the font
    fontHeight = font.size("Tg")[1]
    while text:
        i = 1
        # determine if the row of text will be outside our area
        if y + fontHeight > pygame.Rect(rect).bottom:
            break
        # determine maximum width of line
        while font.size(text[:i])[0] < pygame.Rect(rect).width and i < len(text):
            i += 1
        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1
        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        surface.blit(image, (pygame.Rect(rect).left, y))
        y += fontHeight + lineSpacing
        # remove the text we just blitted
        text = text[i:]
    return text

def displayCredits():
    
    creditsStartTime = pygame.time.get_ticks()
    creditsEndTime = creditsStartTime + (3 * 1000)
    surface.fill(background_color)
    textbox = ((surfaceRectangle[0]+padding),(surfaceRectangle[1]+textTopPadding),(surfaceRectangle[2]-padding*2),(surfaceRectangle[2]-padding))
    credits = "Program Development by: Michael Woodcock & Dr. Virginia Wickline, 2023 Georgia Southern University"
    drawText(surface, credits, black, textbox, my_font)
    pygame.display.flip()
    while pygame.time.get_ticks() < creditsEndTime:
        clock.tick(30)

        # pygame.display.flip()
        # pygame.display.update()
        # pass
        # surface.fill(background_color)
        # textbox = ((surfaceRectangle[0]+padding),(surfaceRectangle[1]+textTopPadding),(surfaceRectangle[2]-padding*2),(surfaceRectangle[2]-padding))
        # credits = "Program Development by: Michael Woodcock & Dr. Virginia Wickline, 2023 Georgia Southern University"
        # drawText(surface, credits, black, textbox, my_font)
        # pygame.display.flip()

    creditsStartTime = pygame.time.get_ticks()
    creditsEndTime = creditsStartTime + (3 * 1000)
    surface.fill(background_color)
    credits2 = "Danva Stimuli used with permission from: Steve Nowicki, Emory University (see Nowicki & Carton, 1994)"
    drawText(surface, credits2, black, textbox, my_font)
    pygame.display.update()
    pygame.display.flip()
    while pygame.time.get_ticks() < creditsEndTime:
        clock.tick(30)
        # pygame.display.update()
        # pygame.display.flip()

    # surface.fill(background_color)
    # credits2 = "Danva Stimuli used with permission from: Steve Nowicki, Emory University (see Nowicki & Carton, 1994)"
    # drawText(surface, credits2, black, textbox, my_font)
    # pygame.display.update()
    # time.sleep(3)

displayCredits()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Fonts
font_size = int(y / 20)
font1 = pygame.font.Font(None, font_size)
font2 = pygame.font.Font(None, font_size + 20)  # Larger font for selected button

# Button information
button_labels = ["Happy", "Sad", "Angry", "Fearful", "Continue"]
button_count = len(button_labels)
button_padding = int(y / 15)
button_width = int((x - button_padding * (button_count + 1)) / button_count)
button_height = int(y / 15)

# Store button rects and fonts
button_rects = []
fontslist = [font1] * button_count

# Initialize button rects
def initialize_button_rects():
    button_rects.clear()
    for i in range(button_count):
        button_rects.append(pygame.Rect(button_padding * (i + 1) + button_width * i, y - button_height - button_padding, button_width, button_height))

initialize_button_rects()

def draw_buttons():
    # surface.fill(white)
    for i, rect in enumerate(button_rects):
        # Draw button border
        border_rect = pygame.Rect(rect.left - 2, rect.top - 2, rect.width + 4, rect.height + 4)
        pygame.draw.rect(surface, black, border_rect)
        
        pygame.draw.rect(surface, background_color, rect)  # Button inside
        text = fontslist[i].render(button_labels[i], True, black)  # Black text
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)

def handleClickedButton(button):
    global currentAnswer, trialIndex, fontslist, stimuliPlayed, stimuliEndTime, stimuliStart, audioStarted, acceptAnswer
    if button == 4:
        showStim(True)
        print('Clicked continue!')
        if acceptAnswer == False:
            print('Unable to accept answer at this time, please wait')
            return
        trialDict[trialIndex]['response'] = str(currentAnswer)
        trialIndex = trialIndex + 1 # update trial index
        currentAnswer = 0
        fontslist[button] = font1
        for index, item in enumerate(fontslist):
            fontslist[index] = font1
        stimuliPlayed = False
        stimuliStart = pygame.time.get_ticks()
        stimuliEndTime = stimuliStart + (displayTime * 1000)
        audioStarted = False
        print(trialIndex)
        # Handle continue button
        for i in range(button_count):
            fontslist[i] = font1
        pass
    else:
        currentAnswer = button + 1
        print(currentAnswer)
        for i in range(button_count):
            fontslist[i] = font1
        fontslist[button] = font2
    
def displayInstructions():
    surface.fill((background_color))
    textbox = ((surfaceRectangle[0]+padding),(surfaceRectangle[1]+textTopPadding),(surfaceRectangle[2]-padding*2),(surfaceRectangle[2]-padding))
    instructions = "I am going to show you some people's faces or play a voice clip and I want you to tell me how they feel. I want you to tell me if they are happy, sad, angry, or fearful (scared). Let's get started. Click anywhere to begin. (Esc will quit)"
    drawText(surface, instructions, black, textbox, my_font)
    
    waitForStart()
    
def displayUpdate(clear = 0):
    global events
    if clear == 0:
        # events = pygame.event.get()
        pygame.display.update()
    else:
        surface.fill((background_color))
        pygame.display.update()
    
def waitForStart():
    global showInstructions, stimShow, displayStimuli, stimuliStart, stimuliEndTime
    waitingForStart = True
    while waitingForStart:        
        events = pygame.event.poll()
        pygame.display.update()        

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            else:
                showInstructions = True
                stimShow = True
                    
        if pygame.mouse.get_pressed()[0]:
            showInstructions = True
            stimShow = True
            waitingForStart = False
            surface.fill(background_color)
            # pygame.display.flip() # TEST DISABLE THIS
            # pygame.display.update()
            displayStimuli = True
            stimuliStart = pygame.time.get_ticks()
            stimuliEndTime = stimuliStart + (displayTime * 1000)
            surface.fill((background_color))
            pass
        
        
        # for event in events: 
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         quit()
        #     elif event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_ESCAPE:
        #             exit()
        #         else:
        #             showInstructions = True
        #             stimShow = True
                    
        #     if pygame.mouse.get_pressed()[0]:
        #         showInstructions = True
        #         stimShow = True
        #         waitingForStart = False
        #         surface.fill(background_color)
        #         # pygame.display.flip() # TEST DISABLE THIS
        #         # pygame.display.update()
        #         displayStimuli = True
        #         stimuliStart = pygame.time.get_ticks()
        #         stimuliEndTime = stimuliStart + (displayTime * 1000)
        #         pass

def displayAudioAdjustmentScreen():
    global waitForVolumeSet
    audioFile = 'src/stimFiles/other/adjustvolume.mp3'
    pygame.mixer.music.load(audioFile)
    pygame.mixer.music.play(-1)

    while waitForVolumeSet:
        surface.fill(background_color)
        textbox = ((displayX/2 - 600 ),(displayY/2 - 200 ),(displayX/2 + 400 ),(displayY/2 + 200 ))
        message = "Please adjust your volume until you can hear the audio file clearly.  Double click anywhere when completed to continue."
        drawText(surface, message, black, textbox, my_font)
        pygame.display.update()
        if waitForVolumeSet == False:
            audioFile = 'src/stimFiles/other/adjustvolume.mp3'
            pygame.mixer.music.load(audioFile)
            pygame.mixer.music.play(-1)
        for event in pygame.event.get(): 
            if pygame.mouse.get_pressed()[0]:
                waitForVolumeSet = False
                pygame.mixer.music.play(0)
    

def present_stimuli():
    global displayMainMenu, stimuliPlayed, currentAnswer, trialIndex, displayStimuli, stimShow, stimuliEndTime, acceptAnswer, display_buttons
    displayMainMenu = False
    surface.fill((background_color))
    if int(trialIndex) >=24:
        return
    (trialDict[trialIndex]['stimFile'])
    # currentTime = pygame.time.get_ticks()
    display_buttons = True
    if displayStimuli == True:
        currentTime = pygame.time.get_ticks()
        # acceptAnswer = False
        while currentTime < stimuliEndTime:
            events = pygame.event.get() #pygame.event.wait()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print('Is current time less than or equal to stimuli end time?')
                        print ( currentTime < stimuliEndTime)
                        for i, rect in enumerate(button_rects):
                            if rect.collidepoint(event.pos):
                                print('Clicked number', i)
                                handleClickedButton(i)
                                break
            draw_buttons()
            currentTime = pygame.time.get_ticks()
            acceptAnswer = False
            
            try:
                #displayUpdate()
                stimuli = pygame.image.load((trialDict[trialIndex]['stimFile'])).convert() # i did use (file).convert()
                stimuliWidth = stimuli.get_width()
                stimuliHeight = stimuli.get_height()
                width, height = surface.get_size()
                pictureScale = .6
                # let's make sure we can scale the image according to actual window size.  Note I based
                # scaling off the display height to deal better with widescreen displays and different aspect ratios
                    # Here we will make the scaled picture pixel height
                scaledPictureHeight = height*(pictureScale)
                    # Here we will make the scaled picture pixel width.  Note we must base it
                    # off of the scaled picture height because we want to maintain the relation
                    # of the picture X being a multiple of the height.  
                scaledPictureWidth = (scaledPictureHeight/stimuliHeight)*stimuliWidth
                # Define variables according to scaled picture information
                pictureXCenter = (scaledPictureWidth/2)
                pictureYCenter = (scaledPictureHeight/2)
                pictureXStart = (width/2)-pictureXCenter
                pictureYStart = (height/2)-pictureYCenter
                # lets put the picture on the screen
                # acceptAnswer = True # Edited August 18
                displayUpdate()
                surface.blit(pygame.transform.scale(stimuli, (scaledPictureWidth, scaledPictureHeight)), (pictureXStart,pictureYStart))
            except:
                if waitForVolumeSet == True:
                    displayAudioAdjustmentScreen()
                if int(trialIndex) >=24:
                    return
                if stimuliPlayed == False:
                    currentAnswer = 0
                    audioFile = (trialDict[trialIndex]['stimFile'])
                    pygame.mixer.music.load(audioFile)
                    pygame.mixer.music.play(0)
                    stimuliPlayed = True
                    displayStimuli = False

        if currentTime >= stimuliEndTime:
            acceptAnswer = True
            surface.fill(background_color)
            pygame.display.update() # TEST disable this
            displayStimuli = False
            stimShow = False

def createDictionary():
    global dictionaryloop, skippedErrors, totalErrors, data_dict, errorList,NamesCorrectAnswers, trialDict, incorrectAnswers, correctAnswers, stimsList, correctAnswerForString, femaleTotalErrors, maleTotalErrors
    global highIntensityErrors, lowIntensityErrors, happyErrors, sadErrors, angryErrors, fearfulErrors
    global happyHighIntensityErrors, happyLowIntensityErrors, sadHighIntensityErrors, sadLowIntensityErrors, angryHighIntensityErrors, angryLowIntensityErrors, fearfulHighIntensityErrors, fearfulLowIntensityErrors
    global femaleHappyErrors, femaleSadErrors, femaleAngryErrors, femaleFearfulErrors
    global maleHappyErrors, maleSadErrors, maleAngryErrors, maleFearfulErrors, misattributedHappySad, misattributedHappyAngry, misattributedHappyFearful, misattributedSadHappy, misattributedSadAngry, misattributedSadFearful, misattributedAngryHappy, misattributedAngrySad, misattributedAngryFearful, misattributedFearfulHappy, misattributedFearfulSad, misattributedFearfulAngry
    data_dict = {}
    stimsList = {}
    incorrectAnswers = {}
    errorList = []
    NamesCorrectAnswers = {}
    genderOfAnswer = ''
    intensityOfAnswer = ''
    totalerrors = totalErrors
    
    for i in trialDict:
        # Let's do the basic things first:
        stimsList['stim' + str(dictionaryloop)] = (trialDict[dictionaryloop]['stimFile'])
        
        if trialDict[dictionaryloop]['response'] == '0':
            skippedErrors = skippedErrors + 1
        
        # Let's concact a string to fill in the correct answer with intensity and gender column, we'll start with emotion
        if trialDict[dictionaryloop]['correctAnswer'] == '1':
            correctAnswerForString = 'Happy '
        elif trialDict[dictionaryloop]['correctAnswer'] == '2':
            correctAnswerForString = 'Sad '
        elif trialDict[dictionaryloop]['correctAnswer'] == '3':
            correctAnswerForString = 'Angry '
        elif trialDict[dictionaryloop]['correctAnswer'] == '4':
            correctAnswerForString = 'Fearful '
            
        # Now let's grab the intensity
        if  trialDict[dictionaryloop]['intensity'] == '1':
            intensityOfAnswer = 'Low '
        elif trialDict[dictionaryloop]['intensity'] == '2':
            intensityOfAnswer = 'High '
        else:
            pass
        
        # Now let's grab the gender:
        if  trialDict[dictionaryloop]['stimuliGender'] == '1':
            genderOfAnswer = 'Female'
        elif trialDict[dictionaryloop]['stimuliGender'] == '2':
            genderOfAnswer = 'Male'
        else:
            pass
        
        # Now let's plug that into the PDF
        correctAnswers['correctAnswer'+ str(dictionaryloop)] = (correctAnswerForString) + (intensityOfAnswer) + (genderOfAnswer)

        if trialDict[dictionaryloop]['response'] != trialDict[dictionaryloop]['correctAnswer']:
            totalErrors = totalErrors + 1
            response = int(trialDict[dictionaryloop]['response'])
            correctAnswerKey = trialDict[dictionaryloop]['correctAnswer']
            
            if trialDict[dictionaryloop]['stimuliGender'] == '2':
                maleTotalErrors = maleTotalErrors + 1
            elif trialDict[dictionaryloop]['stimuliGender'] == '1':
                femaleTotalErrors = femaleTotalErrors + 1
            else:
                pass
            
            if  trialDict[dictionaryloop]['intensity'] == '1':
                lowIntensityErrors = lowIntensityErrors + 1
            elif trialDict[dictionaryloop]['intensity'] == '2':
                highIntensityErrors = highIntensityErrors + 1
            else:
                pass        
            
            if correctAnswerKey == '1':
                happyErrors = happyErrors + 1
                if  trialDict[dictionaryloop]['intensity'] == '1':
                    happyLowIntensityErrors = happyLowIntensityErrors + 1
                elif trialDict[dictionaryloop]['intensity'] == '2':
                    happyHighIntensityErrors = happyHighIntensityErrors + 1
                else:
                    pass        

                if response == 2:
                    misattributedHappySad = misattributedHappySad + 1
                elif response == 3:
                    misattributedHappyAngry = misattributedHappyAngry + 1
                elif response == 4:
                    misattributedHappyFearful = misattributedHappyFearful + 1
                else:
                    pass
                
                if trialDict[dictionaryloop]['stimuliGender'] == '2':
                    maleHappyErrors = maleHappyErrors + 1
                elif trialDict[dictionaryloop]['stimuliGender'] == '1':
                    femaleHappyErrors = femaleHappyErrors + 1
                else: 
                    pass
                
            if correctAnswerKey == '2':
                sadErrors = sadErrors + 1
                if  trialDict[dictionaryloop]['intensity'] == '1':
                    sadLowIntensityErrors = sadLowIntensityErrors + 1     
                elif trialDict[dictionaryloop]['intensity'] == '2':
                    sadHighIntensityErrors = sadHighIntensityErrors + 1                
                else:
                    pass

                if response == 1:
                    misattributedSadHappy = misattributedSadHappy + 1
                elif response == 3:
                    misattributedSadAngry = misattributedSadAngry + 1
                elif response == 4:
                    misattributedSadFearful = misattributedSadFearful + 1
                else:
                    pass
                
                if trialDict[dictionaryloop]['stimuliGender'] == '2':
                    maleSadErrors = maleSadErrors + 1
                elif trialDict[dictionaryloop]['stimuliGender'] == '1':
                    femaleSadErrors = femaleSadErrors + 1
                else: 
                    pass
                
            if correctAnswerKey == '3':
                angryErrors = angryErrors + 1
                if  trialDict[dictionaryloop]['intensity'] == '1':
                    angryLowIntensityErrors = angryLowIntensityErrors + 1        
                elif trialDict[dictionaryloop]['intensity'] == '2':
                    angryHighIntensityErrors = angryHighIntensityErrors + 1                
                else:
                    pass
                
                if response == 1:
                    misattributedAngryHappy = misattributedAngryHappy + 1
                elif response == 2:
                    misattributedAngrySad = misattributedAngrySad + 1
                elif response == 4:
                    misattributedAngryFearful = misattributedAngryFearful + 1
                else:
                    pass
                
                if trialDict[dictionaryloop]['stimuliGender'] == '2':
                    maleAngryErrors = maleAngryErrors + 1
                elif trialDict[dictionaryloop]['stimuliGender'] == '1':
                    femaleAngryErrors = femaleAngryErrors + 1
                else: 
                    pass
                
            if correctAnswerKey == '4':
                fearfulErrors = fearfulErrors + 1
                if  trialDict[dictionaryloop]['intensity'] == '1':
                    fearfulLowIntensityErrors = fearfulLowIntensityErrors + 1
                elif trialDict[dictionaryloop]['intensity'] == '2':
                    fearfulHighIntensityErrors = fearfulHighIntensityErrors + 1
                else:
                    pass
                
                if response == 1:
                    misattributedFearfulHappy = misattributedFearfulHappy + 1
                elif response == 2:
                    misattributedFearfulSad = misattributedFearfulSad + 1
                elif response == 3:
                    misattributedFearfulAngry = misattributedFearfulAngry + 1
                else:
                    pass
                
                if trialDict[dictionaryloop]['stimuliGender'] == '2':
                    maleFearfulErrors = maleFearfulErrors + 1
                elif trialDict[dictionaryloop]['stimuliGender'] == '1':
                    femaleFearfulErrors = femaleFearfulErrors + 1
                else:
                    pass
            else:
                pass

            if response == 1:
                incorrectAnswers['incorrectAnswer'+ str(dictionaryloop)] = 'Happy'        
            elif response == 2:
                incorrectAnswers['incorrectAnswer'+ str(dictionaryloop)] = 'Sad'
            elif response == 3:
                incorrectAnswers['incorrectAnswer'+ str(dictionaryloop)] = 'Angry'
            elif response == 4:
                incorrectAnswers['incorrectAnswer'+ str(dictionaryloop)] = 'Fearful'
            else:
                incorrectAnswers['incorrectAnswer'+ str(dictionaryloop)] = 'Skipped'
        dictionaryloop = dictionaryloop + 1

def createPDF():
    global dictionaryloop, dictionaryloop2, correctAnswers, age, participant, errorsByMisjudgement, session, sessionInput
    print(session)
    totalerrors = totalErrors
    age = ageInput.get_value()
    participant = participantInput.get_value()
    errorsByMisjudgement = totalErrors - skippedErrors
    
    totalErrors1 = totalerrors
    totalErrors2 = totalerrors
    happyErrors2 = happyErrors
    sadErrors2 = sadErrors
    angryErrors2 = angryErrors
    fearfulErrors2 = fearfulErrors

    for i in (dictionarydefinitions):
        data_dict [dictionarydefinitions[dictionaryloop2]] = (eval(dictionarydefinitions[dictionaryloop2]))
        dictionaryloop2 = dictionaryloop2 + 1

    data_dict.update(stimsList)
    data_dict.update(expInfo)
    data_dict.update(incorrectAnswers)
    data_dict.update(correctAnswers)

    happycolor = "#00FF00"
    sadcolor = "#0000FF"
    angrycolor = "#FF0000"
    fearfulcolor = "#FFFF00"
    malecolor = "#FF8300"
    femalecolor = "#7800E1"

    widthmain = 480
    heightmain = 30

    totalerrorsincrement = widthmain/24

    # widthmisattributions = 378  ## NOTE: Moved these to beginning of program for easier edits
    # heightmisattributions = 20
    misattributionerrorsincrement = widthmisattributions/6

    widthgendererrors = 378
    errorsincrementgender = widthgendererrors/24

    happystartx = 0
    happyendx = (happyErrors * totalerrorsincrement)
    sadstartx = happyendx
    sadendx = sadstartx + (sadErrors * totalerrorsincrement)
    angrystartx = sadendx
    angryendx = angrystartx + (angryErrors * totalerrorsincrement)
    fearfulstartx = angryendx
    fearfulendx = fearfulstartx + (fearfulErrors * totalerrorsincrement)

    happyrectangle = [(0, 0), (happyendx , heightmain)]
    sadrectangle = [(sadstartx,0),(sadendx,heightmain) ]
    angryrectangle = [(angrystartx,0), (angryendx, heightmain)]
    fearfulrectangle = [(fearfulstartx,0), (fearfulendx,heightmain)]
    
    # creating new Image object
    totalerrorsgraph = Image.new("RGB", (widthmain, heightmain),color = "#FFFFFF")
    # create rectangle image for happy errors
    happyerrorsrectangle = ImageDraw.Draw(totalerrorsgraph)
    saderrorsrectangle = ImageDraw.Draw(totalerrorsgraph)
    angryerrorsrectangle = ImageDraw.Draw(totalerrorsgraph)
    fearfulerrorsrectangle = ImageDraw.Draw(totalerrorsgraph)

    happyerrorsrectangle.rectangle(happyrectangle, fill =happycolor, outline=None)
    saderrorsrectangle.rectangle(sadrectangle, fill =sadcolor, outline=None)
    angryerrorsrectangle.rectangle(angryrectangle, fill =angrycolor, outline=None)
    fearfulerrorsrectangle.rectangle(fearfulrectangle, fill =fearfulcolor, outline=None)

    totalerrorsgraph.save("src/graphPictures/totalerrorsgraph.jpg")


    #create picture for happy misattributions
    happystartx = 0
    happyendx = (0) # only since we're on the happy misattributions graph
    sadstartx = happyendx
    sadendx = sadstartx + (misattributedHappySad * misattributionerrorsincrement)
    angrystartx = sadendx
    angryendx = angrystartx + (misattributedHappyAngry * misattributionerrorsincrement)
    fearfulstartx = angryendx
    fearfulendx = fearfulstartx + (misattributedHappyFearful * misattributionerrorsincrement)

    happyrectangle = [(0, 0), (happyendx , heightmisattributions)]
    sadrectangle = [(sadstartx,0),(sadendx,heightmisattributions) ]
    angryrectangle = [(angrystartx,0), (angryendx, heightmisattributions)]
    fearfulrectangle = [(fearfulstartx,0), (fearfulendx,heightmisattributions)]
    # creating new Image object
    happyMisattributionsGraph = Image.new("RGB", (widthmisattributions, heightmisattributions),color = "#FFFFFF")

    # create rectangle image for happy Errors
    happyErrorsrectangle = ImageDraw.Draw(happyMisattributionsGraph)
    sadErrorsrectangle = ImageDraw.Draw(happyMisattributionsGraph)
    angryErrorsrectangle = ImageDraw.Draw(happyMisattributionsGraph)
    fearfulErrorsrectangle = ImageDraw.Draw(happyMisattributionsGraph)

    sadErrorsrectangle.rectangle(sadrectangle, fill =sadcolor, outline=None)
    angryErrorsrectangle.rectangle(angryrectangle, fill =angrycolor, outline=None)
    fearfulErrorsrectangle.rectangle(fearfulrectangle, fill =fearfulcolor, outline=None)

    happyMisattributionsGraph.save("src/graphPictures/happyMisattributions.jpg")

    happystartx = 0
    happyendx = (misattributedSadHappy * misattributionerrorsincrement) 
    sadstartx = happyendx
    sadendx = sadstartx # only since we're on the sad misattributions graph
    angrystartx = sadendx
    angryendx = angrystartx + (misattributedSadAngry * misattributionerrorsincrement)
    fearfulstartx = angryendx
    fearfulendx = fearfulstartx + (misattributedSadFearful*misattributionerrorsincrement)

    happyrectangle = [(0, 0), (happyendx , heightmisattributions)]
    angryrectangle = [(angrystartx,0), (angryendx, heightmisattributions)]
    fearfulrectangle = [(fearfulstartx,0), (fearfulendx,heightmisattributions)]

    # creating new Image object
    sadMisattributionsGraph = Image.new("RGB", (widthmisattributions, heightmisattributions),color = "#FFFFFF")

    # create rectangle image for happy Errors
    happyErrorsrectangle = ImageDraw.Draw(sadMisattributionsGraph)
    angryErrorsrectangle = ImageDraw.Draw(sadMisattributionsGraph)
    fearfulErrorsrectangle = ImageDraw.Draw(sadMisattributionsGraph)

    happyErrorsrectangle.rectangle(happyrectangle, fill =happycolor, outline=None)
    angryErrorsrectangle.rectangle(angryrectangle, fill =angrycolor, outline=None)
    fearfulErrorsrectangle.rectangle(fearfulrectangle, fill =fearfulcolor, outline=None)

    sadMisattributionsGraph.save("src/graphPictures/sadMisattributions.jpg")

    happystartx = 0
    happyendx = happystartx + (misattributedAngryHappy * misattributionerrorsincrement) 
    sadstartx = happyendx
    sadendx = sadstartx + (misattributedAngrySad * misattributionerrorsincrement)
    angrystartx = sadendx
    angryendx = angrystartx # only since we're on the Angry misattributions graph
    fearfulstartx = angryendx
    fearfulendx = fearfulstartx + (misattributedAngryFearful * misattributionerrorsincrement)

    happyrectangle = [(0, 0), (happyendx , heightmisattributions)]
    sadrectangle = [(sadstartx,0),(sadendx,heightmisattributions) ]
    fearfulrectangle = [(fearfulstartx,0), (fearfulendx,heightmisattributions)]


    # creating new Image object
    angryMisattributionsGraph = Image.new("RGB", (widthmisattributions, heightmisattributions),color = "#FFFFFF")

    # create rectangle image for happy Errors
    happyErrorsrectangle = ImageDraw.Draw(angryMisattributionsGraph)
    sadErrorsrectangle = ImageDraw.Draw(angryMisattributionsGraph)
    fearfulErrorsrectangle = ImageDraw.Draw(angryMisattributionsGraph)

    happyErrorsrectangle.rectangle(happyrectangle, fill =happycolor, outline=None)
    sadErrorsrectangle.rectangle(sadrectangle, fill =sadcolor, outline=None)
    fearfulErrorsrectangle.rectangle(fearfulrectangle, fill =fearfulcolor, outline=None)

    angryMisattributionsGraph.save("src/graphPictures/angryMisattributions.jpg")

    happystartx = 0
    happyendx = (misattributedFearfulHappy * misattributionerrorsincrement) 
    sadstartx = happyendx
    sadendx = sadstartx + (misattributedFearfulSad*misattributionerrorsincrement)
    angrystartx = sadendx
    angryendx = angrystartx + (misattributedFearfulAngry*misattributionerrorsincrement)
    fearfulstartx = angryendx
    fearfulendx = fearfulstartx # because we are making the fearful graph

    happyrectangle = [(0, 0), (happyendx , heightmisattributions)]
    sadrectangle = [(sadstartx,0),(sadendx,heightmisattributions) ]
    angryrectangle = [(angrystartx,0), (angryendx, heightmisattributions)]
    fearfulrectangle = [(fearfulstartx,0), (fearfulendx,heightmisattributions)]


    # creating new Image object
    fearfulMisattributionsGraph = Image.new("RGB", (widthmisattributions, heightmisattributions),color = "#FFFFFF")
    happyErrorsrectangle = ImageDraw.Draw(fearfulMisattributionsGraph) # create rectangle image for happy Errors
    sadErrorsrectangle = ImageDraw.Draw(fearfulMisattributionsGraph) 
    angryErrorsrectangle = ImageDraw.Draw(fearfulMisattributionsGraph) 
    happyErrorsrectangle.rectangle(happyrectangle, fill =happycolor, outline=None) 
    sadErrorsrectangle.rectangle(sadrectangle, fill =sadcolor, outline=None) 
    angryErrorsrectangle.rectangle(angryrectangle, fill =angrycolor, outline=None) 
    fearfulMisattributionsGraph.save("src/graphPictures/fearfulMisattributions.jpg")

    # Gender Errors Graph
    malestartx = 0
    maleendx = malestartx + (maleTotalErrors * errorsincrementgender) 
    femalestartx = maleendx
    femaleendx = femalestartx + (femaleTotalErrors * errorsincrementgender)
    malerectangle = [(0, 0), (maleendx , heightmisattributions+ height_misattributions_adjustment)]
    femalerectangle = [(femalestartx,0),(femaleendx,heightmisattributions+ height_misattributions_adjustment) ]
    
    # creating new Image object
    genderErrorsGraph = Image.new("RGB", (widthgendererrors, heightmisattributions+ height_misattributions_adjustment),color = "#FFFFFF")
    # create rectangle image for happy Errors
    maleTotalErrorsrectangle = ImageDraw.Draw(genderErrorsGraph)
    femaleTotalErrorsrectangle = ImageDraw.Draw(genderErrorsGraph)
    maleTotalErrorsrectangle.rectangle(malerectangle, fill =malecolor, outline=None)
    femaleTotalErrorsrectangle.rectangle(femalerectangle, fill =femalecolor, outline=None)
    genderErrorsGraph.save("src/graphPictures/errorsbygender.jpg")

    # Now let's insert the images

    fillpdfs.place_image('src/graphPictures/totalerrorsgraph.jpg', 68, 115, 'src/pdfMagic/blankDocumentNumberLine.pdf', 'src/pdfMagic/completed.pdf', 1, width=475, height=100)


    # page2GraphStart = 120       # Moved to outside function for easier debugging
    # happygraphstarty = -161     # Moved to outside function for easier debugging
    #The following are for the other graphs
    fillpdfs.place_image('src/graphPictures/happyMisattributions.jpg', page2GraphStart, happygraphstarty, 'src/pdfMagic/completed.pdf', 'src/pdfMagic/completed1.pdf', 2, width=widthmisattributions, height=heightmisattributions)
    fillpdfs.place_image('src/graphPictures/sadMisattributions.jpg', page2GraphStart, happygraphstarty-43, 'src/pdfMagic/completed1.pdf', 'src/pdfMagic/completed2.pdf', 2, width=widthmisattributions, height=heightmisattributions)
    fillpdfs.place_image('src/graphPictures/angryMisattributions.jpg', page2GraphStart, happygraphstarty-85, 'src/pdfMagic/completed2.pdf', 'src/pdfMagic/completed3.pdf', 2, width=widthmisattributions, height=heightmisattributions)
    fillpdfs.place_image('src/graphPictures/fearfulMisattributions.jpg', page2GraphStart, happygraphstarty-126, 'src/pdfMagic/completed3.pdf', 'src/pdfMagic/completed4.pdf', 2, width=widthmisattributions, height=heightmisattributions)
    fillpdfs.place_image('src/graphPictures/errorsbygender.jpg',page2GraphStart, happygraphstarty-238, 'src/pdfMagic/completed4.pdf', 'src/pdfMagic/completed.pdf', 2, width=widthmisattributions, height=heightmisattributions)
    #We need to remove invalid characters from the file name string:  / ? < > \ : * | " 
    participant = participant.replace(' ', '_')  # Replace spaces with underscores
    participant = participant.replace('/', '_')  # Replace slashes with underscores
    participant = participant.replace(':', '_')  # Replace colons with underscores
    participant = participant.replace('?', '_')  # Replace question marks with underscores
    participant = participant.replace('<', '_')
    participant = participant.replace('>', '_')
    participant = participant.replace('*', '_')
    participant = participant.replace('|', '_')
    participant = participant.replace('\\', '_')
    participant = participant.replace('"', '_')
    participant = participant.replace("'", '_')
    session = session.replace(' ', '_')  # Replace spaces with underscores
    session = session.replace('/', '_')  # Replace slashes with underscores
    session = session.replace(':', '_')  # Replace colons with underscores
    session = session.replace('?', '_')  # Replace question marks with underscores
    session = session.replace('<', '_')
    session = session.replace('>', '_')
    session = session.replace('*', '_')
    session = session.replace('|', '_')
    session = session.replace('\\', '_')
    session = session.replace('"', '_')
    session = session.replace("'", '_')
    fillpdfs.write_fillable_pdf('src/pdfMagic/completed.pdf', ('reports/'+expInfo['date']+participant+danvasubtest+'-session'+session+'.pdf'), data_dict, flatten=False) # was fillpdfs.write_fillable_pdf('src/pdfMagic/completed.pdf', 'reports/completed.pdf', data_dict, flatten=False)



    
    # for some reason I am not having luck directly opening the file, and some coding other than the most obvious seems necesary

    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath('reports/'+expInfo['date']+participant+danvasubtest+'-session'+session+'.pdf', cur_path)
    os.startfile(new_path)

def mainMenuState():#(state)
    global displayMainMenu, showInstructions
    displayMainMenu = False
    showInstructions = True
    displayInstructions()


def viewPreviousReports():
    # Minimize the pygame window
    print('Your main window has been minimized, please re-open it from task bar to return to the program.')
    pygame.display.iconify()
    # Open the 'reports' folder in the current working directory
    folder_to_open = os.path.join(os.getcwd(), 'reports')
    os.startfile(folder_to_open)


width, height = surface.get_size()

menu = pygame_menu.Menu('Welcome to the DANVA II test, please enter your information below', width - menuPadding, height - menuPadding,
                    theme=pygame_menu.themes.THEME_BLUE)

sessionInput = menu.add.text_input('Session :  ', default='001')
session= sessionInput.get_value()
participantInput = menu.add.text_input('Participant :  ', default='')
participant = participantInput.get_value() # put this in the pdf function
ageInput = menu.add.text_input('Age :    ', default='')
age = ageInput.get_value()

def printSelected (value: Tuple[str,int], index = str):
    global file, dictIndex
    test = (value[0])
    testIndex = (test[1])
    dictIndex = 0
    testConditions(testIndex)

testSelector = menu.add.dropselect(
    onchange=(printSelected),
    title='Select Test',
    items=[('Adult Faces', 0),
        ('Adult Postures', 1),
        ('Child Faces', 2),
        ('Adult Voices', 3),
        ('Child Voices', 4)
        ],
    default=0,
    open_middle=False,  # Opens in the middle of the menu
    selection_box_height=10,
    selection_box_width=300,
    selection_infinite=True,

)
menu.add.button('Start', mainMenuState)
menu.add.button('View Previous Reports', viewPreviousReports)
menu.add.button('Quit', pygame_menu.events.EXIT)
pygame.event.set_blocked(pygame.WINDOWCLOSE)
pygame.event.set_blocked(pygame.WINDOWENTER)
pygame.event.set_blocked(pygame.WINDOWEXPOSED)
pygame.event.set_blocked(pygame.WINDOWLEAVE)
pygame.event.set_blocked(pygame.ACTIVEEVENT)
pygame.event.set_blocked(pygame.WINDOWFOCUSGAINED)
pygame.event.set_blocked(pygame.CLIPBOARDUPDATE)
pygame.event.set_blocked(pygame.VIDEOEXPOSE)
pygame.event.set_blocked(pygame.WINDOWFOCUSLOST)
pygame.event.set_blocked(pygame.TEXTEDITING)  #  TEST ONLY!  
pygame.event.set_blocked(pygame.AUDIODEVICEADDED)
pygame.event.set_blocked(pygame.MOUSEMOTION)
while run:

    events = pygame.event.get() #pygame.event.wait()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        print('Clicked number', i)
                        handleClickedButton(i)
                        break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                run = False
                quit()

                
    # events = [events]

    #surface.fill((200, 200, 200))
    if displayMainMenu == True:
        menu.update(events)
        menu.draw(surface)  
        # displayUpdate()  
        pygame.display.update()
        # pygame.display.flip() # TEST REMOVE THIS
    if showInstructions == False and displayMainMenu == False: 
        displayInstructions()
    if showInstructions == True:
        
        #drawButtons()
        pass
    if displayStimuli == True:
        present_stimuli()
        # acceptAnswer = False
    if pygame.mixer.music.get_busy() == True:
        acceptAnswer = False
        # displayX, displayY
        textbox = ((displayX/2 - 100 ),(displayY/2 - 100 ),(displayX/2 + 100 ),(displayY/2 + 100 ))
        message = "Now Playing #" + str(trialIndex + 1)
        drawText(surface, message, black, textbox, my_font)
        # pygame.display.flip()
        audioStarted = True
        stimuliPlayed = False
        displayStimuli = False
        pygame.display.update()
    # if pygame.mixer.music.get_busy() == False:
    #     pygame.display.flip()
    if pygame.mixer.music.get_busy() == False and audioStarted == True:
        surface.fill((200, 200, 200))
        acceptAnswer = True
        pass
    if display_buttons == True:
        draw_buttons()
    displayUpdate()
    clock.tick(30)
    if trialIndex >= len(trialDict):
        createDictionary()
        createPDF()
        # run = False
        # pygame.display.iconify()
        trialIndex = 0
        displayMainMenu = True
        displayStimuli = False
        display_buttons = False
        # mainMenuState()
        # pygame.display.flip() # TEST REMOVE THIS
        showInstructions = True
        pygame.display.quit()
        pygame.quit()
        time.sleep(3.0)
        break