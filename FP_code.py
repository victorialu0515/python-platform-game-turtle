#Victoria Lu
#May 30, 2023
#FP_code.py
#This program uses turtle to create a platform game where the character collects treats and has to shoot a certain amoount of them at an angry dog

#import
import turtle, time
#final value, not changed: [x coord, y coord, platform length]
platformPositions = [[-370, -270, 740], [200, -185, 200], [-400, -95, 625], [-400, 5, 100], [-100, 5, 500], [140, 90, 150], [-180, 130, 300]] 


# jump()
# @param: none
# @return: none
def jump():
    global vY, vX, jumpUp
    #prevents double jumping so character can only jump when jump up is false when it is on a platform
    if (jumpUp == False):
        #slightly diagonal jumping
        if (isLeft):
            vX -= 10
        else:
            vX += 10
        #could change
        for i in range(110):
            vY += 1
        if (isLeft):
            vX -= 10
        else:
            vX += 10
        #not able to jump again (until jumpUp set back to false in platformCollide)
        jumpUp = True
    
# moveLeft()
# @param: none
# @return: none
def moveLeft():
    global vX, isLeft 
    #subtract 20 from xpos to move left every time left arrow pressed
    vX -= 20
    #direction going left
    isLeft = True

# moveRight()
# @param: none
# @return: none
def moveRight():
    global vX, isLeft
    #add 20 from xpos to move right every time right arrow pressed
    vX += 20
    #direction going right
    isLeft = False
   
# shoot()
# @param: none
# @return: none 
def shoot():
    global score, vX, vY, dX, dY, shooting, shots
    #have to have treats collected to shoot and can't already be shooting to avoid double shooting
    if (score > 0 and shooting == False):
        #new temporary turtle for shooting treat
        temp = turtle.Turtle()
        temp.hideturtle()
        temp.speed("fastest")
        temp.penup()
        temp.goto(vX, vY)
        temp.shape("treat.gif")
        tempX = vX
        tempY = vY
        temp.showturtle()
        #treat keep moving left until it hits the enemy or wall
        while (tempX > -370 and enemyCollide(tempX, tempY, dX, dY) == False):
            #can't double shoot
            shooting = True
            tempX -= 18
            temp.goto(tempX, tempY)
        temp.hideturtle()
        #one less treat collected because it was shot
        score -= 1
        shots += 1
        #able to shoot again
        shooting = False

# enemyCollide()
# @param: tX:int, tY:int, dX:int, dY:int
# @return: boolean
# check collision
def enemyCollide(tX, tY, dX, dY):
    global enemyIndex, hits
    #coordinates equal to enemy bordered coordinates
    if (tX <= dX + 20 and tX >= dX and tY <= dY + 20 and tY >= dY - 30):
        #change enemy image shape to next one
        enemyIndex += 1
        hits += 1
        return True
    else:
        return False

# checkWin()
# @param: none
# @return: boolean
def checkWin():
    global enemyIndex
    #on the last enemy image shape
    if (enemyIndex >= len(enemies)-1):
        return True
    else:
        return False
    
# enemyPlayerCollide()
# @param: none
# @return: boolean
# check player enemy collision
def enemyPlayerCollide():
    global vX, vY, dX, dY, lastPlat
    #player coordinates equal to enemy bordered coordinates
    if (lastPlat != 5 and vX <= dX + 25 and vX >= dX - 25 and vY <= dY + 10 and vY >= dY - 10):
        return True

# platformCollide()
# @param: x:int, y:int
# @return: x:int, y:int, gravity:boolean
def platformCollide(x, y):
    global jumpUp, lastPlat
    gravity = True
    #comparing each platform coordinates with player coordinates
    
    #within x range
    if (x >= -370-30 and x <= -370 + 740 + 20):
        #within y range
        if (y >= -270+25  and y <= -270+45):
            #numbered from order of platforms created
            lastPlat = 1
            #no gravity meaning not falling through platform
            gravity = False
            #jumping allowed
            jumpUp = False
            return x, -228, gravity
    
    if (x >= 200-15 and x <= 200 + 200 + 15):
        if (y >= -185  and y <= -145):
            lastPlat = 2
            gravity = False
            jumpUp = False
            return x, -145, gravity
        #if hitting bottom of platform to prevent jumping through
        elif (y >= -250 and lastPlat == 1):
            return x, -228, gravity #lastPlat coord
            
    if (x >= -400-15 and x <= -400 + 625 + 15):
        if (y >= -75  and y<= -55):
            lastPlat = 3
            gravity = False
            jumpUp = False
            return x, -55, gravity
        elif (y >= -140 and lastPlat == 2 and lastPlat != 1):
            return x, -145, gravity 
        
    if (x >= -400-15 and x <= -400 + 100 + 15):
        if (y >= 5 and y<= 50):
            lastPlat = 4
            gravity = False
            jumpUp = False
            return x, 50, gravity
        elif (y >= -50 and lastPlat == 3):
            return x, -55, gravity
        
    if (x >= -100-15 and x <= -100 + 500 + 15):
        if (y >= 5 and y<= 50):
            lastPlat = 5
            gravity = False
            jumpUp = False
            return x, 50, gravity
        elif (y >= -50 and lastPlat == 3):
            return x, -55, gravity
        
    if (x >= 140-15 and x <= 140 + 150 + 15):
        if (y >= 90  and y<= 90+45):
            lastPlat = 6
            gravity = False
            jumpUp = False
            return x, 90+45, gravity
        elif (y >= 40 and lastPlat == 5):
            return x, 5+45, gravity
    
    if (x >= -180-25 and x <= -180 + 300 + 15):
        if (y >= 170  and y<= 180):
            lastPlat = 7
            gravity = False
            jumpUp = False
            return x, 130+45, gravity
        elif (y >= 165 and lastPlat == 5):
            return x, 50, gravity 
    #same
    return x, y, gravity

