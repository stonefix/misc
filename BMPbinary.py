# -*- coding: utf-8 -*-

import re
import struct

def infoFile(file):
    # Парсим хэдер побайтово и выводим
    bmp = open(file, 'rb')
    print('Type:', bmp.read(2).decode())
    print('Size: %s' % struct.unpack('I', bmp.read(4)))
    print('Reserved 1: %s' % struct.unpack('H', bmp.read(2)))
    print('Reserved 2: %s' % struct.unpack('H', bmp.read(2)))
    print('Offset: %s' % struct.unpack('I', bmp.read(4)))
    print('DIB Header Size: %s' % struct.unpack('I', bmp.read(4)))
    print('Width: %s' % struct.unpack('I', bmp.read(4)))
    print('Height: %s' % struct.unpack('I', bmp.read(4)))
    print('Colour Planes: %s' % struct.unpack('H', bmp.read(2)))
    print('Bits per Pixel: %s' % struct.unpack('H', bmp.read(2)))
    print('Compression Method: %s' % struct.unpack('I', bmp.read(4)))
    print('Raw Image Size: %s' % struct.unpack('I', bmp.read(4)))
    print('Horizontal Resolution: %s' % struct.unpack('I', bmp.read(4)))
    print('Vertical Resolution: %s' % struct.unpack('I', bmp.read(4)))
    print('Number of Colours: %s' % struct.unpack('I', bmp.read(4)))
    print('Important Colours: %s' % struct.unpack('I', bmp.read(4)))

def imageToHex(file):
    string = ''
    with open(file, 'rb') as f:
        binValue = f.read(1)
        while len(binValue) != 0:
            hexVal = hex(ord(binValue))
            string += '\\' + hexVal
            binValue = f.read(1)    
    string = re.sub('0x', 'x', string)
    print(string)
    return string

if __name__ == "__main__":
    print("Введите имя bmp файла: ")
    file = input("Имя: ")
    print("Информация о файле:")
    infoFile(file)
    print("Файл в hex формате: ")
    imageToHex(file)