import struct
import datetime

# 格式
# 0xAA08
# BinHead:8 version 1 maxStockCnt 8000 stockId(length)
# StockLabelId * maxStockCnt
# DataPos      * maxStockCnt
# 变长数据，通过 DataPos offset size 来定位

def dumpXrxd(data):
    # magic
    (magic, version, maxStockCnt, stockLen) = struct.unpack('<HHHH', data[:8])
    print(magic, version, maxStockCnt, stockLen)
    assert(magic == 0xAA08)
    assert(version == 1)
    print(maxStockCnt, stockLen)
    offset = 8

    labelIdSz = 16
    dataPosSz = 8
    xrxdSz = 20

    labelIdBuf = data[offset: offset + labelIdSz * maxStockCnt]
    offset += labelIdSz * maxStockCnt

    dataPosBuf = data[offset: offset + dataPosSz * maxStockCnt]
    offset += dataPosSz * maxStockCnt

    for idx in range(stockLen):
        label, idx  = struct.unpack('<12sI', labelIdBuf[idx * labelIdSz: (idx + 1) * labelIdSz])
        label = label.rstrip(b'\x00').decode()
        itemOffset, itemSz = struct.unpack('<II', dataPosBuf[idx * dataPosSz: (idx + 1) * dataPosSz])

        print(label, idx, itemOffset, itemSz)
        item = data[offset + itemOffset: offset + itemOffset + itemSz]
        for xrxdIdx in range(len(item) // 20):
            xrxdData = item[xrxdIdx * xrxdSz : (xrxdIdx + 1) * xrxdSz]
            time, give, allocate, allocatePrice, earnings = struct.unpack('<Iffff', xrxdData)
            dt = datetime.datetime.fromtimestamp(time)
            print(time, dt, give, allocate, allocatePrice, earnings)

