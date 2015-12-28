"""Model to predict missing fragments of a password
   from given fragments.
"""
from sklearn import metrics
from collections import defaultdict
from collections import Counter
import operator

# The known fragments of the password
inputcols = [2, 3, 4]
# The position to predict
outputcol = 1


def BuildModel(data, label):
  """For each instance in data, compute the list of most
     popular labels.
  """
  labellist = defaultdict(list)
  for i in range(len(data)):
    labellist[data[i]].append(label[i])
  model = dict()
  for d, l in labellist.items():
    sortedlabels = sorted(Counter(l).items(), key=operator.itemgetter(1), reverse=True)
    model[d] = [x[0] for x in sortedlabels]
  return model


def Predict(data, model, idx):
  """Return the most popular label (idx==0) or
     the second most popular label (idx==1) corresponding to
     each instance of data.
  """
  result = []
  for d in data:
    popularlabels = model.get(d,[])
    if (len(popularlabels) > idx):
      result.append(popularlabels[idx])
    else:
      result.append(-1)
  return result


def LoadData(srcfile):
  """Expects a list of passwords as input.
     Extracts the data based on inputcols and label
     based on outputcol.
  """
  data = []
  label = []
  with open(srcfile) as f:
    for line in f:
          chars = list(line)
      # The last two chars are always '\r' and '\n'
      if outputcol >= len(chars) - 2:
         continue
      row = []
      for i in inputcols:
        if i < len(chars) - 2:
          row.append(chars[i])
      data.append('-'.join(row))
      label.append(ord(chars[outputcol]))
  return data, label

traindata, trainlabel = LoadData('ten-million.txt')
testdata, testlabel = LoadData('Ashley_Madison.txt')

model = BuildModel(traindata, trainlabel)
predict0 = Predict(testdata, model, 0)
predict1 = Predict(testdata, model, 1)
accuracy0 = metrics.accuracy_score(testlabel, predict0)
accuracy1 = metrics.accuracy_score(testlabel, predict1)

print accuracy0, accuracy0 + accuracy1
