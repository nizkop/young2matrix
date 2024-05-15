
from source.ui_parts.settings.idea_config import get_language
from source.ui_parts.ui_pages import ui_pages

# TODO: check content, english version; title for each page

def get_page_information(page:ui_pages) -> str:
    language = get_language()
    if page == ui_pages.START:
        if language == "en":
            return """
            This is the start page. Here, you determine which permutation group you want to calculate. 
            \n<b>What is a permutation group?</b>
            """
        else:
            return r"""
            <p>Dies ist die Startseite, auf der Sie festlegen können, 
            für welche Permutationsgruppe die Berechnungen gelten sollen.</p> <br>
            <b>Was ist eine Permutationsgruppe?</b>
            <p>Die Gruppe, die alle n! Permuationen einer Menge der Größe n, beinhaltet.</p> <br>    
            <b>Welche Relevanz hat das?</b>
            <p>Beispielsweise Basisfunktionen (die zur Berechnung von Molekülen notwendig sind) müssen je nach ihrer 
            Zuordnung zu einer irreduziblen Darstellung gewisse Anforderungen erfüllen 
            (s. symmetrische/antisymmetrische Anteile). 
            Die Konstruktion von Basisfunktionen mit hierzu passenden Eigenschaften
             kann mit Hilfe von Young-Diagrammen erfolgen.</p>
            <p>Außerdem wird aus dem Verhalten der Young-Tableaus das Verhalten der enthaltenen Basisfunktionen 
            erkennbar und ggf. sind Rückschlüsse auf das chemische System möglich. </p>
            """
    if page == ui_pages.TABLEAUS:
        return """
        <b>Worum geht es hier? </b>
        <p>Um gekoppelte Elektronen zu beschreiben, werden Spinfunktionen benötigt, 
        die entsprechend der Elektronenspins symmetrisch/antisymmetrisch sind. 
        Welche Teile dieser Funktionen symmetrisch oder antisymmetrisch sind, 
        lässt sich durch Young-Tableaus visualisieren. </p> <br>
        <b>Was ist ein Young-Tableau? </b>
        <p>Es werden Elemente in Kästchen neben- und untereinander dargestellt. 
        Kästchen untereinander stehen für eine antisymmetrische Kombination,
        wenn Kästchen nebeneinander liegen, verhalten sich ihre Elemente symmetrisch zueinander. </p>
        <p>Der Name Young-Tableau stammt von der Grundform: Wenn die Anzahl der Kästchen in einer Reihe und in einer 
        Spalte jeweils nur zunimmt, wird dieses mathematische Konstrukt Young-Diagramm/Standard-Tableau genannt.</p>
        """
    if page == ui_pages.MULTIPLIED_OUT_TABLEAUS:
        return """
        <b> Was sind die hier dargestellten Young-Tableaus? </b>
        <p>Young-Tableaus sind eine visuelle Darstellung der Zusammenhänge symmetrischer und 
        antisymmetrischer Funktionsteile. Dementsprechend lassen sich die dahinterliegenden Funktionsteile auch 
        ausmultiplizieren und so kann die Aussage, die hinter der Tableau-Darstellung steckt, 
        als arithmetische Formel angegeben werden. </p>
        <b> Wie sind die Young-Tableaus zu interpretieren?</b>
        <p>Die einzelnen Elementen/Kästchen/Elektronen/oder was auch immer diese repräsentieren sollen, 
        werden dabei zu Indizes an - zuerst einmal - allgemeinen Funktionen a,b,c,...,
        aus denen sich die Gesamtfunktion zusammensetzt. </p>
        """
    if page == ui_pages.SPIN:
        return """
        <b>Worum geht es hier? </b>
        <p>Sollen Spinfunktionen ermittelt werden, besteht die gesamte Basisfunktion maximal aus zwei verschiedenen 
        Funktionen: alpha (α) oder beta (β). Denn die Elektronen besitzen entweder einen alpha-Spin, oder einen beta-Spin. 
        Mehr Möglichkeiten gibt es nicht. </p>
        <b> Was wurde hier berechnet? </b> 
        <p> Die allgemeinen Funktionen/Funktionsteile a,b,c,... wurden hier durch α oder β ersetzt. 
        Diese Seite zeigt die danach übrigen Funktionsteile an. 
        Also die Teile, die sich nach dem Einsetzen nicht gegenseitig aufheben. </p>
        """
    if page == ui_pages.SPATIAL_FUNCTIONS:
        return """
        <b>Worum geht es hier? </b>
        <p>Um Elektronen in einem Molekül zu beschreiben, muss berücksichtigt werden, wie der Raum aussieht, 
        in dem sie sich befinden. Funktionen, die den Aufenthaltsraum/räumlichen Anteil von einem Elektron beschreiben, 
        werden Orbitale genannt. Diese werden hier allerdings weiterhin mit den allgemeinen Funktionen a,b,c,...
        dargestellt.
         </p> </br>       
        <b> Was wurde hier berechnet? </b> 
        <p> In dieser Anwendung werden keine spezifischen Orbitale für die Funktionen a,b,c,... eingesetzt, 
        um allgemeine Ergebnisse zu liefern. 
        Daher entsprechen die Ergebnisse für die Raumfunktionen dem Allgemeinfall ausmultiplizierter Tableaus.</p>
        """
    if page == ui_pages.OVERLAP_SPIN or page == ui_pages.OVERLAP_SPATIAL:
        function_kind = "Spinfunktionen" if page == ui_pages.OVERLAP_SPIN else "Raumfunktionen"
        return f"""
        <b>Worum geht es hier?</b>
        <p>Wenn die {function_kind} als Basisfunktionen zur Berechnung von Molekülen genutzt werden, 
        tauchen Kombinationen von ihnen in Integralen auf. 
        Wenn in einem Integral über den ganzen Raum eine Funktion multiplikativ mit einer anderen Funktion kombiniert 
        wird (ohne dass ein weiterer Opterator auf eine der Funktionen wirkt), 
        wird dies Überlapp/Überlappintegral genannt. </p>
        """
    if page == ui_pages.HAMILTON_SPIN or page == ui_pages.HAMILTON_SPATIAL:
        return """
        <style>
        .operator {
            position: relative;
            display: inline-block;
        }

        .hat {
            position: absolute;
            top: -0.6em;
            left: 50%;
            transform: translateX(-50%);
        }
    </style>
        <b>Worum geht es hier? </b>
        <p> Die Berechnung von Molekülen erfolgt in der Quantenchemie nach der (stationären) Schrödingergleichung. 
        Diese verbindet die Wellenfunktion (bestehend aus den bisher berechneten Basisfunktionen) mit dem sogenannten 
        Hamiltonoperator <span class='operator'>H<span class='hat'>^</span></span>. 
        Dieser bringt im Grunde die kinetische und potentielle Energie des zu berechnenden Systems/Moleküls mit ein. </p>
        <p> Kombinationen von Basisfunktionen, in denen der Hamiltonoperator im Integral wirkt, werden Hamiltonmatrixelemente genannt. </p>
        """
    return "unknown"

