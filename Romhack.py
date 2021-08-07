"""Author: cosarara97
Version: 0.2
This module was created to make the creation of ROM-Hacking tools easier.
It uses the binascii module a lot, and some of it functions are only
used of synonyms of binascii ones."""

#import sys, os
import binascii
from binascii import unhexlify

def conv_file2h(romFile):
    hexString = binascii.hexlify(romFile)
    return hexString


def conv_a2h(asciistr):
    """Converts ASCII hex string to it's hex equivalents."""
    hexstr = binascii.a2b_hex(asciistr)
    return hexstr


def convn_h2a(hexstr):
    """Converts hex string to it's ASCII equivalents."""
    asciistr = binascii.b2a_hex(hexstr)
    return asciistr


def conv_dec2hex(decnum):
    """Converts decimal int to it's hex equivalent
       without 0x (returns string)."""
    hexnum = hex(decnum)[2:]
    return hexnum


def conv_hex2dec(hexnum):
    """Converts hex number (string var) to it's decimal equivalent."""
    decnum = int(str(hexnum), 16)
    return decnum


def search(rom, length, start, byte="ff"):
    """Search for a certain number of repeated bytes in a string variable
       containing a ROM image in Hex. Normally used to search for FF
       bytes, which are free space in GBA ROMs, but also 00, which are free
       space in GB ROMs (i think).
       It returns the offset where all those bytes are in.
       "rom" is a string, "length" is an int, "start" is an int and "byte" is a
       string"""
    whatToSearchFor = byte * length  # whatToSearchFor = byte to search for
                                     # (usually ff) * length of bytes to search.
    offset_found = rom.find(whatToSearchFor, start) / 2
    return offset_found


def openRomRead(fileName):
    romOpenInReadMode = open(fileName, "rb")
    romContents = romOpenInReadMode.read()
    romOpenInReadMode.close()
    romHexString = conv_file2h(romContents)
    return romHexString


def openRomWrite(fileName):
    romOpenInWriteMode = open(fileName, 'wb')
    return romOpenInWriteMode


def readRomByte(hexRom, hexOffset):
    if hexOffset[0:2] == "0x":
        hexOffset = hexOffset[2:]
    decOffset = conv_hex2dec(hexOffset)
    byte = hexRom[decOffset * 2:decOffset * 2 + 2]
    return byte


def readRomData(hexRom, hexOffset, length):
    if hexOffset[0:2] == "0x":
        hexOffset = hexOffset[2:]
    decOffset = conv_hex2dec(hexOffset)
    data = hexRom[decOffset * 2:decOffset * 2 + length * 2]
    return data


def insertSpacesBetweenBytes(hexstring):
    """"This is a very useful one :D If you have a sting like this:
        '36373839302d41', this function will turn it into something like this:
        '36 37 38 39 30 2d 41'. It may be useless when you are working with
        the variables, but useful when you have to show the bytes to the user"""
    new = ""
    for i in range(int(len(hexstring) / 2)):
        pos = i * 2
        new += hexstring[pos:pos + 2] + " "
    return new

######################
#"""Author: Pokecréatorfr """"


def readpointer(rom, adress):
    functionhexvar = readRomData(rom, adress, 4)
    if functionhexvar[6:8] != '09' and functionhexvar[6:8] != '08':
        itsapointer = False
    if functionhexvar[6:8] == '09':
        functionhexvar = functionhexvar[0:6] + '01'
    if functionhexvar[6:8] == '08':
        functionhexvar = functionhexvar[0:6] + '0.'
    functionhexvar = functionhexvar[4:6] + functionhexvar[2:4] + functionhexvar[0:2]
    functionhexvar = functionhexvar.decode(encoding="utf-8")

    return functionhexvar

def add2hex(hex, numb):
    functionvar = conv_hex2dec(hex) + numb
    functionhexvar = conv_dec2hex(functionvar)
    return functionhexvar

def makepointer(adress):
    if len(adress) == 8:
        functionhexvar = '09' + adress[2:8]
    if len(adress) == 7:
        functionhexvar = '09' + adress[1:7]
    if len(adress) == 6:
        functionhexvar = '08' + adress[0:6]
    if len(adress) == 5:
        functionhexvar = '08' + '0' + adress[0:5]
    if len(adress) == 4:
        functionhexvar = '08' + '00' + adress[0:4]
    if len(adress) == 3:
        functionhexvar = '08' + '000' + adress[0:3]
    if len(adress) == 2:
        functionhexvar = '08' + '0000' + adress[0:2]
    if len(adress) == 1:
        functionhexvar = '08' + '00000' + adress[0:1]
    functionhexvar = functionhexvar[6:8] + functionhexvar[4:6] + functionhexvar[2:4] + functionhexvar[0:2]
    return functionhexvar

def writedatainrom(rom, data, adress):
    #print(adress)
    fonctionhexvar2 = openRomRead(rom).decode(encoding="utf-8")
    fonctionhexvar2 = unhexlify(fonctionhexvar2)
    fonctionhexvar = open(rom,'wb')
    fonctionhexvar = fonctionhexvar
    fonctionhexvar3 = unhexlify(data)
    fonctiondecvar = conv_hex2dec(adress)
    fonctionhexvar.write(fonctionhexvar2[0:fonctiondecvar] + fonctionhexvar3 + fonctionhexvar2[fonctiondecvar+len(fonctionhexvar3):len(fonctionhexvar2)])
    fonctionhexvar.close()

def searchdatainrom(rom, data):
    fonctionhexvar = conv_dec2hex(rom.find(data))
    if fonctionhexvar == 'x1':
        fonctionhexvar = '00'
    if fonctionhexvar != '00':
        if conv_hex2dec(fonctionhexvar) % 2 != 0:
            while conv_hex2dec(fonctionhexvar) % 2 != 0:
                fonctiondecvar = conv_hex2dec(fonctionhexvar) + 1
                fonctionhexvar = conv_dec2hex((rom[fonctiondecvar:]).find(data) + fonctiondecvar)
    fonctionhexvar = conv_dec2hex(int(conv_hex2dec(fonctionhexvar)/2))
    return fonctionhexvar

def freebyte(need):
    return b'ff'*need