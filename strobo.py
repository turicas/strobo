# coding: utf-8

import os
import glob
import uuid

from shutil import copyfile, rmtree
from math import ceil

import Image
import ImageDraw
import ImageFont
import ImagePalette
import ImageColor


DEFAULT_IMAGE_QUALITY = 90
DEFAULT_VIDEO_QUALITY = 10
DEFAULT_AUDIO_QUALITY = 5


class ImageText(Image.Image):
    '''Get a text and create an image with that text.
    '''


    def __init__(self, mode='RGBA', size=(320, 240),
                 background_color=(255, 255, 255)):
        Image.Image.__init__(self)
        if background_color == None:
            im = Image.core.new(mode, size)
        else:
            color_type = type(background_color).__name__
            if color_type == 'str' or color_type == 'unicode':
                background_color = ImageColor.getcolor(background_color, mode)
            im = Image.core.fill(mode, size, background_color)
        self.im = im
        self.mode = im.mode
        self.size = im.size
        if im.mode == 'P':
            self.palette = ImagePalette.ImagePalette()


    def write_text(self, (x, y), text, fontfile='DejaVuSansMono.ttf', size=20):
        w_max, h_max = self.size
        draw = ImageDraw.Draw(self)
        self.draw = draw
        font = ImageFont.truetype(fontfile, size)
        total_height = 0
        h_offset = 5
        for line in text:
            if isinstance(line, tuple):
                font = ImageFont.truetype(fontfile, line[0])
                line = line[1]
            else:
                font = ImageFont.truetype(fontfile, size)
            w, h = font.getsize(line)
            total_height += h + h_offset
        height = (h_max - total_height) / 2
        for line in text:
            if isinstance(line, tuple):
                font = ImageFont.truetype(fontfile, line[0])
                line = line[1]
            else:
                font = ImageFont.truetype(fontfile, size)
            w, h = font.getsize(line)
            draw.text(((w_max - w) / 2, height), line, font=font,
                      fill=(0, 7 * 16 + 5, 11 * 16 + 2))
            height += h + h_offset


def normalize_images(list_of_images, destination, size=(640, 480)):
    new_list = []
    for image in list_of_images:
        img = Image.open(image)
        if img.size != size or img.format != 'JPEG':
            img = img.resize(size, Image.ANTIALIAS)
            # TODO: resize image proportionally
            filename = '%s/%s.jpg' % (destination, os.path.basename(image))
            img.save(filename, quality=DEFAULT_IMAGE_QUALITY)
            new_list.append(filename)
        else:
            new_list.append(image)
    return new_list


