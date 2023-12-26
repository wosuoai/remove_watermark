import os
import sys
import cv2
import numpy
from moviepy import editor
import ast
from models.BussinessException import BussinessException
from core.logger import logger

TEMP_VIDEO = 'temp.mp4'

class WatermarkRemover():
    """
    参数参考值
    roi_list = “[624, 14, 221, 34]”
    threshold = 80
    kernel_size = 5
    video_path = 'video'
    save_path = 'output'
    """

    def __init__(self, roi_list: str, threshold: int, kernel_size: int, video_path: str, save_path: str):
        self.roi_list = ast.literal_eval(roi_list)    # 水印区域
        self.threshold = threshold  # 阈值分割所用阈值
        self.kernel_size = kernel_size  # 膨胀运算核尺寸
        self.video_path = video_path    # 原视频文件夹路径
        self.save_path = save_path  # 处理后的视频保存文件夹路径
        logger.debug(f"传入参数经处理后的参数值::roi_list: {self.roi_list}, threshold: {self.threshold}, kernel_size: {self.kernel_size}, video_path: {self.video_path}, save_path: {self.save_path}")

    # # 根据用户手动选择的ROI（Region of Interest，感兴趣区域）框选水印或字幕位置。
    # def select_roi(self, img: numpy.ndarray, hint: str) -> list:
    #     '''
    # 框选水印或字幕位置，SPACE或ENTER键退出
    # :param img: 显示图片
    # :return: 框选区域坐标
    # '''
    #     COFF = 0.7
    #     w, h = int(COFF * img.shape[1]), int(COFF * img.shape[0])
    #     resize_img = cv2.resize(img, (w, h))
    #     roi = cv2.selectROI(hint, resize_img, False, False)
    #     cv2.destroyAllWindows()
    #     watermark_roi = [int(roi[0] / COFF), int(roi[1] / COFF), int(roi[2] / COFF), int(roi[3] / COFF)]
    #     return watermark_roi

    # 对输入的蒙版进行膨胀运算，扩大蒙版的范围
    def dilate_mask(self, mask: numpy.ndarray) -> numpy.ndarray:

        '''
    对蒙版进行膨胀运算
    :param mask: 蒙版图片
    :return: 膨胀处理后蒙版
    '''
        kernel = numpy.ones((self.kernel_size, self.kernel_size), numpy.uint8)
        mask = cv2.dilate(mask, kernel)
        logger.debug(f"对蒙版进行膨胀运算:{mask}")
        return mask

    # 根据手动选择的ROI区域，在单帧图像中生成水印或字幕的蒙版。
    def generate_single_mask(self, img: numpy.ndarray, roi: list, threshold: int) -> numpy.ndarray:
        '''
    通过手动选择的ROI区域生成单帧图像的水印蒙版
    :param img: 单帧图像
    :param roi: 手动选择区域坐标
    :param threshold: 二值化阈值
    :return: 水印蒙版
    '''
        # 区域无效，程序退出
        if len(roi) != 4:
            print('NULL ROI!')
            logger.error("选择的ROI区域错误！")
            raise BussinessException("选择的ROI区域错误！")
            #sys.exit()

        # 复制单帧灰度图像ROI内像素点
        roi_img = numpy.zeros((img.shape[0], img.shape[1]), numpy.uint8)
        start_x, end_x = int(roi[1]), int(roi[1] + roi[3])
        start_y, end_y = int(roi[0]), int(roi[0] + roi[2])
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        roi_img[start_x:end_x, start_y:end_y] = gray[start_x:end_x, start_y:end_y]

        # 阈值分割
        _, mask = cv2.threshold(roi_img, threshold, 255, cv2.THRESH_BINARY)
        logger.debug(f"阈值处理后：{mask}")
        return mask

    # 通过截取视频中多帧图像生成多张水印蒙版，并通过逻辑与计算生成最终的水印蒙版
    def generate_watermark_mask(self, video_path: str) -> numpy.ndarray:
        '''
    截取视频中多帧图像生成多张水印蒙版，通过逻辑与计算生成最终水印蒙版
    :param video_path: 视频文件路径
    :return: 水印蒙版
    '''
        video = cv2.VideoCapture(video_path)
        success, frame = video.read()
        roi = self.roi_list
        mask = numpy.ones((frame.shape[0], frame.shape[1]), numpy.uint8)
        mask.fill(255)

        step = video.get(cv2.CAP_PROP_FRAME_COUNT) // 5
        index = 0
        while success:
            if index % step == 0:
                mask = cv2.bitwise_and(mask, self.generate_single_mask(frame, roi, self.threshold))
            success, frame = video.read()
            index += 1
        video.release()
        logger.debug(f"生成最终的水印蒙版是：{self.dilate_mask(mask)}")

        return self.dilate_mask(mask)

    # 根据手动选择的ROI区域，在单帧图像中生成字幕的蒙版。
    def generate_subtitle_mask(self, frame: numpy.ndarray, roi: list) -> numpy.ndarray:
        '''
    通过手动选择ROI区域生成单帧图像字幕蒙版
    :param frame: 单帧图像
    :param roi: 手动选择区域坐标
    :return: 字幕蒙版
    '''
        mask = self.generate_single_mask(frame, [0, roi[1], frame.shape[1], roi[3]], self.threshold)  # 仅使用ROI横坐标区域
        logger.debug(f"ROI区域生成单帧图像字幕蒙版是：{self.dilate_mask(mask)}")
        return self.dilate_mask(mask)

    def inpaint_image(self, img: numpy.ndarray, mask: numpy.ndarray) -> numpy.ndarray:
        '''
    修复图像
    :param img: 单帧图像
    :parma mask: 蒙版
    :return: 修复后图像
    '''
        telea = cv2.inpaint(img, mask, 1, cv2.INPAINT_TELEA)
        logger.debug(f"修复后图像：{telea}")
        return telea

    def merge_audio(self, input_path: str, output_path: str, temp_path: str):
        '''
    合并音频与处理后视频
    :param input_path: 原视频文件路径
    :param output_path: 封装音视频后文件路径
    :param temp_path: 无声视频文件路径
    '''
        with editor.VideoFileClip(input_path) as video:
            audio = video.audio
            with editor.VideoFileClip(temp_path) as opencv_video:
                clip = opencv_video.set_audio(audio)
                clip.to_videofile(output_path)

    def remove_video_watermark(self):
        '''
    去除视频水印
    '''
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        filenames = [os.path.join(self.video_path, i) for i in os.listdir(self.video_path)]
        mask = None

        for i, name in enumerate(filenames):
            if i == 0:
                # 生成水印蒙版
                mask = self.generate_watermark_mask(name)
                logger.debug(f"生成的水印蒙版是：{mask}")

            # 创建待写入文件对象
            video = cv2.VideoCapture(name)
            fps = video.get(cv2.CAP_PROP_FPS)
            size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            video_writer = cv2.VideoWriter(TEMP_VIDEO, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

            # 逐帧处理图像
            success, frame = video.read()

            while success:
                frame = self.inpaint_image(frame, mask)
                video_writer.write(frame)
                success, frame = video.read()

            video.release()
            video_writer.release()
            logger.debug("视频去水印完成！")

            # 封装视频
            (_, filename) = os.path.split(name)
            output_path = os.path.join(self.save_path, filename.split('.')[0] + '_without_watermark.mp4')  # 输出文件路径
            self.merge_audio(name, output_path, TEMP_VIDEO)
            logger.debug(f"将处理后的视频输出到目标路径：{self.save_path}")

    if os.path.exists(TEMP_VIDEO):
        os.remove(TEMP_VIDEO)

    def remove_video_subtitle(self):
        '''
    去除视频字幕
    '''
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        filenames = [os.path.join(self.video_path, i) for i in os.listdir(self.video_path)]
        roi = []

        for i, name in enumerate(filenames):
            # 创建待写入文件对象
            video = cv2.VideoCapture(name)
            fps = video.get(cv2.CAP_PROP_FPS)
            size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            video_writer = cv2.VideoWriter(TEMP_VIDEO, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

            # 逐帧处理图像
            success, frame = video.read()
            if i == 0:
                roi = self.roi_list

            while success:
                mask = self.generate_subtitle_mask(frame, roi)
                frame = self.inpaint_image(frame, mask)
                video_writer.write(frame)
                success, frame = video.read()

            video.release()
            video_writer.release()
            logger.debug("视频去字幕完成！")

            # 封装视频
            (_, filename) = os.path.split(name)
            output_path = os.path.join(self.save_path, filename.split('.')[0] + '_without_sub.mp4')  # 输出文件路径
            self.merge_audio(name, output_path, TEMP_VIDEO)
            logger.debug(f"将处理后的视频输出到目标路径：{self.save_path}")

        if os.path.exists(TEMP_VIDEO):
            os.remove(TEMP_VIDEO)

async def deal_video_watermark(roi_list: str, threshold: int, kernel_size: int, video_path: str, save_path: str):
    remover = WatermarkRemover(roi_list=roi_list, threshold=threshold, kernel_size=kernel_size, video_path=video_path, save_path=save_path)
    remover.remove_video_watermark()
    return {"message": "Video watermark processed successfully."}


async def deal_video_subtitle(roi_list: str, threshold: int, kernel_size: int, video_path: str, save_path: str):
    remover = WatermarkRemover(roi_list=roi_list, threshold=threshold, kernel_size=kernel_size, video_path=video_path, save_path=save_path)
    remover.remove_video_subtitle()
    return {"message": "Video subtitle processed successfully."}