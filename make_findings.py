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
    """Render warrant tags in their tier colour."""
    t = t.replace('[states]', f'<font color="#{STATE.hexval()[2:]}"><b>[text states]</b></font>')
    t = t.replace('[supports]', f'<font color="#{SUPP.hexval()[2:]}"><b>[text supports]</b></font>')
    t = t.replace('[spec]', f'<font color="#{SPEC.hexval()[2:]}"><b>[speculation]</b></font>')
    return t

story = []
def P(t, s='body'): story.append(Paragraph(tag(t), S[s]))
def B(t): story.append(Paragraph(tag(t), S['bul'], bulletText='\u2014'))
def rule(): story.append(HRFlowable(width='100%', thickness=0.6, color=RULE,
                                    spaceBefore=6, spaceAfter=10))
def gap(h=6): story.append(Spacer(1, h))

P('Tax, Tithe and Tribute', 'title')
P('Findings from the concordagraph corpus &mdash; 151 passages, 170 connections, '
  'every reference verified against an index built from the NRSV. '
  'Warrant tiers mark how much weight the text puts behind each reading.', 'sub')
rule()

P('The central claim', 'h1')
P('The Bible does not treat taxation and tithing as two separate subjects, one sacred '
  'and one secular. It treats a fixed share of production as a contested claim, and it '
  'tracks who ends up holding land as a result. The sacred/secular sorting that most '
  'readers bring to these texts is not the sorting the texts themselves perform.')

P('Findings', 'h1')

P('1. The same tenth, claimed by rivals', 'h2')
P('Leviticus 27:30 makes the tenth of seed and fruit holy to God. Numbers 18:21 assigns '
  'every tithe to the Levites as wages, explicitly because they hold no land. 1 Samuel '
  '8:15 warns that the king will take a tenth of grain and vineyards and give it to his '
  'officers and courtiers. Identical fraction, rival claimants. [states]')
P('The inversion is in the recipients\u2019 relationship to property. The Levitical tenth '
  'exists <i>because</i> its recipients are barred from land; it substitutes for an '
  'allotment. The royal tenth goes to courtiers who, three verses earlier, have just been '
  'given the best fields and vineyards. One tenth compensates for exclusion from property; '
  'the other compounds its concentration. [supports]')
P('This is a sharper distinction than the God-versus-Caesar framing of Matthew 22:21, '
  'which sorts by recipient and therefore by the legitimacy of authority. That sorting '
  'fails repeatedly in the corpus: Amos condemns tithes brought faithfully to a sanctuary, '
  'Malachi accuses the people of robbing God through tithes, and Ezra 7:24 records a '
  'Persian imperial decree exempting temple staff from tribute, custom and toll. '
  'Caesar\u2019s system funding God\u2019s. [states]')

P('2. Extraction, land, bondage \u2014 in three different orders', 'h2')
P('A three-step sequence recurs across three regimes, but the tax occupies a different '
  'position each time. This is the finding that a flat topical list conceals.')
B('<b>Egypt.</b> The land becomes Pharaoh\u2019s and the people are made slaves '
  '(Gen 47:20\u201321) <i>before</i> Joseph institutes the permanent fifth (47:24). '
  'The tax codifies a dispossession already complete. [states]')
B('<b>Israel\u2019s own king.</b> Samuel lists seizure of fields (1 Sam 8:14), then the '
  'tenth (8:15), then slavery (8:17). Extraction sits in the middle, as forecast. [states]')
B('<b>Persia.</b> The people narrate it themselves: fields pledged during famine '
  '(Neh 5:3), money borrowed against those same fields to pay the king\u2019s tax (5:4), '
  'children enslaved and fields in other hands (5:5). Here the tax is the cause. [states]')
P('Note that the Samuel case is not a foreign empire. It is Israel\u2019s own king, a '
  'domestic sovereign of the correct religion. The critique is not that the wrong god is '
  'being paid; it is that the payment concentrates holdings. [supports]')

