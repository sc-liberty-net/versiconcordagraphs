"""make_motifs.py - regenerates motifs.pdf.

A second report, alongside findings.pdf. Where findings.pdf argues from what the
passages SAY, this one argues from the words the passages USE - which only
became checkable when the lemma layer landed. None of its eight findings repeat
findings.pdf's eight.

Every Strong's number, occurrence count and verse list in the text below was
read off strongs_index.json with lemma.py, not recalled. Re-derive any of them:

    python lemma.py lemma G0586 --list
    python lemma.py shared "Mark 7:11" "Matthew 27:6"

    python make_motifs.py
"""
import re
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                HRFlowable, PageBreak)

INK   = colors.HexColor('#1B2620')
INK2  = colors.HexColor('#4C564F')
RULE  = colors.HexColor('#C6CABD')
STATE = colors.HexColor('#14493A')
SUPP  = colors.HexColor('#8A5A0E')
SPEC  = colors.HexColor('#6E7379')

S = {
 'title': ParagraphStyle('title', fontName='Times-Bold', fontSize=22, leading=26,
                         textColor=INK, spaceAfter=4),
 'sub':   ParagraphStyle('sub', fontName='Times-Italic', fontSize=11.5, leading=15,
                         textColor=INK2, spaceAfter=18),
 'h1':    ParagraphStyle('h1', fontName='Times-Bold', fontSize=14.5, leading=18,
                         textColor=INK, spaceBefore=18, spaceAfter=7),
 'h2':    ParagraphStyle('h2', fontName='Times-Bold', fontSize=11.5, leading=15,
                         textColor=INK, spaceBefore=12, spaceAfter=4),
 'body':  ParagraphStyle('body', fontName='Times-Roman', fontSize=10.7, leading=15.2,
                         textColor=INK, spaceAfter=8),
 'bul':   ParagraphStyle('bul', fontName='Times-Roman', fontSize=10.7, leading=15.2,
                         textColor=INK, leftIndent=16, bulletIndent=4, spaceAfter=5),
 'note':  ParagraphStyle('note', fontName='Times-Italic', fontSize=9.8, leading=13.5,
                         textColor=INK2, spaceAfter=8),
}


def tag(t):
    t = t.replace('[states]', f'<font color="#{STATE.hexval()[2:]}"><b>[text states]</b></font>')
    t = t.replace('[supports]', f'<font color="#{SUPP.hexval()[2:]}"><b>[text supports]</b></font>')
    t = t.replace('[spec]', f'<font color="#{SPEC.hexval()[2:]}"><b>[speculation]</b></font>')
    return t


story = []
def P(t, s='body'): story.append(Paragraph(tag(t), S[s]))
def B(t): story.append(Paragraph(tag(t), S['bul'], bulletText='—'))
def rule(): story.append(HRFlowable(width='100%', thickness=0.6, color=RULE,
                                    spaceBefore=6, spaceAfter=10))
def gap(h=6): story.append(Spacer(1, h))

P('What the Words Do', 'title')
P('Motif findings from the tax, tithe and tribute concordagraph &mdash; 158 passages, '
  '180 connections, read through the Hebrew and Greek behind them rather than through '
  'the English in front of them. A companion to <i>findings.pdf</i>; none of the eight '
  'findings below repeats one of its eight.', 'sub')
rule()

P('Why these findings were not available before', 'h1')
P('A connection tagged <i>shared wording</i> is a claim that two passages use the same '
  'word. Read against an English index, that claim is really about a translator&rsquo;s '
  'choice: one word of Hebrew can arrive as three English words, and two unrelated words '
  'can arrive as one. The corpus could assert shared wording; it could not check it.')
P('It can now. Every verse in the corpus is keyed to the Strong&rsquo;s numbers behind it, '
  'from the STEPBible tagged Hebrew Old Testament and Greek New Testament. What follows '
  'comes from asking that index which words actually recur, and how rare they are. '
  'A count matters as much as a match: a word shared by two passages and four hundred '
  'others is vocabulary; a word shared by two passages and nobody else is a thread.')