class Timeline(object):
    '''
    '''


    def __init__(self, fps, (width, height)):
        self.fps = fps
        self.w = width
        self.h = height
        self.frames = []


    def add_image(self, image, duration, fade_in=0, fade_out=0, blank_in=None,
                  blank_out=None):
        self.frames.append({'filename': image, 'duration': duration,
                            'fade_in': fade_in, 'fade_out': fade_out})
        if blank_in != None:
            self.frames[-1]['blank_in'] = blank_in
        if blank_out != None:
            self.frames[-1]['blank_out'] = blank_out


    def create_images(self, path):
        self.path = path
        blank = Image.new('RGBA', (self.w, self.h), color='#FFFFFF')
        blank.save('/tmp/blank.png')
        del(blank)
        blank_in = blank_out = Image.open('/tmp/blank.png')

        count = 1
        self.total_duration = 0
        for img in self.frames:
            if not 'blank_in' in img:
                img['blank_in'] = blank_in
            else:
                if isinstance(img['blank_in'], str):
                    img_tmp = Image.open(img['blank_in'])
                    img['blank_in'] = img_tmp.convert('RGBA')
                    #img['blank_in'] = '%s.png' % img['blank_in']
                    #img_tmp.save(img['blank_in'])
                    #del(img_tmp)
                    #img['blank_in'] = Image.open(img['blank_in'])
            if not 'blank_out' in img:
                img['blank_out'] = blank_out
            else:
                if isinstance(img['blank_out'], str):
                    img_tmp = Image.open(img['blank_out'])
                    img['blank_out'] = img_tmp.convert('RGBA')
                    #img['blank_out'] = '%s.png' % img['blank_out']
                    #img_tmp.save(img['blank_out'])
                    #del(img_tmp)
                    #img['blank_out'] = Image.open(img['blank_out'])

            image = Image.open(img['filename'])
            image = image.convert('RGBA')
            if img['fade_in'] > 0:
                fade_in_total_frames = int(ceil(img['fade_in'] * self.fps))
                for f in range(1, fade_in_total_frames + 1):
                    img_tmp = Image.blend(image, img['blank_in'],
                                          1 - (float(f) / fade_in_total_frames))
                    img_tmp.save('%s/%09d.jpg' % (path, count),
                                 quality=DEFAULT_IMAGE_QUALITY)
                    count += 1

            duration_total_frames = int(ceil(img['duration'] * self.fps))
            for f in range(1, duration_total_frames + 1):
                copyfile(img['filename'], '%s/%09d.jpg' % (path, count))
                count += 1

            if img['fade_out'] > 0:
                fade_out_total_frames = int(ceil(img['fade_out'] * self.fps))
                for f in range(1, fade_out_total_frames + 1):
                    img_tmp = Image.blend(image, img['blank_out'],
                                          (float(f) / fade_out_total_frames))
                    img_tmp.save('%s/%09d.jpg' % (path, count),
                                 quality=DEFAULT_IMAGE_QUALITY)
                    count += 1

            self.total_duration += img['fade_in'] + img['duration'] + \
                                   img['fade_out']
            self.total_frames = count - 1


    def render(self, filename_full, audio=None, with_blank_audio=False,
               delete_temp_files=False):
        if with_blank_audio:
            import wave
            total_frames = int(round(22050 * self.total_duration))
            wav = wave.open('/tmp/blank.wav', 'wb')
            wav.setparams((1, 1, 22050, total_frames,
                           'NONE', 'noncompressed'))
            wav.writeframes(chr(128) * total_frames)
            wav.close()
            audio = '/tmp/blank.wav'

        filenames = '%s/%%09d.jpg' % self.path
        filename = filename_full.split('/')[-1]

        if audio:
            commands = [
                    ('/usr/bin/ffmpeg2theora -v %(video_quality)d '
                     '--inputfps %(fps)d %(path)s/%%09d.jpg '
                     '-o /tmp/%(filename)s-video.ogg'),
                    ('/usr/bin/ffmpeg2theora -a %(audio_quality)d %(audio)s '
                     '-o /tmp/%(filename)s-audio.ogg'),
                    ('/usr/local/bin/oggz-merge -o %(filename_full)s '
                     '/tmp/%(filename)s-video.ogg '
                     '/tmp/%(filename)s-audio.ogg')]
        else:
            commands = [
                    ('/usr/bin/ffmpeg2theora -v %(video_quality)d '
                     '%(path)s/%%09d.jpg -o %(filename_full)s'),]
        data = dict(video_quality=DEFAULT_VIDEO_QUALITY, path=self.path,
                    filename=filename, audio_quality=DEFAULT_AUDIO_QUALITY,
                    audio=audio, filename_full=filename_full, fps=self.fps)

        for cmd in commands:
            cmd = cmd % data
            #TODO: should use logging
            os.system(cmd)

        #TODO: ffmpeg2theora options:
        #       --artist              Name of artist (director).
        #       --title               Title.
        #       --date                Date.
        #       --location            Location.
        #       --organization        Name of organization (studio).
        #       --copyright           Copyright.
        #       --license             License.
        #       --contact             Contact link.

        if delete_temp_files:
            rmtree(self.dirname_frames)
            rmtree(self.dirname)


class SlideShow(Timeline):
    '''
    '''


    def __init__(self, delay, fps=15, size=(320, 240), fade_in=0.5,
                 fade_out=0.5):
        #TODO: add image_fade_in (start) and image_fade_out (end)
        Timeline.__init__(self, fps, (size[0], size[1]))
        self.delay = delay
        self.audio = None
        self.fade_in = fade_in
        self.fade_out = fade_out


    def add_audio(self, audio):
        self.audio = audio


    def add_images(self, *args):
        list_of_files = []
        for i in args:
            list_of_files.extend(glob.glob(i))
        unique = str(uuid.uuid4())
        self.dirname = dirname = '/tmp/%s-resized' % unique
        self.dirname_frames = '/tmp/%s-frames' % unique
        os.mkdir(dirname)
        os.mkdir(self.dirname_frames)
        list_of_files = normalize_images(list_of_files, dirname,
                                         (self.w, self.h))
        total = len(list_of_files)
        black = Image.new('RGBA', (self.w, self.h), color='#000000')
        black.save('/tmp/black.png')
        del(black)
        for i, image in enumerate(list_of_files):
            if i == 0:
                self.add_image(image, self.delay, fade_in=self.fade_in,
                               blank_in='/tmp/black.png')
            elif i < total - 1:
                self.add_image(image, self.delay, fade_in=self.fade_in,
                               blank_in=previous)
            else:
                self.add_image(image, self.delay, fade_in=self.fade_in,
                               blank_in=previous, fade_out=self.fade_out,
                               blank_out='/tmp/black.png')
            previous = image


    def create_images(self):
        Timeline.create_images(self, self.dirname_frames)


    def render(self, filename):
        if self.audio:
            Timeline.render(self, filename, self.audio)
        else:
            Timeline.render(self, filename)
