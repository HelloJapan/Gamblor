# Import pandas
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from pandas.plotting import table

# Convert decimal odds to implied probability
def probConvert(odds):
    return (1.0/odds)*100 

def makeBoxPlot(data):
    data.boxplot(column="Probability", by="Result")
    plt.show()

def makeScatterPlot(data):
    wbets = data[data['Result'].str.contains("Win")]
    lbets = data[data['Result'].str.contains("Loss")]

    plt.figure()
    #plt.axes()
    #plt.subplot(2,1,1)
    plt.plot(lbets['Odds'], lbets['Sport'], "rx")
    #plt.subplot(2,1,2)
    plt.plot(wbets['Odds'], wbets['Sport'], "g+")
    plt.show()
    
def read_excel(filename):
    # Load the xlsx file
    excel_data = pd.read_excel("betDegenData.xlsx", engine='openpyxl')
    # Read the values of the file in the dataframe
    data = pd.DataFrame(excel_data, columns=['Bookmaker', 'Sport', 'Probability', 'Overvalue', 'Odds', 'Result'])

    # Print the content
    print("The content of the file is:\n", data)

    makeScatterPlot(data)
    makeBoxPlot(data)

    features = data.drop(['Bookmaker','Sport','Result'], axis=1) # Drop specified labels from columns
    targets = data["Result"]

    train_features, test_features, train_targets, test_targets = \
        train_test_split(features, targets, train_size=0.75)
    
    # Train the model
    tree = DecisionTreeClassifier(criterion="gini")
    tree = tree.fit(train_features, train_targets)

    # Predict the classes of new, unseen data
    prediction = tree.predict(test_features)

    # Check the accuracy
    score = tree.score(test_features, test_targets)
    print("The prediction accuracy is: {:0.2f}%".format(score * 100))

if __name__ == '__main__':
    read_excel('betDegenData.xlsx')