import os
import re
import errno

def parse_names(css_fn):
    with file(css_fn, 'r') as css_file:
        css_text = css_file.read()
        matches = re.findall(r'.icon-([^:]+):before {\n\s*content: "\\([^"]+)"', css_text, re.MULTILINE)
        return dict(
            (int(codepoint_string, 16), icon_name) for (icon_name, codepoint_string) in matches
        )

codepoints_to_names = parse_names(os.path.join('css', 'font-awesome.css'))
font_path = os.path.join(os.getcwd(), 'font', 'fontawesome-webfont.ttf')

def codepoint_to_name(codepoint):
    return codepoints_to_names.get(codepoint, None)

for d in xrange(0xf000, 0xf094, 1):
    icon_name = codepoint_to_name(d)
    if icon_name is None: continue
    
    codepoint_text_file = 'ch-%s' % icon_name
    
    try:
        os.makedirs('png')
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else: raise
    
    with file(codepoint_text_file, 'w') as f:
        print >>f, unichr(d).encode('u8')
    os.system('''convert -background none -size x54 \\
   -font %(fontpath)s \\
   -pointsize 72 -gravity North label:'@ch-%(icon_name)s' \\
   %(output_file)s''' % {
    'fontpath': font_path,
    'icon_name': icon_name,
    'output_file': os.path.join("png", "icon-%s@2x.png" % icon_name)
    })
    os.system('''convert -background none -size x54 \\
    -font %(fontpath)s \\
    -pointsize 72 -gravity North label:'@ch-%(icon_name)s' \\
    -resize 50%% \\
    %(output_file)s''' % {
     'fontpath': font_path,
    'icon_name': icon_name,
    'output_file': os.path.join("png", "icon-%s.png" % icon_name)
     })
     
    os.remove(codepoint_text_file)