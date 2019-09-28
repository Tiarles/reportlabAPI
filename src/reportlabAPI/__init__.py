# -*- coding: utf-8 -*-

"""  
    This is the main file of xxx
    
    Test Name: xxx
    
    Description: xxx
    
    @author: Tiarles Guterres, Henrique Magnago, Henrique Jank 

"""

# Import's

import datetime
#import tempfile
import os  
#import reportlab 
import numpy as np

import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Paragraph, Flowable, PageTemplate, Frame, \
BaseDocTemplate, NextPageTemplate, Spacer, PageBreak, TableStyle, Table
from reportlab.lib.sequencer import Sequencer
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import white

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

## Part 1 of Definitions

from reportlabAPI.defines import title_1_style, ef_width, ef_height, djv10bi_style, \
margins, height, normal_style, width, grey, c10_style, blue, \
legend_style, title_2_style, v10_style, lightblue, table_style, darkblue, \
title_style, MSG_NOT_COMPLY, MSG_COMPLY, normal_style_l

MSG_NOT_COMPLY = MSG_NOT_COMPLY
MSG_COMPLY = MSG_COMPLY

# Part 2 of Definitions

folder_inputs = './input/' # Folder for inputs

folder_figures = folder_inputs + 'figures_docs/'

from zipfile import ZipFile

pathFontsZip = os.path.realpath(__file__).replace('__init__.py', 'fonts.zip')
pathFontsExtract = os.path.realpath(__file__).replace('__init__.py', '')

with ZipFile(pathFontsZip, 'r') as fzip:
    fzip.extractall(pathFontsExtract)

folder_fonts = os.path.realpath(__file__).replace('__init__.py', 'fonts\\')

pdfmetrics.registerFont(TTFont("Cambria", folder_fonts+'Cambria.ttf'))
pdfmetrics.registerFont(TTFont("Cambria Bold", folder_fonts+'Cambria Bold.ttf'))
pdfmetrics.registerFont(TTFont("Cambria Italic", folder_fonts+'Cambria Italic.ttf'))
pdfmetrics.registerFont(TTFont("Cambria Bold Italic", folder_fonts+'Cambria Bold \
Italic.ttf'))
pdfmetrics.registerFont(TTFont("Verdana", folder_fonts+'Verdana.ttf'))
pdfmetrics.registerFont(TTFont("Verdana Bold", folder_fonts+'Verdana Bold.ttf'))
pdfmetrics.registerFont(TTFont("Verdana Italic", folder_fonts+'Verdana Italic.ttf'))
pdfmetrics.registerFont(TTFont("Verdana Bold Italic", folder_fonts+'Verdana Bold \
Italic.ttf'))
pdfmetrics.registerFont(TTFont("Dejavusans", folder_fonts+'Dejavusans.ttf'))
pdfmetrics.registerFont(TTFont("Dejavusans Bold", folder_fonts+'Dejavusans Bold.ttf'))
pdfmetrics.registerFont(TTFont("Dejavusans Italic", folder_fonts+'Dejavusans Italic.ttf'))
pdfmetrics.registerFont(TTFont("Dejavusans Bold Italic", folder_fonts+'Dejavusans Bold \
Italic.ttf'))

# plt.rc('font',family='Verdana');
# plt.rcParams['grid.color'] = 'k';
# plt.rcParams['grid.linestyle'] = ':';
# plt.rcParams['grid.linewidth'] = 0.5;
# #plt.rcParams['figure.dpi'] = dpi;
# plt.rcParams['figure.figsize'] = [15.5/2.54, 9.5/2.54];
# plt.rcParams['font.size'] = 10;
# plt.rcParams['legend.fontsize'] = 10
# plt.rcParams['axes.titlesize'] = 10
# plt.rc('xtick', labelsize = 10)
# plt.rc('ytick', labelsize = 10);
# plt.rcParams['legend.fontsize'] = 10;
# plt.rcParams['figure.titlesize'] = 10;
# plt.rcParams['legend.fancybox'] = True;
# plt.rcParams['legend.loc'] = 'upper right';
# plt.rcParams['legend.numpoints'] = 2;
# plt.rcParams['legend.framealpha'] = None;
# plt.rcParams['legend.scatterpoints'] = 3;
# plt.rcParams['legend.edgecolor'] = 'inherit'

