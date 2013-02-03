# Script to convert Font-Awesome icons into iOS tab bar icons
# -----------------------------------------------------------
# Copyright (c) 2012, Daniel Tse
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# The views and conclusions contained in the software and documentation are those
# of the authors.

import os
import re
import errno

def parse_names(css_fn):
    with file(css_fn, 'r') as css_file:
        css_text = css_file.read()
        matches = re.findall(r'.icon-([^:]+):before\s+{\s*content: "\\([^"]+)"', css_text, re.MULTILINE)
        return dict(
            (int(codepoint_string, 16), icon_name) for (icon_name, codepoint_string) in matches
        )

codepoints_to_names = parse_names(os.path.join('css', 'font-awesome.css'))
font_path = os.path.join(os.getcwd(), 'font', 'fontawesome-webfont.ttf')

def codepoint_to_name(codepoint):
    return codepoints_to_names.get(codepoint, None)

min_codepoint = min(codepoints_to_names.keys())
max_codepoint = max(codepoints_to_names.keys())

# xrange endpoint is not inclusive
for d in xrange(min_codepoint, max_codepoint + 1):
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
        
    for (icon_height, output_file_suffix) in ( ('50', '@2x'), ('25', '') ):
        os.system(r'''convert -background none -size x54 \
       -font %(fontpath)s \
       -pointsize 72 -gravity North label:'@ch-%(icon_name)s' \
       -resize x%(icon_height)s \
       %(output_file)s''' % {
        'fontpath': font_path,
        'icon_name': icon_name,
        'icon_height': icon_height,
        'output_file': os.path.join("png", "icon-%s%s.png" % (icon_name, output_file_suffix))
        })
             
    os.remove(codepoint_text_file)