# borderCollide()
# @param: x:int, y:int
# @return: x:int, y:int
def borderCollide(x, y):
    #check x and y coord for going past window borders
    if (x < -360):
        x = -360
    if (x > 350):
        x = 350
    if (y < -270):
        y = -270
    if (y > 270):
        y = 270
    return x, y

# obstacleCollide()
# @param: none
# @return: none
def obstacleCollide():
    global vX, vY, jumpUp
    #final list of obstacle coordinates
    for i in obPositions:
        if (vY >= i[1]-10 and vY <= i[1]+40):
            #on right side of obstacle
            if (isLeft == True and vX <= i[0]+75 and vX >= i[0]+50):
                vX = i[0]+85
            #on left side trying to get through
            elif (isLeft == False and vX >= i[0]-25 and vX <=i[0]-10):
                vX = i[0]-35
        #on top of obstacle
        if (vX < i[0]+50 and vX > i[0]-10 and vY >= i[1]+15 and vY <= i[1]+150):
            vY = i[1]+80
        
# treatCollide()
# @param: treat:turtle, position:int[]
# @return: boolean
def treatCollide(treat, position):
    global vY, vX
    #compare player position to position coordinates (loops through list of positions in main loop)
    if (vX >= position[0]-25 and vX <= position[0]+25 and vY >= position[1]-30 and vY <= position[1]+30):
        return True
    return False

# replayPress()
# @param: none
# @return: none
# replay game
def replayPress():
    global replay, loopStatus
    #big loop
    replay = True
    #smaller loop
    loopStatus = True
    
# quit()
# @param: none
# @return: none
# quit game
def quit():
    global replay, loopstatus
    replay = False
    loopstatus = False
    
    #blank background screen
    bg = turtle.Turtle()
    bg.penup()
    bg.goto(0, 0)
    bg.shape("square")
    bg.shapesize(40, 40, 1)
    bg.color("white")
    bg.stamp()
    bg.hideturtle()
    
    #thanks for playing text
    texty = turtle.Turtle()
    texty.penup()
    texty.speed("fastest")
    texty.goto(0, 0)
    texty.color('cornflowerblue')
    font1 = ('Cocogoose', 60)
    texty.pendown()
    texty.write("Thanks for Playing!", align = "CENTER", font = font1)
    texty.hideturtle()
    
    win.exitonclick()

#global variables accessible in private functions
global vX, vY, jumpUp, isLeft, lastPlat, score, prevScore, dX, dY, enemyIndex, choice, loopStatus, shooting, shots, hits

