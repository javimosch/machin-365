# A LibreOffice flat-ODS source with awkward content. The values here are the ground truth.
from xml.sax.saxutils import escape as X, quoteattr as Q
def p(s): return "".join("<text:p>%s</text:p>" % X(l).replace("  "," <text:s/>") for l in s.split("\n"))
def S(v, extra=""): return '<table:table-cell office:value-type="string"%s>%s</table:table-cell>' % (extra, p(v))
def N(v, st=""): return '<table:table-cell office:value-type="float" office:value="%s"%s><text:p>%s</text:p></table:table-cell>' % (v, st and ' table:style-name="%s"'%st, v)
def F(f, v, st=""): return '<table:table-cell table:formula=%s office:value-type="float" office:value="%s"%s><text:p>%s</text:p></table:table-cell>' % (Q("of:"+f), v, st and ' table:style-name="%s"'%st, v)
def D(v): return '<table:table-cell office:value-type="date" office:date-value="%s" table:style-name="ceD"><text:p>x</text:p></table:table-cell>' % v
def B(v): return '<table:table-cell office:value-type="boolean" office:boolean-value="%s"><text:p>%s</text:p></table:table-cell>' % (v, v.upper())
E0 = '<table:table-cell/>'
rows = [
 [S("Label"), S("Value"), S("Note")],
 [S("entities"), S('Tom & "Jerry" <b> \'x\''), N("1234567.89")],
 [S("spaces"), S("  two  spaces  "), N("-0.5")],
 [S("newline"), S("first\nsecond"), N("100000005")],
 [S("unicode"), S("Élément ü 漢 😀 €"), N("0.1")],
 ['<table:table-cell office:value-type="string"><text:p>rich </text:p></table:table-cell>'.replace("rich </text:p>", 'plain <text:span text:style-name="T1">bold</text:span> end</text:p>'), S("00042"), S("1E5")],
 [S("date"), D("2026-11-28"), D("2026-01-01")],
 [S("bool"), B("true"), B("false")],
 [S("money"), N("24.9","ceE"), N("0.2","ceP")],
 [S("sum"), F("=SUM([.C2:.C5])","101239580.49"), F("=[.C2]*2","2469135.78")],
 [S("text formula"), '<table:table-cell table:formula="of:=[.A2]&amp;&quot; &lt;ok&gt;&quot;" office:value-type="string"><text:p>entities &lt;ok&gt;</text:p></table:table-cell>', F("=[.C10]+1","101239581.49")],
 [S("merged", ' table:number-columns-spanned="2" table:number-rows-spanned="1"'), '<table:covered-table-cell/>', S("after merge")],
]
def table(name, rs): return '<table:table table:name=%s><table:table-column table:number-columns-repeated="3" table:style-name="co1"/>%s</table:table>' % (Q(name), "".join("<table:table-row>%s</table:table-row>"%"".join(r) for r in rs))
doc = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" office:version="1.2" office:mimetype="application/vnd.oasis.opendocument.spreadsheet">
<office:automatic-styles>
<number:date-style style:name="ND"><number:day number:style="long"/><number:text>/</number:text><number:month number:style="long"/><number:text>/</number:text><number:year number:style="long"/></number:date-style>
<number:number-style style:name="NE"><number:number number:decimal-places="2" number:min-integer-digits="1" number:grouping="true"/><number:text> €</number:text></number:number-style>
<number:percentage-style style:name="NP"><number:number number:decimal-places="0" number:min-integer-digits="1"/><number:text>%</number:text></number:percentage-style>
<style:style style:name="ceD" style:family="table-cell" style:data-style-name="ND"/><style:style style:name="ceE" style:family="table-cell" style:data-style-name="NE"/><style:style style:name="ceP" style:family="table-cell" style:data-style-name="NP"/>
<style:style style:name="co1" style:family="table-column"><style:table-column-properties style:column-width="4cm"/></style:style>
<style:style style:name="T1" style:family="text"><style:text-properties fo:font-weight="bold"/></style:style>
</office:automatic-styles><office:body><office:spreadsheet>''' + table("Main", rows) + table("Second & <sheet>", [[S("on sheet two"), N("2")]]) + "</office:spreadsheet></office:body></office:document>"
open("xl/rich.fods","w").write(doc)
