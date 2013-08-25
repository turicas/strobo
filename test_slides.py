from strobo import SlideShow
import time

start = time.time()
print 'Creating slideshow...'
slides = SlideShow(delay=2.05, size=(800, 600), fade_in=0.4, fade_out=0.4)
print ' adding images...'
slides.add_images('tests/slide_show/dojo-fotos/*.jpg') #I could pass many arguments
print ' creating images...'
slides.create_images()
print ' Duration: %f seconds' % (time.time() - start)

print 'Rendering video...'
start = time.time()
slides.add_audio('tests/slide_show/macarronada.mp3')
slides.render('dojo-rio.ogv')
print ' Duration: %f seconds' % (time.time() - start)