P('All 158 passages carry lemma data. Every count below is the complete New Testament or '
  'Hebrew Bible total for that word, not a sample.', 'note')

P('Findings', 'h1')

P('1. The New Testament has two verbs for tithing, and Hebrews changes verb mid-argument',
  'h2')
P('<b><i>apodekatoo</i></b> (G0586) occurs four times in the whole New Testament: '
  'Matthew 23:23, Luke 11:42, Luke 18:12, Hebrews 7:5. '
  '<b><i>dekatoo</i></b> (G1183) occurs twice: Hebrews 7:6 and Hebrews 7:9. '
  'That is every occurrence of either. [states]')
P('Set the two lists side by side and the distribution is not random. The first verb '
  'covers the three rebukes &mdash; the two woes and the Pharisee&rsquo;s boast &mdash; '
  'and one more verse: Hebrews 7:5, the commandment in the law for Levi&rsquo;s '
  'descendants to collect. The second verb appears only where Melchizedek collects from '
  'Abraham, and where Levi is said to have paid through him. [states]')
P('So Hebrews describes the Levitical tithe with the same verb Matthew and Luke use for '
  'the Pharisees, and reaches for a different verb the moment it turns to Melchizedek. '
  'The chapter&rsquo;s whole argument is that one priesthood supersedes the other; the '
  'vocabulary sorts them before the argument does. [supports]')
P('This is invisible in English. The NRSV renders both verbs &ldquo;collect tithes&rdquo; '
  'or &ldquo;paid tithes&rdquo; without distinction.', 'note')

P('2. The temple tax and Caesar&rsquo;s tax are the same word, and the translation hides it',
  'h2')
P('<b><i>kensos</i></b> (G2778) occurs four times: Matthew 17:25, Matthew 22:17, '
  'Matthew 22:19, Mark 12:14. It is a Latin loanword &mdash; the Roman <i>census</i> levy. '
  '[states]')
P('Three of those four are the Caesar controversy. The fourth is Matthew 17:25, where '
  'Jesus asks Peter from whom the kings of the earth take &ldquo;toll or tribute&rdquo; '
  '&mdash; and the scene is the collection of the <i>temple</i> tax. The one passage in '
  'the corpus where anyone reasons about a religious levy reasons about it in imperial '
  'fiscal vocabulary. [supports]')
P('The NRSV renders the word &ldquo;tribute&rdquo; in 17:25 and &ldquo;taxes&rdquo; in '
  '22:17. A reader working from the English has no way to see that the temple-tax scene '
  'and the Caesar scene turn on one word. This is the hazard the lemma layer exists for, '
  'running in the direction nobody plans for: not a false link the English invents, but a '
  'true one the English conceals. [states]')

P('3. One word carries both the charge against Jesus and the command from Paul', 'h2')
P('<b><i>phoros</i></b> (G5411) occurs four times: Luke 20:22, Luke 23:2, Romans 13:6, '
  'Romans 13:7. Two in Luke, two in Paul, and nowhere else. [states]')
P('In Luke 20:22 it is the question put to Jesus. In Luke 23:2 it is the accusation at '
  'his trial &mdash; that he forbade paying it. In Romans 13:6 and 13:7 it is Paul '
  'instructing the church to pay it. [states]')
P('Jesus is never recorded using the word. He is asked it once and accused of it once; '
  'the only affirmative uses in the New Testament are Paul&rsquo;s. Whatever one makes of '
  'that, the corpus can now say precisely how small the evidence base is: four verses, '
  'two speakers, and one of them is the prosecution. [supports]')

P('4. Corban occurs twice, and both times the temple fund is where an obligation stops',
  'h2')
P('<b><i>korban</i></b> (G2878) occurs twice: Mark 7:11 and Matthew 27:6. [states]')
P('In Mark, a man declares that the support his parents might have had from him is '
  'Corban, an offering to God &mdash; and the dedication is what stops the support. '
  'In Matthew, the chief priests refuse to put the returned silver into the treasury, '
  'which is the same word, because it is blood money. [states]')
