import re
import functools

def _map_lines(func, sects):
    n_sects = []
    for s in sects:
        n_s = []
        for l in s:
            n_s.append(func(l))
        n_sects.append(n_s)
    return n_sects

def markup_transform(line):
    """ This substitution is happening on a line by line basis:
        A. The markup should not span multiple lines
        B. I need to split the text into individual lines to filter out blank and note lines. """

    ## The following are all from the "translation" guidelines - http://papyri.info/editor/documentation?docotype=translation

    # Transliteration (Using Leiden+ "term")
    # From: the sacred tract {hieras orgados}
    # To: <the sacred tract=hieras orgados>
    # Notes: There will need to be some manual editing involved here to place the first <. 
    #         It may be preferable to use "term with lang" giving <the sacred tract~grc-Latn=hieras orgados>
    leiden_line = re.sub(r'\{(.+?)\}',r'< =\1>', line)

    # Gap in text
    # From: . . . 
    # To: ...
    leiden_line = re.sub(r'\.\s\.\s\.','...',leiden_line)

    # Line numbers
    # From: &10&
    # To: ((10))
    leiden_line = re.sub(r'&(\d+?)&', r'((\1))',leiden_line)

    # Inline notes
    # From: $Painting$
    # To: /*Painting*/
    # Notes: Strictly, very few of these are actually inline notes on AIO.
    #        This seems that it will be a sufficient stop-gap for now though. 
    leiden_line = re.sub(r'\$(.+?)\$', r'/*\1*/',leiden_line)

    ## The following are all from the "text" guidelines - http://papyri.info/editor/documentation?docotype=text

    # Supplied lost words
    # From: [and]
    # To: [and]
    # Notes: No change here, but to be noted that these will have additional semantics after epidoc transform. 

    # Lines
    # From: "... of the ..."
    # To: "4. ... of the ..."

    #Person
    #From: Aristodemos**
    #To: Aristodemos
    # Removing these completely just now to allow for tagging style markup in future. 
    leiden_line = re.sub(r'\*\*', r'',leiden_line)

    #Place
    #From: Athens@@
    #To: Athens
    # Removing these completely just now to allow for tagging style markup in future. 
    leiden_line = re.sub(r'@@', r'',leiden_line)

    # Cleanup mess. 
    leiden_line = re.sub(r'&#160;',' ',leiden_line)
    leiden_line = re.sub(r'\s+',' ',leiden_line)

    return leiden_line

def section_split(text):
    """ Divisions between 'sections' of text in are currently only loosely 
        indicated by multiple blank lines between them. """
    lines = [line.strip() for line in text.split('\n')]
    sections = []
    acc = []
    count = 0
    for l in lines:
        if not l:
            count += 1
            if count > 1 and acc:
                sections.append(acc)
                acc = []
                count = 0
        else:
            count = 0 
            acc.append(l)
    if acc:
        sections.append(acc)
    return sections

def wrap_section(section):
    """  """
    pre = "<D=<=\n"
    post = "\n=>=D>\n"
    return pre + section + post

def number_line(line):
    """ Add leiden+ line numbering, ignoring lines that are notes.
        Not actually numbering, probably not important for now."""
    if line.startswith('/*') and line.endswith('*/'):
        return line
    else: 
        return re.sub(r'^', '1. ', line)

def to_leiden_plus(text):
    """ Crudely go through a text marked up in the old fashion, and 
        convert to the Leiden plus conventions, ready for conversion to epidoc."""
   
    sections = section_split(text)
    leiden_sections = _map_lines(markup_transform, sections)
    numbered_sections = _map_lines(number_line, leiden_sections)
    
    output_string = ""
    for section in numbered_sections:
        output_string += wrap_section("\n".join(section))
    return output_string
