# -*- coding: utf-8 -*-

# ====================================================================
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ====================================================================

# This sample illustrates how to write an Analyzer 'extension' in Python.
#
#   What is happening behind the scenes ?
#
# The PorterStemmerAnalyzer python class does not in fact extend Analyzer,
# it merely provides an implementation for Analyzer's abstract tokenStream()
# method. When an instance of PorterStemmerAnalyzer is passed to PyLucene,
# with a call to IndexWriter(store, PorterStemmerAnalyzer(), True) for
# example, the PyLucene SWIG-based glue code wraps it into an instance of
# PythonAnalyzer, a proper java extension of Analyzer which implements a
# native tokenStream() method whose job is to call the tokenStream() method
# on the python instance it wraps. The PythonAnalyzer instance is the
# Analyzer extension bridge to PorterStemmerAnalyzer.
import site
site.addsitedir("/usr/local/lib/python2.7/site-packages")

import sys, os, lucene


from java.io import File
from org.apache.lucene.analysis.core import LowerCaseFilter, StopFilter, StopAnalyzer
from org.apache.lucene.analysis.en import PorterStemFilter
from org.apache.lucene.analysis.standard import StandardTokenizer, StandardFilter
from org.apache.lucene.util import Version
from org.apache.pylucene.analysis import PythonAnalyzer

from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, Term, DirectoryReader
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.analysis.de import GermanAnalyzer


class PorterStemmerAnalyzer(PythonAnalyzer):

    def createComponents(self, fieldName, reader):

        source = StandardTokenizer(Version.LUCENE_CURRENT, reader)
        print source
        filter = StandardFilter(Version.LUCENE_CURRENT, source)

        #filter = PorterStemFilter(filter)
        #filter = StopFilter(Version.LUCENE_CURRENT, filter, StopAnalyzer.ENGLISH_STOP_WORDS_SET)

        return self.TokenStreamComponents(source, source)


