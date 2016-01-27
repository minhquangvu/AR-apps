from ctypes import *
ar = cdll.LoadLibrary("ARPyInt.dll")

import time

currentStep = 0
timerActive = False
start = time.time()

currentSize = .001 #equivalent to 6.5cm true height

i_x = c_float(0.0)
i_y = c_float(0.0)
i_z = c_float(0.0)
imageLocation = [i_x, i_y, i_z]
imageLocationStored = 0

submenus = ["menu01","menu01","menu02","menu02","menu02","menu02","menu03","menu03","menu03","menu04","menu01","menu01","menu01","menu00"]
#start with menu 01 for now to advance to next step. will start with menu00 once I made a new convex marker
steps = ["step01","step02","step03","step04","step05","step06","step07","step08","step09","step10","step11a","step11b","step11c","step12"]
pred = [None, None, None, None, None, None,"pred01", "pred02", "pred03", None, None, None, None, None, None]


pred_names = ["pred01", "pred02", "pred03"]

# These are the stored predictions
stored_location = [[0.0,0.0,0.0], [0.0,0.0,0.0], [0.0,0.0,0.0] ] 
stored_rotation = [0, 0, 0] 
num_pred = 0 #number of predictions

stored_scale = [0, 0, 0]

# True position
true_position = list()
true_position_stored = False

# True scale
true_scale = 0
true_scale_stored = False

#True rotation
true_rotation = 0

# Conditions:
# 1. convex marker enters, wait 2 seconds, check if still there, advance to "step2"
# 2. play animation for 10 seconds, show "Readybutton".
# 3. press next
# 4. wait N seconds
# 5. 3 markers present, wait 2 seconds, check if still there, storePrediction, advance to 9
# 6. storePrediction, advance to nextStep()
# 7. advance to evalPred()
# 8. 4 markers present (table, teapot, mirror, eye)
# 9. press show rays, advance to 26
# 10. press hide rays, advance to 25
conditions = [1, 2, 3, 4, 4, 4, 4, 5, 6, 6, 7, 3, 3, 3, 5, 7]

def onPatternIn(pattern_id):	#fires when identify a pattern placed in background
	print "Pattern in event", pattern_id
		
def onPatternOut(pattern_id):	#fires when identify a pattern removed from the background
	print "Pattern out event", pattern_id
	#markerPresent[pattern_id] = False
	
def onInit(frameid):	#fires when start the application
	global currentStep
	
	print "INIT Application."
	ar.setWorldReferenceMarker(0)
	
	# TEXT - M. Jan. 21, 2016
	ar.addTextObject(0)
	ar.setText(0," ")
	ar.setTextPos(0,200,900)
	ar.setTextColor(0,200,255,0)
	ar.setTextSize(0,30)
	
	ar.addTextObject(1)
	ar.setText(1," ")
	ar.setTextPos(1,200,830)
	ar.setTextColor(1,200,255,0)
	ar.setTextSize(1,30)
	
	ar.addTextObject(2)
	ar.setText(2," ")
	ar.setTextPos(2,200,760)
	ar.setTextColor(2,200,255,0)
	ar.setTextSize(2,30)
	
	
	ar.addLine(0, c_float(0.0), c_float(0.001), c_float(0.0), c_float(0.05), c_float(0.00202),
               c_float(0.323))  # line teapot - mirror
	ar.addLine(1, c_float(0.0), c_float(0.0), c_float(0.0), c_float(0.001), c_float(0.0005),
               c_float(0.01))  # line teapot - mirror
	ar.addLine(2, c_float(0.0), c_float(0.0), c_float(0.0), c_float(0.015), c_float(0.0015),
               c_float(0.01))  # line teapot - mirror 
	ar.addLine(3, c_float(0.0), c_float(0.0), c_float(0.0), c_float(0.017), c_float(0.017),
               c_float(0.01))  # line teapot - mirror reflection of line 0
	ar.addLine(4, c_float(0.0), c_float(0.0), c_float(0.0), c_float(0.018), c_float(0.017),
               c_float(0.01))  # line teapot - mirror reflection of line 1
	ar.addLine(5, c_float(0.0), c_float(0.0), c_float(0.0), c_float(0.017), c_float(0.018),
               c_float(0.01))  # line teapot - mirror reflection of line 2
			   
			   
	ar.setLineSpeed(0,c_float(30.00)) #set line speed of incoming rate
	ar.setLineSpeed(1,c_float(30.00))
	ar.setLineSpeed(2,c_float(30.00))
	ar.setLineSpeed(3,c_float(30.00)) #set line speed of reflecting rate
	ar.setLineSpeed(4,c_float(30.00))
	ar.setLineSpeed(5,c_float(30.00))
	ar.setLineColor(0, 150, 0 , 150, 100)
	ar.setLineColor(1, 150, 0 , 150, 100)
	ar.setLineColor(2, 150, 0, 150, 100)
	ar.setLineColor(3, 0, 255, 0, 100)
	ar.setLineColor(4, 0, 255, 0, 100)
	ar.setLineColor(5, 0, 255, 0, 100)
	ar.disableLine(0)
	ar.disableLine(1)
	ar.disableLine(2)
	ar.disableLine(3)
	ar.disableLine(4)
	ar.disableLine(5)
	
	
