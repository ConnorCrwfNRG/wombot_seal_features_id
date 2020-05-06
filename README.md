## Getting Started

### Prerequisite Packages
```
cv2 (OpenCV)
numpy
imutils
os
```

### Running and Installation
In order to run our code follow the steps below:

1. Clone or download into your personal repository.
 
2. Open System_combo.py in your favorite python editor.

3. Ensure the correct paths to both the "haarcascade_bolt_last.xml" and "haarcascade_holes.xml" are correct.

4. Ensure the corrct path to the "Test_Video_WHoles.mov" is correct.

5. Run the code :)


### Using the classifier to train models

The Classifier GUI is derived from OpenCV, and it is courtesy of developer Amin Ahmadi

The download link and original instructions can be found here:
<https://amin-ahmadi.com/cascade-trainer-gui/>

In our repository, it can be found in the following directory:
```
wombot_seal_features_id/Cascade Trainer GUI/Cascade-Trainer-GUI
```

#### Training Known Models (holes or bolts)

Bolts will be used to provide an example on how to improve the classifier


1. Go to the directory wombot_seal_features_id/images/bolts

2. Add any non-bolt (negative) pictures to: 
```
wombot_seal_features_id/images/bolts/n
```
- It is best if these negative pictures are in the same frame as the bolt
- It is ***very important*** that these negative pictures do not contain any part of a bolt as this can improperly train the classifier

3. Add any bolt picture (positive) pictures to:
```
wombot_seal_features_id/images/bolts/p
```
- It is best to include only the bolt within the picture or snip
- If possible, obtain pictures with similar lighting settings as the test video

4. Open the Classifier GUI in the following directory:
```
wombot_seal_features_id/Cascade Trainer GUI/Cascade-Trainer-GUI
```

5. Once the Classifier GUI is up, provide the absolute directory to:
```
wombot_seal_features_id/images/bolts
```

This will usually be something like:
```
C:/Users/..../wombot_seal_features_id/images/bolts
```

6. Change the *Negative Image Count* values to accurately reflect the number of images in: 
```
wombot_seal_features_id/images/bolts/n
```

	This can be done Windows by highlighting all pictures in File Explorer and looking at the bottom left corner of the File Explorer window

7. In the *Cascade* tab, change *Feature Type* to *HAAR*, as we are training a *HAAR* Classifier

8. Click *Start* to begin the classifying process.  This may take 2 to 100 minutes depending on sample size, RAM allocation, and processing core allocation

9. Once the Classifier is finished, go to the folder:
```
/wombot_seal_features_id/images/bolts/classifier
```
Where you will find a *cascade.xml* file.  This is the classifier file and is the file to reference in scripts.  

 
#### Training New Models

1. Create a new folder in the following directory and name it *your item*
```
/wombot_seal_features_id/images/
```

2. Within the directory:
```
/wombot_seal_features_id/images/your item
```
Create two folders: *p* and *n*


3. Place positive images into the *p* folder and negative images into the *n* folder

4. Follow steps 2-9 found in *Training Known Models* but using pictures of *your item*

