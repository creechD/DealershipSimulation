#Interphase - Copyright (C) 2009 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

import base64
try:
    import cStringIO
except ImportError:
    import StringIO as cStringIO
import sys

__docformat__ = 'restructuredtext'


def _load_default_images():
    import env
    try:
        env.engine.display.setup_images([(i,_image[i]) for i in _image])
    except AttributeError:
        pass


def _image_encode(image_file):
    """Encode image to base64 encoded string."""
    image = file(image_file, 'r')
    image_obj = cStringIO.StringIO(image.read())
    image.close()
    try:
        image_dat = base64.b64encode(image_obj.getvalue())
    except AttributeError:
        image_dat = base64.encodestring(image_obj.getvalue())
    foutput = open('_'+image_file[:-4]+'.py', 'w')
    foutput.write('_image[\'' + image_file + '\'] = \\\n')
    foutput.write('"')
    foutput.write(image_dat)
    foutput.write('"\n')
    foutput.close()


def _image_decode(image=None):
    """Decode image from base64 encoded string."""
    if image:
        try:
            image_dat = base64.b64decode(_image[image])
        except AttributeError:
            image_dat = base64.decodestring(_image[image])
        image_obj = cStringIO.StringIO(image_dat)
        return image_obj
    else:
        image_objs = {}
        for image in _image:
            try:
                image_dat = base64.b64decode(_image[image])
            except AttributeError:
                image_dat = base64.decodestring(_image[image])
            image_objs[image[:-4]] = ( image, cStringIO.StringIO(image_dat) )
        return image_objs


#Interphase Image Data
_image = {}

_image['panel.png'] = \
"iVBORw0KGgoAAAANSUhEUgAAAV4AAABkCAYAAADOvVhlAAAAAXNSR0IArs4c6QAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9kIChceM9TQp94AAAAddEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIFRoZSBHSU1Q72QlbgAABA5JREFUeF7t2UFOE3EchuGZod17DLdwCBMPARcgXMIrGBLX4hE8h+gpPERp/05pcOOS8C7s00UlRv3kyS9vmmH+8On79PLaPj7cT/N8Ma1vf3/TFwQIECDwCoExpjH2u8vr25d/ZHP8YvPj6+d5WbbTvAjuK3j9VQIECPwrsH6QnefN9ue3L+Nw2D1d3dwtxz/0HF2fcl0MAQIE3lBgnk+tnaaL9+/26+OFZX284EWAAAECbyuwPsv9/evjcnqm60WAAAECicDa3PVRgx+kJdhGCBAg8CywPnEgQYAAAQKtgPC23tYIECAwCa8jIECAQCwgvDG4OQIECAivGyBAgEAsILwxuDkCBAgIrxsgQIBALCC8Mbg5AgQICK8bIECAQCwgvDG4OQIECAivGyBAgEAsILwxuDkCBAgIrxsgQIBALCC8Mbg5AgQICK8bIECAQCwgvDG4OQIECAivGyBAgEAsILwxuDkCBAgIrxsgQIBALCC8Mbg5AgQICK8bIECAQCwgvDG4OQIECAivGyBAgEAsILwxuDkCBAgIrxsgQIBALCC8Mbg5AgQICK8bIECAQCwgvDG4OQIECAivGyBAgEAsILwxuDkCBAgIrxsgQIBALCC8Mbg5AgQICK8bIECAQCwgvDG4OQIECAivGyBAgEAsILwxuDkCBAgIrxsgQIBALCC8Mbg5AgQICK8bIECAQCwgvDG4OQIECAivGyBAgEAsILwxuDkCBAgIrxsgQIBALCC8Mbg5AgQICK8bIECAQCwgvDG4OQIECAivGyBAgEAsILwxuDkCBAgIrxsgQIBALCC8Mbg5AgQICK8bIECAQCwgvDG4OQIECAivGyBAgEAsILwxuDkCBAgIrxsgQIBALCC8Mbg5AgQICK8bIECAQCwgvDG4OQIECAivGyBAgEAsILwxuDkCBAgIrxsgQIBALCC8Mbg5AgQICK8bIECAQCwgvDG4OQIECAivGyBAgEAsILwxuDkCBAgIrxsgQIBALCC8Mbg5AgQICK8bIECAQCwgvDG4OQIECAivGyBAgEAsILwxuDkCBAgIrxsgQIBALCC8Mbg5AgQICK8bIECAQCwgvDG4OQIECAivGyBAgEAsILwxuDkCBAgIrxsgQIBALCC8Mbg5AgQICK8bIECAQCwgvDG4OQIECAivGyBAgEAsILwxuDkCBAgIrxsgQIBALCC8Mbg5AgQICK8bIECAQCwgvDG4OQIECAivGyBAgEAssIZ3jHjTHAECBM5YYIxl7e7+jAV86wQIEGgF1uYuu8vrW596W3drBAicq8AYx+Y+P+Mdh8NOfM/1EHzfBAg0AmOcWjtNm+Pb09XN3fHX7ePD/TTPF9P61vxHrBAgQOB/F1h/jrY+Xjg9XTi9/gATOUIZdRHlLwAAAABJRU5ErkJggg=="

