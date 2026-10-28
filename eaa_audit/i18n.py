"""Statement texts per language."""

SC_NAMES = {'en': {'1.1.1': 'Non-text content (images without text alternatives)',
        '1.2.1': 'Audio-only and video-only content',
        '1.2.2': 'Captions for video',
        '1.3.1': 'Info and relationships (structure)',
        '1.3.5': 'Identify input purpose',
        '1.4.1': 'Use of colour (links distinguishable from text)',
        '1.4.2': 'Audio control',
        '1.4.3': 'Contrast (minimum)',
        '1.4.4': 'Resize text',
        '2.1.1': 'Keyboard access',
        '2.2.1': 'Timing adjustable',
        '2.2.2': 'Pause, stop, hide',
        '2.4.1': 'Bypass blocks',
        '2.4.2': 'Page titled',
        '2.4.3': 'Focus order',
        '2.4.4': 'Link purpose',
        '2.4.6': 'Headings and labels',
        '2.4.7': 'Focus visible',
        '2.4.11': 'Focus not obscured (minimum)',
        '2.5.7': 'Dragging movements',
        '2.5.8': 'Target size (minimum)',
        '3.1.1': 'Language of page',
        '3.3.2': 'Labels or instructions',
        '3.3.8': 'Accessible authentication (minimum)',
        '4.1.2': 'Name, role, value'},
 'ro': {'1.1.1': 'Conținut non-text (imagini fără alternativă text)',
        '1.2.1': 'Conținut doar audio sau doar video',
        '1.2.2': 'Subtitrări pentru video',
        '1.3.1': 'Informații și relații (structură)',
        '1.3.5': 'Identificarea scopului câmpurilor',
        '1.4.1': 'Utilizarea culorii (linkuri distincte de text)',
        '1.4.2': 'Controlul sunetului',
        '1.4.3': 'Contrast (minim)',
        '1.4.4': 'Redimensionarea textului',
        '2.1.1': 'Acces de la tastatură',
        '2.2.1': 'Timp ajustabil',
        '2.2.2': 'Pauză, oprire, ascundere',
        '2.4.1': 'Ocolirea blocurilor repetitive',
        '2.4.2': 'Titlul paginii',
        '2.4.3': 'Ordinea focalizării',
        '2.4.4': 'Scopul linkurilor',
        '2.4.6': 'Titluri și etichete',
        '2.4.7': 'Focalizare vizibilă',
        '2.4.11': 'Focalizare neacoperită (minim)',
        '2.5.7': 'Mișcări de tragere',
        '2.5.8': 'Dimensiunea țintei (minim)',
        '3.1.1': 'Limba paginii',
        '3.3.2': 'Etichete sau instrucțiuni',
        '3.3.8': 'Autentificare accesibilă (minim)',
        '4.1.2': 'Nume, rol, valoare'},
 'de': {'1.1.1': 'Nicht-Text-Inhalt (Bilder ohne Textalternative)',
        '1.2.1': 'Reine Audio- oder Videoinhalte',
        '1.2.2': 'Untertitel für Videos',
        '1.3.1': 'Info und Beziehungen (Struktur)',
        '1.3.5': 'Zweck von Eingabefeldern bestimmen',
        '1.4.1': 'Verwendung von Farbe (Links vom Text unterscheidbar)',
        '1.4.2': 'Audiosteuerung',
        '1.4.3': 'Kontrast (Minimum)',
        '1.4.4': 'Textgröße ändern',
        '2.1.1': 'Tastaturbedienung',
        '2.2.1': 'Zeitvorgaben anpassbar',
        '2.2.2': 'Pausieren, beenden, ausblenden',
        '2.4.1': 'Blöcke umgehen',
        '2.4.2': 'Seitentitel',
        '2.4.3': 'Fokusreihenfolge',
        '2.4.4': 'Linkzweck',
        '2.4.6': 'Überschriften und Beschriftungen',
        '2.4.7': 'Sichtbarer Fokus',
        '2.4.11': 'Fokus nicht verdeckt (Minimum)',
        '2.5.7': 'Ziehbewegungen',
        '2.5.8': 'Zielgröße (Minimum)',
        '3.1.1': 'Sprache der Seite',
        '3.3.2': 'Beschriftungen oder Anweisungen',
        '3.3.8': 'Barrierefreie Authentifizierung (Minimum)',
        '4.1.2': 'Name, Rolle, Wert'},
 'fr': {'1.1.1': 'Contenu non textuel (images sans alternative textuelle)',
        '1.2.1': 'Contenu uniquement audio ou vidéo',
        '1.2.2': 'Sous-titres des vidéos',
        '1.3.1': 'Information et relations (structure)',
        '1.3.5': 'Identification de la finalité des champs',
        '1.4.1': 'Utilisation de la couleur (liens distincts du texte)',
        '1.4.2': 'Contrôle du son',
        '1.4.3': 'Contraste (minimum)',
        '1.4.4': 'Redimensionnement du texte',
        '2.1.1': 'Accès au clavier',
        '2.2.1': 'Délai réglable',
        '2.2.2': 'Pause, arrêt, masquage',
        '2.4.1': 'Contourner les blocs',
        '2.4.2': 'Titre de page',
        '2.4.3': 'Ordre de focus',
        '2.4.4': 'Fonction du lien',
        '2.4.6': 'En-têtes et étiquettes',
        '2.4.7': 'Focus visible',
        '2.4.11': 'Focus non masqué (minimum)',
        '2.5.7': 'Mouvements de glissement',
        '2.5.8': 'Taille de la cible (minimum)',
        '3.1.1': 'Langue de la page',
        '3.3.2': 'Étiquettes ou instructions',
        '3.3.8': 'Authentification accessible (minimum)',
        '4.1.2': 'Nom, rôle, valeur'},
 'es': {'1.1.1': 'Contenido no textual (imágenes sin alternativa de texto)',
        '1.2.1': 'Contenido solo de audio o solo de vídeo',
        '1.2.2': 'Subtítulos de vídeo',
        '1.3.1': 'Información y relaciones (estructura)',
        '1.3.5': 'Identificar el propósito de los campos',
        '1.4.1': 'Uso del color (enlaces distinguibles del texto)',
        '1.4.2': 'Control del audio',
        '1.4.3': 'Contraste (mínimo)',
        '1.4.4': 'Cambio de tamaño del texto',
        '2.1.1': 'Teclado',
        '2.2.1': 'Tiempo ajustable',
        '2.2.2': 'Pausar, detener, ocultar',
        '2.4.1': 'Evitar bloques',
        '2.4.2': 'Título de página',
        '2.4.3': 'Orden del foco',
        '2.4.4': 'Propósito de los enlaces',
        '2.4.6': 'Encabezados y etiquetas',
        '2.4.7': 'Foco visible',
        '2.4.11': 'Foco no oculto (mínimo)',
        '2.5.7': 'Movimientos de arrastre',
        '2.5.8': 'Tamaño del objetivo (mínimo)',
        '3.1.1': 'Idioma de la página',
        '3.3.2': 'Etiquetas o instrucciones',
        '3.3.8': 'Autenticación accesible (mínimo)',
        '4.1.2': 'Nombre, función, valor'},
 'it': {'1.1.1': 'Contenuti non testuali (immagini senza alternativa testuale)',
        '1.2.1': 'Contenuti solo audio o solo video',
        '1.2.2': 'Sottotitoli per i video',
        '1.3.1': 'Informazioni e relazioni (struttura)',
        '1.3.5': 'Identificare lo scopo dei campi',
        '1.4.1': 'Uso del colore (link distinguibili dal testo)',
        '1.4.2': "Controllo dell'audio",
        '1.4.3': 'Contrasto (minimo)',
        '1.4.4': 'Ridimensionamento del testo',
        '2.1.1': 'Tastiera',
        '2.2.1': 'Tempo regolabile',
        '2.2.2': 'Pausa, stop, nascondi',
        '2.4.1': 'Salto dei blocchi',
        '2.4.2': 'Titolo della pagina',
        '2.4.3': 'Ordine del focus',
        '2.4.4': 'Scopo del link',
        '2.4.6': 'Intestazioni ed etichette',
        '2.4.7': 'Focus visibile',
        '2.4.11': 'Focus non nascosto (minimo)',
        '2.5.7': 'Movimenti di trascinamento',
        '2.5.8': 'Dimensione del bersaglio (minimo)',
        '3.1.1': 'Lingua della pagina',
        '3.3.2': 'Etichette o istruzioni',
        '3.3.8': 'Autenticazione accessibile (minimo)',
        '4.1.2': 'Nome, ruolo, valore'}}

