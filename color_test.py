import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

img = np.random.randint(-10, 10, (5, 5))
test = [[0, 1], [1, 2]]
maskArr = np.ma.masked_array(test, mask=[[0, 0], [1, 1]])
maskArr2 = np.ma.masked_array(test, mask=[[1, 1], [0, 0]])
data1 = np.ma.masked_array(test, test == [-5])
data2 = np.ma.masked_array(test, any(2 in test for x in test))
#data2 = np.ma.masked_array(img, img < 0)

fig, ax = plt.subplots()

img1 = ax.imshow(maskArr, cmap="Blues")
img2 = ax.imshow(maskArr2, cmap="Reds")

bar1 = plt.colorbar(img1)
bar2 = plt.colorbar(img2)

bar1.set_label('ColorBar 1')
bar2.set_label('ColorBar 2')

plt.show()