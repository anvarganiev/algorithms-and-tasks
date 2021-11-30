'''
z = r exp(j phi)
Where r = sqrt(x^2 + y^2) and phi=atan2(x,y)
'''
import cv2
import numpy as np
import torch
import torchvision.transforms as transforms

loader = transforms.Compose([transforms.ToTensor()])

def process_img(img_path, img_size):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (img_size, img_size))
    img = img.astype(np.float32) / 255.0
    img = loader(img)
    img = img.unsqueeze(0)
    return img

img = process_img("./house.jpg", 128)

# reconstructed image with phase information only by setting the amplitude component to a constant
def fft_amplitude_aug(img):

    img_fft = torch.fft.fft2(img)
    const_amp = 20000  # whatever the constant amplitude you want
    new_fft = const_amp * torch.exp(1j * img_fft.angle())
    # reconstruct the new image from the modulated Fourier:
    img_ifft = torch.fft.ifft2(new_fft, dim=(-2, -1))

    img_ifft = img_ifft.squeeze(0)
    img_ifft = img_ifft.transpose(2, 0)
    img_ifft = np.array(img_ifft)
    img_ifft = img_ifft.real

    return img_ifft

#  reconstructed image with amplitude information only by setting the phase component to a constant
def fft_phase_aug(img):
    img_fft = torch.fft.fft2(img)
    img_abs = torch.abs(img_fft)
    # img_pha = torch.angle(img_fft)
    img_pha = torch.full(img_fft.shape, 0.5)
    print(f"img_phase: {img_pha}")
    print(f"img_abs: {img_abs}")
    new_fft = img_abs * torch.exp(1j * img_pha)
    img_ifft = torch.fft.ifft2(new_fft, dim=(-2, -1))
    img_ifft = img_ifft.squeeze(0)
    img_ifft = img_ifft.transpose(2, 0)
    img_ifft = np.array(img_ifft)
    img_ifft = img_ifft.real

    return img_ifft


img_ifft = fft_phase_aug(img)

cv2.imshow("", img_ifft)
cv2.waitKey()