def switchTo(step):
	global currentStep
	global steps
	#print "switchTo is successfully called. step received:", step
	

	currentStep = step
	ar.setScene(steps[currentStep])
	ar.switchToSubMenu(submenus[currentStep])
	print "Switched to step: ", steps[currentStep]
	
def onFrame(frameid):
	global currentStep
	global timerActive
	global start
	
	global true_position
	global true_position_stored
	
	global true_scale
	global true_scale_stored
	
	global true_rotation
	
	ar.setWorldReferenceMarker(0)
	
	if currentStep == 0:
		print "currentStep is: ", currentStep
		switchTo(currentStep)
		
		
	if currentStep == 1:
		#print "light animation"
		
		# Mirror
		p0_x = c_float()
		p0_y = c_float()
		p0_z = c_float()
		r0_x = c_float()
		r0_y = c_float()
		r0_z = c_float()
		ar.modelGetTranslationWorldCoord("mirror", byref(p0_x), byref(p0_y), byref(p0_z))
		ar.modelGetRotationWorldCoord("mirror", byref(r0_x), byref(r0_y), byref(r0_z))
		
		
		#Teapot
		p1_x = c_float()
		p1_y = c_float()
		p1_z = c_float()
		r1_x = c_float()
		r1_y = c_float()
		r1_z = c_float()
		ar.modelGetTranslationWorldCoord("teapot", byref(p1_x), byref(p1_y), byref(p1_z))
		ar.modelGetRotationWorldCoord("teapot", byref(r1_x), byref(r1_y), byref(r1_z))
		#print "mirror", p0_x.value, p0_y.value, p0_z.value
		#print "teapot", r1_x.value, r1_y.value, r1_z.value
	
	
		# line 0,1,2 - teapot to mirror 
		ar.setLinePosition(0, p1_x, p1_y, p1_z, p0_x, p0_y, p0_z)
		ar.setLinePosition(1, c_float(p1_x.value), c_float(p1_y.value), p1_z, c_float(p0_x.value+.05), c_float(p0_y.value), p0_z)
		ar.setLinePosition(2, c_float(p1_x.value), c_float(p1_y.value), p1_z, c_float(p0_x.value-.05), c_float(p0_y.value), p0_z)
		
	
		# Reflection calculation
		distance_obj = pow( pow(p0_x.value - p1_x.value,2) + pow(p0_y.value - p1_y.value,2) + pow(p0_z.value - p1_z.value,2),0.5)
		
		vector_i = [(p1_x.value - p0_x.value) , (p1_y.value - p0_y.value), (p1_z.value - p0_z.value)]
	
		
		normal_mirror = [0.0,-1.0,0.0]
		dot_product = ( vector_i[1] * normal_mirror[1])
		dot_product = dot_product
		vector_p = [0.0,0.0,0.0]
		vector_reflect = [0.0,0.0,0.0]
		
		
		vector_p[0] = 2.0*(normal_mirror[0] * dot_product) 
		vector_p[1] = 2.0*(normal_mirror[1] * dot_product) 
		vector_p[2] = 2.0*(normal_mirror[2] * dot_product) 
		
		vector_reflect[0] = vector_p[0] - p1_x.value
		vector_reflect[1] = vector_p[1] - p1_y.value
		vector_reflect[2] = vector_p[2] - p1_z.value
		
		#print   p1_x, p1_y, p1_z
		
		# line 3,4,5 - reflection of line 0, 1, 2 from the mirror
		ar.setLinePosition(3, p0_x, p0_y, p0_z, p1_x, p1_y, p1_z)
		ar.setLinePosition(4, c_float(p0_x.value+.05), c_float(p0_y.value), p0_z, c_float(vector_reflect[0]), c_float(vector_reflect[1]), c_float(p1_z.value))
		ar.setLinePosition(5, c_float(p0_x.value-.05), c_float(p0_y.value), p0_z, c_float(vector_reflect[0]), c_float(vector_reflect[1]), c_float(p1_z.value))
		
		ar.enableLine(0)
		ar.enableLine(1)
		ar.enableLine(2)
		ar.enableLine(3)
		ar.enableLine(4)
		ar.enableLine(5)
		ar.startLineAnimation(0)
		ar.startLineAnimation(1)
		ar.startLineAnimation(2)
		ar.startLineAnimation(3)
		ar.startLineAnimation(4)
		ar.startLineAnimation(5)
		
	else:
		ar.disableLine(0)
		ar.disableLine(1)
		ar.disableLine(2)
		ar.disableLine(3)
		ar.disableLine(4)
		ar.disableLine(5)
		
		
	if (currentStep == 2) or (currentStep == 3) or (currentStep == 4) or (currentStep == 5):  
		ar.disableVideoBackground() #turn off back ground to show narrative
		#if not timerActive :
			#start = time.time()
			#print "Start Timer for 3 seconds"
			#timerActive = True
        #if timerActive:
            #end = time.time()
            #if end - start >= 3:
               # print "End timer", end-start
                #timerActive = False
                #switchTo(currentStep + 1)
	else:
		ar.enableVideoBackground()
	#elif currentStep == 6:
		#turn on background, marker Predict, Pred image, slidebar to adjust. 
		
	if (currentStep == 3):
		if (true_position_stored == False):
			if (true_scale_stored == False):
				calcReflectedImage()
				ar.disableModel("answer")
				true_position_stored = True
				true_scale_stored = True
			
		
	if (currentStep == 10) or (currentStep == 11) or (currentStep == 12):
		ar.enableModel("answer")
		#ar.highlightModelOn("answer")
		
	if currentStep == 13:
		ar.disableModel("answer")
		ar.setText(0," ")
		ar.setText(1," ")
		ar.setText(2," ")
		
		
