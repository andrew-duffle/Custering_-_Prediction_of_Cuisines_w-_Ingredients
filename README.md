# Custering_-_Prediction_of_Cuisines_w-_Ingredients
A prediciton model of cuisines based on teh yummly data set
Andrew Duffle
Project 2V2:
I have selected to use the yummly data for project 2.2. The yummly.json data file is included in the project 2v2 folder for convince.   

Getting the data in:
The code will read the data in and parsed to get  list of ID’s, a list for cuisines, and a list of ingredients. I noticed that Italian food dominated the dataset almost 2:1 any other cuisine. To help keep the data set a little less lop sided I selected to limit the instance of any one cuisine to 1000 (some have 1000 some don’t).   

Creating the feature vector:
I decided to use a binary feature vector for the modeling and classification. First we get a list of unique ingredient by using a vectorizer. To limit the number of features I decided to have a feature only qualify  if it was in between  .1% and 20% of the cuisines. If it is more than this then if should have little weight in the prediction and if it is less than this it is so rare that the chances of it being an ingredient is rare.  Doing this we end up with ~190 features for the entire data set. After the features are acquired each cuisine/ID has a binary feature vector created used for modeling. 

Modeling:
There are two prongs to the modeling. First we train a SVM classification model. WARNING: This takes a long time 3-5min in most cases. This model is used for classification when we feed in ingredient lists from the user inputs that are converted to the feature vectors. The other model is the kmeans clustering model used to find close neighbors. The first 5 from the shared cluster are returned and all the cuisines in the cluster are plotted and out put to a frequency bar chart. 

Running the code:
Running the code is pretty basic. Same as most scripts run from the command line you will navigate to the folder initiate the environment and call the main.py file.  The main.py file will run the user_program function and the modeling script. The user program will ask for input of Exit or List. Exit will exit the program, List will ask for a list of ingredients. You will get an example list of ingredients. After you enter the ingredients you will receive a result and some ID’s of closely related cuisines. The prediction is hit and miss on accuracy it tends to guess the general region but the specific it is not great at. You will also get a bar plot of the frequency of cuisines in the cluster. This loop can be repeated as many times as you would like until you select Exit with