P('3. The temple tax is the bridge', 'h2')
P('Matthew 17:24\u201327 is the only passage where anyone treats a religious levy as a '
  'live obligation and reasons about it. Jesus asks from whom kings take toll or tribute, '
  'concludes that the children are free, and then pays anyway to avoid giving offense. '
  '[states]')
P('It is the only node in the corpus with connections into four different groups: the '
  'imperial-tax cluster through its toll-and-tribute vocabulary, the statutory anchors '
  'through the half-shekel of Exodus 30:13, the Hebrews 7 argument, and the '
  'treasury and money-changer material. The confusion readers carry about tax and tithe '
  'is not a failure of categorisation on their part \u2014 this passage sits genuinely in '
  'the overlap, and resolves in two directions at once. [supports]')

P('4. The New Testament has almost no positive tithe instruction', 'h2')
P('Tax collectors receive seventeen passages. Tithing receives three, and all three are '
  'rebukes: the woes of Matthew 23:23 and Luke 11:42, and the Pharisee\u2019s boast in '
  'Luke 18:12. No one legislates a tenth. [states]')
P('What stands in its place is Hebrews 7 arguing the institution out of force across '
  'eight verses, landing on 7:12 \u2014 a change of priesthood requires a change of law \u2014 '
  'and Paul building a replacement with no fixed rate: weekly, proportional to earnings '
  '(1 Cor 16:2), freely decided and explicitly not under compulsion (2 Cor 9:7). [states]')
P('The practical consequence is that the modern tenth is reimported from the Hebrew Bible '
  'past an argument that the law changed. That is a defensible position, but it is a '
  'position, not a reading. [spec]')

P('5. Both entrusted-money parables reward what the law forbids', 'h2')
P('The master in Matthew 25:27 and the nobleman in Luke 19:23 each fault a servant for '
  'not putting money in the bank to collect interest. Deuteronomy 23:19 forbids charging '
  'interest to a fellow Israelite; Leviticus 25:36\u201337, Exodus 22:25, Psalm 15:5 and '
  'Ezekiel 18:8 repeat the prohibition as a test of righteousness. [states]')
P('Luke 19:11 places its parable immediately after Zacchaeus, and tells us why: people '
  'expected the kingdom to appear immediately. The servant\u2019s charge in 19:22 \u2014 a '
  'harsh man taking what he did not deposit \u2014 is 1 Samuel 8 in parable form, and the '
  'parable ends with the king\u2019s enemies slaughtered in his presence (19:27). Whatever '
  'these parables commend, a straightforward endorsement of the master\u2019s economics is '
  'not available. [supports]')

P('6. Both tithe statutes sit inside chapters that price people', 'h2')
P('Leviticus 27 opens with a schedule of monetary equivalents for human beings \u2014 fifty '
  'shekels for an adult male (27:3), with the priest assessing those too poor to pay '
  '(27:8) \u2014 and only then declares the tithe holy (27:30). Numbers 18 fixes the '
  'redemption of the firstborn at five shekels (18:15\u201316) three verses before assigning '
  'the tithe to the Levites (18:21). [states]')
P('The valuation language runs forward: thirty shekels for a slave killed by an ox '
  '(Exod 21:32), thirty weighed out as the shepherd\u2019s wage (Zech 11:12), thirty pieces '
  'of silver for handing Jesus over (Matt 26:15) \u2014 money the treasury then refuses '
  '(Matt 27:6). [supports]')
P('Reading the tithe statutes without this frame makes them look like pure cultic '
  'instruction. In context they are one line item in a system that also prices persons. '
  '[supports]')

P('7. Every empire exempts the religious establishment', 'h2')
P('Joseph does not buy the Egyptian priests\u2019 land, because they hold a fixed allowance '
  'from Pharaoh (Gen 47:22). Artaxerxes rules it unlawful to impose tribute, custom or toll '
  'on priests, Levites, singers, doorkeepers or temple servants (Ezra 7:24). A Seleucid '
  'decree frees Jerusalem\u2019s tithes and revenues from tax (1 Macc 10:31). [states]')