def onMenuButton(button):
	print "[Py] Button pressed :", button
	global currentSize
	global currentStep
	global newSize
	global num_pred
	#global timerActive
	#global start

	if button == "ReadyNext":
		if (currentStep == 10) or (currentStep == 11) or (currentStep == 12):
			print "Currentstep is ", currentStep, "proceed to next step"
			currentStep = 12
			switchTo(currentStep+1)
		else:
			switchTo(currentStep+1)
			#return currentStep
	if button == "ReadyBack":
		#print "currentStep is ", currentStep
		if (currentStep == 7) or (currentStep == 8) or (currentStep == 9):
			print "call to restore origin"
			switchTo(currentStep-1)
			newSize = .001
			ar.modelSetScale(pred[(currentStep)], c_float(newSize), c_float(newSize), c_float(newSize))
			ar.set3DModelToMarker(pred[currentStep], 2)
			
			if num_pred > 0:
				num_pred = num_pred - 1
			
			#saveLocation(pred[currentStep])
		elif (currentStep == 2):
			ar.enableVideoBackground()
			switchTo(currentStep-1)
			#currentStep = currentStep -1
			#return currentStep
		else:
			switchTo(currentStep-1)
			#currentStep = currentStep -1
		#return currentStep
	if button =="savePredButton":
		print "savePredButton clicked"
		saveLocation(pred[currentStep])
		currentSize=.001
		switchTo(currentStep+1)
		#print "save PredButton is called. go to next predict "
	if button =="Increase": #five times to maximum
		newSize=currentSize + .0003
		if newSize>=.0026:	#set limit so image wont get too big.
			newSize=currentSize
		else:
			newSize=currentSize+.0003
		ar.modelSetScale(pred[currentStep], c_float(newSize), c_float(newSize), c_float(newSize))
		currentSize = newSize
		print "increase size of image", currentSize
	if button =="Decrease": #8 times to minimum, correct ans is around 7
		newSize=currentSize-.00009
		if newSize<=0.00026:		#set limit so image wont get too small.
			newSize=currentSize+.00009
		else:
			newSize=currentSize-.00009
			ar.modelSetScale(pred[currentStep], c_float(newSize), c_float(newSize), c_float(newSize))
			currentSize = newSize
		print "increase size of image", currentSize
	if button == "testPredsButton":
		print "test button pressed"
		evalPred()
	if button =="Exit":
		print "end button pressed"
		ar.exit_ar()
			
