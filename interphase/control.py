#Interphase - Copyright (C) 2009 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from __future__ import division
import os
from env import engine

__docformat__ = 'restructuredtext'


class Control(object):
    """
    **Control Object**
    
    The Control class provides the base control. To create Control instances, use the add() method of the Interface object, which should be passed the arguments that will be used to instantiate a control.
    
    Clicking on control with identity 'Control' generates a State Object with the control being 'Control', and button pressed being 'Control' for main button or 'Control_top' or 'Control_bottom' for switches. With the method add_action(), an action function can be attached to the control that will be called when pressed.
    """

    def __init__(self,
        panel,
        identity,
        control_type,
        position,
        size=None,
        color=(40,80,120),
        fill=1,
        control_outline=None,
        control_image=None,
        font_color=None,
        font_type=None,
        font_size=None,
        split_text=True,
        center_text=True,
        control_list=None,
        icon_list=None,
        icon_size=None,
        tip_list=None,
        link=None,
        link_activated=True,
        activated_color=(0,120,160),
        activated_toggle=True,
        label=None,
        label_display=True,
        active=True,
        control_response=None,
        hold_response=1000,
        delay_response=0,
        loop=False,
        reverse=False,
        control_button=True,
        text_margin=5,
        text_paste=False,
        event=None):
        """
        Control Object: Define panel control.

        Parameters:
        panel: obj panel holding control.
            - automatically set by panel add() method.
        identity: 'id' control name.
        control_type: 'type' control type.
            - 'function_select', 'function_toggle': master control.
            - 'control_select', 'control_toggle': standard control.
            - 'label': label control.
            - 'textbox': textbox control.
        position: (x,y) control placement on panel. Values < 1 are %panel.
        Optional parameters <default>:
        size: (w,h) control size override panel specified <None>.
            - 'auto', 'auto_width': fit items.
            - 'min', 'min_width': fit using control_minsize.
            - 'panel': use exact control_minsize.
        color: (r,g,b) control color <(40,80,120)>.
        fill: int button edge width, and 0 filled -1 none <1>.
        control_outline: display control edge <None>.
        control_image: 'image' control background image overrides panel <None>.
            - 'none' suppress image.
            - Image in data folder.
        font_color: (r,g,b) font color. Overrides panel <None>.
        font_type: [] font type list. Overrides panel <None>.
        font_size: int font size. Overrides panel <None>.
        split_text: bool split text at space to new line <True>.
        control_list: [] list held by control <None>.
            - numeric: [0] '__numeric', [1] (start,stop,step).
            - alpha: [0] '__alpha', [1] 'upper','lower','mixed'.
            - alphanumeric: [0] '__alphanumeric' in list[0], [1] 'upper','lower','mixed'.
            - filelist: [0] '__filelist', [1] path, [2] root, [3] ext.
            - 'item': Value listing. Leading '__' not display or display available icon.
        icon_list: [] control icons <None>.
            - replace '__item' in control_list - separate images or a composite image.
        icon_size: (w,h) control icon size <None>.
            - values < 1 are %control size.
            - default use control size.
        tip_list: [] tip list - single tip or multiple tip list <None>.
        link: [] function control link to activate other controls <None>.
        link_activated: bool function control link activated <True>.
        activated_color: (r,g,b) highlight color of activated control <(0,120,160)>.
        activated_toggle: bool control activated toggle <True>.
            - 'lock' for activate lock.
        label: '' supply label to replace 'id' text <None>.
        label_display: bool control label displayed <True>.
        active: bool control active state <True>.
        control_response: int control response (ms). Overrides panel <None>.
        hold_response: int hold (ms) before control response quicken <1000>.
            - 0 no response change.
        delay_response: int initial delay (ms) before control response <0>.
        loop: bool option list loop <False>.
        reverse: bool control switches reversed <False>.
        control_button: bool control switches displayed <True>.
        center_text: bool control text centered <True>.
        text_margin: int or (t,r,b,l) textbox margin <5>.
        text_paste: bool textbox copy/paste function <False>.
        event: bool interaction generates events. Overrides panel <None>.
        """
        self.id = identity      #control identity
        self.panel = panel      #panel holding control
        if control_type in ['function_select', 'function_toggle', 'control_select', 'control_toggle', 'label', 'textbox']:
            self.control_type = control_type    #functional type of control
        else:
            raise ValueError('Incorrect control type.')
        if self.control_type in ['function_select', 'control_select', 'textbox']:
            self.switches = control_button
        else:
            self.switches = False
        self.listing = []   #list item held by control
        self.place = 0      #current place in list
        if not control_list:
            control_list = []
        if not icon_list:
            icon_list = []
        if not tip_list:
            tip_list = []
        self.reverse = reverse
        if not self.reverse:
            self.button_forward = self.id+'_bottom'
            self.button_reverse = self.id+'_top'
        else:
            self.button_forward = self.id+'_top'
            self.button_reverse = self.id+'_bottom'
        if not size:
            self.size = self.panel._control_size
        else:
            self.size = size
        if self.size == 'min' and not self.panel._control_minsize:
            self.size = 'auto'
        if not font_color:
            self.font_color = self.panel._font_color
        else:
            self.font_color = font_color
        self.font_type = font_type
        if not font_size:
            if not self.control_type == 'textbox':
                self.font_size = self.panel._font_size
            else:
                self.font_size = 12
        else:
            self.font_size = font_size
        self.split_text = split_text
        if not self.control_type == 'textbox':
            self.center_text = center_text
        else:
            self.center_text = False
        self.list_type = ''     #list/_numeric...
        self.control_icon = {}
        self.icon_size = icon_size
        self.listing, self.value, self.control_icon, self.icon_size, self.size = self._set_listing(control_list, icon_list, self.size)
        pos_x, pos_y = position     #control position in panel
        if pos_x < 1:
            pos_x = int(pos_x*self.panel._size[0])
        if pos_y < 1:
            pos_y = int(pos_y*self.panel._size[1])
        pos_x, pos_y = pos_x - (self.size[0]//2), pos_y - (self.size[1]//2)
        self.position = int(pos_x), int(pos_y)
        self.display = self.set_display_info(self.size, self.font_color, self.font_type, self.font_size, center=self.center_text)
        self.label = self.set_label_info(self.size, self.font_color, self.font_type, self.font_size)
        if label:
            self.label_text = label
        else:
            self.label_text = self.id
        self.label_display = label_display
        self.tips = self._set_tips(tip_list)
        self.color = {'normal':color, 'activated':activated_color, 'fill':fill}
        self.active_color = self.color['normal']
        if activated_toggle == 'lock':
            self.activated_toggle = False
            self.activated_lock = True
        else:
            self.activated_toggle = activated_toggle
            self.activated_lock = False
        self.control_image = {}
        if control_image:
            self.set_control_image(control_image)
        else:
            if control_type != 'textbox':
                self.control_image = self.panel._control_image
        if control_outline is None:
            if not self.control_image:
                self.control_outline = True
            else:
                self.control_outline = False
        elif control_outline in (True, False):
            self.control_outline = control_outline
        self.outline = self.control_outline
        self.text_image = {}
        self.button, self.rects = self._define_buttons(self.control_type, self.size, color, fill)
        self.loop = loop    #listing loops back
        if control_response is not None:
            self.control_response = control_response
        else:
            self.control_response = self.panel._control_response
        self.hold_response_set = hold_response
        self.control_response_hold = 25
        self.delay_response = delay_response
        if self.listing:
            if ( (len(self.listing) > (self.hold_response_set//100)) or (self.listing[0][:-2] == '__numeric' and abs(self.numeric['h']-self.numeric['l']) > (self.hold_response_set//100)) ) and (self.control_response > self.control_response_hold):
                self.hold_response = self.hold_response_set      #response increase with hold
            else:
                self.hold_response = 0
        else:
            self.hold_response = 0
        if link:
            self.link = {}
            for item in self.listing:
                try:
                    self.link[item] = link.pop(0)
                except IndexError:
                    self.link[item] = []
        else:
            self.link = {}
        self.link_activated = link_activated
        self._function = lambda control,value:None      #control function
        self._functionObj = None
        if event is not None:
            self.event = event
        else:
            self.event = self.panel._event
        self.enabled = True
        self.activated = False
        self.active = active
        self.button_list = self._set_buttonlist()
        self.text_margin = {}
        try:
            self.text_margin['t'], self.text_margin['r'], self.text_margin['b'], self.text_margin['l'] = text_margin
        except TypeError:
            self.text_margin['t'] = self.text_margin['r'] = self.text_margin['b'] = self.text_margin['l'] = text_margin
        self._text_paste = text_paste
        self._initiate()

    def _initiate(self):
        pass

    def _define_buttons(self, control_type, size, color, fill, initialize=True):
        """Define control layout."""
        button = {}
        rects = {}
        if self.switches:
            x1, y1, x2, y2 = self._define_button_placement(control_type, size)
            if not self.control_image:
                button[self.id] = lambda: engine.draw.rect(self.panel.image, self.active_color, (self.position,size), fill)
            else:
                background = engine.transform.smoothscale(self.control_image['bg'], size)
                button[self.id+'_bg'] = lambda: self.panel.image.blit(background, self.position)
                button[self.id] = lambda: engine.draw.rect(self.panel.image, self.active_color, (self.position,size), fill)
            if not self.panel._button_image:
                button[self.id+'_top'] = lambda: engine.draw.polygon(self.panel.image, color, ((x1,y1-10),(x1-5,y1),(x1+5,y1)), fill)
            else:
                button[self.id+'_top'] = lambda: self.panel.image.blit(self.panel._button_image['t'], (x1-self.panel._button_size[0]//2,y1-self.panel._button_size[1]))
            if not self.panel._button_image:
                button[self.id+'_bottom'] = lambda: engine.draw.polygon(self.panel.image, color, ((x2,y2+10),(x2-5,y2),(x2+5,y2)), fill)
            else:
                button[self.id+'_bottom'] = lambda: self.panel.image.blit(self.panel._button_image['b'], (x2-self.panel._button_size[0]//2,y2))
        else:
            if not self.control_image:
                button[self.id] = lambda: engine.draw.rect(self.panel.image, self.active_color, (self.position,size), fill)
            else:
                background = engine.transform.smoothscale(self.control_image['bg'], size)
                button[self.id+'_bg'] = lambda: self.panel.image.blit(background, self.position)
                button[self.id] = lambda: engine.draw.rect(self.panel.image, self.active_color, (self.position,size), fill)
        self.button = button
        if initialize:
            button, rects = self._define_button_initialize(button)
            return button, rects

    def _define_button_placement(self, control_type, size):
        if self.panel._button_placement[control_type] == 'left':
            x, y = self.position
            x1 = x-(self.panel._button_size[0]//2+2)
            y1 = int(y+(0.25*size[1])+4)
            x2 = x-(self.panel._button_size[0]//2+2)
            y2 = int(y+(0.75*size[1])-4)
        elif self.panel._button_placement[control_type] == 'right':
            x, y = self.position
            x1 = x+size[0]+(self.panel._button_size[0]//2+2)
            y1 = int(y+(0.25*size[1])+4)
            x2 = x+size[0]+(self.panel._button_size[0]//2+2)
            y2 = int(y+(0.75*size[1])-4)
        return x1, y1, x2, y2

    def _define_button_initialize(self, button):
        rects = {}
        for btn in button:
            if btn not in self.panel._controls_disabled:
                offset_x, offset_y = self.panel._panel_rect[0], self.panel._panel_rect[1]
                rect = button[btn]()
                rect[0], rect[1] = rect[0] + offset_x, rect[1] + offset_y
                rects[btn] = rect
        return button, rects

    def _activate(self):
        pass

    def _display(self, image):
        for btn in self.button_list:
            rect = self.button[btn]()
        if self.list_type.startswith('__') or not self.value.startswith('__'):
            self.display.add(self.value)
            image = self.display.render(image)
        else:
            if self.control_icon:
                if self.value in self.control_icon:
                    x,y = self.position
                    size = self.size
                    isize = self.control_icon[self.value].get_size()
                    x += int( (size[0]-isize[0])/2 )
                    y += int( (size[1]-isize[1])/2 )
                    image.blit(self.control_icon[self.value], (x,y))
        return image

    def _set_listing(self, control_list=None, icon_list=None, size='auto', case=False, data_folder=None, data_zip=None, file_obj=None, color_key=None, surface=None):
        """Initiate control option list."""
        if not control_list:
            control_list = ['']
        if not icon_list and not surface:
            icon_list = []
        control_icon = {}
        icon_size = None
        self.value = ''
        self.place = 0
        if control_list:
            if control_list[0] == '__numeric':
                self.numeric = {}
                try:
                    if len(control_list[1]) == 1:
                        self.numeric['l'] = 0
                        self.numeric['h'] = control_list[1][0]
                        self.numeric['step'] = 1
                    elif len(control_list[1]) == 2:
                        self.numeric['l'] = control_list[1][0]
                        self.numeric['h'] = control_list[1][1]
                        self.numeric['step'] = 1
                    elif len(control_list[1]) == 3:
                        self.numeric['l'] = control_list[1][0]
                        self.numeric['h'] = control_list[1][1]
                        self.numeric['step'] = control_list[1][2]
                except IndexError:
                        self.numeric['l'] = 0
                        self.numeric['h'] = 100
                        self.numeric['step'] = 1
                numeric_type = 'integer'
                for num in ('l','h','step'):
                    if not isinstance(self.numeric[num], int):
                        numeric_type = 'float'
                        break
                if numeric_type == 'integer':
                    self.list_type = control_list[0]+'_i'
                    self.listing = [self.list_type]
                    self.numeric['value'] = str(self.numeric['l'])
                elif numeric_type == 'float':
                    self.list_type = control_list[0]+'_f'
                    self.listing = [self.list_type]
                    precision = 1
                    for num in ('l','h','step'):
                        self.numeric[num] = float(self.numeric[num])
                        fractional = len(str(self.numeric[num]).rsplit('.')[1])
                        if fractional > precision:
                            precision = fractional
                    self.numeric['precision'] = precision
                    integer, fractional = str(self.numeric['l']).rsplit('.')
                    fractional = fractional[:self.numeric['precision']]
                    self.numeric['value'] = integer + '.' + fractional
                if self.control_type[:8] == 'function':
                    self.control_type = 'control'+self.control_type[8:]
                if self.numeric['step'] > 0:
                    if not self.reverse:
                        self.button_forward = self.id+'_top'
                        self.button_reverse = self.id+'_bottom'
                    else:
                        self.button_forward = self.id+'_bottom'
                        self.button_reverse = self.id+'_top'
                else:
                    if not self.reverse:
                        self.button_forward = self.id+'_bottom'
                        self.button_reverse = self.id+'_top'
                    else:
                        self.button_forward = self.id+'_top'
                        self.button_reverse = self.id+'_bottom'
                self.value = self.numeric['l']
            elif control_list[0] == '__alpha':
                self.list_type = control_list[0]
                if not case:
                    try:
                        case = control_list[1]
                    except IndexError:
                        case = 'upper'
                if case == 'upper':
                    char = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                elif case == 'lower':
                    char = ' abcdefghijklmnopqrstuvwxyz'
                elif case == 'mixed':
                    char = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                self.listing = char
                self.value = self.listing[self.place]
            elif control_list[0] == '__alphanumeric':
                self.list_type = control_list[0]
                if not case:
                    try:
                        case = control_list[1]
                    except IndexError:
                        case = 'upper'
                if case == 'upper':
                    char = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                elif case == 'lower':
                    char = ' abcdefghijklmnopqrstuvwxyz0123456789'
                elif case == 'mixed':
                    char = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                self.listing = char
                self.value = self.listing[self.place]
            elif control_list[0] == '__filelist':
                self.list_type = control_list[0]
                try:
                    file_path = control_list[1]
                except IndexError:
                    file_path = None
                try:
                    file_root = control_list[2]
                except IndexError:
                    file_root = None
                try:
                    file_ext = control_list[3]
                except IndexError:
                    file_ext = None
                if not file_path:
                    file_path = os.curdir
                file_list = os.listdir(file_path)
                file_list = [item for item in file_list if os.path.isfile(os.path.join(file_path,item))]
                if file_root:
                    file_list = [item for item in file_list if item.startswith(file_root)]
                if file_ext:
                    file_list = [item for item in file_list if item.endswith(file_ext)]
                self.listing = file_list
                self.listing.sort()
                if self.listing:
                    self.value = self.listing[0]
                else:
                    self.listing.append('None')
                    self.value = 'None'
            else:
                self.list_type = 'list'
                for item in control_list:
                    self.listing.append(str(item))
                self.value = self.listing[self.place]
                if icon_list or surface:      #icon in listing
                    listing_icon = []
                    for item in self.listing:
                        if item.startswith('__'):
                            listing_icon.append(item)
                    if listing_icon:
                        control_icon = self._set_listing_icon(listing_icon, icon_list, data_folder, data_zip, file_obj, color_key, surface)
        self.panel._control_values[self.id] = self.value
        self.size, self.icon_size = self._set_control_size(self.listing, control_icon, size, self.font_size)
        if control_icon:
            self.control_icon = self._set_icon_size(control_icon, self.icon_size)
        return self.listing, self.value, self.control_icon, self.icon_size, self.size

    def _set_listing_icon(self, listing_icon, icon_list=None, data_folder=None, data_zip=None, file_obj=None, color_key=None, surface=None):
        """Set icons of control list."""
        if isinstance(icon_list, str):
            icon_list = [icon_list]
        control_icon = {}
        frames = len(listing_icon)
        if icon_list:
            data_folder, data_zip, color_key = self.panel._data_source(data_folder, data_zip, color_key, file_obj)
            if len(icon_list) == 1 and frames > 1:
                images = self.panel._load_image(icon_list[0], frames, path=data_folder, zipobj=data_zip, fileobj=file_obj, colorkey=color_key)
                for num, item in enumerate(listing_icon):
                    control_icon[item] = images[num]
            else:
                for num, item in enumerate(listing_icon):
                    img = self.panel._load_image(icon_list[num], path=data_folder, zipobj=data_zip, fileobj=file_obj, colorkey=color_key)
                    control_icon[item] = img
        elif surface:
            for num, item in enumerate(listing_icon):
                img = surface[num]
                if color_key:
                    if color_key is -1:
                        color_key = img.get_at((0,0))
                    img.set_colorkey(color_key, engine.RLEACCEL)
                control_icon[item] = img
        else:
            return None
        return control_icon

    def _set_icon_size(self, control_icon, size):
        """Resize icon to control dimension."""
        for icon in control_icon:
            width, height = control_icon[icon].get_size()
            if not (width == size[0] and height == size[1]):
                if width != size[0]:
                    w = size[0]
                    h = int( (w/width) * height )
                    if h > size[1]:
                        h = size[1]
                        w = int( (h/height) * width )
                elif height != size[1]:
                    h = size[1]
                    w = int( (h/height) * width )
                    if w > size[0]:
                        w = size[0]
                        h = int( (w/width) * height )
                control_icon[icon] = engine.transform.smoothscale(control_icon[icon], (w,h))
        return control_icon

    def _set_control_size(self, listing, control_icon, size, font_size):
        """Set control size."""
        if not isinstance(size, str):
            width, height = size
        elif size in ('auto', 'auto_width', 'min', 'min_width'):   #size adjusted to largest string
            if listing:
                text_display = self.panel._text(self.panel.image, self.font_type)
                text_display.set_font_size(font_size)
                if listing[0][:-2] != '__numeric':
                    lst = []
                    num_lines = 1
                    for item in listing:
                        if item.startswith('__'):
                            continue
                        item = str(item)
                        if self.split_text:
                            items = item.split(' ')
                            if len(items) > num_lines:
                                num_lines = len(items)
                            lst.extend(items)
                        else:
                            lst.append(item)
                    longest_string = 'x'
                    widest, height = text_display.check_size(longest_string)
                    for item in lst:
                        width, height = text_display.check_size(str(item))
                        if width > widest:
                            longest_string = item
                            widest = width
                    width, height = text_display.check_size(str(longest_string))
                    if num_lines > 1:
                        height = (height * num_lines) + (num_lines)
                else:
                    if len(str(self.numeric['h'])) > len(str(self.numeric['l'])):
                        longest_string = self.numeric['h']
                    else:
                        longest_string = self.numeric['l']
                    width, height = text_display.check_size(str(longest_string))
                if size in ('auto'):
                    if width > height:
                        dim = width
                    else:
                        dim = height
                    width, height = dim, dim
                elif size == 'min':
                    if self.panel._control_minsize:
                        minsize = self.panel._control_minsize
                        if width < minsize['min'][0]:
                            width = minsize['min'][0]
                        if height < minsize['min'][1]:
                            height = minsize['min'][1]
                        if width/height > minsize['size'][0]/minsize['size'][1]:
                            height = int( width * (minsize['size'][1]/minsize['size'][0]) )
                        else:
                            width = int( height * (minsize['size'][0]/minsize['size'][1]) )
                elif size == 'min_width':
                    if self.panel._control_minsize:
                        if self.panel._control_minsize['min'][0] > width:
                            width = self.panel._control_minsize['min'][0]
            else:
                if self.panel._control_minsize:
                    width, height = self.panel._control_minsize['min']
                else:
                    width, height = (20,20)
        else:
            if self.panel._control_minsize:
                width, height = self.panel._control_minsize['size']
            else:
                width, height = (20,20)
        if control_icon:
            if size in ('auto', 'auto_width'):
                w_max = h_max = 0
                for icon in control_icon:
                    icon_w, icon_h = control_icon[icon].get_size()
                    if icon_w > w_max:
                        w_max = icon_w
                    if icon_h > h_max:
                        h_max = icon_h
                icon_width, icon_height = w_max, h_max
                if icon_width > icon_height:
                    if icon_width > width:
                        change = icon_width-width
                        width += change
                        height += change
                else:
                    if icon_height > height:
                        change = icon_height-height
                        width += change
                        height += change
            else:
                icon_width, icon_height = width, height
        else:
            icon_width, icon_height = width, height
        if self.icon_size:
            if self.icon_size[0] > 1:
                icon_width, icon_height = int(self.icon_size[0]), int(self.icon_size[1])
                if size in ('auto', 'auto_width', 'min', 'min_width'):
                    if width < icon_width:
                        width = icon_width
                    if height < icon_height:
                        height = icon_height
                if size == 'min' and self.panel._control_minsize:
                    minsize = self.panel._control_minsize
                    if width/height > minsize['size'][0]/minsize['size'][1]:
                        height = int( width * (minsize['size'][1]/minsize['size'][0]) )
                    else:
                        width = int( height * (minsize['size'][0]/minsize['size'][1]) )
            else:
                icon_width, icon_height = int(width*self.icon_size[0]), int(height*self.icon_size[1])
                self.icon_size = None
        if size in ('min', 'min_width') and self.panel._control_minsize and width <= self.panel._control_minsize['min'][0]:
            padding = self.panel._control_minsize['pad']
        else:
            padding = ( min(width,height) // 10 ) + 4
            if padding % 2:
                padding -= 1
        if size in ('auto', 'auto_width', 'min', 'min_width'):
            width, height = width+padding, height+padding
        else:
            if not self.icon_size:
                if width > 10 and height > 10:
                    icon_width -= padding
                    icon_height -= padding
        size = width, height
        icon_size = icon_width, icon_height
        return size, icon_size

    def set_control_image(self, control_image=None, data_folder=None, data_zip=None, file_obj=None, color_key=None, surface=None):
        """Set image of control."""
        if control_image:
            if isinstance(control_image, str):
                control_image = [control_image]
            if control_image[0] != 'none':
                data_folder, data_zip, color_key = self.panel._data_source(data_folder, data_zip, color_key, file_obj)
                self.control_image['bg'] = self.panel._load_image(control_image[0], path=data_folder, zipobj=data_zip, fileobj=file_obj, colorkey=color_key)
            else:
                if 'bg' in self.control_image:
                    del self.control_image['bg']
        elif surface:
            self.control_image['bg'] = surface.copy()
            if color_key:
                if color_key is -1:
                    color_key = self.control_image['bg'].get_at((0,0))
                self.control_image['bg'].set_colorkey(color_key, engine.RLEACCEL)
        else:
            try:
                self.control_image['bg'] = self.panel._image_default['control_image']['bg'].copy()
            except:
                if 'bg' in self.control_image:
                    del self.control_image['bg']
        if self.panel._initialized:
            if not self.control_image:
                self.control_outline = True
            else:
                self.control_outline = self.outline
            self._set_buttonlist()
            self._define_buttons(self.control_type, self.size, self.color['normal'], self.color['fill'], initialize=False)
            self.panel._display_controls()
        return self.control_image

    def set_color(self, color=None, activated_color=None, fill=None):
        """Set control color."""
        if color:
            self.color['normal'] = color
        if activated_color:
            self.color['activated'] = activated_color
        if fill:
            self.color['fill'] = fill
        self._define_buttons(self.control_type, self.size, self.color['normal'], self.color['fill'], initialize=False)
        if not self.activated:
            self.active_color = self.color['normal']
        else:
            self.active_color = self.color['activated']
        self.panel._update_panel = True

    def _set_tips(self, tip_list=None):
        """Set tips of control list."""
        if tip_list:
            self.tips = {}
            if len(tip_list) == 1:
                self.tips[self.id] = tip_list[0]
            else:
                for item in self.listing:
                    try:
                        self.tips[item] = tip_list.pop(0)
                    except IndexError:
                        self.tips[item] = ''
        else:
            self.tips = {}
        return self.tips

    def set_list(self, control_list, icon_list=None, size=None, icon_size=None, case=False, data_folder=None, data_zip=None, file_obj=None, color_key=None, surface=None, append=False, index=None, keep_link=True, keep_tip=True):
        """Set control listing of a control."""
        if not control_list:
            return
        if not size:
            size = self.size
        if control_list[0] not in ('__numeric_i', '__numeric_f', '__alpha', '__alphanumeric', '__filelist'):
            if append:
                for item in control_list:
                    self.listing.append(str(item))
                self.value = self.listing[self.place]
                self.panel._control_values[self.id] = self.value
                for item in control_list:
                    if self.link:
                        if item not in self.link:
                            self.link[item] = []
                    if self.tips:
                        if item not in self.tips:
                            self.tips[item] = ''
                if icon_list or surface:      #icon in listing
                    listing_icon = []
                    for item in control_list:
                        if item.startswith('__'):
                            listing_icon.append(item)
                    if listing_icon:
                        control_icon = self._set_listing_icon(listing_icon, icon_list, data_folder, data_zip, file_obj, color_key, surface)
                        control_icon = self._set_icon_size(control_icon, self.icon_size)
                        for icon in control_icon:
                            self.control_icon[icon] = control_icon[icon]
            elif index is not None:
                item = str(control_list[0])
                self.listing[index] = item
                if index == self.place:
                    self.value = self.listing[self.place]
                    self.panel._control_values[self.id] = self.value
                if self.link:
                    if item not in self.link:
                        self.link[item] = []
                if self.tips:
                    if item not in self.tips:
                        self.tips[item] = ''
                if icon_list or surface:
                    listing_icon = []
                    if item.startswith('__'):
                        listing_icon.append(item)
                    if listing_icon:
                        control_icon = self._set_listing_icon(listing_icon, icon_list, data_folder, data_zip, file_obj, color_key, surface)
                        control_icon = self._set_icon_size(control_icon, self.icon_size)
                        for icon in control_icon:
                            self.control_icon[icon] = control_icon[icon]
            else:
                size_old = self.size
                pos_old = self.position[0]+self.size[0]//2, self.position[1]+self.size[1]//2
                place_old = self.place
                if not (set(control_list) & set(self.listing)):
                    keep_link = False
                    keep_tip = False
                self.size = size
                self.listing = []
                if keep_link:
                    if self.link:
                        link = self.link
                        self.link = {}
                        for item in control_list:
                            if item in link:
                                self.link[item] = link[item]
                            else:
                                self.link[item] = []
                else:
                    self.link = {}
                if keep_tip:
                    if self.tips:
                        if not ( len(self.tips) == 1 and self.id in self.tips ):
                            tips = self.tips
                            self.tips = {}
                            for item in control_list:
                                if item in tips:
                                    self.tips[item] = tips[item]
                                else:
                                    self.tips[item] = ''
                else:
                    self.tips = {}
                if icon_list or surface:
                    if not icon_size:
                        self.icon_size = None
                    else:
                        self.icon_size = icon_size
                self.listing, self.value, self.control_icon, self.icon_size, self.size = self._set_listing(control_list, icon_list, size, case, data_folder, data_zip, file_obj, color_key, surface)
                if self.size != size_old:
                    self.position = pos_old[0]-self.size[0]//2, pos_old[1]-self.size[1]//2
                    if not self.control_image:
                        self.control_outline = True
                    else:
                        self.control_outline = self.outline
                    self._set_buttonlist()
                    self.button, self.rects = self._define_buttons(self.control_type, self.size, self.color['normal'], self.color['fill'])
                try:
                    if self.place > len(self.listing):
                        self.place = len(self.listing)
                    else:
                        self.place = place_old
                    self.value = self.listing[self.place]
                    self.panel._control_values[self.id] = self.value
                except IndexError:
                    self.place = 0
                    self.value = ''
                    self.panel._control_values[self.id] = self.value
        else:
            self.listing = []
            self._set_listing(control_list, icon_list, size)
        if self.listing:
            if ( len(self.listing) > self.hold_response_set ) or ( self.listing[0][:-2] == '__numeric' and abs(self.numeric['h']-self.numeric['l']) > self.hold_response_set ):
                self.hold_response = self.hold_response_set
            else:
                self.hold_response = 0
        self.panel._update_panel = True

    def set_list_icon(self, control_list, icon_list=None, data_folder=None, data_zip=None, file_obj=None, color_key=None, surface=None, icon_size=None):
        """Set control listing icon of a control, changing if item in listing or appending new item."""
        for num, item in enumerate(control_list):
            if not item.startswith('__'):
                control_list[num] = '__'+control_list[num]
        control_icon = self._set_listing_icon(control_list, icon_list, data_folder, data_zip, file_obj, color_key, surface)
        if icon_size:
            if icon_size[0] > 1:
                icon_width, icon_height = int(icon_size[0]), int(icon_size[1])
            else:
                icon_width, icon_height = int(self.size[0]*icon_size[0]), int(self.size[0]*icon_size[1])
                if icon_width % 2:
                    icon_width += 1
                if icon_height % 2:
                    icon_height += 1
            icon_size = icon_width, icon_height
        else:
            icon_size = self.icon_size
        control_icon = self._set_icon_size(control_icon, icon_size)
        for icon in control_icon:
            self.control_icon[icon] = control_icon[icon]
        for item in control_list:
            if item not in self.listing:
                self.listing.append(str(item))
                if self.link:
                    if item not in self.link:
                        self.link[item] = []
                if self.tips:
                    if item not in self.tips:
                        self.tips[item] = ''
        self._define_buttons(self.control_type, self.size, self.color['normal'], self.color['fill'], initialize=False)
        self.panel._update_panel = True
        return control_icon

    def get_list(self):
        """Return control listing."""
        return self.listing[:]

    def remove_list(self, items=None, index=None):
        """Remove specified items (or item at index) from control listing, including corresponding tips and links. Passing no parameter removes complete control list."""
        if index is not None:
            item = self.listing[index]
            items = [item]
        elif items is None:
            items = self.listing[:]
        for item in items:
            if item in self.listing:
                self.listing.remove(item)
            if item in self.tips:
                del self.tips[item]
            if item in self.link:
                del self.link[item]
        try:
            if self.place > len(self.listing):
                self.place = len(self.listing)
            self.value = self.listing[self.place]
            self.panel._control_values[self.id] = self.value
        except IndexError:
            self.place = 0
            self.value = ''
            self.panel._control_values[self.id] = self.value
        self.panel._update_panel = True

    def set_label(self, label=None):
        """Set control label."""
        if label is None:
            self.label_text = ''
        else:
            self.label_text = label
        self.panel._update_panel = True

    def get_label(self):
        """Get control label."""
        return self.label_text

    def set_tip(self, *tip):
        """Set tip for a control item. Parameters: tip: str or [] - single control tip or tip list for control list items; or tuple item:str,tip:str tip for control list item."""
        tip_length = len(tip)
        if tip_length == 1:
            item = None
            tip = tip[0]
        elif tip_length == 2:
            item = tip[0]
            tip = tip[1]
        elif tip_length == 0:
            tip = 0
        else:
            raise TypeError('set_tip() arguments incorrect.')
        if tip:
            if isinstance(tip, str):
                tip = [tip]
            if item is not None:
                if item in self.listing:
                    if not self.tips:
                        for item in self.listing:
                            self.tips[item] = ''
                    self.tips[item] = tip[0]
                    return True
                else:
                    return False
            else:
                self._set_tips(tip)
                return True
        else:
            if self.tips:
                if item:
                    self.tips[item] = ''
                else:
                    self.tips = {}
            return True

    def get_tip(self, item=None):
        """Get the tip for a control item, or list of tips if no parameter given. Parameter: item:str"""
        if item:
            if item in self.tips:
                return self.tips[item]
            else:
                return None
        else:
            return self.tips

    def set_link(self, control, link):
        """Set linked controls. Parameters: control:str, link:[]."""
        if control in self.listing:
            if not self.link:
                for item in self.listing:
                    self.link[item] = []
            self.link[control] = link
            return True
        else:
            return False

    def set_link_activated(self, setting='Toggle'):
        """Set whether linked control active immediately or upon control button activation."""
        link_change = False
        if setting == 'Toggle':
            self.link_activated = not self.link_activated
            link_change = True
        elif setting in (True, False):
            self.link_activated = setting
            link_change = True
        if link_change:
            if self.control_type == 'function_select':
                self.check_link(self.id, True)
            return self.link_activated
        else:
            return None

    def add_action(self, function, obj=None):
        """Bind action function to control. Function should take two arguments, for instance Function(control, value), that will receive the control button pressed and control value. Optional obj argument to provide object for method binding in Pyjs -O mode."""
        self._function = function
        try:
            if obj and engine.env.pyjs_mode.optimized:
                self._functionObj = obj
        except AttributeError:
            pass
        return None

    def get_id(self):
        """Get control identity"""
        return self.id

    def get_position(self):
        """Retrieve control position."""
        pos_x, pos_y = self.position
        pos_x, pos_y = pos_x + (self.size[0]//2), pos_y + (self.size[1]//2)
        return pos_x, pos_y

    def get_size(self):
        """Retrieve control size."""
        return self.size

    def set_text_margin(self, margin):
        """Set text margin. Parameter: margin int or (t,r,b,l)."""
        try:
            self.text_margin['t'], self.text_margin['r'], self.text_margin['b'], self.text_margin['l'] = margin
        except TypeError:
            self.text_margin['t'] = self.text_margin['r'] = self.text_margin['b'] = self.text_margin['l'] = margin
        self.display.set_margin(margin)
        try:
            self.line_max = self.set_line_max()
        except:
            pass

    def get_text_margin(self):
        """Get text margin. Return [t,r,b,l]."""
        return [self.text_margin['t'], self.text_margin['r'], self.text_margin['b'], self.text_margin['l']]

    def is_activated(self):
        """Check whether control is activated."""
        return self.activated

    def set_activated(self, setting='Toggle'):
        """Set control activated."""
        change = False
        if setting == 'Toggle':
            self.activated = not self.activated
            change = True
        elif setting in (True, False):
            self.activated = setting
            change = True
        if change:
            if self.link and not self.link_activated:
                for button in self.link[self.value]:
                    self.panel._controls[button].active = self.activated
            if not self.activated:
                self.active_color = self.color['normal']
            else:
                self.active_color = self.color['activated']
            self.panel._update_panel = True
            return self.activated
        else:
            return None

    def is_activated_lock(self):
        """Check control activate lock."""
        return self.activated_lock

    def set_activated_lock(self, setting='Toggle'):
        """Set control activate lock."""
        if setting == 'Toggle':
            self.activated_lock = not self.activated_lock
        elif setting in (True, False):
            self.activated_lock = setting
        self.activated_toggle = not self.activated_lock
        self.panel._update_panel = True
        return self.activated_lock

    def set_value(self, value, change_index=True):
        """Set the value of a control. Parameters: value - control value; change_index - True change list index to first available value, False to leave index position unchanged, index number for specific index if is value."""
        self.check_link(self.id, False)
        if self.list_type[:9] != '__numeric':
            self.value = str(value)
        else:
            if self.list_type[9:] == '_i':
                try:
                    value = int(value)
                    self.value = value
                    self.numeric['value'] = str(self.value)
                except ValueError:
                    self.value = value
                    change_index = False
            else:
                try:
                    value = round(float(value),self.numeric['precision'])
                    self.value = value
                    self.numeric['value'] = str(self.value)
                except ValueError:
                    self.value = value
                    change_index = False
        self.panel._control_values[self.id] = self.value
        if change_index is not False:
            if change_index is True:
                if value in self.listing:
                    self.place = self.listing.index(value)
            else:
                try:
                    if self.listing[change_index] == self.value:
                        self.place = change_index
                except IndexError:
                    pass
        if self.is_active():
            self.check_link(self.id, True)
        self.panel._update_panel = True
        return self.value, self.place

    def get_value(self):
        """Get the value of a control."""
        return self.value

    def set_list_index(self, index):
        """Set the place in control listing."""
        if self.list_type[:9] != '__numeric':
            if index >= 0 and index < len(self.listing):
                self.place = index
                self.set_value(self.listing[self.place], change_index=False)
        else:
            self.set_value(index)
        return self.value

    def get_list_index(self, item=None):
        """Get the current place in control listing, or index of first occurrence of item."""
        if self.list_type[:9] != '__numeric':
            if item is None:
                return self.place
            else:
                try:
                    index = self.listing.index(item)
                    return index
                except ValueError:
                    return None
        else:
            return self.value

    def is_active(self):
        """Check whether a control is active."""
        return self.active

    def set_active(self, setting='Toggle'):
        """Set control active setting."""
        if setting == 'Toggle':
            self.active = not self.active
            self.panel._update_panel = True
            return self.active
        elif setting in (True, False):
            self.active = setting
            self.panel._update_panel = True
            return self.active
        else:
            return None

    def is_enabled(self):
        """Check whether control is enabled."""
        return self.enabled

    def set_enabled(self, setting='Toggle'):
        """Set control enabled setting."""
        if setting == 'Toggle':
            if not self.enabled:
                self.panel.enable_control(self.id)
            else:
                self.panel.disable_control(self.id)
            return self.enabled
        elif setting in (True, False):
            if setting:
                self.panel.enable_control(self.id)
            else:
                self.panel.disable_control(self.id)
            return self.enabled
        else:
            return None

    def _set_buttonlist(self):
        """List specifying button members of a control. Designations for control 'id': main button:'id', button switches:'id_top'/'id_bottom'."""
        self.button_list = []
        if self.control_image:
            self.button_list.append(self.id+'_bg')
            if self.control_outline:
                self.button_list.append(self.id)
        else:
            if self.control_outline:
                self.button_list.append(self.id)
        if self.switches:
            self.button_list.extend([self.id+'_top', self.id+'_bottom'])
        return self.button_list

    def resize_control(self, size):
        """Resize control."""
        self.icon_size = None
        pos_old = self.position[0]+self.size[0]//2, self.position[1]+self.size[1]//2
        self.size, self.icon_size = self._set_control_size(self.listing, self.control_icon, size, self.font_size)
        if self.control_icon:
            self.control_icon = self._set_icon_size(self.control_icon, self.icon_size)
        self.position = pos_old[0]-self.size[0]//2, pos_old[1]-self.size[1]//2
        self.button, self.rects = self._define_buttons(self.control_type, self.size, self.color['normal'], self.color['fill'])
        label_size = self.label.get_font_size()
        label_position = ( self.position[0]+(self.size[0]//2), self.position[1]-(label_size+3) )
        self.label.set_position(label_position,center=True)
        self.panel._update_panel = True

    def set_display_info(self, size, font_color, font_type, font_size, position=None, text=None, center=True):
        """Initiate control display text."""
        if text:    #set display text
            self.value = text
            self.panel._control_values[self.id] = self.value
        display = self.panel._text(self.panel.image, font_type)
        display.set_font_size(font_size)
        display.set_font_color(font_color)
        display.set_font_bgcolor(None)
        display.split_text = self.split_text
        if center:
            display.set_text_alignment('center')
        else:
            display.set_text_alignment('left')
        if not position:
            if center:
                width, height = display.check_size('x')
                position = ( self.position[0]+(size[0]//2), self.position[1]+(size[1]//2)-(height//2) )
            else:
                position = self.position
        display.set_position(position)
        return display

    def set_display_text(self, font_color=None, font_bgcolor=None, font_type=None, font_size=None, split_text=None, size=None, info=False):
        """Set display text properties."""
        update_control = False
        if font_color:
            self.font_color = font_color
            self.display.set_font_color(self.font_color)
        if font_bgcolor:
            self.display.set_font_bgcolor(font_bgcolor)
        if font_type:
            if isinstance(font_type, str):
                font_type = [font_type]
            self.display.set_font(font_type)
            update_control=True
        if font_size:
            self.font_size = font_size
            self.display.set_font_size(self.font_size)
            update_control = True
        if split_text is not None:
            self.split_text = split_text
            self.display.set_split_text(self.split_text)
            update_control = True
        if update_control:
            if not size:
                size = self.size
            self.icon_size = None
            pos_old = self.position[0]+self.size[0]//2, self.position[1]+self.size[1]//2
            self.size, self.icon_size = self._set_control_size(self.listing, self.control_icon, size, self.font_size)
            if self.control_icon:
                self.control_icon = self._set_icon_size(self.control_icon, self.icon_size)
            self.position = pos_old[0]-self.size[0]//2, pos_old[1]-self.size[1]//2
            self.button, self.rects = self._define_buttons(self.control_type, self.size, self.color['normal'], self.color['fill'])
            width, height = self.display.check_size('x')
            position = ( self.position[0]+(self.size[0]//2), self.position[1]+(self.size[1]//2)-(height//2) )
            self.display.set_position(position,center=True)
            label_size = self.label.get_font_size()
            label_position = ( self.position[0]+(self.size[0]//2), self.position[1]-(label_size+3) )
            self.label.set_position(label_position,center=True)
        self.panel._update_panel = True
        if info:
            if info == 'font':
                return self.display.get_font()
            elif info == 'default':
                return self.display.get_font('default')
            elif info == 'system':
                return self.display.get_font('system')

    def get_display_text(self):
        """Get display text object."""
        return self.display

    def set_label_info(self, size, font_color, font_type, font_size, position=None, text=None):
        """Initiate control label text."""
        if text:    #set label text
            self.label_text = text
            return
        label = self.panel._text(self.panel.image, font_type)
        label.set_font_size(font_size)
        label.set_font_color(font_color)
        label.set_font_bgcolor(None)
        if self.control_type == 'label':
            label.set_position((self.position[0], self.position[1]-(font_size+3)),center=True)
            return label
        if not position:
            position = ( self.position[0]+(size[0]//2), self.position[1]-(font_size+3) )
        if not text:
            text = self.id
        label.set_position(position,center=True)
        return label

    def set_label_text(self, font_color=None, font_bgcolor=None, font_type=None, font_size=None, split_text=None):
        """Set label text properties."""
        update_position = False
        if font_color:
            self.label.set_font_color(font_color)
        if font_bgcolor:
            self.label.set_font_bgcolor(font_bgcolor)
        if font_type:
            if isinstance(font_type, str):
                font_type = [font_type]
            self.label.set_font(font_type)
        if font_size:
            self.label.set_font_size(font_size)
            update_position = True
        if split_text is not None:
            self.label.set_split_text(split_text)
            update_position = True
        if update_position:
            if self.label.split_text and self.label_text.count(' '):
                num_lines = len(self.label_text.split(' '))
                self.label.y = self.position[1]-(((self.label.font_size-2)*num_lines)+2)
            else:
                self.label.y = self.position[1]-(self.label.font_size+2)
        self.panel._update_panel = True

    def check_link(self, ctrl, activate):
        """Maintain active state of linked controls."""
        control = self.panel._controls[ctrl]
        if control.link:
            if not activate:
                for ctr in control.link[control.value]:
                    self.panel._controls[ctr].set_active(False)
                    if not self.panel._controls[ctr].is_activated_lock():
                        self.panel._controls[ctr].set_activated(False)
                    self.check_link(ctr, activate)
            else:
                if (control.control_type == 'function_select' and control.link_activated) or control.control_type == 'function_toggle':
                    for ctr in control.link[control.value]:
                        self.panel._controls[ctr].set_active(True)
                        self.check_link(ctr, activate)
                else:
                    for ctr in control.link[control.value]:
                        self.panel._controls[ctr].set_active(control.activated)
                        self.check_link(ctr, control.activated)

    def _check(self):
        if self.activated and self.activated_toggle:
            self.activated = False
            self.active_color = self.color['normal']
            return True
        else:
            return False

    def reset(self, change_index=True):
        """Reset value to start of control list."""
        if self.list_type[:9] == '__numeric':
            if change_index:
                self.value = self.numeric['l']
            else:
                if self.listing[0][-1] == 'i':
                    self.value = int(self.numeric['value'])
                else:
                    self.value = float(self.numeric['value'])
            self.panel._control_values[self.id] = self.value
        else:
            self.check_link(self.id, False)
            if change_index:
                self.place = 0
            self.value = self.listing[self.place]
            self.panel._control_values[self.id] = self.value
            if self.is_active():
                self.check_link(self.id, True)
        self.panel._update_panel = True
        return self.value

    def next(self):
        """Set value to next in control list."""
        if self.list_type[:9] == '__numeric':
            self._action(self.button_forward)
        else:
            self.check_link(self.id, False)
            if self.place < len(self.listing)-1:
                self.place += 1
            else:
                self.place = 0
            self.value = self.listing[self.place]
            self.panel._control_values[self.id] = self.value
            if self.is_active():
                self.check_link(self.id, True)
        self.panel._update_panel = True
        return self.value

    def previous(self):
        """Set value to previous in control list."""
        if self.list_type[:9] == '__numeric':
            self._action(self.button_reverse)
        else:
            self.check_link(self.id, False)
            if self.place > 0:
                self.place -= 1
            else:
                self.place = len(self.listing)-1
            self.value = self.listing[self.place]
            self.panel._control_values[self.id] = self.value
            if self.is_active():
                self.check_link(self.id, True)
        self.panel._update_panel = True
        return self.value

    def _action_numeric_i(self, button):
        """Function of integer numeric control."""
        def greater(val1, val2, direction=1):
            if val1 > val2:
                return direction >= 0
            else:
                return not (direction >= 0)
        if button == self.id:
            self.activated = not self.activated
        elif button == self.button_forward:
            self.activated = False
            self.value += self.numeric['step']
            if greater(self.value, self.numeric['h'], self.numeric['step']) and self.value != self.numeric['h']:
                if self.loop:
                    self.value = self.numeric['l']
                else:
                    self.value = self.numeric['h']
            self.numeric['value'] = str(self.value)
        elif button == self.button_reverse:
            self.activated = False
            self.value -= self.numeric['step']
            if not greater(self.value, self.numeric['l'], self.numeric['step']) and self.value != self.numeric['l']:
                if self.loop:
                    self.value = self.numeric['h']
                else:
                    self.value = self.numeric['l']
            self.numeric['value'] = str(self.value)

    def _action_numeric_f(self, button):
        """Function of float numeric control."""
        self._action_numeric_i(button)
        self.value = round(self.value, self.numeric['precision'])
        integer, fractional = str(self.value).rsplit('.')
        fractional = fractional[:self.numeric['precision']]
        self.numeric['value'] = integer + '.' + fractional

    def _action(self, button):
        """Function of control."""
        if self.switches:
            if self.listing:
                if self.listing[0][:-2] == '__numeric':
                    if self.listing[0][-1] == 'i':
                        self._action_numeric_i(button)
                    else:
                        self._action_numeric_f(button)
                else:
                    if button == self.id:
                        self.activated = not self.activated
                        self.value = self.listing[self.place]
                    elif button == self.button_forward:
                        self.activated = False
                        if self.place < len(self.listing)-1:
                            self.place += 1
                        else:
                            if self.loop:
                                self.place = 0
                            else:
                                self.place = len(self.listing)-1
                        self.value = self.listing[self.place]
                    elif button == self.button_reverse:
                        self.activated = False
                        if self.place > 0:
                            self.place -= 1
                        else:
                            if self.loop:
                                self.place = len(self.listing)-1
                            else:
                                self.place = 0
                        self.value = self.listing[self.place]
        else:
            if self.listing[0][:-2] == '__numeric':
                if button == self.id:
                    button = self.button_forward
                { 'i':self._action_numeric_i,'f':self._action_numeric_f }[self.listing[0][-1]](button)
            else:
                if button == self.id:
                    self.activated = not self.activated
                    if self.place < len(self.listing)-1:
                        self.place += 1
                    else:
                        self.place = 0
                self.value = self.listing[self.place]
        if not self.activated:
            self.active_color = self.color['normal']
        else:
            self.active_color = self.color['activated']
        self.panel._control_values[self.id] = self.value
        if not self._functionObj:
            self._function(button, self.value)
        else:   #pyjs -O function>unbound method
            engine.util.call(self._functionObj, self._function, (button,self.value))
        self.panel._control_event.append(self)
        self.panel._update_panel = True
        return button, self.value


class FunctionControl(Control):
    """
    **FunctionControl Object**

    The FunctionControl class is a Control subclass. The class has extended features including the function to link other controls to its various values, allowing to build complex interface panels.
    """

    def _activate(self):
        for item in self.link:
            for ctr in self.link[item]:
                self.panel._controls[ctr].set_active(False)
        if self.active and self.link_activated:
            for function in self.link:
                for link in self.link[function]:
                    if link in self.link[self.value]:
                        self.panel._controls[link].check_link(self.id, True)

    def _action(self, button):
        """Function of control."""
        if self.switches:
            if button == self.id:
                self.activated = not self.activated
                self.check_link(self.id, self.activated)
            elif button == self.button_forward:
                self.activated = False
                self.check_link(self.id, False)
                if self.place < len(self.listing)-1:
                    self.place += 1
                else:
                    if self.loop:
                        self.place = 0
                    else:
                        self.place = len(self.listing)-1
                self.value = self.listing[self.place]
                self.check_link(self.id, True)
            elif button == self.button_reverse:
                self.activated = False
                self.check_link(self.id, False)
                if self.place > 0:
                    self.place -= 1
                else:
                    if self.loop:
                        self.place = len(self.listing)-1
                    else:
                        self.place = 0
                self.value = self.listing[self.place]
                self.check_link(self.id, True)
        else:
            if button == self.id:
                self.check_link(self.id, False)
                self.activated = not self.activated
                if self.place < len(self.listing)-1:
                    self.place += 1
                else:
                    self.place = 0
                self.value = self.listing[self.place]
                self.check_link(self.id, True)
        if not self.activated:
            self.active_color = self.color['normal']
        else:
            self.active_color = self.color['activated']
        self.panel._control_values[self.id] = self.value
        if not self._functionObj:
            self._function(button, self.value)
        else:   #pyjs -O function>unbound method
            engine.util.call(self._functionObj, self._function, (button,self.value))
        self.panel._control_event.append(self)
        self.panel._update_panel = True
        return button, self.value


class Label(Control):
    """
    **Label Object**

    The Label class is a Control subclass that provides a simple label.
    """

    def _define_buttons(self, control_type, size, color, fill, initialize=True):
        """Define control layout."""
        button = {}
        rects = {}
        button[self.id] = lambda:None
        self.button = button
        if initialize:
            return button, rects

    def _set_buttonlist(self):
        """List specifying button members of a control. Designations for control 'id': main button:'id', button switches:'id_top'/'id_bottom'."""
        self.button_list = []
        return self.button_list

    def set_display_info(self, size, font_color, font_type, font_size, position=None, text=None, center=True):
        """Initiate control display text."""
        if text:    #set display text
            self.value = text
            self.panel._control_values[self.id] = self.value
        display = self.panel._text(self.panel.image, font_type)
        display.set_font_size(font_size)
        display.set_font_color(font_color)
        display.set_font_bgcolor(None)
        display.set_position(self.position,center=True)
        return display


class Textbox(Control):
    """
    **Textbox Object**

    The Textbox class is a Control subclass. The control value can be set to a long text string, which can be scrolled. The text applied will undergo formating that includes wordwrap, and custom format methods can be linked in with the add_format method.
    
    If the clipboard is enabled with the Control parameter text_paste, the control can use the copy and paste feature with the mouse while holding SHIFT and CTRL. The clipboard functionality in Pyjsdl handled by pyjsdl.display.textarea displayed by textarea.toggle(). For a control of identity 'Control', the clipboard access results in reporting in the InterfaceState object as button 'Control_copy' and 'Control_paste'.
    """

    def _initiate(self):
        self.display.set_multiline()
        if self._text_paste:
            self.panel._clipboard_init()
        self.display.set_position((0,0))
        if self.text_margin:
            margin = [self.text_margin['t'], self.text_margin['r'], self.text_margin['b'], self.text_margin['l']]
            self.display.set_margin(margin)
        self.line_max = self.set_line_max()
        self.line_width = self.size[0]
        self.line_pos = 0
        self.scroll_line = 1
        self.hold_response = self.hold_response_set
        self.image = engine.Surface(self.size, engine.SRCALPHA)
        self.change = True
        self._format_function = []
        self._formatObj = None
        self._format_splitlines = True
        self._format_wordwrap = True
        self.text = self.format_text()

    def format_text(self):
        """Format text to display in textbox. Format include splitting text into lines, apply custom format functions, then wordwrap to fit in textbox."""
        text = self.get_value()
        if self._format_splitlines:
            text = [line for line in text.splitlines()]
        if not self._formatObj:
            for func in self._format_function:
                text = func(text)
        else:   #pyjs -O function>unbound method
            for func in self._format_function:
                text = engine.util.call(self._formatObj, func, (text,))
        if self._format_wordwrap:
            text = self.display.word_wrap(text, self.line_width)
        self.text = text
        return self.text

    def add_format(self, function, obj=None):
        """Custom format functions. Parameter function is a list of functions that will be applied to text formatting. The functions should receive a text argument, and return the formated text. Passing string 'splitlines', 'nosplitlines', 'wordwrap', 'nowordwrap' will modify standard format procedure. Optional obj argument to provide object for method binding in Pyjs -O mode."""
        func = []
        for fn in function:
            if fn == 'splitlines':
                self._format_splitlines = True
            elif fn == 'wordwrap':
                self._format_wordwrap = True
            elif fn == 'nosplitlines':
                self._format_splitlines = False
            elif fn == 'nowordwrap':
                self._format_wordwrap = False
            else:
                func.append(fn)
        self._format_function = func
        try:
            if obj and engine.env.pyjs_mode.optimized:
                self._formatObj = obj
        except AttributeError:
            pass

    def set_line_max(self, line=None):
        """Set max lines of textbox. Optional line parameter."""
        if line is None:
            box_size = self.size[1] - (self.text_margin['t']+self.text_margin['b']) + 2
            self.line_max = box_size // self.display.linesize
        else:
            self.line_max = line
        return self.line_max

    def get_line_max(self):
        """Get max lines of textbox."""
        return self.line_max

    def set_line_width(self, width=None):
        """Set width of line, margin included. If width is None, reset to textbox width."""
        if width is None:
            self.line_width = self.size[0]
        else:
            self.line_width = width

    def get_line_width(self):
        """Get line width."""
        return self.line_width

    def check_size(self, text):
        """Get size required for given text."""
        width, height = self.display.check_size(text)
        return width, height

    def get_size(self, *text):
        """Get size of textbox. Optional parameter (col,row) to return estimated width for col and height for row, adjusted for margins."""
        if not text:
            return self.size
        else:
            return self.display.surface_size(*text)

    def resize_control(self, size):
        """Resize control."""
        pos_old = self.position[0]+self.size[0]//2, self.position[1]+self.size[1]//2
        self.size = size
        self.position = pos_old[0]-self.size[0]//2, pos_old[1]-self.size[1]//2
        self.button, self.rects = self._define_buttons(self.control_type, self.size, self.color['normal'], self.color['fill'])
        label_size = self.label.get_font_size()
        label_position = ( self.position[0]+(self.size[0]//2), self.position[1]-(label_size+3) )
        self.label.set_position(label_position,center=True)
        self.image = engine.Surface(self.size, engine.SRCALPHA)
        self.line_max = self.set_line_max()
        self.line_width = self.size[0]
        self.text = self.format_text()
        self.change = True
        self.panel._update_panel = True

    def _display(self, image):
        for btn in self.button_list:
            rect = self.button[btn]()
        if self.change:
            for line in self.text[self.line_pos:self.line_pos+self.line_max]:
                self.display.add(line)
            if not self.control_image:
                self.image.fill(self.color['normal'])
                self.image = self.display.render(self.image)
            else:
                if not hasattr(self.image, 'clear'):
                    self.image = self.display.render(engine.Surface(self.size, engine.SRCALPHA))
                else:
                    self.image.clear()
                    self.image = self.display.render(self.image)
            self.change = False
        image.blit(self.image, self.position)
        return image

    def set_value(self, value):
        """Set the value of a control. Parameters: value - control value."""
        self.check_link(self.id, False)
        self.value = str(value)
        self.panel._control_values[self.id] = self.value
        self.line_pos = 0
        self.change = True
        self.text = self.format_text()
        if self.is_active():
            self.check_link(self.id, True)
        self.panel._update_panel = True
        return self.value

    def get_value(self, format_text=False):
        """Get the value of a control. Parameter: format_text bool to retrieve formatted text list rather than nonformatted text string, defaults to False."""
        if not format_text:
            return self.value
        else:
            return self.text

    def text_copy(self):
        """Copy text to clipboard."""
        try:
            text = self.get_value()
            if text:
                self.panel.set_clipboard(text)
        except:
            text = None
        return text

    def text_paste(self):
        """Paste text from clipboard."""
        try:
            text = self.panel.get_clipboard()
        except:
            text = None
        if text:
            self.set_value(text)
        return text

    def _action(self, button):
        """Function of control."""
        if button == self.button_forward:
            self.next()
        elif button == self.button_reverse:
            self.previous()
        elif button == self.id:
            mods = engine.key.get_mods()
            if mods & engine.KMOD_CTRL:
                if self._text_paste:
                    try:
                        text = self.panel.get_clipboard()
                    except:
                        text = None
                    if text:
                        self.set_value(text)
                        button = self.id + '_paste'
            elif mods & engine.KMOD_SHIFT:
                if self._text_paste:
                    try:
                        value = self.get_value()
                        if value:
                            self.panel.set_clipboard(value)
                            button = self.id + '_copy'
                    except:
                        pass
        self._function(button, self.value)
        self.panel._update_panel = True
        return button, self.value

    def set_scroll_line(self, line):
        """Set number of line to scroll."""
        self.scroll_line = line
        return None

    def get_text(self, display=False):
        """Get formated text lines. Parameter: display set to True to get lines currently showing, defaults to False to get all text lines."""
        if not display:
            return self.text
        else:
            return self.text[self.line_pos:self.line_pos+self.line_max]

    def next(self, line=None):
        """Scroll text forward. Parameter: line to scroll, defaults to one line."""
        if line is None:
            line = self.scroll_line
        self.line_pos += line
        if self.line_pos > len(self.text)-self.line_max:
            self.line_pos = len(self.text)-self.line_max
        self.change = True
        self.panel._update_panel = True
        return self.text[self.line_pos:self.line_pos+self.line_max]

    def previous(self, line=None):
        """Scroll text reverse. Parameter: line to scroll, defaults to one line."""
        if line is None:
            line = self.scroll_line
        self.line_pos -= line
        if self.line_pos < 0:
            self.line_pos = 0
        self.change = True
        self.panel._update_panel = True
        return self.text[self.line_pos:self.line_pos+self.line_max]

