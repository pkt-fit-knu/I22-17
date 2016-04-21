class Histogram():
    def __init__(self, path):
        from PIL import Image
        self.img_src = Image.open(path)
        self.img_width = self.img_src.size[0]
        self.img_height = self.img_src.size[1]
        self.img_size = self.img_width * self.img_height
        self.img_pixels = self.img_src.load()
        self.hist_arr = [self.__get_histogram_array(channel) for channel in range(0, 3)]
        self.hist_s = [self.__get_s_array(channel) for channel in range(0, 3)]

    def __get_histogram_array(self, channel):
        hist = [0 for i in range(0, 256)]
        for i in range(0, self.img_width):
            for j in range(0, self.img_height):
                hist[self.img_pixels[i, j][channel]] += 1
        return hist

    def __get_s_array(self, channel):
        import math
        s = []
        for i in range(0, 256):
            sigma = 0
            for j in range(0, i):
                sigma += self.hist_arr[channel][j] / self.img_size
            s.append(math.floor(sigma * 255))
        return s
        
    def set_new_pixel(self, x, y):
        self.img_src.putpixel((x, y), 
            (self.hist_s[0][old_pixel[0]], self.hist_s[1][old_pixel[1]], self.hist_s[2][old_pixel[2]]))
    
    def set_new_image(self):
        for i in range(0, self.img_width):
            for j in range(0, self.img_height):
                old_pixel = self.img_pixels[i, j]
                self.img_src.putpixel((i, j), (self.hist_s[0][old_pixel[0]], 
                                               self.hist_s[1][old_pixel[1]], 
                                               self.hist_s[2][old_pixel[2]]))

    def draw_histogram(self):
        from PIL import Image, ImageDraw
        h = 300
        hist = Image.new('RGB', (256, h), (255, 255, 255))
        draw = ImageDraw.Draw(hist)
        for diag in [(0, (255, 0, 0)), (1, (0, 255, 0)), (2, (0, 0, 255))]:
            channel = diag[0]
            color = diag[1]
            maximum = max(self.hist_arr[channel])
            for i in range(1, 256):
                x1, y1 = i - 1 , h - (self.hist_arr[channel][i-1] / maximum) * h
                x2, y2 = i, h - (self.hist_arr[channel][i] / maximum) * h
                draw.line((x1, y1, x2, y2), fill=color)
        hist.show()
    
    def show_new_image(self):
        self.img_src.show()
        self.draw_histogram()
        self.set_new_image()
        self.img_pixels = self.img_src.load()
        self.hist_arr = [self.__get_histogram_array(channel) for channel in range(0, 3)]
        self.img_src.show()
        self.draw_histogram()
    
h = Histogram('test2.jpg')
# h.draw_histogram()
h.show_new_image()