figwidth = 15.5*cm
figheigth = 9.5*cm
def reset_indexes():
    # Reset indexes
    _ = Paragraph('Figure <seqreset id = "figure"/> - ',legend_style)
    _ = Paragraph('Equation (<seqreset id = "equation"/>) - ', legend_style)
    _ = Paragraph('Table <seqreset id = "table"/> - ', table_style)
    _ = Paragraph('<font color = "{color}">{txt}</font>'.\
        format(color = white, txt = '<seqreset id = "chapter"/>   ' + '' + '<seqreset id="subchapter"/>'),
            title_1_style)

reset_indexes()

year =  str(datetime.date.today().strftime("%Y"))
month = str(datetime.date.today().strftime("%m"))
day = str(datetime.date.today().strftime("%d"))
now = datetime.datetime.now()
date = month + "." + day +'.' + year
time = ('%02d' % now.hour) + ':' + ('%02d' % now.minute)
#%% Classes

class PdfImage(Flowable):
    '''
    PdfImage wraps the first page from a PDF file as a Flowable.
    which can be included into a ReportLab Platypus document.
    Based on the vectorpdf extension in rst2pdf 
    (http://code.google.com/p/rst2pdf/)
    '''

    def __init__(self, filename_or_object, width=None, height=None, kind='direct'):
#        from reportlab.lib.units import inch
        # If using StringIO buffer, set pointer to begining
        if hasattr(filename_or_object, 'read'):
            filename_or_object.seek(0)
        page = PdfReader(filename_or_object, decompress=False).pages[0]
        self.xobj = pagexobj(page)
        self.imageWidth = width
        self.imageHeight = height
        x1, y1, x2, y2 = self.xobj.BBox

        self._w, self._h = x2 - x1, y2 - y1
        if not self.imageWidth:
            self.imageWidth = self._w
        if not self.imageHeight:
            self.imageHeight = self._h
        self.__ratio = float(self.imageWidth)/self.imageHeight
        if kind in ['direct','absolute'] or width==None or height==None:
            self.drawWidth = width or self.imageWidth
            self.drawHeight = height or self.imageHeight
        elif kind in ['bound','proportional']:
            factor = min(float(width)/self._w,float(height)/self._h)
            self.drawWidth = self._w*factor
            self.drawHeight = self._h*factor

    def wrap(self, aW, aH):
        return self.drawWidth, self.drawHeight

    def drawOn(self, canv, x, y, _sW=0):
        if _sW > 0 and hasattr(self, 'hAlign'):
            a = self.hAlign
            if a in ('CENTER', 'CENTRE', TA_CENTER):
                x += 0.5*_sW
            elif a in ('RIGHT', TA_RIGHT):
                x += _sW
            elif a not in ('LEFT', TA_LEFT):
                raise ValueError("Bad hAlign value " + str(a))

        xobj = self.xobj
        xobj_name = makerl(canv._doc, xobj)

        xscale = self.drawWidth/self._w
        yscale = self.drawHeight/self._h

        x -= xobj.BBox[0] * xscale
        y -= xobj.BBox[1] * yscale

        canv.saveState()
        canv.translate(x, y)
        canv.scale(xscale, yscale)
        canv.doForm(xobj_name)
        canv.restoreState()


