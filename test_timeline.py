# coding: utf-8
from strobo import ImageText, Timeline
import Image
import shutil
import time

def create_title_image():
    image = ImageText()
    image_text = ['web2py',
                  'http://www.web2py.com/',
                  '',
                  (18, u'por Álvaro Justen - Turicas'),
                  (18, 'http://blog.justen.eng.br/')]
    image.write_text((None, 20), image_text)
    image.save('web2py_alvaro.png')


def create_blank_image():
    image = ImageText(background_color='#FFFFFF')
    image.save('blank.png')


def create_forum_image():
    image = ImageText()
    image_text = [(14, ''),
                  (20, ''),
                  (20, ''),
                  (20, ''),
                  (20, ''),
                  (14, u'Fórum de Tecnologia em Software Livre'),
                  (14, 'SERPRO-RJ, 16 de setembro de 2009'),
                  (10, 'http://www.softwarelivre.serpro.gov.br/riodejaneiro'),]
    image.write_text((None, 20), image_text)
    img_serpro = Image.open('tests/timeline/SERPRO.jpg')
    image.paste(img_serpro, (95, 10))
    image.save('palestra_web2py.png')


def create_timeline_and_render_video():
    t = Timeline(30, (320, 240))
    t.add_image('web2py_alvaro.png', duration=3, fade_in=1.5, fade_out=1.5)
    t.add_image('blank.png', duration=1)
    t.add_image('palestra_web2py.png', duration=5, fade_in=1.5, fade_out=1.5)
    t.add_image('blank.png', duration=0.5)
    try:
        shutil.rmtree('img/')
    except OSError:
        pass
    finally:
        try:
            shutil.os.mkdir('img/')
        except OSError:
            pass
    t.create_images('img/')
    t.render('intro', with_blank_audio=True)


def run_and_print_time(list_of_functions):
    for function_ in list_of_functions:
        print 'Running %s' % function_.__name__
        start = time.time()
        function_()
        duration = time.time() - start
        print ' Duration: %f seconds' % duration


run_and_print_time((create_title_image, create_blank_image, create_forum_image,
                    create_timeline_and_render_video))        
