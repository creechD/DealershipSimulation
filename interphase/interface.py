#Interphase - Copyright (C) 2009 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from __future__ import division
from control import Control, FunctionControl, Label, Textbox
from util import Text, load_image
import os
from env import engine

__docformat__ = 'restructuredtext'


"""
:undocumented:EVENT
"""
EVENT = {'controlselect':30, 'controlinteract':31}


class Interface(engine.sprite.Sprite):
    """
    **Interface Object**

    To design an interface panel, interphase.Interface can be subclassed. Within the __init__() method call interphase.Interface.__init__(). Interface Object provides several methods to design and utilize an interface panel. Use add() to add controls to panel, place into a method called add_controls(); if added otherwise call activate() after to activate the panel. The program maintains the update of the panel including changes through the methods, however panel_update() can be used to force an update if required. If the Interface Object is subclassed, when overriding the update() method call interphase.Interface.update().
    
    Interface interaction can be maintained with the InterfaceState object, that is returned by update() or get_state(), or through Pygame event queue checking for event.type interphase.EVENT[ 'controlselect' ] and interphase.EVENT[ 'controlinteract' ] with the attribute event.state that references the InterfaceState object. To turn the panel off, deactivate() sets state.active to false. The panel can be drawn to the display with the draw() method.
    
    The module includes demo.py that demonstrates some of Interphase functionality.
    """

    _image_default = None
    _image_source = None
    _clipboard = None
    _clipboard_type = None
    _event_queue = []

    def __init__(self,
        identity='Interface_Panel',
        position=None,
        image=None,
        color=(0,0,0),
        size=(350,100),
        screen=(500,500),
        moveable=False,
        position_offset=(0,0),
        move_rate=(200,200),
        fixed=False,
        button_image=None,
        control_image=None,
        color_key=None,
        control_minsize=None,
        control_size='min',
        button_size=(12,12),
        function_button='left',
        control_button='right',
        scroll_button=None,
        font_color=(125,130,135),
        font_type=None,
        font_size=10,
        label_display=False,
        info_display=False,
        info_fontsize=10,
        info_fontcolor=(125,130,135),
        info_position=(2,0),
        tips_display=False,
        tips_fontsize=8,
        tips_fontcolor=(125,130,135),
        tips_position=(0,-15),
        control_response=125,
        pointer_interact=False,
        data_folder='data',
        data_zip=None,
        text_paste=False,
        event=False):
        """
        **Interface Object: Define panel.**

        Optional Parameters <default>:
        identity: 'id' panel name <'Interface_Panel'>.
        position: (x,y) panel placement on screen <None>.
            values < 1 are %screen.
            None centers on screen.
        image: 'image' panel image <None>.
            None use default image, 'none' suppress default image.
            Image in data folder.
        color: (r,g,b) panel color <(0,0,0)>.
        size: (w,h) dimension of panel <(350,100)>.
        screen: (w,h) dimension of screen <(500,500)>.
        moveable: bool panel can move <False>.
        position_offset: (x,y) panel move offset <(0,0)>.
        move_rate: (x,y) panel move rate pix/s <(200,200)>.
            values < 1 are %position_offset/s.
        fixed: bool panel fixed in place <False>.
        button_image: ['U','D'] or 'composite' control button image <None>.
            None use default image, 'none' suppress default image.
            Image in data folder.
        control_image: 'image' control background image <None>.
            None use default image, 'none' suppress default image.
            Image in data folder.
        color_key: (r,g,b) image color key transparency <None>.
            transparency set by image alpha value or color_key.
            value -1 color_key from pixel at (0,0).
        control_minsize: (x,y) minimum control size <None>.
        control_size: '' global control size if control_minsize set <'min'>.
            'auto', 'auto_width': fit items.
            'min', 'min_width': fit using control_minsize.
            'panel': use exact control_minsize.
        button_size: (x,y) button size <(12,12)>.
        function_button: placement of buttons of function_select <'left'>.
        control_button: placement of buttons of control_select <'right'>.
        scroll_button: activate scroll wheel <None>.
            - None,'vertical','horizontal','both'
        font_color: (r,g,b) font color of control text <(125,130,135)>.
        font_type: [] font type list <None>.
            None: default system font; []: use first font available.
            <control>.set_display_text(info='system') gets system fonts.
            'file:<font_name>' path to font file.
        font_size: int font size of control text <10>.
        label_display: bool label displayed <False>.
        info_display: bool info text displayed <False>.
        info_fontsize: int font size used for info text <10>.
        info_fontcolor: (r,g,b) font color used for info text <(125,130,135)>.
        info_position: (x,y) position of info text <(2,0)>.
        tips_display: bool tip text displayed <False>.
        tips_fontsize: int font size used for tip text <8>.
        tips_fontcolor: (r,g,b) font color used for tip text <(125,130,135)>.
        tips_position: (x,y) position offset of tip text <(0,-15)>.
        control_response: int control click response (ms) <125>.
        pointer_interact: bool pointer interact monitored <False>.
        data_folder: '' image data folder <'data'>.
        data_zip: '' image data zip <None>.
        text_paste: bool clipboard support <False>.
        event: bool interaction generates events <False>.
        """
        engine.sprite.Sprite.__init__(self)
        self._panel = engine.sprite.RenderUpdates(self)
        self._text = Text
        self._load_image = load_image
        self._data = data_folder
        self._data_zip = data_zip
        if self._data_zip and self._data:
            self._data_zip = os.path.join(self._data, self._data_zip)
        self._zipfile = None
        self._id = identity
        self._width, self._height = screen
        self._size = size
        if position:
            pos_x, pos_y = position
            if pos_x < 1:
                pos_x = pos_x * self._width
            if pos_y < 1:
                pos_y = pos_y * self._height
            self._x, self._y = int(pos_x), int(pos_y)
        else:
            self._x, self._y = self._width//2, self._height//2
        self._moveable = moveable                            #panel moveable
        self._positionx, self._positiony = self._x, self._y     #panel original placement
        self._offsetx, self._offsety = position_offset
        directionx, directiony = move_rate        #panel move speed
        if directionx < 1:
            directionx = directionx * abs(self._offsetx)
        if directiony < 1:
            directiony = directiony * abs(self._offsety)
        self._directionx, self._directiony = int(directionx), int(directiony)
        self._move_ratex, self._move_ratey = int(self._directionx/40), int(self._directiony/40)
        self._move_initiate = False
        self._color = color
        self._initialized = False
        self._controls = {}      #panel controls
        self._control_values = {}
        self._color_key = color_key
        self.image = None
        self.rect = None
        self._control_image = {}
        self._button_image = {}
        self._button_size = button_size
        self._set_image(image, control_image, button_image)    #load panel images
        if control_minsize:
            self._control_minsize = {}
            padding = ( min(control_minsize[0],control_minsize[1]) // 10 ) + 4
            if padding % 2:
                padding -= 1
            self._control_minsize['size'] = control_minsize
            self._control_minsize['min'] = control_minsize[0]-padding, control_minsize[1]-padding
            self._control_minsize['pad'] = padding
        else:
            self._control_minsize = None
        self._control_size = control_size
        self._button_placement = { 'function_select':function_button, 'control_select':control_button, 'textbox':'right' }
        if scroll_button:
            try:
                if scroll_button == 'vertical':
                    self._scroll_button = set([4,5])
                elif scroll_button == 'horizontal':
                    self._scroll_button = set([6,7])
                else:
                    self._scroll_button = set([4,5,6,7])
            except NameError:   #set module not available
                from java.util import HashSet
                if scroll_button == 'vertical':
                    self._scroll_button = HashSet([4,5])
                elif scroll_button == 'horizontal':
                    self._scroll_button = HashSet([6,7])
                else:
                    self._scroll_button = HashSet([4,5,6,7])
        else:
            self._scroll_button = None
        self._scroll_button_selected = {4:'_top', 5:'_bottom', 6:'_top', 7:'_bottom'}
        self._scroll_button_selected_alt = {4:'_top', 5:'_bottom', 6:'_bottom', 7:'_top'}
        self._control_events = 1
        if moveable:
            self._displayed = False
        else:
            self._displayed = True
        self._panel_disabled = False     #disabled on move
        self._display_fixed = fixed      #moveable panel fixed in place
        self._active = True
        self._panel_active = False
        self._panel_display = True     #panel controls display on or toggled with pointer interact
        self._panel_rect = engine.Rect(self.rect)
        self._font_color = font_color
        self._font_type = font_type
        self._font_size = font_size
        self._text(self.image, self._font_type, self._font_size)     #initialize Text defaults
        self._info_display = info_display   #info display toggle
        self._info_displaying = False   #info currently displaying
        self._info = self._text(self.image)  #info displayed on panel
        self._info.set_font_size(info_fontsize)
        self._info.set_font_color(info_fontcolor)
        self._info.set_font_bgcolor(None)
        self._info.set_position(info_position)
        self._tips_display = tips_display
        self._tips = self._text(self.image)
        self._tips.set_font_size(tips_fontsize)
        self._tips.set_font_color(tips_fontcolor)
        self._tips.set_font_bgcolor(None)
        self._tips_position = tips_position    #default tips over pointer
        self._control_hover = None    #interact during tips_display
        self._controls_disabled = {}
        self._active_color = (255,0,0)
        self._update_display = True      #update panel display
        self._control_response = control_response   #response speed of control
        self._control_press = {'control':None, 'button':None, 'response':0, 'hold':0, 'rtime':0, 'htime':0}
        self._label_display = label_display  #show control labels
        self._panel_interact = False
        self._control_moveable = False  #control moveable
        self._control_move = None   #control selected to move
        self._pointer_position = (0,0)
        self._pointer_interact = pointer_interact   #detect control hover
        self._clock = engine.time.Clock()
        self._update_panel = True   #set for panel update
        self._initial_update = 10   #panel updates for short duration
        self._panel_function = []   #list of panel functions to run on panel update
        self._sustain_update = False    #panel register sustained update status
        self._control_event = []    #controls recently pressed
        self._interface = {'state':None, 'update':False}    #interface control state
        self._event = event
        self._events = {}
        self._events['controlselect'] = engine.event.Event(EVENT['controlselect'], self._interface)
        self._events['controlinteract'] = engine.event.Event(EVENT['controlinteract'], self._interface)
        self.add_controls()
        self.activate()

    def add_controls(self):
        """Method to overide in subclass for adding controls."""
        pass

    def add(self, identity, control_type, position, **parameters):
        """Add control to panel."""
        panel = self
        if control_type in ('control_select', 'control_toggle'):
            interface_control = Control(panel, identity, control_type, position, **parameters)
        elif control_type in ('function_select', 'function_toggle'):
            interface_control = FunctionControl(panel, identity, control_type, position, **parameters)
        elif control_type == 'label':
            interface_control = Label(panel, identity, control_type, position, **parameters)
        elif control_type == 'textbox':
            interface_control = Textbox(panel, identity, control_type, position, **parameters)
        self._controls[identity] = interface_control
        return interface_control

    def activate(self, activate_panel=True):
        """Panel activation."""
        if activate_panel:
            self._active = True
            self._panel_active = True
            self._panel_disabled = False
            self._activate_controls()
            if not self._initialized:
                if self._moveable and not self._display_fixed:
                    self._x, self._y = self._positionx+self._offsetx, self._positiony+self._offsety
                self._initialized = True
            if self._zipfile:
                self._zip_file(close=True)
            self._panel_function.append(self._force_update)
            self.panel_update()
        else:
            self.deactivate()

    def deactivate(self):
        """Panel deactivation."""
        self._active = False
        self._control_press['control'] = None
        self._panel_disabled = True
        self.panel_update()

    def _force_update(self):
        if self._initial_update:
            self._update_panel = True
            self._initial_update -= 1
        else:
            self._initial_update = 10
            self._panel_function.pop()

    def _activate_controls(self):
        """Panel controls activation."""
        for ctrl in self._controls:
            self._controls[ctrl]._activate()

    def add_control(self, identity, control_type, position, **parameters):
        """Add control to panel."""
        interface_control = self.add(identity, control_type, position, **parameters)
        return interface_control

    def get_control(self, *control):
        """Retrieve control object. Multiple controls return a dictionary of control objects, and if no parameter given return dictionary of all control objects."""
        if not control:
            return self._controls.copy()
        elif len(control) == 1:
            return self._controls[control[0]]
        ctr = {}
        for ctrl in control:
            ctr[ctrl] = self._controls[ctrl]
        return ctr

    def remove_control(self, *control):
        """Remove control from panel."""
        if control:
            for ctrl in control:
                del self._controls[ctrl]
                del self._control_values[ctrl]
                for item in self._controls:
                    if self._controls[item].control_type in ('function_select', 'function_toggle'):
                        for function in self._controls[item].link:
                            if ctrl in self._controls[item].link[function]:
                                self._controls[item].link[function].remove(ctrl)
        else:
            self._controls.clear()
            self._control_values.clear()

    def enable_control(self, *control):
        """Set control enabled."""
        if not control:
            control = self._controls.keys()
        control_unchanged = []
        for ctrl in control:
            if ctrl in self._controls_disabled:
                self._controls[ctrl].rects = self._controls_disabled[ctrl].copy()
                #panel move - change rect pos or define controls
                del self._controls_disabled[ctrl]
                self._controls[ctrl].enabled = True
            else:
                control_unchanged.append(ctrl)
        return control_unchanged

    def disable_control(self, *control):
        """Set control disabled."""
        if not control:
            control = self._controls.keys()
        for ctrl in control:
            if not self._controls[ctrl].enabled:
                continue
            self._controls_disabled[ctrl] = self._controls[ctrl].rects.copy()
            self._controls[ctrl].rects = {}
            if self._controls[ctrl] is self._control_press['control']:
                self._control_press['control'] = None
            self._controls[ctrl].enabled = False

    def get_value(self, *control):
        """Retrieve current value of control. Multiple controls return a dictionary of values, and if no parameter given return dictionary of all values."""
        if not control:
            return self._control_values
        elif len(control) == 1:
            return self._control_values[control[0]]
        value = {}
        for ctrl in control:
            value[ctrl] = self._control_values[ctrl]
        return value

    def get_position(self):
        """Retrieve panel position."""
        return self._x, self._y

    def get_size(self):
        """Retrieve panel size."""
        return self._size

    def _zip_file(self, zip_file=None, close=False):
        """Retrieve zipfile object."""
        import zipfile
        if not close:
            if not zip_file:
                zip_file = self._data_zip
            if not self._zipfile:
                self._zipfile = zipfile.ZipFile(zip_file)
        else:
            self._zipfile.close()
            self._zipfile = None
        return self._zipfile

    def _data_source(self, data_folder=None, data_zip=None, color_key=None, file_obj=None):
        """Retrieve default data source."""
        if not file_obj:
            if data_folder is None:
                data_folder = self._data
            if data_zip is None and data_folder == self._data:
                if self._data_zip:
                    data_zip = self._zip_file()
        else:
            data_folder = data_zip = None
        if color_key is None:
            color_key = self._color_key
        return data_folder, data_zip, color_key

    def get_default_image(self, mode=None, path=None):
        """Get or save default images."""
        image = {}
        try:
            img_obj = self._default_image()
            for img in img_obj:
                if not img_obj[img]:
                    return image
            if mode == 'save':
                try:
                    for img in img_obj:
                        filename = '_'+img_obj[img][0]
                        if path:
                            filename = os.path.join(path, filename)
                        image_file = file(filename, 'w')
                        image_file.write(img_obj[img][1].read())
                        img_obj[img][1].seek(0)
                        image_file.close()
                except IOError:
                    pass
            image['panel_image'] = self.set_panel_image(img_obj['panel'][0], file_obj=img_obj['panel'][1])
            image['control_image'] = self.set_control_image(img_obj['control'][0], file_obj=img_obj['control'][1])
            image['button_image'] = self.set_button_image(img_obj['button'][0], file_obj=img_obj['button'][1])
        except IOError:
            pass
        return image

    def _default_image(self):
        """Set default images."""
        try:
            from image import _image_decode
            image_obj = _image_decode()
        except:
            image_obj = {}
            for img in ('panel', 'control', 'button'):
                image_obj[img] = ('none', None)
        return image_obj

    def _set_image(self, image, control_image, button_image):
        """Set panel, control and button images."""
        if Interface._image_default:
            if image == Interface._image_source['panel_image']:
                image = None
            if control_image == Interface._image_source['control_image']:
                control_image = None
            if button_image == Interface._image_source['button_image']:
                button_image = None
        default_image = {}
        if not Interface._image_default and (not image or not control_image or not button_image):
            img_obj = self._default_image()
            default_image = {}
            default_image['panel_image'] = self.set_panel_image(img_obj['panel'][0], file_obj=img_obj['panel'][1])
            default_image['control_image'] = self.set_control_image(img_obj['control'][0], file_obj=img_obj['control'][1])
            default_image['button_image'] = self.set_button_image(img_obj['button'][0], file_obj=img_obj['button'][1])
        if image:
            self._panel_image = self.set_panel_image(image)
        if control_image:
            self._control_image = self.set_control_image(control_image)
        if button_image:
            self._button_image = self.set_button_image(button_image)
        if not Interface._image_default:
            Interface._image_default = {}
            Interface._image_source = {}
            if image:
                default_image['panel_image'] = self._panel_image.copy()
            if control_image:
                default_image['control_image'] = self._control_image.copy()
            if button_image:
                default_image['button_image'] = self._button_image.copy()
            Interface._image_default = default_image
            Interface._image_source['panel_image'] = image
            Interface._image_source['control_image'] = control_image
            Interface._image_source['button_image'] = button_image
        if not image:
            self._panel_image = Interface._image_default['panel_image'].copy()
            if self._panel_image.get_size() != self._size:
                self._panel_image = engine.transform.smoothscale(self._panel_image, self._size)
            self.image = self._panel_image.copy()
            self.rect = self.image.get_rect(center=(self._x,self._y))
        if not control_image:
            self._control_image = Interface._image_default['control_image'].copy()
        if not button_image:
            self._button_image = Interface._image_default['button_image'].copy()

    def get_panel_image(self, change=False):
        """Get panel image to modify. Parameter Change - True: mod permanent, False: mod transitory."""
        if change:
            return self._panel_image
        else:
            return self.image

    def set_panel_image(self, image=None, data_folder=None, data_zip=None, file_obj=None, color_key=None, surface=None):
        """Set image used for panel."""
        if image:
            if isinstance(image, str):
                image = [image]
            if image[0] != 'none':
                data_folder, data_zip, color_key = self._data_source(data_folder, data_zip, color_key, file_obj)
                self._panel_image = self._load_image(image[0], path=data_folder, zipobj=data_zip, fileobj=file_obj, colorkey=color_key)
                if self._panel_image.get_size() != self._size:
                    self._panel_image = engine.transform.smoothscale(self._panel_image, self._size)
            else:
                self._panel_image = engine.Surface(self._size)
                self._panel_image.fill(self._color)
        elif surface:
            self._panel_image = surface.copy()
            if color_key:
                if color_key is -1:
                    color_key = self._panel_image.get_at((0,0))
                self._panel_image.set_colorkey(color_key, engine.RLEACCEL)
            if self._panel_image.get_size() != self._size:
                self._panel_image = engine.transform.smoothscale(self._panel_image, self._size) 
        else:
            self._panel_image = Interface._image_default['panel_image'].copy()
        self.image = self._panel_image.copy()
        self.rect = self.image.get_rect(center=(self._x,self._y))
        if self._initialized:
            self._display_controls()
        return self._panel_image

    def set_control_image(self, control_image=None, data_folder=None, data_zip=None, file_obj=None, color_key=None, surface=None):
        """Set image used for control."""
        if control_image:
            if isinstance(control_image, str):
                control_image = [control_image]
            if control_image[0] != 'none':
                data_folder, data_zip, color_key = self._data_source(data_folder, data_zip, color_key, file_obj)
                self._control_image['bg'] = self._load_image(control_image[0], path=data_folder, zipobj=data_zip, fileobj=file_obj, colorkey=color_key)
            else:
                if 'bg' in self._control_image:
                    del self._control_image['bg']
        elif surface:
            self._control_image['bg'] = surface.copy()
            if color_key:
                if color_key is -1:
                    color_key = self._control_image['bg'].get_at((0,0))
                self._control_image['bg'].set_colorkey(color_key, engine.RLEACCEL)
        else:
            try:
                self._control_image['bg'] = Interface._image_default['control_image']['bg'].copy()
            except:
                if 'bg' in self._control_image:
                    del self._control_image['bg']
        for ctrl in self._controls:
            if not self._control_image:
                self._controls[ctrl].control_outline = True
            else:
                self._controls[ctrl].control_outline = self._controls[ctrl].outline
            self._controls[ctrl]._set_buttonlist()
        if self._initialized:
            for ctrl in self._controls:
                self._controls[ctrl]._define_buttons(self._controls[ctrl].control_type, self._controls[ctrl].size, self._controls[ctrl].color['normal'], self._controls[ctrl].color['fill'], initialize=False)
            self._display_controls()
        return self._control_image

    def set_button_image(self, button_image=None, data_folder=None, data_zip=None, file_obj=None, color_key=None, surface=None):
        """Set image used for buttons."""
        if button_image:
            if isinstance(button_image, str):
                button_image = [button_image]
            if button_image[0] != 'none':
                data_folder, data_zip, color_key = self._data_source(data_folder, data_zip, color_key, file_obj)
                self._button_image = {}
                button_frames = 2
                if len(button_image) == 1:
                    images = self._load_image(button_image[0], button_frames, path=data_folder, zipobj=data_zip, fileobj=file_obj, colorkey=color_key)
                    self._button_image['t'] = engine.transform.smoothscale(images[0], self._button_size)
                    self._button_image['b'] = engine.transform.smoothscale(images[1], self._button_size)
                else:
                    for num, frame in enumerate(['t','b']):
                        img = self._load_image(button_image[num], path=data_folder, zipobj=data_zip, fileobj=file_obj, colorkey=color_key)
                        self._button_image[frame] = engine.transform.smoothscale(img, self._button_size)
            else:
                self._button_image = {}
        elif surface:
            for num, frame in enumerate(['t','b']):
                img = surface[num].copy()
                if color_key:
                    if color_key is -1:
                        color_key = img.get_at((0,0))
                    img.set_colorkey(color_key, engine.RLEACCEL)
                self._button_image[frame] = engine.transform.smoothscale(img, self._button_size)
        else:
            self._button_image = Interface._image_default['button_image'].copy()
        if self._initialized:
            for ctrl in self._controls:
                self._controls[ctrl]._define_buttons(self._controls[ctrl].control_type, self._controls[ctrl].size, self._controls[ctrl].color['normal'], self._controls[ctrl].color['fill'], initialize=False)
            self._display_controls()
        return self._button_image

    def get_clipboard(self):
        """Retrieve text from clipboard."""
        raise AttributeError, "clipboard unavailable"

    def set_clipboard(self, text):
        """Save text to clipboard."""
        raise AttributeError, "clipboard unavailable"

    def _clipboard_init(self):
        if not Interface._clipboard:
            try:
                from gtk import Clipboard
                Interface._clipboard = Clipboard()
                Interface._clipboard_type = 'gtk'
            except ImportError:
                try:
                    from Tkinter import Tk
                    Interface._clipboard = Tk()
                    Interface._clipboard.withdraw()
                    Interface._clipboard_type = 'tk'
                except ImportError:
                    try:
                        global StringSelection, DataFlavor, UnsupportedFlavorException, IOException, IllegalStateException
                        from java.awt.datatransfer import StringSelection, DataFlavor
                        from java.awt.datatransfer import UnsupportedFlavorException
                        from java.io import IOException
                        from java.lang import IllegalStateException
                        from java.awt import Toolkit
                        Interface._clipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
                        Interface._clipboard_type = 'jtk'
                    except ImportError:
                        try:
                            engine.display.textbox_init()
                            Interface._clipboard = engine.display.textarea
                            Interface._clipboard_type = 'js'
                        except AttributeError:
                            Interface._clipboard = None
                            Interface._clipboard_type = None
        if Interface._clipboard_type == 'gtk':
            self.get_clipboard = self._get_clipboard_gtk
            self.set_clipboard = self._set_clipboard_gtk
        elif Interface._clipboard_type == 'tk':
            self.get_clipboard = self._get_clipboard_tk
            self.set_clipboard = self._set_clipboard_tk
        elif Interface._clipboard_type == 'jtk':
            self.get_clipboard = self._get_clipboard_jtk
            self.set_clipboard = self._set_clipboard_jtk
        elif Interface._clipboard_type == 'js':
            self.get_clipboard = self._get_clipboard_js
            self.set_clipboard = self._set_clipboard_js

    def _get_clipboard_gtk(self):
        text = Interface._clipboard.wait_for_text()
        return text

    def _set_clipboard_gtk(self, text):
        Interface._clipboard.set_text(text)
        Interface._clipboard.store()
        return

    def _get_clipboard_tk(self):
        text = Interface._clipboard.clipboard_get()
        return text

    def _set_clipboard_tk(self, text):
        Interface._clipboard.clipboard_clear()
        Interface._clipboard.clipboard_append(text)

    def _get_clipboard_jtk(self):
        contents = Interface._clipboard.getContents(None)
        if contents != None:
            try:
                text = contents.getTransferData(DataFlavor.stringFlavor)
            except (UnsupportedFlavorException, IOException):
                text = None
        else:
            text = None
        return text

    def _set_clipboard_jtk(self, text):
        try:
            Interface._clipboard.setContents(StringSelection(text), None)
        except IllegalStateException:
            pass
        return

    def _get_clipboard_js(self):
        text = Interface._clipboard.getText()
        return text

    def _set_clipboard_js(self, text):
        Interface._clipboard.setText(text)
        return

    def is_active(self):
        """Check whether panel is active."""
        return self._active

    def is_moveable(self, setting=None):
        """Check whether panel is moveable."""
        if not setting:
            return self._moveable
        elif setting == 'Fixed':
            return self._display_fixed

    def set_moveable(self, setting='Toggle', position_offset=None, move_rate=None):
        """Set panel moveable setting."""
        if position_offset:
            self._offsetx, self._offsety = position_offset
        if move_rate:
            self._directionx, self._directiony = move_rate
        if setting == 'Toggle':
            self._moveable = not self._moveable
            return self._moveable
        elif setting in (True, False):
            self._moveable = setting
            return self._moveable
        elif setting == 'Fixed':
            self._display_fixed = not self._display_fixed
            return self._display_fixed
        else:
            return None

    def move(self, x, y):
        """Move panel to new position x,y."""
        self._x, self._y = x, y
        self._panel_rect.x = self._x-(self.width//2)
        self._panel_rect.y = self._y-(self.height//2)
        for ctrl in self._controls:
            control_type = self._controls[ctrl].control_type
            size = self._controls[ctrl].size
            color = self._controls[ctrl].color['normal']
            fill = self._controls[ctrl].color['fill']
            self._controls[ctrl].button, self._controls[ctrl].rects = self._controls[ctrl]._define_buttons(control_type, size, color, fill)
        self._update_panel = True

    def set_panel_display(self, setting='Toggle'):
        """Set whether panel display toggled with pointer interaction."""
        if setting == 'Toggle':
            self._panel_display = not self._panel_display
            return self._panel_display
        elif setting in (True, False):
            self._panel_display = setting
            return self._panel_display
        else:
            return None

    def is_info_display(self):
        """Check whether info is displayed."""
        return self._info_display

    def set_info_display(self, setting='Toggle'):
        """Set info display setting."""
        if setting == 'Toggle':
            self._info_display = not self._info_display
            return self._info_display
        elif setting in (True, False):
            self._info_display = setting
            return self._info_display
        else:
            return None

    def is_label_display(self):
        """Check whether label is displayed."""
        return self._label_display

    def set_label_display(self, setting='Toggle'):
        """Set label display setting."""
        if setting == 'Toggle':
            self._label_display = not self._label_display
            self._update_panel = True
            return self._label_display
        elif setting in (True, False):
            self._label_display = setting
            self._update_panel = True
            return self._label_display
        else:
            return None

    def is_tips_display(self):
        """Check whether tips are displayed."""
        return self._tips_display

    def set_tips_display(self, setting='Toggle'):
        """Set tips display setting."""
        if setting == 'Toggle':
            self._tips_display = not self._tips_display
            return self._tips_display
        elif setting in (True, False):
            self._tips_display = setting
            return self._tips_display
        else:
            return None

    def add_info(self, *message_append):
        """Add text to info."""
        self._info.add(*message_append)
        self._info_displaying = True

    def clear_info(self):
        """Clear text from info."""
        self._info.clear_text()

    def get_id(self):
        """Get panel identity"""
        return self._id

    def get_state(self):
        """Get the state object of the panel."""
        return self._interface['state']

    def set_update(self, sustain=False):
        """Set panel update. Parameter: sustain bool for continuous update, default False."""
        if not sustain:
            self._sustain_update = False
            if self._force_update not in self._panel_function:
                self._panel_function.append(self._force_update)
            self._update_panel = True
        else:
            self._sustain_update = True
            self._update_panel = True

    def is_update(self):
        """Check if panel was updated or set to sustained update."""
        if not self._sustain_update:
            return self._interface['update']
        else:
            return self._sustain_update

    def draw(self, surface):
        """Draw panel on surface. Return Rect of surface area changed."""
        rect = self._panel.draw(surface)
        return rect

    def clear(self, surface, background):
        """Clear panel from surface of previous draw, using background."""
        self._panel.clear(surface, background)
        return None

    def get_pointer_position(self):
        """Get position of pointer determined at latest update."""
        return self._pointer_position

    def set_pointer_interact(self, setting='Toggle'):
        """Set pointer interact monitoring."""
        if setting == 'Toggle':
            self._pointer_interact = not self._pointer_interact
            return self._pointer_interact
        elif setting in (True, False):
            self._pointer_interact = setting
            return self._pointer_interact
        else:
            return None

    def process_event(self, clear=False):
        """
        Internally process event handlers.
        Required if no call to framework event method such as event.get or event.pump.
        Optional clear argument to remove events from framework event queue.
        With scroll_button active, call panel update prior to framework event method calls.
        """
        if not clear:
            engine.event.pump()
        else:
            engine.event.clear()

    def get_event_queue(self):
        """
        Return interface event queue.
        Event queue has mouse press events sequestered upon panel interaction with scroll_button active.
        """
        return self._event_queue

    def move_control(self, control=None, position=None, offset=None):
        """Move selected control. If no position supplied, use position of mouse pointer."""
        if not control:
            if self._control_move:
                control = self._control_move
            else:
                return
        control = self.get_control(control)
        x, y = self.get_position()
        size = self.get_size()
        if not position:
            if not offset:
                mouse_x, mouse_y = self._pointer_position
                pos = mouse_x - x + (size[0]//2), mouse_y - y + (size[1]//2)
                pos = [pos[0]-(control.size[0]//2), pos[1]-(control.size[1]//2)]
            else:
                pos = [control.position[0]+offset[0], control.position[1]+offset[1]]
        else:
            pos = position[0], position[1]
            pos = [pos[0]-(control.size[0]//2), pos[1]-(control.size[1]//2)]
        ladj = 0
        radj = 0
        if control.control_type in self._button_placement:
            if self._button_placement[control.control_type] == 'left':
                ladj = 16
            elif self._button_placement[control.control_type] == 'right':
                radj = 16
        if pos[0] - ladj < 0:
            pos[0] = ladj
        elif pos[0]+control.size[0]+radj > size[0]:
            pos[0] = size[0]-(control.size[0]+radj)
        if pos[1] < 0:
            pos[1] = 0
        elif pos[1]+control.size[1] > size[1]:
            pos[1] = size[1]-control.size[1]
        pos = (pos[0], pos[1])
        dx, dy = pos[0]-control.position[0], pos[1]-control.position[1]
        control.position = pos
        control_type = control.control_type
        size = control.size
        color = control.color['normal']
        fill = control.color['fill']
        control._define_buttons(control_type, size, color, fill, initialize=False)
        for rect in control.rects:
            control.rects[rect].move_ip(dx,dy)
        width, height = control.display.check_size('x')
        pos = ( control.position[0]+(size[0]//2), control.position[1]+(size[1]//2)-(height//2) )
        control.display.set_position((pos),center=True)
        control.text_image = {}
        pos = ( control.position[0]+(size[0]//2), control.position[1]-(control.font_size+3) )
        control.label.set_position((pos),center=True)
        self._update_panel = True

    def set_control_move(self, control=None, mouse_visible=True):
        """Select control to move."""
        if control:
            self._control_move = control
            if not mouse_visible:
                engine.mouse.set_visible(False)
        else:
            self._control_move = None
            engine.mouse.set_visible(True)

    def get_control_move(self):
        """Return selected control to move."""
        return self._control_move

    def is_control_moveable(self):
        """Check whether control is moveable."""
        return self._control_moveable

    def set_control_moveable(self, setting='Toggle'):
        """Set control moveable."""
        if setting == 'Toggle':
            self._control_moveable = not self._control_moveable
            return self._control_moveable
        elif setting in (True, False):
            self._control_moveable = setting
            return self._control_moveable

    def _display_controls(self):
        """Draws controls on panel.""" 
        if self._panel_active:
            if not hasattr(self.image, 'clear'):
                self.image = self._panel_image.copy()
            else:
                self.image.clear()
                self.image.blit(self._panel_image, (0,0))
            for ctrl in self._controls:
                if self._controls[ctrl].active:
                    self.image = self._controls[ctrl]._display(self.image)
                    if self._label_display and self._controls[ctrl].label_display:
                        if not self._controls[ctrl].label_text.startswith('__'):
                            self._controls[ctrl].label.add(self._controls[ctrl].label_text)
                            self.image = self._controls[ctrl].label.render(self.image)
            if self._tips_display:
                if self._panel_interact:
                    mouse_x, mouse_y = self._pointer_position
                    if self._control_hover:
                        if not self._controls[self._control_hover].active or not self._controls[self._control_hover].rects[self._control_hover].collidepoint(mouse_x,mouse_y):
                            self._control_hover = None
                    if not self._control_hover:
                        for ctrl in self._controls:
                            if self._controls[ctrl].active:
                                if self._controls[ctrl].tips:
                                    try:
                                        if self._controls[ctrl].rects[ctrl].collidepoint(mouse_x,mouse_y):
                                            self._control_hover = ctrl
                                            break
                                    except:
                                        if not ctrl in self._controls_disabled:
                                            self._controls[ctrl].tips = None
                    try:
                        if self._control_hover:
                            if len(self._controls[self._control_hover].tips) == 1:
                                tip = self._controls[self._control_hover].tips[self._controls[self._control_hover].tips.keys()[0]]
                            else:
                                tip = self._controls[self._control_hover].tips[self._controls[self._control_hover].value]
                            pos = mouse_x-(self._x-(self._size[0]//2)), mouse_y-(self._y-(self._size[1]//2))
                            pos = pos[0]+self._tips_position[0], pos[1]+self._tips_position[1]
                            self._tips.set_position(pos, center=True)
                            self._tips.add(tip)
                            self.image = self._tips.render(self.image)
                    except:
                        pass
                else:
                    self._control_hover = None
            if self._info_display:
                if self._info_displaying:
                    if self._info.has_text():
                        self.image = self._info.render(self.image)
                    else:
                        self._info_displaying = False
            self.rect = self.image.get_rect(center=(self._x,self._y))

    def _display_update(self):
        """Update control panel on display."""
        if self._moveable:
            self._moveable_panel()
        if self._info_displaying:
            self._update_panel = True
        if self._control_event:
            for ctrl in self._control_event:
                if ctrl._check():
                    self._update_panel = True
            self._control_event[:] = []
        update, self._pointer_position = self._panel_interaction()
        self._panel_action()
        return update

    def _panel_action(self):
        for function in self._panel_function:
            try:
                function()
            except TypeError:   #pyjs -O function>unbound method
                function(self)

    def set_panel_function(self, function=None):
        """Add function to panel update list, call without function to delete list."""
        if function:
            self._panel_function.append(function)
        else:
            self._panel_function = []

    def _moveable_panel(self):
        """Update moveable panel."""
        def move_panel(pos_i, pos_f, z, z_dir, rate_x=0, rate_y=0):
            if not self._move_initiate:
                fps = self._clock.get_fps()
                self._move_ratex = int(self._directionx/fps)
                if not self._move_ratex:
                    self._move_ratex = 1
                self._move_ratey = int(self._directiony/fps)
                if not self._move_ratey:
                    self._move_ratey = 1
                self._move_initiate = True
            if rate_x:
                rate_x = rate_x*z_dir * z
                rate = rate_x
            else:
                rate_y = rate_y*z_dir * z
                rate = rate_y
            if abs(pos_i-pos_f) > abs(rate):
                self.rect.move_ip((rate_x, rate_y))
                pos_i += rate
                self._panel_disabled = True
            else:
                adj = abs(pos_i-pos_f)
                if rate_x:
                    rate_x = adj*z_dir * z
                else:
                    rate_y = adj*z_dir * z
                self.rect.move_ip((rate_x, rate_y))
                pos_i = pos_f
                self._panel_disabled = False
                self._move_initiate = False
            return pos_i
        if self._displayed or self._display_fixed:
            if self._offsetx:
                if self._x != self._positionx:
                    z = self._offsetx//abs(self._offsetx)
                    z_dir = -1
                    self._x = move_panel(self._x, self._positionx, z, z_dir, rate_x=self._move_ratex)
                    self._update_panel = True
            if self._offsety:
                if self._y != self._positiony:
                    z = self._offsety//abs(self._offsety)
                    z_dir = -1
                    self._y = move_panel(self._y, self._positiony, z, z_dir, rate_y=self._move_ratey)
                    self._update_panel = True
        else:
            if self._offsetx:
                if self._x != self._positionx+self._offsetx:
                    z = self._offsetx//abs(self._offsetx)
                    z_dir = 1
                    self._x = move_panel(self._x, self._positionx+self._offsetx, z, z_dir, rate_x=self._move_ratex)
                    self._update_panel = True
            if self._offsety:
                if self._y != self._positiony+self._offsety:
                    z = self._offsety//abs(self._offsety)
                    z_dir = 1
                    self._y = move_panel(self._y, self._positiony+self._offsety, z, z_dir, rate_y=self._move_ratey)
                    self._update_panel = True
        return self._panel_disabled

    def _panel_interaction(self):
        """Check for mouse interaction with panel."""
        self._pointer_position = engine.mouse.get_pos()
        if self._displayed:
            if not self.rect.collidepoint(self._pointer_position):
                self._panel_interact = False
                self._displayed = False
                if not self._panel_display:
                    if self._panel_active:
                        self._panel_active = False
                        self.image = self._panel_image.copy()
            else:
                self._panel_interact = True
        else:
            if self.rect.collidepoint(self._pointer_position):
                self._panel_interact = True
                self._panel_active = True
                self._displayed = True
        return self._panel_interact, self._pointer_position

    def _control_interact(self, pos):
        """Check control interaction."""
        if not self._displayed or not self._panel_active or self._panel_disabled:
            return None, None
        control_interact = None
        button_interact = None
        if self._tips_display:
            self._update_panel = True
            if self._control_hover:    #control interaction in tips display
                control_interact, button_interact = self._control_hover, self._control_hover
        else:
            if self._pointer_interact:     #detect pointer move interact
                self._update_panel = True
                for ctrl in self._controls:
                    if self._controls[ctrl].active:
                        for rect in self._controls[ctrl].rects:
                            if self._controls[ctrl].rects[rect].collidepoint(pos):
                                control_interact, button_interact = ctrl, rect
                                break
        return control_interact, button_interact

    def _control_scroll(self, pos, btn):
        for control in self._controls:
            if not self._controls[control].active or self._controls[control].control_type not in ['function_select', 'control_select', 'textbox']:
                continue
            for button in self._controls[control].rects:
                if button.endswith('_bg'):
                    continue
                if self._controls[control].rects[button].collidepoint(pos):
                    if not self._controls[control].listing[0][:-2] == '__numeric':  #TODO: encapsulate in control
                        return control, control+self._scroll_button_selected[btn]
                    else:
                        return control, control+self._scroll_button_selected_alt[btn]
        return None, None

    def _control_select(self, pos):
        """Check control selected."""
        if not self._displayed or not self._panel_active or self._panel_disabled:
            return None, None
        if not engine.mouse.get_pressed()[0]:
            if self._control_press['control']:
                self._control_press['control'] = None
            if self._scroll_button is None:
                return None, None
            else:
                self._event_queue[:] = engine.event.get(engine.MOUSEBUTTONDOWN)
                scroll_event = None
                for event in self._event_queue:
                    if event.button in self._scroll_button:
                        if not scroll_event:
                            scroll_event = event.button
                        else:
                            self._control_events += 1
                if scroll_event:
                    return self._control_scroll(pos, scroll_event)
                else:
                    return None, None
        control_select = None
        button_select = None
        if not self._control_press['control']:
            for control in self._controls:
                if not self._controls[control].active:
                    continue
                for button in self._controls[control].rects:
                    if button.endswith('_bg'):
                        continue
                    if self._controls[control].rects[button].collidepoint(pos):
                        self._control_press['control'] = self._controls[control]
                        self._control_press['button'] = button
                        self._control_press['hold'] = self._control_press['control'].hold_response
                        if self._control_press['control'].delay_response:
                            self._control_press['response'] = self._control_press['control'].delay_response
                            if self._control_press['hold']:
                                self._control_press['hold'] += self._control_press['control'].delay_response
                        else:
                            self._control_press['response'] = self._control_press['control'].control_response
                            control_select, button_select = control, button
                        self._control_press['rtime'] = self._control_press['htime'] = engine.time.get_ticks()
                        return control_select, button_select
        else:
            if self._control_press['control'].active:
                time = engine.time.get_ticks()
                if (time-self._control_press['rtime']) > self._control_press['response']:
                    self._control_press['rtime'] = engine.time.get_ticks()
                    control_select = self._control_press['control'].id
                    button_select = self._control_press['button']
                    if not self._control_press['hold'] or (time-self._control_press['htime']) < self._control_press['hold']:
                        self._control_press['response'] = self._control_press['control'].control_response
                    else:
                        self._control_press['response'] = self._control_press['control'].control_response_hold
            else:
                self._control_press['control'] = None
        return control_select, button_select

    def _interact(self):
        """Check for mouse interaction with controls."""
        control_interact, button_interact = self._control_interact(self._pointer_position)
        control_select, button_select = self._control_select(self._pointer_position)
        return control_interact, button_interact, control_select, button_select

    def _control_action(self, control, button):
        """Does control action, returns button pressed and current control value."""
        if button:
            if self._control_events == 1:
                button, value = self._controls[control]._action(button)
                return button, value
            else:
                for evt in range(self._control_events):
                    button, value = self._controls[control]._action(button)
                self._control_events = 1
                return button, value
        else:
            return None, None

    def panel_update(self, force_update=True):
        """Update control panel, determines interaction, does control action."""
        update = self._display_update()
        if update:
            control_interact, button_interact, control_select, button_select = self._interact()
            if control_select:
                button_select, value = self._control_action(control_select, button_select)
                self._update_panel = True
            else:
                button_select, value = None, None
        self._clock.tick()
        if force_update:
            self._update_panel = True
        if self._update_panel:
            self._display_controls()
            panel = self
            if update:
                self._interface['state'] = InterfaceState(panel, control_interact, button_interact, control_select, button_select, value)
                if control_select:
                    if self._controls[control_select].event:
                        engine.event.post(self._events['controlselect'])
                if control_interact:
                    if self._controls[control_interact].event:
                        engine.event.post(self._events['controlinteract'])
            else:
                self._interface['state'] = InterfaceState(panel)
            self._interface['update'] = True
            self._update_panel = False
        else:
            if self._interface['update']:
                panel = self
                self._interface['state'] = InterfaceState(panel)
                self._interface['update'] = False
            self._interface['state'].panel_interact = self._panel_interact
        return self._interface['state']

    def update(self):
        """Update control panel. If overriding in interface subclass, call Interface.update(self)."""
        interface_state = self.panel_update(0)
        return interface_state


class InterfaceState(object):
    """
    **State Object**

    * Attributes:
        * panel:              Interface panel
        * controls:           Interface controls
        * panel_active        Panel active
        * panel_update        Panel update
        * panel_interact:     Pointer interface interact
        * control_interact:   Pointer control interact
        * button_interact:    Pointer button interact
        * control:            Control selected
        * button:             Button selected
        * value:              Control value
        * values:             Panel control values
    
    State Object shows current state of control panel. The control_interact, button_interact register only with pointer_interact or tips_display. When control event is active, generates pygame event.type interphase.EVENT['controlselect'] and interphase.EVENT['controlinteract'] with attribute event.state.
    """

    __slots__ = [
        'panel',
        'controls',
        'panel_active',
        'panel_update',
        'panel_interact',
        'control_interact',
        'button_interact',
        'control',
        'button',
        'value',
        'values']

    def __init__(self,
        panel,
        control_interact=None,
        button_interact=None,
        control_select=None,
        button_select=None,
        value=None):
        self.panel = panel
        self.controls = panel._controls
        self.panel_active = panel._active
        self.panel_update = panel._update_panel
        self.panel_interact = panel._panel_interact
        self.control_interact = control_interact
        self.button_interact = button_interact
        self.control = control_select
        self.button = button_select
        self.value = value
        self.values = panel._control_values

