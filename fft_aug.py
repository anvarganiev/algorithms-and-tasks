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

def fft_amplitude_aug(img):

    img_fft = torch.fft.fft2(img)
    const_amp = 20000  # whatever the constant amplitude you want
    new_fft = const_amp * torch.exp(1j * img_fft.angle())
    # reconstruct the new image from the modulated Fourier:
    img_ifft = torch.fft.ifft2(new_fft, dim=(-2, -1))

    img_ifft = img_ifft.squeeze(0)
    img_ifft = img_ifft.transpose(2, 0)
    img_ifft = np.array(img_ifft)

    return img_ifft

img_ifft = fft_amplitude_aug(img)

cv2.imshow("", img_ifft.real/255)
cv2.waitKey()