def saveLocation(pred): 
	global num_pred
	global stored_location
	global stored_rotation
	
	global currentSize
	
	ar.setWorldReferenceMarker(0)

    # associate the model to the new marker
	ar.set3DModelToMarker(pred, 0)

    # but keep the old position by calculating the relation between marker 2 and 0
	ar.setModelToMarkerRel(pred, 2, 0)
	print "set relative position"
	
	# Get Position Of Predict Model
	x1 = c_float()
	y1 = c_float()
	z1 = c_float()
	ar.modelGetTranslationWorldCoord(pred, byref(x1), byref(y1), byref(z1))  
	
	print "X: ", x1.value
	print "Y: ", y1.value
	print "Z: ", z1.value
	predictLocation = [x1.value, y1.value, z1.value]
	#print predictLocation[0], predictLocation[1], predictLocation[2]

	stored_location[num_pred] = predictLocation
	print "prediction ", num_pred , " location ", stored_location[num_pred]
	
	
	
	# Get Rotation Of Predict Model
	r1_x = c_float()
	r1_y = c_float()
	r1_z= c_float()
	ar.markerGetRotation(2, byref(r1_x), byref(r1_y), byref(r1_z))  
	
	print "RX: ", r1_x.value
	print "RY: ", r1_y.value
	print "RZ: ", r1_z.value
	#predictRotation = r1_z.value
	#print predictRotation[0], predictRotation[1], predictRotation[2]
	stored_rotation[num_pred] = r1_z.value
	print "prediction ", num_pred , " rotation ", stored_rotation[num_pred]
	
	
	
	
	# Get size of Predict Model
	stored_scale[num_pred] = currentSize
	print "prediction", num_pred, "currentSize", currentSize
	
	num_pred = num_pred + 1;
	
def calcReflectedImage():  # calculate the true image location & scale. 
	
	global true_position
	global true_rotation
	global true_scale
	
	
	ar.setWorldReferenceMarker(0)
	ar.set3DModelToMarker("answer", 0)
	
	# Mirror
	p0_x = c_float()
	p0_y = c_float()
	p0_z = c_float()
	r0_x = c_float()
	r0_y = c_float()
	r0_z = c_float()
	ar.modelGetTranslationWorldCoord("mirror", byref(p0_x), byref(p0_y), byref(p0_z))
	ar.modelGetRotationWorldCoord("mirror", byref(r0_x), byref(r0_y), byref(r0_z))
		
	
	#teapot
	p1_x = c_float()
	p1_y = c_float()
	p1_z = c_float()
	r1_x = c_float()
	r1_y = c_float()
	r1_z = c_float()
	ar.modelGetTranslationWorldCoord("teapot", byref(p1_x), byref(p1_y), byref(p1_z))
	ar.modelGetRotationWorldCoord("teapot", byref(r1_x), byref(r1_y), byref(r1_z))
		
	
		# line 0 - teapot to mirror 
		# ar.setLinePosition(0, p0_x, p0_y, p0_z, p1_x, p1_y, p1_z)
		
		# line 1 - mirror normal vector
		# ar.setLinePosition(1, p0_x, p0_y, p0_z, c_float(0.0), c_float(-0.1), c_float(0.0))
		
	
		# Reflection calculation
	x = (p0_x.value - p1_x.value)/10
	y = (p0_y.value - p1_y.value)/10
	z = (p0_z.value - p1_z.value)/10
	distance_obj = pow( pow(x,2) + pow(y,2) + pow(z,2),0.5)
		
	vector_i = [(p1_x.value - p0_x.value) , (p1_y.value - p0_y.value), (p1_z.value - p0_z.value)]
	
		
	normal_mirror = [0.0,-1.0,0.0]
	dot_product = (.1*(vector_i[1])* normal_mirror[1])
	dot_product = dot_product
	vector_p = [0.0,0.0,0.0]
	vector_reflect = [0.0,0.0,0.0]
		
		
		
	vector_p[0] = 2.0*(normal_mirror[0] * dot_product)
	vector_p[1] = 2.0*(normal_mirror[1] * dot_product) 
	vector_p[2] = 2.0*(normal_mirror[2] * dot_product) 
		
	vector_reflect[0] = vector_p[0] - (p1_x.value)/10
	vector_reflect[1] = vector_p[1] - (p1_y.value)/10
	vector_reflect[2] = vector_p[2] - (p1_z.value)/10
	
	
	ar.modelSetTranslation("answer",c_float(-vector_reflect[0]), c_float(-vector_reflect[1]), c_float(p1_z.value))
	ar.modelSetRotation("answer", c_float(0.0), c_float(0.0),c_float(-r1_z.value-3.141592))
		

	focalLength = .01053	#focallength is 10cm	
	distance_img = ((focalLength*distance_obj)/(distance_obj - focalLength))/1
	print "distance_img", distance_img
	print "distance_obj", distance_obj
		
	newSize = .001*(distance_img/distance_obj)
	
	# store the true scale 
	true_scale = newSize
	print "true_scale is ", true_scale
	
	ar.modelSetScale("answer", c_float(true_scale), c_float(true_scale), c_float(true_scale))
	
	# store the true position of the reflected image	
	true_position.append([-vector_reflect[0]+.06, -vector_reflect[1], p1_z.value ] )
	
	# store the true rotation
	true_rotation = -r1_z.value-3.141592
	print "true_rotation is", true_rotation
	
	

	