_image['control.png'] = \
"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"

_image['button.png'] = \
"iVBORw0KGgoAAAANSUhEUgAAADIAAAAZCAYAAABzVH1EAAAAAXNSR0IArs4c6QAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAAOJgAADiYBou8l/AAAAAd0SU1FB9oKHgUDLwMwAZUAAARXSURBVFjDvVjfTxxVFP6+c8GmbhVakJQQ1LYYKtpaiYASTfFR/wO1je8Nxv/Abvvqk7Upz0bU/0AfwR+hwiqgNViVtrFKaBqKoG414j3Hh52ZnZnd2VmNyyR37+z9eb5zvnPOnUs0+QyPP18ys6cMAECQ+GJpbmakmbnthS4DCMAAsFJVfhAsF3XlPhnjcqeeeGYCBI+Z2dcEYbRoQXE8boorS5dn8oEYAVpMkAAQDbAACQlYDHNaynCuMagt6pc8IMuXZ6GmUwBMoYAazAwGM/U2lQcieBbAQMKEUFVBwBBMKGhYogHVubQqYMIAfpJrkeNjEx2EbVV3TxtSO7+a/3Q7a/49hW6QHAG58O/4Yk1wLuhTjLblUlL/vhjDn7ayAbgI4HTW/L/KGwBQurfj4KoBAzXEDhYKWfcfntU/frtVyrXIY8PjFqdmtH/MOCtfzjVcp7C/FyBfATANsMKGOLtIGCxyl7iy4soP2Zdys1NQe6+hAEdPjJ0FWMynhBWvLs+fy1PK/d39dwA7UCG2gYHIlfdwNdahcJVe8XmAbf668XMXALisTQf7hml7OWMWOLcBZork//DdJnjfwfN3N9cbAtm7b3+BlJMUQiggCTJ8l0otBCmgVPtZMzZs55t/lrdnM8PvkaFhkHwJwPtNsbSixJfN7INrK4sNhx7oPWRZfpyIuk34+Ob6jWhE3fB7bWURXnVKVaGq8Km6ps0rvOpUHggAEJEL4sREBOIEItXCoHZ1+hLFiYm4Cw0T4oOPHAOFLwD8MKkFS8byQDUEYUEfaS+q2kc3f7iSCaSnf7CD0K0gAcSWM8R9J8yfSQ8KciYIeHTeXvt+u2Fm7x94fB7ASF3Dp30x4gINsNJPq9+M5Vml9+Gj78BwOua1ka5Yh3KpdjPDu7d+vPpqwtLpTfoOD42p6qiqUmNUUvWV2sfafKKfqjrad3horAl6XRInTFPGuYg6jdrpnFyqWTPdoKpn1KslQSi8ryd8Tbt5r2fygKxdX5kXkQWRwFei4mqBJEA5E5GFtesr8w0Pja3i7274YWJKd9+RtwC81uhUnD6Y1g+OfHtjbfX1PMscevTJLQIdWSerdJsB2ze+XerMkqvlMX43clW0WWfPQ+cAvNFQ5Sn15Bjm/Nbtm2cbjRjsG6Z1Oc22d/L/5l0vG6uLdXeWmJNPqvoguflY4vNQ9ZXaB9HL+9popsl5qjqZB/W7tUUTkWLFyV3M4eP/oyBQzAIBANyNk2l5a73lJ2wp/7IO81pUr1Dv4X01pPpAy+ZjR5GwP16CMBw/tgRjinkgAECcTDsnRhc7ogSh1zkxJzKdt0bbnn0PjHjVgRZ9vQ3sKfSMKLW08/tGth9L2yRhpzK+Qgnk05Ttha6PATwXZoHKWqx+T6fJFOdXTbCs8/kAlnbKG7nZ/omnT35GcNxgjO4jACM4t/z57LPNAGn5DcdO+Q5bfVPD9kKXVq3RmjunPCD/x93ZPwYwF3oTtqJJAAAAAElFTkSuQmCC"


def main():
    image_file = sys.argv[1]
    _image_encode(image_file)

if __name__ == '__main__':
    main()