class OneColumnTemplate(PageTemplate):
    '''
        Heir of the class PageTemplate from reportlab.platypus is a type of 
        PDF page inserted in report an used in the RLDocTemplate class.
    '''

    def __init__(self, id, pageSize = A4):
        self.pageWidth = pageSize[0]
        self.pageHeight = pageSize[1]
        self.pageWidth = pageSize[0]
        self.pageHeight = pageSize[1]
        frame2 = Frame(2.54*cm,
                       1.25*cm,
                       self.pageWidth - 2*2.54*cm,
                       self.pageHeight - 2.54*cm - 1.25*cm - (title_1_style.fontSize*2), id = 'Normal')
        PageTemplate.__init__(self, id, [frame2])  # note lack of onPage
        
    def afterDrawPage(self, canvas, doc):
        canvas.saveState()

        txt = 'Test report'
        ptxt = Paragraph('<font color = "{color}">{txt}</font>'.format(color = grey, txt = txt),c10_style)
        ptxt.wrapOn(canvas, ef_width, ef_height)
        ptxt_width = ptxt.getActualLineWidths0()
        y = height - 1.5*cm - c10_style.leading
        x = width - margins['right'] - np.max(ptxt_width)
        ptxt.drawOn(canvas, x, y)

        txt = Test_Name
        ptxt = Paragraph('<font color = "{color}">{txt}</font>'.format(color = blue, txt = txt),djv10bi_style)
        ptxt.wrapOn(canvas, ef_width, ef_height)
        y = height - 1.5*cm - djv10bi_style.leading
        x = margins['left']
        ptxt.drawOn(canvas, x, y)

        txt = 'www.typhoon-hil.com'
        ptxt = Paragraph('<font color = "{color}">{txt}</font>'.format(color = blue, txt = txt),normal_style)
        ptxt.wrapOn(canvas, ef_width, ef_height)
        ptxt_width = ptxt.getActualLineWidths0()
        y = margins['bottom'] - normal_style.leading
        x = 0.5*width - 0.5*np.max(ptxt_width)
        ptxt.drawOn(canvas, x, y)

        pg_num = canvas.getPageNumber()
        txt = str(pg_num)
        ptxt = Paragraph('<font color = "{color}">{txt}</font>'.format(color = grey, txt = txt),normal_style)
        ptxt.wrapOn(canvas, ef_width, ef_height)
        y = margins['bottom'] - normal_style.leading
        x = width - margins['right'] - 10
        ptxt.drawOn(canvas, x, y)
        
        chapter_title = doc.chapter
        txt = str(chapter_title)
        ptxt = Paragraph('<font color = "{color}">{txt}</font>'.format(color = blue, txt = txt),title_1_style)
        ptxt.wrapOn(canvas, ef_width, ef_height)
        y = height - margins['top'] - 0.5*title_1_style.fontSize
        x = margins['left']
        ptxt.drawOn(canvas, x, y)

        y = height - margins['top'] - 2*title_1_style.fontSize
        x1 = margins['left']
        x2 = width - margins['right']
        canvas.setLineWidth(0.5)
        canvas.line(x1,y,x2,y)

        y = margins['bottom']
        x1 = margins['left']
        x2 = width - margins['right']
        canvas.setStrokeColorRGB(128.0/255,128.0/255,128.0/255)
        canvas.setLineWidth(0.5)
        canvas.line(x1,y,x2,y)

        canvas.restoreState()

 
class Credits(PageTemplate):
    '''
        Heir of the class PageTemplate from reportlab.platypus is a type of 
        PDF page inserted in report an used in the RLDocTemplate class.
    '''
    global logo_width, logo_height
    logo_height = 2.4*cm
    logo_width = 8.9*cm
    def __init__(self, id, pageSize = A4):
        self.pageWidth = pageSize[0]
        self.pageHeight = pageSize[1]
        self.pageWidth = pageSize[0]
        self.pageHeight = pageSize[1]
        frame3 = Frame(2.54*cm,
                       1.25*cm,
                       self.pageWidth - 2*2.54*cm,
                       self.pageHeight - 2.54*cm - 1.25*cm  - 1.75*cm - (title_1_style.fontSize*2) - logo_height, id = 'Credits')
        PageTemplate.__init__(self, id, [frame3])  # note lack of onPage
        
    def afterDrawPage(self, canvas, doc):
        canvas.saveState()

        txt = 'Test report'
        ptxt = Paragraph('<font color = "{color}">{txt}</font>'.format(color = grey, txt = txt),c10_style)
        ptxt.wrapOn(canvas, ef_width, ef_height)
        ptxt_width = ptxt.getActualLineWidths0()
        y = height - 1.5*cm - c10_style.leading
        x = width - margins['right'] - np.max(ptxt_width)
        ptxt.drawOn(canvas, x, y)

        txt = Test_Name
        ptxt = Paragraph('<font color = "{color}">{txt}</font>'.format(color = blue, txt = txt),djv10bi_style)
        ptxt.wrapOn(canvas, ef_width, ef_height)
        y = height - 1.5*cm - djv10bi_style.leading
        x = margins['left']
        ptxt.drawOn(canvas, x, y)

        txt = 'www.typhoon-hil.com'
        ptxt = Paragraph('<font color = "{color}">{txt}</font>'.format(color = blue, txt = txt),normal_style)
        ptxt.wrapOn(canvas, ef_width, ef_height)
        ptxt_width = ptxt.getActualLineWidths0()
        y = margins['bottom'] - normal_style.leading
        x = 0.5*width - 0.5*np.max(ptxt_width)
        ptxt.drawOn(canvas, x, y)

        pg_num = canvas.getPageNumber()
        txt = str(pg_num)
        ptxt = Paragraph('<font color = "{color}">{txt}</font>'.format(color = grey, txt = txt),normal_style)
        ptxt.wrapOn(canvas, ef_width, ef_height)
        y = margins['bottom'] - normal_style.leading
        x = width - margins['right'] - 10
        ptxt.drawOn(canvas, x, y)
        
        chapter_title = doc.chapter
        txt = str(chapter_title)
        ptxt = Paragraph('<font color = "{color}">{txt}</font>'.format(color = blue, txt = txt),title_1_style)
        ptxt.wrapOn(canvas, ef_width, ef_height)
        y = height - margins['top'] - 0.5*title_1_style.fontSize
        x = margins['left']
        ptxt.drawOn(canvas, x, y)

        y = height - margins['top'] - 2*title_1_style.fontSize
        x1 = margins['left']
        x2 = width - margins['right']
        canvas.setLineWidth(0.5)
        canvas.line(x1,y,x2,y)

        y = margins['bottom']
        x1 = margins['left']
        x2 = width - margins['right']
        canvas.setStrokeColorRGB(128.0/255,128.0/255,128.0/255)
        canvas.setLineWidth(0.5)
        canvas.line(x1,y,x2,y)

        from reportlab.platypus import Image
