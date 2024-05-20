import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torchvision.models import VGG16_Weights
import numpy as np
class PerceptualLoss(nn.Module):
    def __init__(self):
        super(PerceptualLoss, self).__init__()
        vgg = models.vgg16(weights=VGG16_Weights.IMAGENET1K_V1).features
        self.features = nn.Sequential(*list(vgg)[:16]).eval()
        for param in self.features.parameters():
            param.requires_grad = False
        self.criterion = nn.MSELoss()
    
    def forward(self, x, y):
        x_features = self.features(x)
        y_features = self.features(y)
        return self.criterion(x_features, y_features)
    