T = {'en': {'title': 'Accessibility statement for {org}',
        'intro': '{org} is committed to making {site} accessible to people with disabilities, in '
                 'line with the European Accessibility Act (Directive (EU) 2019/882) and the '
                 'standard EN 301 549, which refers to the Web Content Accessibility Guidelines '
                 '(WCAG).',
        'law': 'National law: {law}.',
        'alts': 'Accessible alternatives available for the content above:',
        'tech': 'Technologies this website relies on: {tech}.',
        'review': 'We review this statement at least every {months} months.',
        'h_status': 'Conformance status',
        'status_partial': '{site} is partially conformant with EN 301 549 (which requires WCAG 2.1 '
                          'level AA). We also check the newer WCAG 2.2 criteria. Partially '
                          'conformant means that some parts of the content do not fully meet the '
                          'standard.',
        'status_full': '{site} is fully conformant with EN 301 549 (WCAG 2.1 level AA) and the '
                       'WCAG 2.2 level AA criteria we checked, based on the evaluation described '
                       'below.',
        'h_limits': 'Known limitations',
        'limits_none': 'The automated check found no failures. This does not prove that the site '
                       'has no barriers.',
        'limits_intro': 'The following content does not yet meet the requirements:',
        'limit_line': '{sc} {name}: {n} place(s) on {pages} page(s)',
        'review_intro': 'These points were flagged for human review and may also be barriers:',
        'manual_intro': 'These aspects cannot be verified by an automated tool and are {state}:',
        'manual_done': 'covered by our manual evaluation',
        'manual_todo': 'not yet evaluated',
        'h_micro': 'Exemption',
        'micro': '{org} is a microenterprise within the meaning of Directive (EU) 2019/882 (fewer '
                 'than 10 employees and annual turnover or balance sheet total of at most EUR 2 '
                 'million). Service-related accessibility requirements do not legally apply to it; '
                 'we publish this statement voluntarily and work to improve accessibility '
                 'gradually.',
        'h_measures': 'Measures to support accessibility',
        'measures_default': 'We check pages with an automated tool before release.',
        'h_feedback': 'Feedback and contact',
        'feedback': 'If you cannot use part of this website, contact us and describe the problem '
                    'and the page. We will reply within {days} days.',
        'contact_email': 'E-mail: {v}',
        'contact_phone': 'Phone: {v}',
        'contact_addr': 'Address: {v}',
        'h_enforce': 'Enforcement procedure',
        'enforce': 'If you are not satisfied with our reply, you can complain to the competent '
                   'authority: {auth}.',
        'h_prep': 'Preparation of this statement',
        'prep': 'This statement was prepared on {date}. Method: automated scan of {pages} page(s) '
                'with EAA Site Auditor{manual}.',
        'prep_manual': ' and manual evaluation ({who})'},
 'ro': {'title': 'Declarație de accesibilitate pentru {org}',
        'intro': '{org} se angajează să facă {site} accesibil persoanelor cu dizabilități, în '
                 'conformitate cu Actul european privind accesibilitatea (Directiva (UE) 2019/882) '
                 'și cu standardul EN 301 549, care face trimitere la Ghidul pentru '
                 'accesibilitatea conținutului web (WCAG).',
        'law': 'Legislația națională: {law}.',
        'alts': 'Alternative accesibile disponibile pentru conținutul de mai sus:',
        'tech': 'Tehnologii pe care se bazează acest site: {tech}.',
        'review': 'Revizuim această declarație cel puțin o dată la {months} luni.',
        'h_status': 'Starea de conformitate',
        'status_partial': '{site} este parțial conform cu EN 301 549 (care cere WCAG 2.1 nivel '
                          'AA). Verificăm și criteriile mai noi din WCAG 2.2. Parțial conform '
                          'înseamnă că unele părți ale conținutului nu respectă pe deplin '
                          'standardul.',
        'status_full': '{site} este pe deplin conform cu EN 301 549 (WCAG 2.1 nivel AA) și cu '
                       'criteriile WCAG 2.2 nivel AA verificate, pe baza evaluării descrise mai '
                       'jos.',
        'h_limits': 'Limitări cunoscute',
        'limits_none': 'Verificarea automată nu a găsit erori. Acest lucru nu dovedește că site-ul '
                       'nu are bariere.',
        'limits_intro': 'Următorul conținut nu respectă încă cerințele:',
        'limit_line': '{sc} {name}: {n} locuri pe {pages} pagini',
        'review_intro': 'Aceste puncte au fost semnalate pentru verificare manuală și pot '
                        'constitui bariere:',
        'manual_intro': 'Aceste aspecte nu pot fi verificate de un instrument automat și sunt '
                        '{state}:',
        'manual_done': 'acoperite de evaluarea noastră manuală',
        'manual_todo': 'încă neevaluate',
        'h_micro': 'Derogare',
        'micro': '{org} este o microîntreprindere în sensul Directivei (UE) 2019/882 (mai puțin de '
                 '10 angajați și cifră de afaceri anuală sau total bilanț de maximum 2 milioane '
                 'EUR). Cerințele de accesibilitate pentru servicii nu i se aplică legal; publicăm '
                 'această declarație voluntar și îmbunătățim accesibilitatea treptat.',
        'h_measures': 'Măsuri pentru sprijinirea accesibilității',
        'measures_default': 'Verificăm paginile cu un instrument automat înainte de publicare.',
        'h_feedback': 'Feedback și contact',
        'feedback': 'Dacă nu puteți utiliza o parte a acestui site, contactați-ne și descrieți '
                    'problema și pagina. Vă vom răspunde în {days} zile.',
        'contact_email': 'E-mail: {v}',
        'contact_phone': 'Telefon: {v}',
        'contact_addr': 'Adresă: {v}',
        'h_enforce': 'Procedura de aplicare',
        'enforce': 'Dacă nu sunteți mulțumit de răspunsul nostru, puteți depune o plângere la '
                   'autoritatea competentă: {auth}.',
        'h_prep': 'Elaborarea acestei declarații',
        'prep': 'Declarația a fost elaborată la {date}. Metodă: scanare automată a {pages} pagini '
                'cu EAA Site Auditor{manual}.',
        'prep_manual': ' și evaluare manuală ({who})'},
 'de': {'title': 'Erklärung zur Barrierefreiheit für {org}',
        'intro': '{org} bemüht sich, {site} für Menschen mit Behinderungen zugänglich zu machen, '
                 'gemäß dem Europäischen Barrierefreiheitsgesetz (Richtlinie (EU) 2019/882) und '
                 'der Norm EN 301 549, die auf die Web Content Accessibility Guidelines (WCAG) '
                 'verweist.',
        'law': 'Nationales Recht: {law}.',
        'alts': 'Barrierefreie Alternativen für die oben genannten Inhalte:',
        'tech': 'Technologien, auf die sich diese Website stützt: {tech}.',
        'review': 'Wir überprüfen diese Erklärung mindestens alle {months} Monate.',
        'h_status': 'Stand der Vereinbarkeit',
        'status_partial': '{site} ist teilweise mit EN 301 549 (die WCAG 2.1 Stufe AA verlangt) '
                          'vereinbar. Wir prüfen zusätzlich die neueren Kriterien von WCAG 2.2. '
                          'Teilweise vereinbar bedeutet, dass einige Inhalte die Norm nicht '
                          'vollständig erfüllen.',
        'status_full': '{site} ist auf Grundlage der unten beschriebenen Bewertung vollständig mit '
                       'EN 301 549 (WCAG 2.1 Stufe AA) und den geprüften WCAG-2.2-Kriterien Stufe '
                       'AA vereinbar.',
        'h_limits': 'Bekannte Einschränkungen',
        'limits_none': 'Die automatische Prüfung hat keine Fehler gefunden. Das beweist nicht, '
                       'dass die Website barrierefrei ist.',
        'limits_intro': 'Die folgenden Inhalte erfüllen die Anforderungen noch nicht:',
        'limit_line': '{sc} {name}: {n} Stelle(n) auf {pages} Seite(n)',
        'review_intro': 'Diese Punkte wurden zur manuellen Prüfung markiert und können ebenfalls '
                        'Barrieren sein:',
        'manual_intro': 'Diese Aspekte kann ein automatisches Werkzeug nicht prüfen; sie sind '
                        '{state}:',
        'manual_done': 'durch unsere manuelle Bewertung abgedeckt',
        'manual_todo': 'noch nicht bewertet',
        'h_micro': 'Ausnahme',
        'micro': '{org} ist ein Kleinstunternehmen im Sinne der Richtlinie (EU) 2019/882 (weniger '
                 'als 10 Beschäftigte und Jahresumsatz oder Bilanzsumme von höchstens 2 Mio. EUR). '
                 'Die Barrierefreiheitsanforderungen für Dienstleistungen gelten rechtlich nicht '
                 'für uns; wir veröffentlichen diese Erklärung freiwillig und verbessern die '
                 'Barrierefreiheit schrittweise.',
        'h_measures': 'Maßnahmen zur Unterstützung der Barrierefreiheit',
        'measures_default': 'Wir prüfen Seiten vor der Veröffentlichung mit einem automatischen '
                            'Werkzeug.',
        'h_feedback': 'Rückmeldung und Kontakt',
        'feedback': 'Wenn Sie einen Teil dieser Website nicht nutzen können, schreiben Sie uns und '
                    'beschreiben Sie das Problem und die Seite. Wir antworten innerhalb von {days} '
                    'Tagen.',
        'contact_email': 'E-Mail: {v}',
        'contact_phone': 'Telefon: {v}',
        'contact_addr': 'Anschrift: {v}',
        'h_enforce': 'Durchsetzungsverfahren',
        'enforce': 'Wenn Sie mit unserer Antwort nicht zufrieden sind, können Sie sich an die '
                   'zuständige Behörde wenden: {auth}.',
        'h_prep': 'Erstellung dieser Erklärung',
        'prep': 'Diese Erklärung wurde am {date} erstellt. Methode: automatische Prüfung von '
                '{pages} Seite(n) mit EAA Site Auditor{manual}.',
        'prep_manual': ' und manuelle Bewertung ({who})'},
 'fr': {'title': "Déclaration d'accessibilité de {org}",
        'intro': "{org} s'engage à rendre {site} accessible aux personnes handicapées, "
                 "conformément à l'Acte européen sur l'accessibilité (directive (UE) 2019/882) et "
                 "à la norme EN 301 549, qui renvoie aux Règles pour l'accessibilité des contenus "
                 'Web (WCAG).',
        'law': 'Droit national : {law}.',
        'alts': 'Alternatives accessibles disponibles pour les contenus ci-dessus :',
        'tech': 'Technologies utilisées par ce site : {tech}.',
        'review': 'Nous réexaminons cette déclaration au moins tous les {months} mois.',
        'h_status': 'État de conformité',
        'status_partial': '{site} est partiellement conforme à la norme EN 301 549 (qui exige le '
                          'niveau AA des WCAG 2.1). Nous vérifions aussi les critères plus récents '
                          'des WCAG 2.2. Partiellement conforme signifie que certaines parties du '
                          'contenu ne respectent pas entièrement la norme.',
        'status_full': '{site} est entièrement conforme à la norme EN 301 549 (WCAG 2.1 niveau AA) '
                       "et aux critères WCAG 2.2 niveau AA vérifiés, selon l'évaluation décrite "
                       'ci-dessous.',
        'h_limits': 'Limitations connues',
        'limits_none': "Le contrôle automatique n'a détecté aucune erreur. Cela ne prouve pas que "
                       "le site est exempt d'obstacles.",
        'limits_intro': 'Les contenus suivants ne répondent pas encore aux exigences :',
        'limit_line': '{sc} {name} : {n} endroit(s) sur {pages} page(s)',
        'review_intro': 'Ces points ont été signalés pour vérification humaine et peuvent aussi '
                        'constituer des obstacles :',
        'manual_intro': 'Ces aspects ne peuvent pas être vérifiés par un outil automatique et sont '
                        '{state} :',
        'manual_done': 'couverts par notre évaluation manuelle',
        'manual_todo': 'pas encore évalués',
        'h_micro': 'Dérogation',
        'micro': '{org} est une microentreprise au sens de la directive (UE) 2019/882 (moins de 10 '
                 "salariés et chiffre d'affaires annuel ou total du bilan d'au plus 2 millions "
                 "d'euros). Les exigences d'accessibilité applicables aux services ne s'appliquent "
                 'pas légalement à elle ; nous publions cette déclaration volontairement et '
                 "améliorons l'accessibilité progressivement.",
        'h_measures': "Mesures en faveur de l'accessibilité",
        'measures_default': 'Nous contrôlons les pages avec un outil automatique avant leur '
                            'publication.',
        'h_feedback': "Retour d'information et contact",
        'feedback': 'Si vous ne pouvez pas utiliser une partie de ce site, contactez-nous en '
                    'décrivant le problème et la page concernée. Nous répondrons sous {days} '
                    'jours.',
        'contact_email': 'E-mail : {v}',
        'contact_phone': 'Téléphone : {v}',
        'contact_addr': 'Adresse : {v}',
        'h_enforce': 'Procédure de recours',
        'enforce': "Si notre réponse ne vous satisfait pas, vous pouvez saisir l'autorité "
                   'compétente : {auth}.',
        'h_prep': 'Établissement de cette déclaration',
        'prep': 'Cette déclaration a été établie le {date}. Méthode : analyse automatique de '
                '{pages} page(s) avec EAA Site Auditor{manual}.',
        'prep_manual': ' et évaluation manuelle ({who})'},
 'es': {'title': 'Declaración de accesibilidad de {org}',
        'intro': '{org} se compromete a hacer {site} accesible a las personas con discapacidad, de '
                 'conformidad con el Acta Europea de Accesibilidad (Directiva (UE) 2019/882) y la '
                 'norma EN 301 549, que remite a las Pautas de Accesibilidad para el Contenido Web '
                 '(WCAG).',
        'law': 'Legislación nacional: {law}.',
        'alts': 'Alternativas accesibles disponibles para el contenido anterior:',
        'tech': 'Tecnologías en las que se basa este sitio web: {tech}.',
        'review': 'Revisamos esta declaración al menos cada {months} meses.',
        'h_status': 'Estado de conformidad',
        'status_partial': '{site} es parcialmente conforme con la norma EN 301 549 (que exige el '
                          'nivel AA de WCAG 2.1). También comprobamos los criterios más recientes '
                          'de WCAG 2.2. Parcialmente conforme significa que algunas partes del '
                          'contenido no cumplen totalmente la norma.',
        'status_full': '{site} es totalmente conforme con la norma EN 301 549 (WCAG 2.1 nivel AA) '
                       'y con los criterios WCAG 2.2 nivel AA comprobados, según la evaluación '
                       'descrita a continuación.',
        'h_limits': 'Limitaciones conocidas',
        'limits_none': 'La comprobación automática no encontró errores. Esto no demuestra que el '
                       'sitio carezca de barreras.',
        'limits_intro': 'El siguiente contenido aún no cumple los requisitos:',
        'limit_line': '{sc} {name}: {n} lugar(es) en {pages} página(s)',
        'review_intro': 'Estos puntos se marcaron para revisión manual y también pueden ser '
                        'barreras:',
        'manual_intro': 'Estos aspectos no pueden verificarse con una herramienta automática y '
                        'están {state}:',
        'manual_done': 'cubiertos por nuestra evaluación manual',
        'manual_todo': 'pendientes de evaluar',
        'h_micro': 'Exención',
        'micro': '{org} es una microempresa en el sentido de la Directiva (UE) 2019/882 (menos de '
                 '10 empleados y volumen de negocios anual o balance general total de hasta 2 '
                 'millones de euros). Los requisitos de accesibilidad de los servicios no le son '
                 'legalmente aplicables; publicamos esta declaración voluntariamente y mejoramos '
                 'la accesibilidad de forma gradual.',
        'h_measures': 'Medidas de apoyo a la accesibilidad',
        'measures_default': 'Comprobamos las páginas con una herramienta automática antes de '
                            'publicarlas.',
        'h_feedback': 'Comentarios y contacto',
        'feedback': 'Si no puede utilizar alguna parte de este sitio web, contáctenos y describa '
                    'el problema y la página. Responderemos en un plazo de {days} días.',
        'contact_email': 'Correo electrónico: {v}',
        'contact_phone': 'Teléfono: {v}',
        'contact_addr': 'Dirección: {v}',
        'h_enforce': 'Procedimiento de reclamación',
        'enforce': 'Si no está satisfecho con nuestra respuesta, puede presentar una reclamación '
                   'ante la autoridad competente: {auth}.',
        'h_prep': 'Elaboración de esta declaración',
        'prep': 'Esta declaración se elaboró el {date}. Método: análisis automático de {pages} '
                'página(s) con EAA Site Auditor{manual}.',
        'prep_manual': ' y evaluación manual ({who})'},
 'it': {'title': 'Dichiarazione di accessibilità di {org}',
        'intro': '{org} si impegna a rendere {site} accessibile alle persone con disabilità, in '
                 "conformità all'Atto europeo sull'accessibilità (direttiva (UE) 2019/882) e alla "
                 "norma EN 301 549, che rinvia alle Linee guida per l'accessibilità dei contenuti "
                 'Web (WCAG).',
        'law': 'Normativa nazionale: {law}.',
        'alts': 'Alternative accessibili disponibili per i contenuti sopra indicati:',
        'tech': 'Tecnologie su cui si basa questo sito: {tech}.',
        'review': 'Riesaminiamo questa dichiarazione almeno ogni {months} mesi.',
        'h_status': 'Stato di conformità',
        'status_partial': '{site} è parzialmente conforme alla norma EN 301 549 (che richiede il '
                          'livello AA delle WCAG 2.1). Verifichiamo anche i criteri più recenti '
                          'delle WCAG 2.2. Parzialmente conforme significa che alcune parti del '
                          'contenuto non rispettano pienamente la norma.',
        'status_full': '{site} è pienamente conforme alla norma EN 301 549 (WCAG 2.1 livello AA) e '
                       'ai criteri WCAG 2.2 livello AA verificati, in base alla valutazione '
                       'descritta di seguito.',
        'h_limits': 'Limitazioni note',
        'limits_none': 'Il controllo automatico non ha rilevato errori. Ciò non dimostra che il '
                       'sito sia privo di barriere.',
        'limits_intro': 'I seguenti contenuti non soddisfano ancora i requisiti:',
        'limit_line': '{sc} {name}: {n} punto/i su {pages} pagina/e',
        'review_intro': 'Questi punti sono stati segnalati per la verifica manuale e possono '
                        'costituire barriere:',
        'manual_intro': 'Questi aspetti non possono essere verificati da uno strumento automatico '
                        'e sono {state}:',
        'manual_done': 'coperti dalla nostra valutazione manuale',
        'manual_todo': 'non ancora valutati',
        'h_micro': 'Esenzione',
        'micro': '{org} è una microimpresa ai sensi della direttiva (UE) 2019/882 (meno di 10 '
                 'dipendenti e fatturato annuo o totale di bilancio non superiore a 2 milioni di '
                 'euro). I requisiti di accessibilità per i servizi non si applicano legalmente; '
                 "pubblichiamo questa dichiarazione volontariamente e miglioriamo l'accessibilità "
                 'gradualmente.',
        'h_measures': "Misure a sostegno dell'accessibilità",
        'measures_default': 'Controlliamo le pagine con uno strumento automatico prima della '
                            'pubblicazione.',
        'h_feedback': 'Feedback e contatti',
        'feedback': 'Se non riesci a usare una parte di questo sito, contattaci descrivendo il '
                    'problema e la pagina. Risponderemo entro {days} giorni.',
        'contact_email': 'E-mail: {v}',
        'contact_phone': 'Telefono: {v}',
        'contact_addr': 'Indirizzo: {v}',
        'h_enforce': 'Procedura di ricorso',
        'enforce': "Se la nostra risposta non ti soddisfa, puoi rivolgerti all'autorità "
                   'competente: {auth}.',
        'h_prep': 'Redazione di questa dichiarazione',
        'prep': 'Questa dichiarazione è stata redatta il {date}. Metodo: scansione automatica di '
                '{pages} pagina/e con EAA Site Auditor{manual}.',
        'prep_manual': ' e valutazione manuale ({who})'}}

