# SmartCar
本代码仓库，用于存放智能车开发代码。包括上位机程序和下位机程序。上位机程序以Python和Qt为主，下位机，以C语言为主。
上位机编程语言：新增 C#.

;通信帧定义
[serialFrame]
frame_head(1byte)=0xAA
frame_head(1byte)=0xAA
frame_body(9bytes)=uint8,uint8,uint8,uint16(2bytes),uint16(2bytes),uint16(2bytes)
frame_tail(1byte)=0xFE
