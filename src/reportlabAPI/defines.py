# -*- coding: utf-8 -*-
"""
    This is the module ``report_defines.py`` for report generation by 
    simulation in Typhoon HIL API in Python.
    
    Reserved to some value and text definitions for the report used in 
    ``Report_function.py`` module.

    Test Name: Modulation performance test
    
    Description: This test set evaluates the performance of modulation 
    algorithms for grid-tied inverters. The tests are performed in open-loop,
    where the grid is replaced by a variable RL load.
    
    @author: Grupo de Eletrônica de Potência e Controle (GEPOC);
             Tiarles Guterres (1°/2019)


    Modules tree:
    
    report_run (Top-Level)                
     | -> report_function
         | -> report_defines                <- This file
     | -> report_parameters              
     | -> simulation_functions
     | -> Interface_module
"""

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

import numpy as np

MSG_NOT_COMPLY = '<font color="red">Failed</font>'
MSG_COMPLY = '<font color="green">OK</font>'

### SIZES

width, height = A4

margins = {'right': 2.54*cm, 'left': 2.54*cm, 'top': 2.54*cm, 
           'bottom': 1.25*cm}
# efective width
ef_width  = np.floor(width - margins['left'] - margins['right']) 
# efective height
ef_height = np.floor(height - margins['top'] - margins['bottom']) 


### COLORS

darkblue = colors.Color(23.0/255,54.0/255,93.0/255)
blue = colors.Color(54.0/255,95.0/255,145.0/255)
lightblue = colors.Color(79.0/255,129.0/255,189.0/255)
grey = colors.Color(128.0/255,128.0/255,128.0/255)

### TEXT STYLE: used for wrapping  data on flowables

styles = getSampleStyleSheet()

normal_style = styles["BodyText"]
normal_style.alignment = TA_JUSTIFY
normal_style.wordWrap = 1
normal_style.fontName = 'Verdana'
normal_style.fontSize = 10
normal_style.firstLineIndent = 0
normal_style.leftIndent = 0
normal_style.leading = normal_style.fontSize*1.5
normal_style.spaceAfter = 0

normal_style_l = styles["BodyText"]
normal_style_l.alignment = TA_LEFT
normal_style_l.wordWrap = 1
normal_style_l.fontName = 'Verdana'
normal_style_l.fontSize = 10
normal_style_l.firstLineIndent = 0
normal_style_l.leftIndent = 0
normal_style_l.leading = normal_style.fontSize*1.5
normal_style_l.spaceAfter = 0

title_style = styles["Title"]
title_style.alignment = TA_LEFT
title_style.wordWrap = 1
title_style.fontName = 'Cambria'
title_style.fontSize = 26
title_style.firstLineIndent = 0
title_style.leftLineIndent = 0
title_style.leading = title_style.fontSize
title_style.spaceAfter = 0
title_style.spaceBefore = 0

title_1_style = styles["Heading1"]
title_1_style.alignment = TA_LEFT
title_1_style.wordWrap = 1
title_1_style.fontName = 'Cambria Bold'
title_1_style.fontSize = 16
title_1_style.firstLineIndent = 0
title_1_style.leftLineIndent = 0
title_1_style.leading = 0*title_1_style.fontSize
title_1_style.spaceAfter = 0
title_1_style.spaceBefore = 0

title_2_style = styles["Heading2"]
title_2_style.alignment = TA_LEFT
title_2_style.wordWrap = 1
title_2_style.fontName = 'Cambria'
title_2_style.fontSize = 14
title_2_style.firstLineIndent = 0
title_2_style.leftLineIndent = 0
title_2_style.leading = title_2_style.fontSize
title_2_style.spaceAfter = 10
title_2_style.spaceBefore = 0

v10_style = styles["Heading6"]
v10_style.alignment = TA_LEFT
v10_style.wordWrap = 1
v10_style.fontName = 'Verdana'
v10_style.fontSize = 10
v10_style.firstLineIndent = 0
v10_style.leftLineIndent = 0
v10_style.leading = v10_style.fontSize*1.5

c10_style = styles["Heading5"]
c10_style.alignment = TA_LEFT
c10_style.wordWrap = 1
c10_style.fontName = 'Verdana'
c10_style.fontSize = 10
c10_style.firstLineIndent = 0
c10_style.leftLineIndent = 0
c10_style.leading = c10_style.fontSize

djv10bi_style = styles["Heading4"]
djv10bi_style.alignment = TA_LEFT
djv10bi_style.wordWrap = 1
djv10bi_style.fontName = 'Dejavusans Bold Italic'
djv10bi_style.fontSize = 10
djv10bi_style.firstLineIndent = 0
djv10bi_style.leftLineIndent = 0
djv10bi_style.leading = djv10bi_style.fontSize

legend_style = styles["Heading3"]
legend_style.alignment = TA_CENTER
legend_style.wordWrap = 1
legend_style.fontName = 'Verdana'
legend_style.fontSize = 9
legend_style.firstLineIndent = 0
legend_style.leftLineIndent = 0
legend_style.leading = legend_style.fontSize

table_style = styles["Normal"]
table_style.alignment = TA_CENTER
table_style.wordWrap = 1
table_style.fontName = 'Verdana'
table_style.fontSize = 8
table_style.leading = 0.4*cm

#Table_style = styles["Normal"]
#Table_style.alignment = TA_CENTER
#Table_style.wordWrap = 1
#Table_style.fontName = 'Verdana'
#Table_style.fontSize = 8
#Table_style.leading = 0.4*cm