MANUAL_LOCAL = {'en': ['Keyboard operation of every feature, including custom widgets (2.1.1, 2.1.2)',
        'Whether alt texts are accurate and useful, not just present (1.1.1)',
        'Captions, audio descriptions and transcripts content quality (1.2.x)',
        'Logical reading order and meaningful sequence (1.3.2)',
        'Colour contrast of text over images, gradients and UI states such as hover (1.4.3, '
        '1.4.11)',
        'Reflow at 320 px and 400% zoom, text spacing (1.4.10, 1.4.12)',
        'Focus visibility on every component and focus order (2.4.3, 2.4.7, 2.4.11)',
        'Consistent navigation and help placement across pages (3.2.3, 3.2.6)',
        'Error identification and suggestions in forms (3.3.1, 3.3.3)',
        'Screen reader behaviour with at least one real screen reader (4.1.2, 4.1.3)'],
 'ro': ['Utilizarea tuturor funcțiilor doar de la tastatură (2.1.1, 2.1.2)',
        'Dacă textele alternative sunt corecte și utile (1.1.1)',
        'Calitatea subtitrărilor, descrierilor audio și transcrierilor (1.2.x)',
        'Ordinea logică de citire (1.3.2)',
        'Contrastul textului peste imagini și al stărilor interactive (1.4.3, 1.4.11)',
        'Reorganizarea conținutului la 320 px și zoom 400% (1.4.10, 1.4.12)',
        'Focalizare vizibilă și ordinea focalizării (2.4.3, 2.4.7, 2.4.11)',
        'Navigare și ajutor consecvente între pagini (3.2.3, 3.2.6)',
        'Identificarea și corectarea erorilor din formulare (3.3.1, 3.3.3)',
        'Utilizarea cu un cititor de ecran real (4.1.2, 4.1.3)'],
 'de': ['Bedienung aller Funktionen nur mit der Tastatur (2.1.1, 2.1.2)',
        'Ob Alternativtexte zutreffend und hilfreich sind (1.1.1)',
        'Qualität von Untertiteln, Audiodeskription und Transkripten (1.2.x)',
        'Sinnvolle Lesereihenfolge (1.3.2)',
        'Kontrast von Text auf Bildern und bei Zuständen wie Hover (1.4.3, 1.4.11)',
        'Reflow bei 320 px und 400 % Zoom, Textabstände (1.4.10, 1.4.12)',
        'Sichtbarer Fokus und Fokusreihenfolge (2.4.3, 2.4.7, 2.4.11)',
        'Einheitliche Navigation und Hilfe über alle Seiten (3.2.3, 3.2.6)',
        'Fehlererkennung und Korrekturvorschläge in Formularen (3.3.1, 3.3.3)',
        'Nutzung mit einem echten Screenreader (4.1.2, 4.1.3)'],
 'fr': ['Utilisation de toutes les fonctions au clavier seul (2.1.1, 2.1.2)',
        'Pertinence et exactitude des textes alternatifs (1.1.1)',
        "Qualité des sous-titres, de l'audiodescription et des transcriptions (1.2.x)",
        'Ordre de lecture logique (1.3.2)',
        'Contraste du texte sur images et dans les états interactifs (1.4.3, 1.4.11)',
        'Réorganisation à 320 px et zoom à 400 %, espacement du texte (1.4.10, 1.4.12)',
        'Visibilité et ordre du focus (2.4.3, 2.4.7, 2.4.11)',
        'Navigation et aide cohérentes entre les pages (3.2.3, 3.2.6)',
        'Identification et correction des erreurs de formulaire (3.3.1, 3.3.3)',
        "Utilisation avec un vrai lecteur d'écran (4.1.2, 4.1.3)"],
 'es': ['Uso de todas las funciones solo con el teclado (2.1.1, 2.1.2)',
        'Que los textos alternativos sean correctos y útiles (1.1.1)',
        'Calidad de subtítulos, audiodescripción y transcripciones (1.2.x)',
        'Orden de lectura lógico (1.3.2)',
        'Contraste del texto sobre imágenes y en estados interactivos (1.4.3, 1.4.11)',
        'Reflujo a 320 px y zoom del 400 %, espaciado del texto (1.4.10, 1.4.12)',
        'Foco visible y orden del foco (2.4.3, 2.4.7, 2.4.11)',
        'Navegación y ayuda coherentes entre páginas (3.2.3, 3.2.6)',
        'Identificación y corrección de errores en formularios (3.3.1, 3.3.3)',
        'Uso con un lector de pantalla real (4.1.2, 4.1.3)'],
 'it': ['Uso di tutte le funzioni con la sola tastiera (2.1.1, 2.1.2)',
        'Correttezza e utilità dei testi alternativi (1.1.1)',
        'Qualità di sottotitoli, audiodescrizione e trascrizioni (1.2.x)',
        'Ordine di lettura logico (1.3.2)',
        'Contrasto del testo su immagini e negli stati interattivi (1.4.3, 1.4.11)',
        'Reflow a 320 px e zoom al 400 %, spaziatura del testo (1.4.10, 1.4.12)',
        'Focus visibile e ordine del focus (2.4.3, 2.4.7, 2.4.11)',
        'Navigazione e aiuto coerenti tra le pagine (3.2.3, 3.2.6)',
        'Identificazione e correzione degli errori nei moduli (3.3.1, 3.3.3)',
        'Uso con un vero screen reader (4.1.2, 4.1.3)']}

NATIONAL_LAW = {'en': '',
 'ro': 'Legea nr. 232/2022',
 'de': 'Barrierefreiheitsstärkungsgesetz (BFSG)',
 'fr': '',
 'es': 'Ley 11/2023, de 8 de mayo',
 'it': 'D.Lgs. 82/2022'}

AUTHORITY_HINT = {'en': 'national market surveillance / enforcement body and URL',
 'ro': 'autoritatea competentă pentru sectorul dvs. (ANPC, Autoritatea pentru Digitalizarea '
       'României, ANCOM, CNA …) și URL',
 'de': 'zuständige Marktüberwachungsbehörde (z. B. MLBF Magdeburg) und URL',
 'fr': 'autorité compétente pour votre secteur (DGCCRF, ARCOM, ARCEP …) et URL',
 'es': 'autoridad competente de su comunidad autónoma y su sector, y URL',
 'it': 'autorità competente per il vostro settore (es. AgID) e URL'}