P('A dedication that blocks what is owed, and a treasury that will not receive what is '
  'tainted. In both, the fund is the point at which a payment fails to move &mdash; once '
  'by the giver&rsquo;s device, once by the institution&rsquo;s scruple. The corpus holds '
  'both passages and connects neither to the other. [supports]')

P('5. &ldquo;Render unto Caesar&rdquo; is a repayment verb', 'h2')
P('<b><i>apodidomi</i></b> (G0591) carries both halves of Matthew 22:21, and it is '
  'the verb of Romans 13:7 as well. It appears in 46 verses. [states]')
P('Its sense is fixed by its company rather than by argument. The same verb is the '
  'creditor&rsquo;s demand in Matthew 18:28 &mdash; &ldquo;Pay what you owe&rdquo; &mdash; '
  'and the Samaritan&rsquo;s promise in Luke 10:35, &ldquo;I will repay you.&rdquo; It is '
  'what one does with a debt, not what one does with a gift. [states]')
P('Which makes the ruling in Matthew 22:21 a sentence about ownership, not about '
  'jurisdiction. The coin carries the emperor&rsquo;s likeness, so handing it over is '
  'giving back what was already his. And because the same verb governs the second clause, '
  'what is God&rsquo;s is to be given back too &mdash; on the same grounds, and the clause '
  'declines to say what falls under it. [supports]')

P('6. One coin holds the tax, the wage, the debt and the mercy', 'h2')
P('<b><i>denarion</i></b> (G1220) occurs in fifteen verses, and the range is the '
  'observation. It is the coin produced for the tax (Matthew 22:19, Luke 20:24); the '
  'day&rsquo;s wage agreed in the vineyard (Matthew 20:2, 20:13); the debt one slave '
  'throttles another over (Matthew 18:28) and the two debts a creditor forgives '
  '(Luke 7:41); the two coins the Samaritan leaves at the inn (Luke 10:35); and, in '
  'Revelation 6:6, a day&rsquo;s wage for a day&rsquo;s wheat under famine. [states]')
P('The corpus already joins the wage to the tax coin. It does not join either to the debt '
  'or to the mercy, and those are the same coin. A single unit of account is doing the '
  'work of tribute, labour, obligation and relief &mdash; which is the corpus&rsquo;s '
  'central claim about a fixed share, arriving from the direction of vocabulary rather '
  'than of statute. [supports]')

P('7. The silver arc ends by refusing silver', 'h2')
P('<b><i>argyrion</i></b> (G0694) occurs in twenty verses, and in Matthew they fall in '
  'order: money entrusted to slaves for increase (25:18, 25:27), the price agreed for '
  'handing Jesus over (26:15), the silver brought back and thrown down (27:3, 27:5), the '
  'treasury refusing it (27:6), the same silver named as the price set on a man (27:9), '
  'and then the word again for the money paid to the soldiers at the tomb (28:12, 28:15). '
  '[states]')
P('The last occurrence in the corpus&rsquo;s own range of books is 1 Peter 1:18, which '
  'says the ransom was not paid in perishable things like silver or gold. A vocabulary '
  'that runs from investment through purchase to bribery closes by naming itself as the '
  'wrong medium. [supports]')
P('This is the most associative of the eight, and it is offered as a reading rather than '
  'a result. The word is common enough that its occurrences need not form an argument; '
  'what can be checked is that they fall in that order in that Gospel. [spec]')

P('8. The corpus&rsquo;s centre of gravity is the Torah, not the Gospels', 'h2')
P('Counting how many different groups each passage reaches, the widest reach in the whole '
  'graph belongs to Deuteronomy 14:29 &mdash; five groups. Behind it, at four each: '
  'Matthew 17:24, Exodus 30:13, 1 Samuel 8:15, Hebrews 7:5, Numbers 18:21, '
  'Leviticus 27:30. Six of those seven are Hebrew Bible, and four are tithe statutes. '
  '[states]')