P('Set against Numbers 18, where the priestly class is landless by design and funded by a '
  'transfer, the exemptions describe a different arrangement entirely: a religious '
  'establishment holding property and shielded from the levy that falls on everyone else. '
  '[supports]')

P('8. The remedy is remission, and it is consistently under-read', 'h2')
P('Deuteronomy 15:1\u20132 mandates remission of debts every seventh year; Leviticus 25 '
  'proclaims liberty and the return of property in the fiftieth. Nehemiah 5:10\u201311 '
  'enacts it \u2014 the taking of interest stopped, fields, orchards and houses restored '
  'that very day. Luke 4:18\u201319 announces release in jubilee vocabulary. [states]')
P('The Nehemiah chapter is usually cited for its description of the crisis. Its remedy is '
  'one paragraph further on. [supports]')

story.append(PageBreak())
P('Where the corpus is thin', 'h1')
B('<b>Babylon barely appears as a tax regime.</b> The corpus gives vassalage, rebellion '
  'and deportation (2 Kgs 24:1), not levies. The honest label is absence of evidence, not '
  'an inference about Babylonian practice.')
B('<b>Rome\u2019s vocabulary is registration and lawfulness,</b> not economics. Augustus '
  'decrees a registration (Luke 2:1); the Gospel controversies ask whether payment is '
  '<i>lawful</i>; the trial charge is that Jesus forbade paying (Luke 23:2). The exception '
  'is 2 Macc 8:10, where tribute owed to Rome is raised by selling captives into slavery.')
B('<b>Assyrian tribute is financed by liquidating sacred property.</b> Menahem exacts from '
  'the wealthy (2 Kgs 15:20); Hezekiah empties the treasury and strips the temple doors '
  '(18:15\u201316); Jehoiakim taxes the land for Pharaoh Neco (23:35). A distinct failure '
  'mode from the land cycle, and under-represented in the graph.')

P('Method, and what it cost', 'h1')
P('Every reference in the corpus resolves against a verse index built from the source PDF. '
  'The build script refuses to write the graph if any reference fails, any edge dangles, '
  'or any warrant tier is misspelled. That check is not decoration \u2014 it caught real '
  'errors twice.')
P('The first indexer produced wrong citations for Matthew 17, Matthew 23 and Luke 11 '
  '\u2014 the three most important tithe passages in the New Testament \u2014 because its '
  'verse-splitter required each number to be exactly one more than the last and broke at '
  'the verses the NRSV omits from its running text. The text it returned was real; only '
  'the labels were false. That is the characteristic shape of a ghost-citation, and it is '
  'why the index exists.')
P('One known gap: Matthew 6:12 cannot be addressed, because the Lord\u2019s Prayer is set '
  'without inline verse numbers in the source. That node points at 6:9, which carries the '
  'whole prayer.', 'note')

P('Standing caution', 'h1')
P('Instructions that reward associative reading \u2014 metaphor, motif, unorthodox '
  'connection \u2014 reliably manufacture connections. A fabricated <i>connection</i> is not '
  'a fabricated <i>fact</i>: every citation can be real while the link between them belongs '
  'to the reader. Warrant tiers are the only counterweight that catches this, and the '
  'speculation tier in this corpus is there to be argued with, not cited.')

doc = SimpleDocTemplate('/mnt/user-data/outputs/findings.pdf', pagesize=LETTER,
                        leftMargin=1.05*inch, rightMargin=1.05*inch,
                        topMargin=0.95*inch, bottomMargin=0.95*inch,
                        title='Tax, Tithe and Tribute \u2014 Findings',
                        author='Bible Study project')

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 8.5)
    canvas.setFillColor(INK2)
    canvas.drawCentredString(LETTER[0]/2, 0.62*inch, str(doc.page))
    canvas.restoreState()

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print('findings.pdf written')