def evalPred(): #Minh add 01/21. 
	
		
	global pred_names
	
	global true_position
	global true_position_stored	
	global stored_location
	
	
	global true_rotation
	global stored_rotation

	global true_scale
	global stored_scale
	
	global currentStep
	
	stored_scoreLocation = [0, 0, 0]
	stored_scoreRotation= [0, 0, 0]
	stored_scoreSize = [0,0,0]
	score_total = [0, 0, 0]
	distance_stored = [0,0,0]
	
	
	distance_list=[0,0,0] #distance_between of each prediction in distance evaluation stored here
	rotation_list=[0,0,0] #rotation_difference of each prediction in rotation evaluation stored here
	scale_list=[0,0,0]    #scale difference of each prediction in scale evaluation stored here
	evaluation_list = [0,0,0] # [distance difference, rotation #]
	
	
	
	
	#distance evaluation
	minimum_distance = 100000.000
	minimum_distance_idx = -1
	idx_a = 0
	correctness = []
	true_position_vec = true_position[0]
	
	#print "True position: ", true_position_vec
	#print "Length:", len(stored_location)
	#print "Length:", len(stored_scoreLocation)
	#print "Length:", len(stored_scoreSize)
	
	for predict_position in stored_location:

		#print "\n\nEVAL: ", predict
		#print pow(predict[0] - true_position_vec[0],2) + pow(predict[1] - true_position_vec[1],2) + pow(predict[2] - true_position_vec[2],2)
		
		distance_between = pow( pow(predict_position[0] - true_position_vec[0],2) + pow(predict_position[1] - true_position_vec[1],2) + pow(predict_position[2] - true_position_vec[2],2),0.5)
		distance_list[idx_a] = distance_between
		print "distance: ", distance_between
		
		#if distance_between < minimum_distance:
			#minimum_distance = distance_between
			#minimum_distance_idx = idx_a;
		#idx_a = idx_a + 1
		
		if (distance_between > 0.05): #distance over 50cm
			score_location = 0
		elif (distance_between <=0.05) and (distance_between >0.02): #between 50cm and 19cm
			score_location = 2
		else:
			score_location = 3
		
		stored_scoreLocation[idx_a] = score_location
		
		idx_a = idx_a + 1
		
		print "score_location", score_location
	#print "\n\nClosest prediction is object: ", minimum_distance_idx, " at a distance of " , minimum_distance
	
	

	
	
	
	
	#rotation evaluation
	idx_c = 0
	
	for predict_rotation in stored_rotation:
		rotation_difference = abs(true_rotation - predict_rotation)
		rotation_list[idx_c] = rotation_difference
		print "rotation_difference", rotation_difference
		
		if rotation_difference > 3.14:
			score_rotation = 0.15
		elif (rotation_difference <= 3.14) and (rotation_difference > 1.047):
			score_rotation = .1
		else:
			score_rotation = 0
		
		stored_scoreRotation[idx_c] = score_rotation
		idx_c = idx_c +1
		
		print "score_rotation", score_rotation
		
		
		
		
		
	#scale evaluation
	minimum_difference = 1000
	minimum_difference_idx = -1
	idx_b = 0
	
	for predict_size in stored_scale:
		#print "predict size: ", predict_size
		difference_scale = predict_size - true_scale
		scale_list[idx_b]=difference_scale
		print "scale_difference: ", difference_scale
		
		#if (difference < minimum_difference) and (predict_size < .01): #choose the predict closer to the true image and smaller than original object.
			#minimum_difference = difference
			#minimum_difference_idx = idx_b
			
		#idx_b = idx_b + 1
		
		if difference_scale > .0002: #two increments difference
			score_size = 0
		elif (difference_scale <= .0002) and (difference_scale >.0005): #between 2 and 5 increment difference
			score_size =.5
		else:
			score_size =.75
		
		stored_scoreSize[idx_b] = score_size
		
		idx_b = idx_b +1
		print "score_size", score_size
	
	
	
	
	
	
	#total evaluation
	
	highscore = -1
	highscore_predictNumber = -1
	
	for predict_number in [0, 1, 2]:
		#print "predict_number is ", predict_number
		score_total[predict_number] = (stored_scoreLocation[predict_number] + stored_scoreRotation[predict_number])/2.0
		print "total score of prediction ", predict_number + 1, " is ", score_total[predict_number]
	
		if score_total[predict_number] > highscore:
			if (score_total[predict_number] == score_total[predict_number-1]) or (score_total[predict_number] == score_total[predict_number-2]):
				if (distance_list[predict_number-1] < distance_list[predict_number]):
					highscore = score_total[predict_number-1]
					highscore_predictNumber = predict_number-1
				elif (distance_list[predict_number-2] < distance_list[predict_number]):
					highscore = score_total[predict_number-2]
					highscore_predictNumber = predict_number-2
			else:
				highscore = score_total[predict_number]
				highscore_predictNumber = predict_number
				
	evaluation_list[0] = round((distance_list[highscore_predictNumber]*9.5)/.01,3)
	evaluation_list[1] = round((rotation_list[highscore_predictNumber]*180)/3.14,3)
	evaluation_list[2] = round((scale_list[highscore_predictNumber]/true_scale)*100,0)
					
	print  " Highscore: ", highscore, " Prediction", highscore_predictNumber+1
	
	if highscore_predictNumber == 0:
		currentStep = 10
	elif highscore_predictNumber == 1:
		currentStep = 11
	else:
		currentStep = 12
	
	ar.setScene(steps[currentStep])
	ar.switchToSubMenu(submenus[currentStep])
	print "Switched to step: ", steps[currentStep]
	
	
	#Evaluation script on screen
	ar.setText(0,str(evaluation_list[0]).strip('[]'))
	
	ar.setText(1,str(evaluation_list[1]).strip('[]'))
	
	ar.setText(2,str(evaluation_list[2]).strip('[]'))
	
	
	
	#print "\n\nClosest size is object: ", minimum_difference_idx, " with accuracy of ", (1-(minimum_difference/stored_scale[minimum_difference_idx]))*100, " %"
	
	
	#rubrik for location
	#0: distance_between > 0.30
	#1: distance_between (0.30, 0.20)
	#2: distance_between < 0.20
	
	#rubrik for size
	#0: difference > 0.015
	#1: difference (0.015, 0.005)
	#2: difference < 0.005
	
	
	#ar.enableModel(pred_names[minimum_distance_idx])
	#ar.modelSetTranslation(pred_names[minimum_distance_idx], stored_location[minimum_distance_idx[0]], stored_location[minimum_distance_idx[1]], stored_location[minimum_distance_idx[2]])
	#ar.modelSetScale(pred_names[minimum_distance_idx], c_float(stored_scale[minimum_difference_idx]), c_float(stored_scale[minimum_difference_idx]), c_float(stored_scale[minimum_difference_idx]))
	
	
	
	
	
	
		#comparison between real image and predict image. Show %correct if placed within .15
		#distance_between = pow( pow(-vector_reflect[0] - p2_x.value,2) + pow(-vector_reflect[1] - p2_y.value,2) + pow(p1_z.value - p2_z.value,2),0.5)
		
		#distance_true = pow( pow(-vector_reflect[0] - p0_x.value,2) + pow(-vector_reflect[1] - p0_y.value,2) + pow(p1_z.value - p0_z.value,2),0.5)
		
		#distance_predict = pow( pow(p2_x.value - p0_x.value,2) + pow(-p2_y.value - p0_y.value,2) + pow(p2_z.value - p0_z.value,2),0.5)
		
		#correctness[i] = distance_predict/distance_true
		#print" correct % ", correctness[i]
		
		#if(distance_between <= .15) and (correctness[i+1] > correctness[i]):
	#		most_correctness = correctness[i+1]
	#		ar.disableModel(predicts[i])
	#	elif (correctnes[i+1] <= correctness[i]) and (predict is not predicts[0]):
	#		most_correctness = correctness[i]
	#		ar.disableModel(predict)
	#	elif (distance_between > .15):
	#		print "none in range"
			
	#	i = i+1
	
	
		
