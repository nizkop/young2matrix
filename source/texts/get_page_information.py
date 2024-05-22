
from source.ui_parts.settings.settings_config import get_language
from source.ui_parts.settings.language_choices import language_choices
from source.ui_parts.ui_pages import ui_pages

# TODO: check content

def get_page_information(page:ui_pages) -> str:
    language = get_language()
    if page == ui_pages.START:
        if language == language_choices.en.name:
            return r"""
            <p>This is the starting page, where you may determine, for which particular permutation group 
            the calculations shall be carried out. </p> <br>
            <b>What is a permutation group?</b>
            <p>The group holding all n! permuations of a set of size n.</p> <br>    
            <b>Why is this relevant?</b>
            <p>
            For example, the basic functions (that you need to calculate molecules) need to have fitting characteristics
            depending on which irreducible representation they should belong to (s. symmetric / antisymmetric parts).
            To construct this basic/basis functions with the accurate properties you can use young diagrams.</p>
            <p>Additionally, if you see the behavior of the young tableaus, you can extrapolate it to the 
            behavior of chemical systems. </p>
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
        if language == language_choices.en.name:
            return """
            <b>What is happening here? </b>
            <p>To describe coupled electrons, spin functions are necessary. This spin functions need to be 
            symmetric/antisymmetric, depending on the electrons, they describe. 
            Young tableaus are able to visualize, which parts are symmetric and which parts are antisymmetric. </p> <br>
            <b>What is a young tableau? </b>
            <p>There are multiple elements in a young tableau; they are displayed next to eachother or above/below eachother.
            This has different meaning: Boxes below eachother represent an antisymmetric combination,
            boxes next to eachother say, that their elements behave symmetrically with regard to eachother. </p>
            <p>The name young tableau is based on the basic form of a tableau: 
            If the number of boxes is only increasing in each row and each column, 
            this mathematical construct is called young diagram/standard tableau. 
            To be precise, another requirement for this is, that the numbers start with 1 
            and that they are increasing by one from there.
            </p>
            """
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
        Spalte jeweils nur zunimmt, wird dieses mathematische Konstrukt Young-Diagramm/Standard-Tableau genannt. 
        Außerdem muss hierfür gelten, dass die Zahlen bei 1 beginnen und von dort in Einerschritten ansteigen. </p>
        """
    if page == ui_pages.MULTIPLIED_OUT_TABLEAUS:
        if language == language_choices.en.name:
            return """
            <b> What are the displayed young tableaus here? </b>
            <p>young tableaus are a visual display of the correlation between symmetric and antisymmetric function parts. 
            Thereby this function parts can be multiplied out to form the meaning of the tableau as an arithmetic function. </p>
            <b> How to interpret young tableaus?</b>
            <p>
            The single elements/boxes/electrons/whatever they should represent,
            become indices of - for now - general functions a,b,c,... that build up the total function. </p>
            """
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
        if language == language_choices.en.name:
            return """
            <b>What is happening here? </b>
            <p>If you want to build spin function, the total basis function has to be build from only two different functions: 
            alpha (α) oder beta (β). This is, because electron are possessing either an alpha spin or a beta spin. 
            There are not other possibilities. </p>
            <b> What was calculated here? </b> 
            <p> 
            The general functions/function parts a,b,c,... were replaced by α or β. 
            This screen shows what is left of the function afterwards; 
            meaning which function parts have not cancelled each other.</p>
            """
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
        if language == language_choices.en.name:
            return """
            <b>What is happening here? </b>
            <p>To describe electrons within a molecule, it is necessary to consider the space they occupate.
            Functions describing the occupational space of an electron, are called orbitals. 
            But here, they are still represented by the general functions a,b,c,...
             </p> </br>       
            <b> What was calculated here? </b> 
            <p> 
            In this application the functions a,b,c,... are not replaced by specific orbitals, 
            to keep the result generally valid. 
            This is why the results for the spatial functions are the same than that of the multiplied out tableaus.</p>
            """
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
        if language == language_choices.en.name:
            function_kind = "spin functions" if page == ui_pages.OVERLAP_SPIN else "spatial functions"
            return f"""
            <b>What is happening here?</b>
            <p>If the {function_kind} are used as basis functions to calculate molecules,
             combinations of them occur. 
             If a function in an integral over the total space is multiplicatively combined with another function  
             (without the interference of an operator acting on one of the functions)
             this is called overlap/overlap integral. </p>
            """
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
        style = """
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
        """
        if language == language_choices.en.name:
            return style + """
                    <b>What is happening here? </b>
                    <p> Quantum chemistry is calculating molecules by solving the (stationary) Schrödinger equation. 
                    This equation combines the wave function (that is build from the prior found basis functions) and 
                    the hamilton opterator <span class='operator'>H<span class='hat'>^</span></span>. 
                    Basically, this adds the kinetic and potential energy to the to-be-calculated system/molecule. </p>
                    <p> combinations of basis functions are called hamilton matrix elements, 
                    when the hamilton operator is acting within the integral. </p>
                    """


        return style+"""
        <b>Worum geht es hier? </b>
        <p> Die Berechnung von Molekülen erfolgt in der Quantenchemie nach der (stationären) Schrödingergleichung. 
        Diese verbindet die Wellenfunktion (bestehend aus den bisher berechneten Basisfunktionen) mit dem sogenannten 
        Hamiltonoperator <span class='operator'>H<span class='hat'>^</span></span>. 
        Dieser bringt im Grunde die kinetische und potentielle Energie des zu berechnenden Systems/Moleküls mit ein. </p>
        <p> Kombinationen von Basisfunktionen, in denen der Hamiltonoperator im Integral wirkt, werden Hamiltonmatrixelemente genannt. </p>
        """
    return "unknown"