replay = True
while (replay == True):

    win = turtle.Screen()
    
    win.title("VictOreo Platform game")
    win.setup(800, 600)
    win.bgpic("backgroundSS.gif")
    
    #make another object for drawing platforms
    todd = turtle.Turtle()
    todd.color("moccasin")
    todd.pensize(2)
    todd.speed("fastest")
    todd.hideturtle()
    
    #obstacles
    numObst = 2
    obstacles = []
    obPositions = [[-175, -256], [10, 22]]
    
    #make turtle object obstacles and adding to list
    for i in range(numObst):
        obstacles.append(turtle.Turtle())
        obstacles[i].hideturtle()
        obstacles[i].speed("fastest")
        obstacles[i].penup()
        obstacles[i].goto(obPositions[i][0], obPositions[i][1])
        obstacles[i].color("firebrick")
        obstacles[i].begin_fill()
        for j in range(3):
            obstacles[i].forward(50)
            obstacles[i].left(120)
        obstacles[i].end_fill()
        obstacles[i].hideturtle()
    
    
    #treats
    win.register_shape("treat.gif")
    numTreats = 6
    treats = []
    #all shown at first
    shown = [True]*numTreats
    tPositions = [[0, -220], [-330, -220], [300, -125], [0, -40], [-350, 70], [200, 150]]
    
    #creating turtle object treats and adding to list
    for i in range(numTreats):
        treats.append(turtle.Turtle())
        treats[i].speed("fastest")
        treats[i].penup()
        treats[i].goto(tPositions[i][0], tPositions[i][1])
        treats[i].shape("treat.gif")
    
    
    #dog
    #list of gif files for different stages of the dog emotions
    enemies = ["madEnemy.gif", "madEnemy2.gif", "madEnemy3.gif", "enemy.gif", "neutralEnemy.gif", "neutralEnemy2.gif", "happyEnemy.gif", "happyEnemy2.gif", "happyEnemy3.gif", "happyEnemy3.gif"]
    #register each image
    for i in enemies:
        win.register_shape(i)
    #make enemy turtle object
    dog = turtle.Turtle()
    dog.speed("fastest")
    dog.penup()
    dog.goto(-80, 180)
    dog.shape("madEnemy.gif")
    #dog constant moving speed
    move = 15
    
    #victoreo
    win.register_shape("oreo.gif")
    win.register_shape("oreoleft.gif")
    victoreo = turtle.Turtle()
    victoreo.speed("fastest")
    victoreo.penup()
    victoreo.goto(-250, -220)
    victoreo.shape("oreo.gif")

    #(re)assign values to variables
    score = 0
    prevScore = 0
    lastPlat = 1
    enemyIndex = 0
    isLeft = False
    vX = -250
    vY = -220
    dX = -80
    dY = 180
    shots = 0
    hits = 0
    shooting = False
    
    #keyboard commands
    turtle.listen()
    turtle.onkey(jump, "Up")
    turtle.onkey(moveLeft, "Left")
    turtle.onkey(moveRight, "Right")
    turtle.onkey(shoot, "v")
    
    loopStatus = False
    first = True
    while (True):
        
        #gameplay while enemy not fully happy yet
        while (checkWin() == False):
            #enemy and player positions constantly updating
            victoreo.goto(vX, vY)
            dog.goto(dX, dY)
            
            #dog moving side to side
            dX += move
            if (dX > 70):
                move = -15
            if (dX < -110):
                move = 15
            
            #change victoreo facing direction accordingly
            if (isLeft == True):
                victoreo.shape("oreoleft.gif")
            else:
                victoreo.shape("oreo.gif")
            
            #change vX and vY depending on other factors
            vX, vY, gravity = platformCollide(vX, vY)
            vX, vY = borderCollide(vX, vY)
            obstacleCollide()
            
            #if all treats are collected and none are shown then loop through and show all again
            if (not any(shown)):
                for i in range(len(treats)):
                    treats[i].showturtle()
                    shown[i] = True
            
            #loop through list of treats
            for i in range(len(treats)):
                #treat being collected
                if (shown[i] == True and treatCollide(treats[i], tPositions[i]) == True):
                    treats[i].hideturtle()
                    shown[i] = False
                    score += 1
            
            #score needs updating
            if (score != prevScore):
                #clear previous number
                todd.clear()
                todd.speed("fastest")
                todd.penup()
                todd.goto(325,223)
                todd.color('midnight blue')
                name = "{}".format(score)
                font1 = ('futura', 25)
                todd.write(name, font = font1)
            #update prevscore now
            prevScore = score
            
            #reset position and take all treats away
            if (enemyPlayerCollide()):
                vX = -250
                vY = -220
                score = 0
            #gravity pulling down
            if (gravity):
                vY -= 13
            
            #dog image correlatign to amount of treats recieved
            dog.shape(enemies[enemyIndex])
            
            win.tracer(3)
            
        #prevent repeating text in loop
        if (first == True):
            #background of text
            bg = turtle.Turtle()
            bg.penup()
            bg.goto(0, 0)
            bg.shape("square")
            bg.shapesize(50, 40, 1)
            bg.color("moccasin")
            bg.stamp()
            bg.hideturtle()
            
            #text
            texty = turtle.Turtle()
    
            texty.penup()
            texty.speed("fastest")
            texty.color('cornflowerblue')
            texty.goto(0, 0)
            texty.pendown()
            font1 = ('Cocogoose', 80)
            font2 = ('Futura', 25)
            texty.write("YOU WIN", align = "CENTER", font = font1)
            texty.color("slategray")
            texty.penup()
            texty.goto(0, -70)
            texty.pendown()
            #calculate shooting accuracy percentage
            texty.write(f"Your shooting accuracy score is: {round(100*hits/shots, 2)}%", align = "CENTER", font = font2)
            texty.penup()
            texty.goto(0, -120)
            texty.pendown()
            texty.color("maroon")
            texty.write("Press R to replay | Press Q to quit the game", align = "CENTER", font = font2)
            texty.hideturtle()
            first = False
        
        #press q or r
        win.onkey(replayPress, "r")
        win.onkey(quit, "q")
        
        #waiting for user response
        if (loopStatus == True):
            break
        win.tracer(2)
    
    #break out of loop when q was pressed
    if (replay == False):
        break
    #help reset everything on screen
    win.clearscreen()
        

win.exitonclick()