#        logo = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logo1.png')
        logo = os.path.realpath(__file__).replace('__init__.py', 'logo1.png')
        
        I = Image(logo)
        I.drawHeight = logo_height
        I.drawWidth = logo_width
        x = margins['right'] + (ef_width-logo_width)/2.0
        y = self.pageHeight - 2.54*cm - 1.25*cm - (title_1_style.fontSize*2) - logo_height
        I.drawOn(canvas, x, y)
        
        canvas.restoreState()


class RLDocTemplate(BaseDocTemplate):
    '''
        Heir of the class BaseDocTemplate from reportlab.platypus is a type of 
        doc used to generate the report starting from a list of Flowables 
        construct in ``Report_RUN.py`` module.
    '''
    def afterInit(self):
        self.addPageTemplates(FrontCoverTemplate('Cover', self.pagesize))
        self.addPageTemplates(OneColumnTemplate('Normal', self.pagesize))
        self.addPageTemplates(Credits('Credits', self.pagesize))
        self.seq = Sequencer()

    def beforeDocument(self):
        self.canv.showOutline()
        self.title = "(Document Title Goes Here)"
        self.chapter = "(No chapter yet)"
        self.seq.reset('section')
        self.seq.reset('chapter')

    def afterFlowable(self, flowable):
        """Detect Level 1 and 2 headings, build outline,
        and track chapter title."""

        if isinstance(flowable, Paragraph):
            style = flowable.style.name
            txt = flowable.getPlainText()

            if style == 'Title':
                self.title = txt
            elif style == 'Heading1':
                self.chapter = txt 
                key = 'ch%s' % self.seq.nextf('chapter')
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(txt, key, 0, 0)
                self.seq.reset("section")
                self.notify('TOCEntry', (0, txt, self.page, key))
            elif style == 'Heading2':
                self.section = flowable.text
                key = 'ch%ss%s' % (self.seq.thisf("chapter"), self.seq.nextf("section"))
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(txt, key, 1, 0)
                self.notify('TOCEntry', (1, txt, self.page, key))

        
