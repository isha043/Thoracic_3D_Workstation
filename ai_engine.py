import torch
import torch.nn as nn

class DoubleConvolution(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )
    def forward(self, x): return self.conv(x)

class UNetDiagnosticAI(nn.Module):
    def __init__(self, in_channels=1, out_channels=1):
        super().__init__()
        self.encoder1 = DoubleConvolution(in_channels, 64)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.encoder2 = DoubleConvolution(64, 128)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.bottleneck = DoubleConvolution(128, 256)
        self.upconv2 = nn.ConvTranspose2d(256, 128, 2, 2)
        self.decoder2 = DoubleConvolution(256, 128)
        self.upconv1 = nn.ConvTranspose2d(128, 64, 2, 2)
        self.decoder1 = DoubleConvolution(128, 64)
        self.final_classifier = nn.Conv2d(64, out_channels, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        enc1 = self.encoder1(x)
        enc2 = self.encoder2(self.pool1(enc1))
        bottle = self.bottleneck(self.pool2(enc2))
        up2 = self.upconv2(bottle)
        dec2 = self.decoder2(torch.cat((up2, enc2), dim=1))
        up1 = self.upconv1(dec2)
        dec1 = self.decoder1(torch.cat((up1, enc1), dim=1))
        return self.sigmoid(self.final_classifier(dec1))
