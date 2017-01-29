# -*- coding: utf-8 -*-

# provides tex2unicode and unicode2tex


################################################################
# LaTeX accents replacement
latexAccents = [
  ( u"à", "\\`a" ), # Grave accents
  ( u"è", "\\`e" ),
  ( u"ì", "\\`\\i" ),
  ( u"ò", "\\`o" ),
  ( u"ù", "\\`u" ),
  ( u"ỳ", "\\`y" ),
  ( u"À", "\\`A" ),
  ( u"È", "\\`E" ),
  ( u"Ì", "\\`\\I" ),
  ( u"Ò", "\\`O" ),
  ( u"Ù", "\\`U" ),
  ( u"Ỳ", "\\`Y" ),
  ( u"á", "\\'a" ), # Acute accents
  ( u"é", "\\'e" ),
  ( u"í", "\\'\\i" ),
  ( u"ó", "\\'o" ),
  ( u"ú", "\\'u" ),
  ( u"ý", "\\'y" ),
  ( u"Á", "\\'A" ),
  ( u"É", "\\'E" ),
  ( u"Í", "\\'\\I" ),
  ( u"Ó", "\\'O" ),
  ( u"Ú", "\\'U" ),
  ( u"Ý", "\\'Y" ),
  ( u"â", "\\^a" ), # Circumflex
  ( u"ê", "\\^e" ),
  ( u"î", "\\^\\i" ),
  ( u"ô", "\\^o" ),
  ( u"û", "\\^u" ),
  ( u"ŷ", "\\^y" ),
  ( u"Â", "\\^A" ),
  ( u"Ê", "\\^E" ),
  ( u"Î", "\\^\\I" ),
  ( u"Ô", "\\^O" ),
  ( u"Û", "\\^U" ),
  ( u"Ŷ", "\\^Y" ),
  ( u"ä", "\\\"a" ),    # Umlaut or dieresis
  ( u"ë", "\\\"e" ),
  ( u"ï", "\\\"\\i" ),
  ( u"ö", "\\\"o" ),
  ( u"ü", "\\\"u" ),
  ( u"ÿ", "\\\"y" ),
  ( u"Ä", "\\\"A" ),
  ( u"Ë", "\\\"E" ),
  ( u"Ï", "\\\"\\I" ),
  ( u"Ö", "\\\"O" ),
  ( u"Ü", "\\\"U" ),
  ( u"Ÿ", "\\\"Y" ),
  ( u"ç", "\\c{c}" ),   # Cedilla
  ( u"Ç", "\\c{C}" ),
  ( u"œ", "{\\oe}" ),   # Ligatures
  ( u"Œ", "{\\OE}" ),
  ( u"æ", "{\\ae}" ),
  ( u"Æ", "{\\AE}" ),
  ( u"å", "{\\aa}" ),
  ( u"Å", "{\\AA}" ),
  ( u"–", "--" ),   # Dashes
  ( u"—", "---" ),
  ( u"ø", "{\\o}" ),    # Misc latin-1 letters
  ( u"Ø", "{\\O}" ),
  ( u"ß", "{\\ss}" ),
  ( u"¡", "{!`}" ),
  ( u"¿", "{?`}" ),
  ( u"\\", "\\\\" ),    # Characters that should be quoted
  ( u"~", "\\~" ),
  ( u"&", "\\&" ),
  ( u"$", "\\$" ),
  ( u"{", "\\{" ),
  ( u"}", "\\}" ),
  ( u"%", "\\%" ),
  ( u"#", "\\#" ),
  ( u"_", "\\_" ),
  ( u"©", "\copyright" ), # Misc
  ( u"ı", "{\\i}" ),
  ( u"‘", "`" ),    #Quotes
  ( u"’", "'" ),
  ( u"“", "``" ),
  ( u"”", "''" ),
  ( u"‚", "," ),
  ( u"„", ",," ),
  ( u"", ",," )
]

mathModeLaTeX = [
  ( u'≥', '\\ge' ),   # Math operators
  ( u'≤', '\\le' ),
  ( u'≠', '\\neq' ),
  ( u'µ', '\\mu' ),
  ( u'°', '\\deg' ),
  ( u'α', '\\alpha' ),
  ( u'β', '\\beta' ),
  ( u'γ', '\\gamma' ),
  ( u'δ', '\\delta' ),
  ( u'ϵ', '\\epsilon' ),
  ( u'ζ', '\\zeta' ),
  ( u'η', '\\eta' ),
  ( u'θ', '\\theta' ),
  ( u'ι', '\\iota' ),
  ( u'κ', '\\kappa' ),
  ( u'λ', '\\lambda' ),
  ( u'μ', '\\mu' ),
  ( u'ν', '\\nu' ),
  ( u'ξ', '\\xi' ),
  ( u'π', '\\pi' ),
  ( u'ρ', '\\rho' ),
  ( u'σ', '\\sigma' ),
  ( u'τ', '\\tau' ),
  ( u'υ', '\\upsilon' ),
  ( u'ϕ', '\\phi' ),
  ( u'χ', '\\chi' ),
  ( u'ψ', '\\psi' ),
  ( u'ω', '\\omega' ),
  ( u'A', '\\Alpha' ),
  ( u'B', '\\Beta' ),
  ( u'Γ', '\\Gamma' ),
  ( u'Δ', '\\Delta' ),
  ( u'E', '\\Epsilon' ),
  ( u'Ζ', '\\Zeta' ),
  ( u'Η', '\\Eta' ),
  ( u'Θ', '\\Theta' ),
  ( u'Ι', '\\Iota' ),
  ( u'Κ', '\\Kappa' ),
  ( u'Λ', '\\Lambda' ),
  ( u'Μ', '\\Mu' ),
  ( u'Ν', '\\Nu' ),
  ( u'Ξ', '\\Xi' ),
  ( u'Π', '\\Pi' ),
  ( u'Ρ', '\\Rho' ),
  ( u'Σ', '\\Sigma' ),
  ( u'Τ', '\\Tau' ),
  ( u'ϒ', '\\Upsilon' ),
  ( u'Φ', '\\Phi' ),
  ( u'X', '\\Chi' ),
  ( u'Ψ', '\\Psi' ),
  ( u'Ω', '\\Omega')
]

def addDollar(list):
    return [u"$%s$"%x for x in list]

latexAccentsDict = dict(latexAccents)
latexAccentsDictR = dict (zip(latexAccentsDict.values(),latexAccentsDict.keys()))

tmp = dict(mathModeLaTeX)
mathModeLaTeXDictR = dict (zip(tmp.values(),tmp.keys()))
mathModeLaTeXDictR["$"] = ""  # just kill all inline math

mathModeLaTeXDict = dict(mathModeLaTeX)
mathModeLaTeXDict = dict (zip(mathModeLaTeXDict.keys(), addDollar(mathModeLaTeXDict.values())))

def string_replace(dct,text):
    keys = dct.keys()
    for n in keys:
        # if '%' not in text: break
        text = text.replace(n,dct[n])
    return text


def tex2unicode(s):
   s= string_replace(latexAccentsDictR, s)
   s= string_replace(mathModeLaTeXDictR, s)
   return s


def unicode2tex(s):
   s= string_replace(latexAccentsDict, s)
   s= string_replace(mathModeLaTeXDict, s)
   return s