class FrontCoverTemplate(PageTemplate):
    '''
    Heir of the class PageTemplate from reportlab.platypus is a type of 
    PDF page inserted in report an used in the RLDocTemplate class.
    '''
    def __init__(self, id, pageSize = A4):
        self.pageWidth = pageSize[0]
        self.pageHeight = pageSize[1]
        frame1 = Frame(2.54*cm,
                       1.25*cm,
                       self.pageWidth - 2*2.54*cm,
                       self.pageHeight - 2.54*cm - 1.25*cm, id = 'Cover')
        PageTemplate.__init__(self, id, [frame1])  # note lack of onPage

    def afterDrawPage(self, canvas, doc):
        canvas.saveState()
        
        logo_height = 2.4*cm
        logo_width = 8.9*cm#logo_width = 2.54*cm
        

        txt = 'Test report'
        ptxt = Paragraph('<font color = "{color}">{txt}</font>'.format(color = darkblue, txt = txt),title_style)
        xx, yy = ptxt.wrapOn(canvas, ef_width, ef_height)
        x = margins['left']
        y = height - margins['top'] - 4*yy
        ptxt.drawOn(canvas, x, y)

        y = y - 10
        x1 = margins['left'] - 4
        x2 = width - margins['right'] + 4
        canvas.setLineWidth(1)
        canvas.setStrokeColorRGB(79.0/255,129.0/255,189.0/255)
        canvas.line(x1,y,x2,y)

        txt = '<font size = 11><font name = "Verdana Bold">Test Name:</font> {Test_Name}</font>'.format(Test_Name = Test_Name)
        ptxt = Paragraph(txt,normal_style)
        xx, yy = ptxt.wrapOn(canvas, ef_width, ef_height)
        y = y - yy - 3*normal_style.leading
        x = margins['left']
        ptxt.drawOn(canvas, x, y)

        txt = '<font size = 11><font name = "Verdana Bold">Date:</font> {date}</font>'.format(date = date)
        ptxt = Paragraph(txt,normal_style)
        xx, yy = ptxt.wrapOn(canvas, ef_width, ef_height)
        x = margins['left']
        y = y - yy - normal_style.leading
        ptxt.drawOn(canvas, x, y)

        txt = '<font size = 11><font name = "Verdana Bold">Time:</font> {time}</font>'.format(time = time)
        ptxt = Paragraph(txt,normal_style)
        xx, yy = ptxt.wrapOn(canvas, ef_width, ef_height)
        x = margins['left']
        y = y - yy - normal_style.leading
        ptxt.drawOn(canvas, x, y)

        txt = '<font size = 11><font name = "Verdana Bold">Description</font></font>'
        ptxt = Paragraph(txt,normal_style)
        xx, yy = ptxt.wrapOn(canvas, ef_width, ef_height)
        x = margins['left']
        y = y - yy - 3*normal_style.leading
        ptxt.drawOn(canvas, x, y)

        txt = '<font size = 10><font name = "Verdana">{description}</font></font>'.format(description = User_description)
        ptxt = Paragraph(txt,normal_style)
        xx, yy = ptxt.wrapOn(canvas, ef_width, ef_height)
        x = margins['left']
        y = y - yy - normal_style.leading
        ptxt.drawOn(canvas, x, y)

        from reportlab.platypus import Image
#        logo = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logo1.png')
        logo = os.path.realpath(__file__).replace('__init__.py', 'logo1.png')

        
        I = Image(logo)
        I.drawHeight = logo_height
        I.drawWidth = logo_width
        x = margins['right'] + (ef_width-logo_width)/2.0#x = width - doc.rightMargin - logo_width
        y = 1.27*cm
        I.drawOn(canvas, x, y)

        #txt = 'Powered by'
        #ptxt = Paragraph(txt,normal_style)
        #ptxt.wrapOn(canvas, width, height)
        #ptxt_width = ptxt.getActualLineWidths0()
        #x = width - doc.rightMargin - logo_width - np.max(ptxt_width)
        #y = 1.75*cm - normal_style.leading
        #ptxt.drawOn(canvas, x, y)

        canvas.restoreState()

#%% Tables

def sumarryTable(df1, df2,
                 master_rows_name = ('Steady State', 'Transient'), 
                 title_table = 'Report summary'):
    N_transient = df2.columns.size

    table = np.zeros((df1.index.size + 3, 
                      df1.columns.size + df2.columns.size+1)).tolist()

    table[0][0] = Paragraph('Table <seq id = "table"/> - ' + title_table,
         table_style)
    table[1][0] = Paragraph('', table_style)
    table[2][0] = Paragraph('', table_style)
    table[1][df1.columns.size+1] = Paragraph(master_rows_name[1],table_style)
    table[1][1] = Paragraph(master_rows_name[0],table_style)
    
    # Generate the first part of the summary table (df1)
    T_line = 3
    
    for index in df1.index:
        print(index)
        line = df1.loc[index]
#        column = df1[icolumn]
        T_column = 1
        table[T_line][0] = Paragraph(str(index), table_style)
        for icolumn in df1.columns:
            cell = line[icolumn]
            table[T_line][T_column] = Paragraph(str(cell),table_style)
            table[2][T_column] = Paragraph(str(icolumn),table_style)
            
            T_column = T_column + 1
        T_line = T_line + 1
    
    # Generate the second part of the summary table (df2)
    
    T_line = 3
    
    for index in df2.index:
        line = df2.loc[index]
#        column = df2[icolumn]
        T_column = 1 + df1.columns.size
        table[T_line][0] = Paragraph(str(index), table_style)
        for icolumn in df2.columns:
            cell = line[icolumn]