if __name__ == '__main__':
    test_text = """Berlin/Hamburg - Manche Bitten klingen ganz harmlos, sind aber als Befehle zu verstehen. Eine solche als Bitte getarnte Vorladung verschärft jetzt den Machtkampf in der AfD - und könnte ihn eskalieren lassen.

"Wir wenden uns mit der Bitte um ein offenes und ehrliches Gespräch an Sie", so beginnt der Brief einiger prominenter AfD-Funktionäre an Bernd Lucke, den prominentesten von drei Parteivorsitzenden, in der AfD offiziell Sprecher genannt.
Das Drei-Seiten-Papier hat es in sich: "Führung nach Gutsherrenart" werfen die Verfasser Lucke vor, von "Drohungen" ist die Rede, von Aktionen "ohne Rücksprache" mit dem Parteivorstand. Am Ende des Schreibens steht ein Gesprächstermin, der 18. Januar, 9 Uhr; da soll sich Lucke in Frankfurt am Main einfinden.

Es ist der bislang schärfste Angriff wichtiger AfD-Funktionäre auf Lucke, das Gesicht der Partei. Zu den Unterzeichnern gehören seine beiden Co-Vorsitzenden Frauke Petry und Konrad Adam, aber auch der brandenburgische Landeschef Alexander Gauland und die Europaabgeordneten Beatrix von Storch und Marcus Pretzell. Die Unterschriften der beiden letztgenannten dürften Lucke besonders wurmen: Weder Storch noch Pretzell sitzen im Bundesvorstand; in der Partei-Hierarchie stehen sie deutlich unter ihm.

Damit die Aktion nicht unbemerkt bleibt, hat Petry den Brief über ihren Mailaccount in CC auch an alle Landesvorsitzenden der AfD geschickt.

Die Briefschreiber wollen so verhindern, dass Lucke beim Parteitag Ende Januar eine Satzungsänderung durchsetzt und fortan die AfD als alleiniger Vorsitzender lenkt. Sie werfen Lucke besonders einen Alleingang im Vorfeld des Parteitages vor: Er hatte seinerseits ohne Absprache alle Kreisvorsitzenden für den 18. Januar zu einem gesonderten Vortreffen nach Frankfurt eingeladen. Petry und Co., die eine Doppel- oder Dreierspitze für die AfD wollen, hatten vergeblich versucht, ihn davon abzubringen. Sie fürchten nicht zu Unrecht, Lucke werde dort versuchen, die Funktionäre "auf Linie" zu bringen.
Nun wollen sie Lucke ausmanövrieren: Für ihre Einladung zum Tribunal haben die Briefeschreiber exakt den Tag gewählt, an dem Lucke sein Treffen in Frankfurt abhalten wollte. Lucke hatte für 12 Uhr eingeladen - nun soll er sich am selben Tag um 9 Uhr seinen Kritikern stellen. Aus dieser Runde dürfte er wohl kaum gestärkt in die nächste gehen.

Mit seiner als privat deklarierten Einladung hat Lucke seinen Kritikern das beste Argument geliefert: Jetzt können sie ihn als machtgeilen Alleinherrscher darstellen. "Drohungen sind keine vertrauensbildende Maßnahme", schreiben sie und geben sich unschuldig. "Wie erst mag eine solche Drohung wirken, wenn sie ein alleiniger Vorsitzender ausspricht?"

Bei dem Machtkampf geht es auch um die strategische Ausrichtung der AfD. Die Briefeschreiber wollen die Partei weiter öffnen für "Menschen, die eine islamische Überfremdung fürchten", wie sie schreiben, und für solche, die über "den Einfluss amerikanischer Banken auf die Politik oder die Souveränität Deutschlands nachdächten". Die Botschaft lautet: Pegida-Anhänger, Verschwörungstheoretiker, ihr seid willkommen.

Petry und Gauland haben längst öffentlichkeitswirksam solche Signale gesendet: Petry lud jüngst die Pegida-Organisatoren zu einem Treffen mit ihrer sächsischen Landtagsfraktion ein. Gauland kam, wie er sagt, vor wenigen Wochen "als Beobachter" zu einem Pegida-Marsch - und verteidigte die Anti-Islam-Bewegung mehrfach. Lucke wollen die Briefschreiber nur das Euro-Thema überlassen, das längst nicht mehr das populärste ist.

Schon oft hat es in strategischen Fragen geknirscht zwischen Lucke und seinen Vorstandskollegen. Doch bislang versuchte die Parteispitze immer nach Kräften, den Anschein der Geschlossenheit zu vermitteln.
Petry achtete bei ihren strategischen Alleingängen, etwa im Umgang mit Überläufern der rechtspopulistischen "Freiheit"-Partei, stets geschickt darauf, alles nach den Regeln der Form zu machen. Eigene Aktionen leistete sie sich nur in ihrem Territorium Sachsen, auf Bundesebene lief immer alles nach Absprache.

Der Brief jetzt lässt aber keinen Zweifel, dass der Bruch endgültig ist - und dass Petry und ihre Mitstreiter bereit sind, den Parteichef frontal anzugreifen.

Ankara/Istanbul - Vor 92 Jahren wurde die Türkische Republik gegründet. Bislang hat es im laut Verfassung laizistischen Staat keinen einzigen Neubau einer christlichen Kirche gegeben. Das wird sich nun offenbar bald ändern. Die Regierung hat laut übereinstimmenden Zeitungsberichten den Bau einer Kirche genehmigt. Das Gotteshaus für die christliche syrische Minderheit soll im Istanbuler Stadtteil Yesilköy am Marmarameer auf städtischem Grund und Boden entstehen.

Über die Genehmigung berichten sowohl die Nachrichtenagentur AFP unter Berufung auf türkische Regierungskreise als auch türkische Zeitungen wie "Hürriyet" oder die englische Onlineausgaben von "Sabah" sowie "World Bulletin". Offenbar wurde die Entscheidung im Rahmen eines Treffens von Regierungschef Ahmet Davutoglu mit Vertretern nichtmuslimischer Religionsgemeinschaften am Freitag bekannt gegeben.
Stiftung soll Kirchenbau bezahlen

Bislang wurden in der modernen Türkei Kirchen lediglich saniert oder wieder für die Öffentlichkeit zugänglich gemacht. Ein Neubau ist aber noch nie genehmigt worden. Die Bevölkerung der Türkei ist zu 99 Prozent muslimischen Glaubens. Der Staatsführung um Präsident Recep Tayyip Erdogan wird von Kritikern vorgeworfen, das Land islamisieren zu wollen.

Angehörige christlicher Minderheiten werden in der Türkei vereinzelt Opfer von religiös motivierter Gewalt. Papst Franziskus hatte erst vor etwas mehr als einem Monat bei seinem Türkei-Besuch deutlich Meinungs- und Glaubensfreiheit gefordert.

Der christlichen syrischen Minderheit in der Türkei gehören etwa 20.000 Menschen an. Es handelt sich um orthodoxe und katholische Christen, die vor allem im Südosten des Landes leben. Der Bau der neuen Kirche soll aus den Mitteln einer Stiftung bezahlt und in den kommenden Monaten begonnen werden.

Berlin - "Gentrifizierung, die: Aufwertung eines Stadtteils durch dessen Sanierung oder Umbau mit der Folge, dass die dort ansässige Bevölkerung durch wohlhabendere Bevölkerungsschichten verdrängt wird."

So beschreibt der Duden ein Phänomen, das vor allem in Großstädten zu beobachten ist: Viele Menschen ziehen in günstige Wohnviertel, durch die Nachfrage steigen die Preise, bis die Mieten schließlich nur noch für die Wohlhabenderen bezahlbar sind - und die Künstler, Studenten, Geringverdiener weichen müssen. In der Weihnachtszeit hat nun ein Fall aus Berlin für Aufsehen gesorgt, der von einigen als Beispiel für Gentrifizierung genannt wird. Auf Facebook hat ein Nutzer die aktuelle Infobroschüre einer evangelischen Kirchengemeinde in Berlin-Mitte gepostet, Seite 25, Rubrik "Taufen". 29 Namen von Kindern und Erwachsenen sind dort zu lesen, darunter die folgenden:
Viktor Paul Theodor, Ada Mai Helene, Rufus Oliver Friedrich, Cäcilie Helene, Edvard Neo, Freya Luise Apollonia, Frederick Theodor Heinrich, Leonore Anna Maria Chiara Helena. Viele der Nachnamen lassen zudem auf einen adligen Hintergrund schließen.

"Das Comeback alter Adelsgeschlechter in Berlin-Mitte = Gentrifizierung im eigentlichen Sinne", lautet ein Kommentar unter dem Facebook-Foto. "In Dresden Gorbitz sähe die Liste anders aus", schreibt ein anderer Nutzer. Ein dritter fasst zusammen: "So heißt also die Gentrifizierung."

Im "Gentrification Blog", betrieben von einem wissenschaftlichen Mitarbeiter der Berliner Humboldt-Universität, ist vor kurzem ein Beitrag zu der Taufliste erschienen: "Berlin: Am Taufbecken der Gentrification - Kirche im Aufwertungsgebiet" heißt er. Die Liste lese sich "wie eine Mischung aus FDP-Wahlliste für das Europaparlament und dem Verzeichnis der höheren Beamten des Diplomatischen Dienstes", heißt es in dem Artikel. Und: "Der Wortsinn der Gentrification - der ja auf die Wiederkehr des niederen Landadels (der Gentry) in den Städten anspielt - bekommt hier jedenfalls einen unerwarteten Realitätsgehalt."

Zu dem Artikel stellte der Autor eine Taufliste aus dem Jahr 2007 aus einer Gemeinde im benachbarten Stadtteil Prenzlauer Berg. Darauf sind unter anderem diese Namen zu finden: Ruby, Matteo, Iwan, Lennart, Emilia, Annabelle, Andreas, Anke.

Jene Kirchgemeinde, in der die mondänen Namen zur Taufe aufgeführt sind, listet auch die Verstorbenen auf. Zwei sind es in der aktuellen Infobroschüre. Nzitu. Und: Herbert."""

    lucene.initVM()

    # language processor and storage
    analyzer = PorterStemmerAnalyzer(Version.LUCENE_CURRENT)
    store = SimpleFSDirectory(File('./data-test/'))

    # writes data to the index
    config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer, overwrite=True)
    writer = IndexWriter(store, config)

    # add Document
    doc = Document()
    doc.add(Field('content', test_text, Field.Store.YES, Field.Index.ANALYZED))
    doc.add(Field('url', "http://test.com", Field.Store.YES, Field.Index.NOT_ANALYZED))
    writer.updateDocument(Term("url", "http://test.com"), doc)

    writer.commit()
    writer.close()