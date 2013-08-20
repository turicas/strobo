# coding: utf-8
from strobo import ImageText
import Image
import ImageDraw
import shutil
import time


print 'Creating image...'
start = time.time()
image = ImageText(size=(800, 600), background_color='#FFFFFF')
tamanho = 30
tamanho2 = tamanho + 20
image_text = [(tamanho, u'Fotos por:'),
              (tamanho2, u'Rodolfo Carvalho'),
              (tamanho, 'http://rodolfocarvalho.net/'),
              '',
              (tamanho, u'Música por:'),
              (tamanho2, u'Daniel Cukier'),
              (tamanho, 'http://agileandart.blogspot.com/'),
              '',
              (tamanho, u'Vídeo por:'),
              (tamanho2, u'Álvaro Justen - Turicas'),
              (tamanho, 'http://blog.justen.eng.br/'),
]
image.write_text((0, 20), image_text)
image.save('dojo_intro.png')
duration = time.time() - start
print 'Done in %f seconds' % duration