#            print(T_line)
#            print(T_column)
            table[T_line][T_column] = Paragraph(str(cell), table_style)
            table[2][T_column] = Paragraph(str(icolumn),table_style)

            T_column = T_column + 1
        T_line = T_line + 1
        
    t = Table(table)
    
    t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
               ('BOX', (0,1), (-1,-1), 2, colors.black),
               ('LINEABOVE', (0,2), (-1,2), 2, colors.black),
               ('LINEABOVE', (0,3), (-1,3), 2, colors.black),
               ('LINEBEFORE', (1,1), (1,-1), 2, colors.black),
               ('LINEBEFORE', (df1.columns.size+1,1), (df1.columns.size+1,-1), 2, colors.black),
               ('SPAN', (0,0), (-1,0)),
               ('SPAN', (0,1), (0,2)),
               ('SPAN', (df1.columns.size+1,1), (-1,1)),
               ('SPAN', (1,1), (df1.columns.size,1)),
               ('ALIGN',(0,0),(0,0),'CENTER'),
               ('ALIGN',(0,1),(-1,-1),'CENTER'),
               ('VALIGN',(0,1),(-1,-1),'MIDDLE'),
              ]))
    
    report.append(Spacer(1,20))
    report.append(t)
    report.append(Spacer(1,20))

def putInSubViaLatex(line):
    line_ret = line.replace('_{', '<sub>')
    line_ret = line_ret.replace('}', '</sub>')
    return line_ret

def detailed_Table_df(dataframe, maxValue=np.nan, minValue=np.nan, 
                      caption='', corner = ' ', 
                      decimation = 2, latexSub=False, notation=False, 
                      mode='colorful'):
    '''
    DOCSTRING AQUI !!!
    
    '''
    
    if np.isnan(maxValue):
        maxValue = dataframe.max().max()
    if np.isnan(minValue):
        minValue = dataframe.max().max()

    dict_df = {}
    for column in dataframe.columns:
        line = dataframe[column]
        for index in dataframe.index:
            dict_df[(column, index)] = line[index]

    detailed_Table(dict_df, 
                   np.array(dataframe.index),
                   np.array(dataframe.columns), 
                   maxValue, minValue=minValue, caption=caption,
                   corner=corner, decimation=decimation,
                   latexSub=latexSub, notation=notation, mode=mode)
        
def detailed_Table(data, x_axis, y_axis, maxValue, minValue=-1, caption='', corner = ' ', 
                   decimation = 2, latexSub=False, notation=False, 
                   mode='colorful'):

    '''
    Function like detailed_Tables (Depreciated), but with only one table 
    at time per test.
    
    @author: Tiarles Guterres
    '''

    table       = np.zeros( (x_axis.size + 2, y_axis.size + 1) ).tolist()
    table_float = np.zeros( (x_axis.size + 2, y_axis.size + 1) ).tolist()
    Normalized  = np.zeros( (x_axis.size + 2, y_axis.size + 1) ).tolist()

    tableMin = 9999999999
    tableMax = -99999999999

    value = 0

    table[1][0] = corner
    table[0][0] = Paragraph('Table <seq id = "table"/> - ' + caption, \
                            table_style)

    T_line = 0

    # N-3) Search in the dict the cells and put in the lists

    for i in x_axis:
        T_column = 0
        for j in y_axis:
            if T_column == 0:
                if isinstance(i, str):
                    if latexSub:
                        i2 = putInSubViaLatex(i)
                        table[T_line + 2][0] = Paragraph(i2, table_style)
                    else:
                        table[T_line + 2][0] = Paragraph(i, table_style)
                else:
                    table[T_line + 2][0] = Paragraph(str(np.round(i,2)), \
                                                     table_style)
            
            if T_line == 0:
                if isinstance(j, str):
                    if latexSub:
                        j2 = putInSubViaLatex(j)
                        table[1][T_column+1] = Paragraph(j2, table_style)
                    else:
                        table[1][T_column+1] = Paragraph(j, table_style)
                else:
                    table[1][T_column+1] = Paragraph(str(np.round(j,2)), \
                         table_style)
            
            value = data[(j, i)]
            
