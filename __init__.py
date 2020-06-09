import PIL
import PIL.ImageFont
import PIL.Image
import PIL.ImageDraw
import PIL.ImageOps
import tkinter.filedialog
from tkinter import messagebox
import os
import datetime
#字符画所使用的的字符集
ascii_char=list(r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.")
width=int(170) #字符画的宽度
height=int(192) #字符画的高度

PIXEL_ON=0
PIXEL_OFF=255
PIL.Image.MAX_IMAGE_PIXELS=None
#将256灰度映射到字符集上
def get_char(r,g,b,alpha=256):
    if alpha==0:
        return ''
    length=len(ascii_char)
    gray=int(0.2126*r+0.7152*g+0.0722*b) #计算灰度
    unit=(256.0+1)/length
    return ascii_char[int(gray/unit)] #不同灰度对应不同字符
    #通过灰度来区分色块



#txt转image
def text_image(text_path,font_path=None):
    grayscale='L'
    # print("解析txt开始:%s", datetime.datetime.now())
    #解析txt文件，读取文件每行的字符，放到一个元组中
    with open(text_path) as text_file:
        lines=tuple(l.rstrip() for l in text_file.readlines())
        #rstrip :删除字符串结尾字符
        #tuple ：元组
    large_font=10
    font_path=font_path or 'cour.tff'
    #创建一个字体对象
    # print("解析txt结束:%s", datetime.datetime.now())
    try:
        # print("创建字体对象开始:%s", datetime.datetime.now())
        font=PIL.ImageFont.truetype(font_path,size=large_font)
        # print("创建字体对象结束:%s", datetime.datetime.now())
    except IOError:
        font=PIL.ImageFont.load_default()
        # print('')
    #制作背景图像根据字体和线条
    pt2px=lambda pt: int(round(pt*96.2/72))
    # key = lambda s: font.getsize(s)[0]
    # start=datetime.datetime.now()
    # print("获取lines元组中元素的宽度start:%s", datetime.datetime.now())
    # liness=[]
    # maxs=0
    # maxline=''
    # for ln in lines:
    #     # print(key(ln))
    #     if(key(ln)>maxs):
    #         maxs=key(ln)
    #         maxline=ln
        # liness.append(key(ln))
    # print("获取lines元组中元素的宽度end:%s", datetime.datetime.now())
    #获取lines元组中宽度最大的一个字符串
    # print("获取lines元组中宽度最大的一个字符串start:%s",datetime.datetime.now())
    # max_width_line=max(liness,key=lambda s: s)
    # max_width_line=maxline
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
    # print('max_width_line:%s',max_width_line)
    # print("获取lines元组中宽度最大的一个字符串end:%s",datetime.datetime.now())
    # end=datetime.datetime.now()
    # print("获取lines元组中宽度最大的一个字符串所用时间:%s",end-start)
    # print(max_width_line)
    # print(font.getsize(lines[0])[0])
    # print(lines[0])
    test_string=r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'."
    #获取字符串test_string的高度，转换成像素的高度
    # print("获取字符串test_string的高度，转换成像素的高度start:%s",datetime.datetime.now())
    max_height=pt2px(font.getsize(test_string)[1])
    # print("获取字符串test_string的高度，转换成像素的高度end:%s,max_height:%s",datetime.datetime.now(),max_height)
    #获取txt中宽度最大的字符串的宽度，转换成像素的宽度
    # print("获取txt中宽度最大的字符串的宽度，转换成像素的宽度start:%s",datetime.datetime.now())
    max_width=pt2px(font.getsize(max_width_line)[0])
    # print("获取txt中宽度最大的字符串的宽度，转换成像素的宽度end:%s,max_width:%s",datetime.datetime.now(),max_width)
    #图像的高度
    # print("获取图像的高度start:%s",datetime.datetime.now())
    height=max_height*len(lines)
    # print("获取图像的高度end:%s,height:%s",datetime.datetime.now(),height)
    #图像的宽度
    # print("获取图像的宽度start:%s",datetime.datetime.now())
    width=int(round(max_width+20))
    # print("获取图像的宽度end:%s,width:%s",datetime.datetime.now(),width)
    #创建一张空白图片 grayscale：模式，L,RGB...
    # print("创建空白图像对象开始:%s", datetime.datetime.now())
    image=PIL.Image.new(grayscale,(width,height),color=PIXEL_OFF)
    # print("创建空白图像对象结束:%s", datetime.datetime.now())
    #创建一个可以用来对image进行操作的对象
    # print("创建draw对象开始:%s", datetime.datetime.now())
    draw=PIL.ImageDraw.Draw(image)
    # print("创建draw对象结束:%s", datetime.datetime.now())
    vertical_position=5 #垂直
    horizontal_position=5 #水平
    line_spacing=int(round(max_height*0.8)) #行间距
    print("开始写入文本:%s", datetime.datetime.now())

    for line in lines:
        #向图片上写文字
        # (horizontal_position,vertical_position)：开始的位置
        # line：内容
        #fill=PIXEL_ON,颜色
        # font=font 字体
        # print("第%s行写入文本开始:%s", i,datetime.datetime.now())
        draw.text((horizontal_position,vertical_position),line,fill=PIXEL_ON,font=font)
        # print("第%s行写入文本结束:%s", i,datetime.datetime.now())
        vertical_position+=line_spacing
    print("结束写入文本:%s", datetime.datetime.now())
    #将输入图像转换为反色图像
    c_box=PIL.ImageOps.invert(image).getbbox()
    # image.resize((500, 500), PIL.Image.NEAREST)
    print("去掉图像的边框开始:%s", datetime.datetime.now())
    #去掉图像的边框
    image=image.crop(c_box)

    print("去掉图像的边框结束:%s", datetime.datetime.now())
    return image

if __name__=='__main__':
    root = tkinter.Tk()  # 创建一个实例
    root.withdraw()  # 隐藏实例
    messagebox.showinfo("提示","请选择一张图片，注意：图片越大生成的速度越慢")
    print("开始main:%s",datetime.datetime.now())
    default_dir=r"d:\\"
    # 图片所在位置
    file_path=tkinter.filedialog.askopenfilename(title=u'选择图片jpg,png格式',initialdir=(os.path.expanduser(default_dir)))
    print(file_path)
    messagebox.showinfo("提示","正在生成字符画请稍后")
    #选择图片
    im=PIL.Image.open(file_path)
    #获取图片的宽和高
    newWidth=im.width
    newHeight=im.height
    #判断原图的尺寸，原图越大，修改后的尺寸越小
    if(newWidth>1500 or newHeight>1500):
        w = int(im.width*0.45)
        h = int(im.height/4)
    elif(newWidth>1000 or newHeight*1.8>1000):
        w = int(im.width * 1.8 / 2)
        h = int(im.height / 2)
    else:
        w = int(im.width * 0.9)
        h = int(im.height/2)
    #修改图片的尺寸
    im=im.resize((w,h),PIL.Image.NEAREST)
    txt=''
    for i in range(h):
        for j in range(w):
            txt+=get_char(*im.getpixel((j,i)))
        txt+='\n'

    #选择文件保存的位置
    txtpath=file_path.replace('jpg','txt').replace('png','txt').replace('gif','txt')
    with open(txtpath,'w') as f:
        f.write(txt)

    print("开始生成图像")
    image=text_image(txtpath,'simfang.ttf')
    # print("显示图像开始:%s", datetime.datetime.now())
    # image.show()
    # print("显示图像结束:%s", datetime.datetime.now())

    print("保存图像开始:%s", datetime.datetime.now())
    newPath=txtpath.replace('txt','png')
    image.save(newPath)
    print("保存图像结束:%s", datetime.datetime.now())
    ims = PIL.Image.open(newPath)
    # print(newWidth)
    # print(newHeight)
    # ims.resize((w, h), PIL.Image.NEAREST)
    # ims.save(txtpath.replace('txt','png'))
    out = ims.resize((newWidth, newHeight),PIL.Image.ANTIALIAS) #resize image with high-quality
    out.save(newPath, 'png')
    print("生成字符画成功")
    messagebox.showinfo("提示", "生成字符画成功，请在原图的同一文件夹下查看")