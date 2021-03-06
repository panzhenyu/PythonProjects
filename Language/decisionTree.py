from sklearn.feature_extraction import DictVectorizer
import csv
from sklearn import tree
from sklearn import preprocessing

allElectornicsData = open(r'C:\Users\78467\Desktop\AllElectronics.csv', 'r')
reader = csv.reader(allElectornicsData)
headers = next(reader)
print(headers)
featureList = []
labelList = []
for row in reader:
    labelList.append(row[len(row) - 1])
    rowDict = {}
    for i in range(1, len(row) - 1):
        rowDict[headers[i]] = row[i]
    featureList.append(rowDict)

print(featureList)
print(labelList)

vec = DictVectorizer()
dummyX = vec.fit_transform(featureList).toarray()

print("dummyX: " + str(dummyX))
print(vec.get_feature_names())
print("labelList: " + str(labelList))

# vectorize class labels
lb = preprocessing.LabelBinarizer()
dummyY = lb.fit_transform(labelList)
print("dummyY: ", str(dummyY))

# Using decision tree for classification
clf = tree.DecisionTreeClassifier(criterion='gini')
clf = clf.fit(dummyX, dummyY)
print("clf: ", str(clf))

# Visualize model
# dot -Tpdf iris.dot -o ouput.pdf
with open(r"C:\Users\78467\Desktop\allElectronicInformationGainOri.dot", 'w') as f:
    f = tree.export_graphviz(clf, feature_names=vec.get_feature_names(), out_file=f)