#            if isinstance(i, str) or isinstance(j, str):
#                value = data[(j, i)]
#            else:
#                value = data[(np.round(j, 2), np.round(i, 2))]
            
            if np.isnan(value):
                table[T_line+2][T_column+1] = Paragraph('NaN', table_style)
            elif np.isinf(value):
                #print('Inf:', value)
                table[T_line+2][T_column+1] = Paragraph('Inf', table_style)
            elif notation:
                value2 = format(value, '.%de' % decimation)
                table[T_line+2][T_column+1] = Paragraph(value2, table_style)
            elif decimation == 0:
                table[T_line+2][T_column+1] = Paragraph(str(np.int(np.round(value))), table_style)
            else:
                table[T_line+2][T_column+1] = Paragraph(str(np.round(value, decimation)), table_style)

            if value < tableMin:
                tableMin = value
            if value > tableMax:
                tableMax = value
            
            table_float[T_line+2][T_column+1] = value
            
            T_column = T_column + 1
        T_line = T_line + 1
    
    # N-2) Create the Table flowable in reportlab
    
    t = Table(table)
    t.setStyle(TableStyle(
            [('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
             ('BOX', (0,1), (-1,-1), 2, colors.black),
             ('LINEABOVE', (0,2), (-1,2), 2, colors.black),
             ('LINEBEFORE', (1,1), (1,-1), 2, colors.black),
             ('SPAN', (0,0), (-1,0)),
             ('ALIGN',(0,0),(0,0),'CENTER'),
             ('ALIGN',(0,1),(-1,-1),'CENTER')]))
    
    # N-2) Normalize the table values
    
    for ind1, aux1 in enumerate(table_float):
        for ind2, aux2 in enumerate(aux1):
        
            if (tableMax == tableMin):
                Normalized[ind1][ind2] = 0
            elif (maxValue == tableMin or maxValue == tableMax):
                Normalized[ind1][ind2] = (table_float[ind1][ind2] - tableMin) / (tableMax - tableMin)
            elif table_float[ind1][ind2] <= maxValue:
                Normalized[ind1][ind2] = (table_float[ind1][ind2] - tableMin) / (maxValue - tableMin)
            else:
                Normalized[ind1][ind2] = (table_float[ind1][ind2] - maxValue) / (tableMax - maxValue)

    # N-1) Calculate and insert the color in the specific cell
    if mode == 'colorful':
        for ind1, aux1 in enumerate(table_float):
            for ind2, aux2 in enumerate(aux1):
                if (ind1 >= 2 and ind2 >= 1):        
                    c = Normalized[ind1][ind2]
                    #print("table_float: ",table_float[ind1][ind2])
                    #print("c:",c)
                    if np.isnan(c) or np.isinf(c):
                        #print('Inf or Nan:', table_float[ind1][ind2])
                        R, G, B = (0.8235294117647058, 
                                   0.45294117647058824, 
                                   0.45294117647058824)
                    elif table_float[ind1][ind2] <= maxValue:
                        R = (100.0 + 155.0*c)/255.0
                        G = (205.0 +  50.0*c)/255.0
                        B = (100.0 + 155.0*c)/255.0
                    else:
                        R = (255.0 -  50.0*c)/255.0
                        G = (255.0 - 155.0*c)/255.0
                        B = (255.0 - 155.0*c)/255.0
    
                    if not (np.isfinite(R) and np.isfinite(G) and 
                            np.isfinite(B)):
                        raise Exception('RGB value not valid!')
    
                    t.setStyle(TableStyle([('BACKGROUND', 
                                            (ind2,ind1), 
                                            (ind2,ind1), 
                                            (R,G,B))]))
    elif mode == 'red_limit':
            for ind1, aux1 in enumerate(table_float):
                for ind2, aux2 in enumerate(aux1):
                    if (ind1 >= 2 and ind2 >= 1): 
                        if (maxValue < table_float[ind1][ind2] or 
                            minValue > table_float[ind1][ind2]):
                            R, G, B = (0.8235294117647058, 0.45294117647058824, 
                                       0.45294117647058824)
                            t.setStyle(TableStyle([('BACKGROUND', 
                                                    (ind2,ind1), 
                                                    (ind2,ind1), 
                                                    (R,G,B))]))
    
    # N) Insert a space before table and insert the table in report list flow
    report.append(Spacer(1,5))
    report.append(t)

    
#%% 
#Textual Functions

def addPageBreak():
    '''
        Function that add a PageBreak element in report list.
    '''
    try:
        report.append(PageBreak())
        return True
    except Exception:
        return False

def report_Pop():
    '''
        Function that remove the last element.
    '''
    report.pop()
def addSpacer(width, height):
    '''
        Function that add a Spacer element in report list.
    '''
    try:
        report.append(Spacer(width, height))
        return True
    except Exception:
        return False


#def addSubtitle(txt):
#    '''
#    Method that add a text like subtitle in the report list.
#    '''
#    addTextParagraph('<font color = "{color}"><seq template = "%(chapter)s.' +
#        '%(subchapter+)s"/>{txt}</font>'.format(txt = " "+txt, 
#            color = lightblue), style='title_2')


#def addSubtitle(txt):
#    '''
#    Method that add a text like subtitle in the report list.
#    '''
#    addTextParagraph('<font color = "{color}"><seq template = "%(chapter)s.'+
#        '%(subchapter+)s"/>{txt}</font>'.format(txt = " "+txt, 
#          color = lightblue), style='title_2')

#def addSubtitle(txt):
#    '''
#    Method that add a text like subtitle in the report list.
#    '''
#    addTextParagraph('<font color = "{color}"><seq template = "%(chapter)s.\
#%(subchapter+)s"/>{txt}</font>'.format(txt = " "+txt, color = lightblue), 
#    style='title_2')
        
def addSubtitle(txt):
    '''
    Method that add a text like subtitle in the report list.
    '''
    addTextParagraph(('<font color = "{color}"><seq template = "%(chapter)s.'+
        '%(subchapter+)s"/>{txt}</font>').\
        format(txt = " "+txt, color = lightblue), style='title_2')

def addTextParagraph(txt, style='text'):
    '''
        This function put the text inserted in a text Paragraph style and 
        add in report.

        Parameters
        ---------
        text: str
            The text who wants to paragraph in report.
        style: bool
        
        Returns
        -------
        If no one exception occurs, return True, else False.
    '''
    try:
        if style == 'text':
            report.append(Paragraph(txt,normal_style))
        elif style == 'text_l':
            report.append(Paragraph(txt,normal_style_l))
        elif style == 'title_2':
            report.append(Paragraph(txt,title_2_style))
        elif style == 'text_8':
            report.append(Paragraph(f'<font size = 8>{txt}</font>',
                                    normal_style))
        return True
    except Exception:
        return False
    return

def new_chapter(txt):
    '''
        Breaks the document and add a chapter title
    '''
    report.append(PageBreak())

    ptxt = Paragraph('<font color = "{color}">{txt}</font>'.\
    format(color = white, txt = '<seq id = "chapter"/>   ' + txt + 
        '<seqreset id="subchapter"/>'), title_1_style)

    report.append(ptxt)

#%%
# Figure Insertion

#def insert_figure(figure,legend):
#    '''
#        Insert a PDF figure with legend at the document.
#    '''
#    tabledata = [[[figure,Paragraph('Figure <seq id = "figure"/> - ' + legend,legend_style)]]]
#    tab = Table(tabledata)
#    report.append(tab)

def insert_figure(figname, caption):
    fig_pdf = PdfImage(figname)
    fig_pdf.hAlign = 'CENTER'
#    insert_figure(fig_pdf, caption)
    
    tabledata = [[[fig_pdf,Paragraph('Figure <seq id = "figure"/> - ' + caption,legend_style)]]]
    tab = Table(tabledata)
    report.append(tab)

#%%
# Build Functions

report = []

def build_doc(test_name, test_description):
    global Test_Name, User_description, doc, report
    
    report = []
    
    Test_Name = test_name
    User_description = test_description
    
    doc = RLDocTemplate("report.pdf", pagesize = A4,
                        rightMargin = 2.54*cm, leftMargin = 2.54*cm,
                        topMargin = 2.54*cm, bottomMargin = 1.25*cm)
    
    reset_indexes()

def build_cover():
    '''
        Add a Normal Page template (the Cover) to report list. 
    '''
    report.append(NextPageTemplate('Normal'))


def build_credits(acknowledgement, members):
    '''
        Breaks the document and add a Credits template (the credits chapter) to report list. 
    '''
    report.append(NextPageTemplate('Credits'))
    report.append(PageBreak())
    ptxt = Paragraph('<font color = "{color}">{txt}</font>'.\
                     format(color = white,txt='Credits'), title_1_style)
    report.append(ptxt)
    report.append(Paragraph('Acknowledgement: ' + acknowledgement ,v10_style))
    report.append(Spacer(1,5))
    report.append(Paragraph('Developed by:',v10_style))
    
    for member in members:
        report.append(Paragraph(member,v10_style))


def save_doc(name, withDate=True):
    from time import ctime
    global doc, report
    
    if withDate:
        reportName = name+'_'+ctime().replace(':', '_').replace(' ', '_')+'.pdf'
    else:
        reportName = name
        
    doc.build(report, filename=reportName)
    
    return reportName