P('The page draws the temple tax at the centre, because that is the group marked as hub. '
  'The connective tissue is elsewhere. What actually holds this corpus together is the '
  'law about a fixed share, with the Gospel controversies hanging off it. [supports]')
P('And the single verse that reaches furthest is the one that names who the third-year '
  'tithe was for: the Levite without an allotment, the resident alien, the orphan and the '
  'widow. Whatever else the corpus is about, that is the verse it keeps having to come '
  'back through. [supports]')

story.append(PageBreak())

P('Connections the corpus is missing', 'h1')
P('Each of these was found by the lemma index, not proposed and then justified. They are '
  'listed for Ethan to admit or refuse; none has been added.')
B('<b>Mark 7:11 to Matthew 27:6</b> &mdash; shared wording, and the text says it. Two '
  'occurrences of one word, both in the corpus, currently unconnected.')
B('<b>Matthew 17:25 to Matthew 22:19 and to Mark 12:14</b> &mdash; shared wording. '
  'Neither link exists. The existing edge from 17:25 to 22:17 is tagged <i>same idea, '
  'the text supports it</i>; on the evidence it is shared wording, and the text states it.')
B('<b>Luke 20:22, Luke 23:2, Romans 13:6, Romans 13:7</b> &mdash; the four verses of '
  '<i>phoros</i>, currently joined only in part and only conceptually.')
B('<b>Luke 7:41 to Matthew 20:2 and Matthew 22:19</b> &mdash; the denarius, across debt, '
  'wage and tax. The wage-to-tax link exists; the debt is outside it.')
B('<b>Hebrews 7:5 to Matthew 23:23, Luke 11:42 and Luke 18:12</b> &mdash; the four '
  'occurrences of one tithing verb, spanning the rebuke group and the Hebrews argument. '
  'No edge joins those two groups on this basis.')

P('A limit this method cannot pass', 'h1')
P('The lemma index is the Hebrew Old Testament and the Greek New Testament. Strong&rsquo;s '
  'numbers do not cross between them: a Hebrew word and the Greek word that renders it '
  'carry unrelated numbers. So no claim of shared wording between a Hebrew Bible passage '
  'and a New Testament one can be tested here at all. Every such connection in this corpus '
  'is conceptual by necessity, not by choice.')
P('Checked, and it passed: the corpus currently claims <b>zero</b> shared-wording edges '
  'across that boundary. Whoever built it was already observing a discipline the tool can '
  'only now confirm. [states]')
P('A Septuagint layer would lift the restriction, since it would put the Hebrew Bible into '
  'Greek and let a Greek word be traced from one testament to the other. That is a real '
  'project, not a switch, and it would introduce its own question &mdash; whether a New '
  'Testament writer is echoing the Greek translation or the Hebrew behind it.', 'note')

P('Standing caution', 'h1')
P('Grounding a motif in a lemma removes one failure mode and not the others. That two '
  'passages share a rare word is a fact; that the sharing means something is still a '
  'reading, and it still belongs to the reader. The counts in this report are there so '
  'that a reader can weigh the claims rather than take them &mdash; a word shared with '
  'nobody else is evidence, a word shared with four hundred verses is not, and the '
  'difference is printed beside every one.')
P('Findings 1 through 4 rest on complete occurrence lists of two to four verses, and can '
  'be checked in a minute. Findings 6 and 7 rest on wider words and are weaker in '
  'proportion. Finding 7 is marked as speculation and should be argued with.')

doc = SimpleDocTemplate('motifs.pdf', pagesize=LETTER,
                        leftMargin=1.05*inch, rightMargin=1.05*inch,
                        topMargin=0.95*inch, bottomMargin=0.95*inch,
                        title='What the Words Do — Motif Findings',
                        author='Bible Study project')

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 8.5)
    canvas.setFillColor(INK2)
    canvas.drawCentredString(LETTER[0]/2, 0.62*inch, str(doc.page))
    canvas.restoreState()

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print('motifs.pdf written')
