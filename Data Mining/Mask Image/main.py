class Graphic():
    def __init__(self, path):
        from PIL import Image
        self.src = Image.open(path)
        self.pixels = self.src.load()
        self.width = self.src.size[0]
        self.height = self.src.size[1]
        self.mask = [[1, 2, 1],
                     [2, 4, 2],
                     [1, 2, 1]]
    
    def _change_pixel_on_mask(self, mask_image, x, y):
        sigma = [0, 0, 0]
        mask_size = (len(self.mask[0]), len(self.mask))
        mask_center = (mask_size[0]//2, mask_size[1]//2)
        for channel in range(3):
            for i in range(mask_size[0]):
                for j in range(mask_size[1]):
                    xi = x + i - mask_center[0]
                    yj = y + j - mask_center[0]
                    if xi < 0 or xi >= self.width or yj < 0 or yj >= self.height:
                        continue
                    sigma[channel] += self.mask[i][j] * self.pixels[xi, yj][channel]
            sigma[channel] //= 16
        mask_image.putpixel((x, y), (sigma[0], sigma[1], sigma[2]))
    
    def add_mask(self):
        from PIL import Image
        mask_img = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        for i in range(self.width):
            for j in range(self.height):
                self._change_pixel_on_mask(mask_img, i, j)
        return mask_img
    
    def show_image_on_mask(self):
        self.src.show()
        self.add_mask().show()

        
t = Graphic('test1.jpg')
t.show_image_on_mask()