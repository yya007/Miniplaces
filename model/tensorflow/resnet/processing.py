from torch.utils.data import Dataset
from scipy.misc import imread

class MiniPlaces(Dataset):
  def __init__(self, data_path, category, transform=None):
    self.imgs = []
    self.labels = []
    with open(data_path + category + '.txt','r') as f:
      for line in f:
        path, label = line.split()
        self.imgs.append(data_path + 'images/' + path)
        self.labels.append(int(label))
    self.transform = transform

  def __getitem__(self, i):
    img = imread(self.imgs[i], mode='RGB').astype(float)
    label = self.labels[i]
    if self.transform != None:
      img = self.transform(img)
    return img, label

  def __len__(self):
    return len(self.imgs)