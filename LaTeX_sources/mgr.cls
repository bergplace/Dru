%% This is file `mgr.cls',
%%
%% Plik LaTeX'owej klasy dokumentu wspomagającej pisanie pracy magisterskiej
%% oraz testowo pracy inzynierskiej
%% na wydziale Elektroniki Politechniki Wrocławskiej
%%
%% Autor: Adam Ratajczak
%% www:http://rab.ict.pwr.wroc.pl/~ar/LaTeX/mgr.html
%% Ostatnia modyfikacja: 06.06.2011
%%
%% Do pliku klasy dołączone są:
%%  * plik instrukcji manual.pdf
%%  * przykład użycia dyplom.tex [dyplom_inz.tex]
%%
%%
\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{mgr}
              [2005/12/01
 Non-Standard LaTeX document class]
\newcommand\@ptsize{}
\newif\if@openright
\newif\if@mainmatter \@mainmattertrue
\newif\if@archive \@archivefalse
\newif\if@eng \@engfalse
\newif\if@pl \@pltrue
\newif\if@en \@enfalse
\DeclareOption{8pt}{\renewcommand\@ptsize{8}}
\DeclareOption{10pt}{\renewcommand\@ptsize{0}}
\DeclareOption{11pt}{\renewcommand\@ptsize{1}}
\DeclareOption{12pt}{\renewcommand\@ptsize{2}}
\DeclareOption{printmode}{\renewcommand\@ptsize{2}%
        \@twosidetrue  \@mparswitchtrue%
        \@openrighttrue
        \setlength\overfullrule{0pt}}
\DeclareOption{oneside}{\@twosidefalse \@mparswitchfalse}
\DeclareOption{twoside}{\@twosidetrue  \@mparswitchtrue}
\DeclareOption{openright}{\@openrighttrue}
\DeclareOption{openany}{\@openrightfalse}
\DeclareOption{leqno}{\input{leqno.clo}}
\DeclareOption{fleqn}{\input{fleqn.clo}}
\DeclareOption{archivemode}{\renewcommand\@ptsize{8}%
        \@twosidetrue  \@mparswitchtrue%
        \@openrightfalse \@archivetrue%
        \setlength\overfullrule{0pt}}
\DeclareOption{eng}{\@engtrue}
%warianty jezykowe
\DeclareOption{pl}{\@pltrue \@enfalse}
\DeclareOption{en}{\@entrue \@plfalse}

\DeclareOption{draft}{\setlength\overfullrule{5pt}}
\DeclareOption{final}{\setlength\overfullrule{0pt}}
\DeclareOption{openbib}{%
  \AtEndOfPackage{%
   \renewcommand\@openbib@code{%
      \advance\leftmargin\bibindent
      \itemindent -\bibindent
      \listparindent \itemindent
      \parsep \z@
      }%
   \renewcommand\newblock{\par}}%
}
\ExecuteOptions{12pt,twoside,final,openright}
\ProcessOptions
%rozmiar kartki
\setlength\paperheight {297mm}
\setlength\paperwidth  {210mm}
%wybranie odpowiedniej wielkości czcionki
\ifnum\@ptsize=8 %poniżej definicja czcionki 8pt
\renewcommand\normalsize{%
   \@setfontsize\normalsize\@viiipt{9.5}%
   \abovedisplayskip 8\p@ \@plus4\p@ \@minus4\p@
   \abovedisplayshortskip \z@ \@plus3\p@
   \belowdisplayshortskip 5\p@ \@plus3\p@ \@minus3\p@
   \belowdisplayskip \abovedisplayskip
   \let\@listi\@listI}
\normalsize
\newcommand\small{%
   \@setfontsize\small\@viipt\@viiipt%
   \abovedisplayskip 5\p@ \@plus2\p@ \@minus2\p@
   \abovedisplayshortskip \z@ \@plus1\p@
   \belowdisplayshortskip 3\p@ \@plus\p@ \@minus2\p@
   \def\@listi{\leftmargin\leftmargini
               \topsep 3\p@ \@plus\p@ \@minus\p@
               \parsep 2\p@ \@plus\p@ \@minus\p@
               \itemsep \parsep}%
   \belowdisplayskip \abovedisplayskip
}
\newcommand\footnotesize{%
   \@setfontsize\footnotesize\@vipt\@viipt
   \abovedisplayskip 4\p@ \@plus2\p@ \@minus2\p@
   \abovedisplayshortskip \z@ \@plus1\p@
   \belowdisplayshortskip 2.5\p@ \@plus\p@ \@minus\p@
   \def\@listi{\leftmargin\leftmargini
               \topsep 3\p@ \@plus\p@ \@minus\p@
               \parsep 2\p@ \@plus\p@ \@minus\p@
               \itemsep \parsep}%
   \belowdisplayskip \abovedisplayskip
}
\newcommand\scriptsize{\@setfontsize\scriptsize\@vpt\@vipt}
\newcommand\tiny{\@setfontsize\tiny\@vpt\@vipt}
\newcommand\large{\@setfontsize\large\@xpt\@xipt}
\newcommand\Large{\@setfontsize\Large\@xipt\@xiipt}
\newcommand\LARGE{\@setfontsize\LARGE\@xiipt{14}}
\newcommand\huge{\@setfontsize\huge\@xivpt{18}}
\newcommand\Huge{\@setfontsize\Huge\@xviipt{22}}
\setlength\parindent{12pt}
\setlength\smallskipamount{3\p@ \@plus 1\p@ \@minus 1\p@}
\setlength\medskipamount{6\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\bigskipamount{12\p@ \@plus 4\p@ \@minus 4\p@}
\setlength\topskip   {9\p@}
\setlength\footskip{30\p@}
\setlength\maxdepth{.5\topskip}

\setlength\footnotesep{6.3\p@}
\setlength{\skip\footins}{7\p@ \@plus 4\p@ \@minus 2\p@}
\setlength\floatsep    {10\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\textfloatsep{15\p@ \@plus 2\p@ \@minus 4\p@}
\setlength\intextsep   {10\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\dblfloatsep    {10\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\dbltextfloatsep{15\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\@fptop{0\p@ \@plus 1fil}
\setlength\@fpsep{8\p@ \@plus 2fil}
\setlength\@fpbot{0\p@ \@plus 1fil}
\setlength\@dblfptop{0\p@ \@plus 1fil}
\setlength\@dblfpsep{8\p@ \@plus 2fil}
\setlength\@dblfpbot{0\p@ \@plus 1fil}
\setlength\partopsep{2\p@ \@plus \p@ \@minus \p@}
\def\@listi{\leftmargin\leftmargini
            \parsep 4\p@  \@plus2\p@ \@minus\p@
            \topsep 6\p@ \@plus2\p@   \@minus3\p@
            \itemsep \parsep}
\let\@listI\@listi
\@listi
\def\@listii {\leftmargin\leftmarginii
              \labelwidth\leftmarginii
              \advance\labelwidth-\labelsep
              \topsep    4\p@   \@plus2\p@ \@minus\p@
              \parsep    2\p@ \@plus\p@    \@minus\p@
              \itemsep   \parsep}
\def\@listiii{\leftmargin\leftmarginiii
              \labelwidth\leftmarginiii
              \advance\labelwidth-\labelsep
              \topsep    2\p@\@plus\p@\@minus\p@
              \parsep    \z@
              \partopsep \p@ \@plus\z@ \@minus\p@
              \itemsep   \topsep}
\def\@listiv {\leftmargin\leftmarginiv
              \labelwidth\leftmarginiv
              \advance\labelwidth-\labelsep}
\def\@listv  {\leftmargin\leftmarginv
              \labelwidth\leftmarginv
              \advance\labelwidth-\labelsep}
\def\@listvi {\leftmargin\leftmarginvi
              \labelwidth\leftmarginvi
              \advance\labelwidth-\labelsep}
\else %pozostałe, standardowe czcionki
  \input{bk1\@ptsize.clo}
\fi
%standardowe rozmiary i wartości liczników
\setlength\lineskip{1\p@}
\setlength\normallineskip{1\p@}
\renewcommand\baselinestretch{}
\setlength\parskip{0\p@ \@plus \p@}
\@lowpenalty   51
\@medpenalty  151
\@highpenalty 301
\setcounter{topnumber}{2}
\renewcommand\topfraction{.7}
\setcounter{bottomnumber}{1}
\renewcommand\bottomfraction{.3}
\setcounter{totalnumber}{3}
\renewcommand\textfraction{.2}
\renewcommand\floatpagefraction{.5}
\setcounter{dbltopnumber}{2}
\renewcommand\dbltopfraction{.7}
\renewcommand\dblfloatpagefraction{.5}
%definicje nagłówków i stopek
\if@twoside
  \def\ps@headings{%
      \let\@oddfoot\@empty\let\@evenfoot\@empty
      \def\@evenhead{\vbox{{\small\bfseries\thepage\hfill\leftmark}%
      \\ \hbox{\vrule height3pt width0pt}\leavevmode \leaders \hrule \hfill \kern \z@ \hbox{}}}%
      \def\@oddhead{\vbox{{\small\bfseries\rightmark\hfill\thepage}%
      \\ \hbox{\vrule height3pt width0pt}\leavevmode \leaders \hrule \hfill \kern \z@ \hbox{}}}%
      \let\@mkboth\markboth
    \def\chaptermark##1{%
      \markboth {%
        \ifnum \c@secnumdepth >\m@ne
          \if@mainmatter
            \thechapter. \ %
          \fi
        \fi
        ##1}{}}%
    \def\sectionmark##1{%
      \markright {%
        \ifnum \c@secnumdepth >\z@
          \thesection. \ %
        \fi
        ##1}}}
\else
  \def\ps@headings{%
    \let\@oddfoot\@empty
    \def\@oddhead{\vbox{{\small\bfseries\rightmark\hfill\thepage}%
      \\ \hbox{\vrule height3pt width0pt}\leavevmode \leaders \hrule \hfill \kern \z@ \hbox{}}}%
    \let\@mkboth\markboth
    \def\chaptermark##1{%
      \markright {%
        \ifnum \c@secnumdepth >\m@ne
          \if@mainmatter
            \thechapter. \ %
          \fi
        \fi
        ##1}}}
\fi
\def\ps@myheadings{%
    \let\@oddfoot\@empty\let\@evenfoot\@empty
    \def\@evenhead{\thepage\hfil\slshape\leftmark}%
    \def\@oddhead{{\slshape\rightmark}\hfil\thepage}%
    \let\@mkboth\@gobbletwo
    \let\chaptermark\@gobble
    \let\sectionmark\@gobble
    }

%marginesy itp
\topmargin -18mm
\addtolength{\headheight}{2pt}
\headsep 3mm
\oddsidemargin 0pt
\addtolength{\oddsidemargin}{-1in}
\addtolength{\oddsidemargin}{2.5cm}
\evensidemargin 0pt
\addtolength{\evensidemargin}{-1in}
\addtolength{\evensidemargin}{2.5cm}
\textwidth 16cm
\textheight 25cm 

%definicje danych do utworzenia strony tyułowej
\if@pl
\newcommand{\@naglowek}{PRACA DYPLOMOWA \\ MAGISTERSKA}
\newcommand{\@napisProwadzacy}{Prowadz\k{a}cy prac\k{e}:}
\newcommand{\@napisOcena}{Ocena pracy:}
\fi
\if@en
\newcommand{\@naglowek}{MASTER OF SCIENCE THESIS}
\newcommand{\@napisProwadzacy}{Supervisor:}
\newcommand{\@napisOcena}{Grade:}
\fi

\if@eng
\if@pl
\renewcommand{\@naglowek}{PRACA DYPLOMOWA \\ IN\.ZYNIERSKA}
\fi
\if@en
\renewcommand{\@naglowek}{ENGINEERING THESIS}
\fi

%\renewcommand{\@napisProwadzacy}{Prowadz\k{a}cy prac\k{e}:}
%\renewcommand{\@napisOcena}{Ocena pracy:}
\fi

\renewcommand{\@author}{Brak autora\typeout{MGR.cls Warning: Brak podanego nazwiska autora, uzyj polecenia author}}
\renewcommand{\author}[1]{\renewcommand{\@author}{#1}}
\renewcommand{\@title}{Brak polskiego tytułu pracy dyplomowej\typeout{MGR.cls Warning: Brak podanego polskiego tytu\l{}u pracy dyplomowej, uzyj polecenia title }}  
\renewcommand{\title}[1]{\renewcommand{\@title}{#1}}
\newcommand{\@engtitle}{Brak angielskiego tytułu pracy dyplomowej\typeout{MGR.cls Warning: Brak podanego angielskiego tytulu pracy dyplomowej, uzyj polecenia engtitle}}
\newcommand{\engtitle}[1]{\renewcommand{\@engtitle}{#1}}
\newcommand{\@supervisor}{Brak prowadzącego\typeout{MGR.cls Warning: Brak podanego nazwiska prowadzacego, uzyj polecenia supervisor}}
\newcommand{\supervisor}[1]{\renewcommand{\@supervisor}{#1}}
\newcommand{\@guardian}{}
\newcommand{\guardian}[1]{\renewcommand{\@guardian}{
{\Large\sc Opiekun:}\\[3mm]
{\large #1}\\
\vfill}}
\newcommand{\@field}{Brak kierunku\typeout{MGR.cls Warning: Brak podanej nazwy kierunku studiow, uzyj polecenia field}}
\newcommand{\field}[1]{\renewcommand{\@field}{#1}}
\newcommand{\@specialisation}{Brak specjalności\typeout{MGR.cls Warning: Brak podanej nazwy specjalnosci, uzyj polecenia specialisation}}
\newcommand{\specialisation}[1]{\renewcommand{\@specialisation}{#1}}
\renewcommand{\@date}{\the\year}
\renewcommand{\date}[1]{\renewcommand{\@date}{#1}}

%dodatkowe polecenia zmiany czcionki na 12pt dla poprawnego złożenia strony tytułowej
\newcommand\@normalsizetemp{%
   \@setfontsize\normalsize\@xiipt{14.5}%
   \abovedisplayskip 12\p@ \@plus3\p@ \@minus7\p@
   \abovedisplayshortskip \z@ \@plus3\p@
   \belowdisplayshortskip 6.5\p@ \@plus3.5\p@ \@minus3\p@
   \belowdisplayskip \abovedisplayskip
   \let\@listi\@listI}
\newcommand\@small{%
   \@setfontsize\small\@xipt{13.6}%
   \abovedisplayskip 11\p@ \@plus3\p@ \@minus6\p@
   \abovedisplayshortskip \z@ \@plus3\p@
   \belowdisplayshortskip 6.5\p@ \@plus3.5\p@ \@minus3\p@
   \def\@listi{\leftmargin\leftmargini
               \topsep 9\p@ \@plus3\p@ \@minus5\p@
               \parsep 4.5\p@ \@plus2\p@ \@minus\p@
               \itemsep \parsep}%
   \belowdisplayskip \abovedisplayskip
}
\newcommand\@footnotesize{%
   \@setfontsize\footnotesize\@xpt\@xiipt
   \abovedisplayskip 10\p@ \@plus2\p@ \@minus5\p@
   \abovedisplayshortskip \z@ \@plus3\p@
   \belowdisplayshortskip 6\p@ \@plus3\p@ \@minus3\p@
   \def\@listi{\leftmargin\leftmargini
               \topsep 6\p@ \@plus2\p@ \@minus2\p@
               \parsep 3\p@ \@plus2\p@ \@minus\p@
               \itemsep \parsep}%
   \belowdisplayskip \abovedisplayskip
}
\newcommand\@scriptsize{\@setfontsize\scriptsize\@viiipt{9.5}}
\newcommand\@tiny{\@setfontsize\tiny\@vipt\@viipt}
\newcommand\@large{\@setfontsize\large\@xivpt{18}}
\newcommand\@Large{\@setfontsize\Large\@xviipt{22}}
\newcommand\@LARGE{\@setfontsize\LARGE\@xxpt{25}}
\newcommand\@huge{\@setfontsize\huge\@xxvpt{30}}
\let\@Huge=\@huge

%definicja tworząca stronę tytułową
\def\maketitle{%
%chwilowa podmiana czcionki na 12pt w celu złożenia strony tytułowej
\setlength\smallskipamount{3\p@ \@plus 1\p@ \@minus 1\p@}
\setlength\medskipamount{6\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\bigskipamount{12\p@ \@plus 4\p@ \@minus 4\p@}
\setlength\footnotesep{8.4\p@}
\setlength{\skip\footins}{10.8\p@ \@plus 4\p@ \@minus 2\p@}
\setlength\floatsep    {12\p@ \@plus 2\p@ \@minus 4\p@}
\setlength\textfloatsep{20\p@ \@plus 2\p@ \@minus 4\p@}
\setlength\intextsep   {14\p@ \@plus 4\p@ \@minus 4\p@}
\setlength\dblfloatsep    {14\p@ \@plus 2\p@ \@minus 4\p@}
\setlength\dbltextfloatsep{20\p@ \@plus 2\p@ \@minus 4\p@}
\setlength\@fptop{0\p@ \@plus 1fil}
\setlength\@fpsep{10\p@ \@plus 2fil}
\setlength\@fpbot{0\p@ \@plus 1fil}
\setlength\@dblfptop{0\p@ \@plus 1fil}
\setlength\@dblfpsep{10\p@ \@plus 2fil}
\setlength\@dblfpbot{0\p@ \@plus 1fil}
\setlength\partopsep{3\p@ \@plus 2\p@ \@minus 2\p@}
\def\@listi{\leftmargin\leftmargini
            \parsep 5\p@  \@plus2.5\p@ \@minus\p@
            \topsep 10\p@ \@plus4\p@   \@minus6\p@
            \itemsep5\p@  \@plus2.5\p@ \@minus\p@}
\let\@listI\@listi
\@listi
\def\@listii {\leftmargin\leftmarginii
              \labelwidth\leftmarginii
              \advance\labelwidth-\labelsep
              \topsep    5\p@   \@plus2.5\p@ \@minus\p@
              \parsep    2.5\p@ \@plus\p@    \@minus\p@
              \itemsep   \parsep}
\def\@listiii{\leftmargin\leftmarginiii
              \labelwidth\leftmarginiii
              \advance\labelwidth-\labelsep
              \topsep    2.5\p@\@plus\p@\@minus\p@
              \parsep    \z@
              \partopsep \p@ \@plus\z@ \@minus\p@
              \itemsep   \topsep}
\def\@listiv {\leftmargin\leftmarginiv
              \labelwidth\leftmarginiv
              \advance\labelwidth-\labelsep}
\def\@listv  {\leftmargin\leftmarginv
              \labelwidth\leftmarginv
              \advance\labelwidth-\labelsep}
\def\@listvi {\leftmargin\leftmarginvi
              \labelwidth\leftmarginvi
              \advance\labelwidth-\labelsep}
%chwilowa podmiana komend
\let\@tempnormalsize=\normalsize
\let\normalsize=\@normalsize
\let\@tempsmall=\small
\let\small=\@small
\let\@tempfootnotesize=\footnotesize
\let\footnotesize=\@footnotesize
\let\@tempscriptsize=\scriptsize
\let\scriptsize=\@sriptsize
\let\@temptiny=\tiny
\let\tiny=\@tiny
\let\@templarge=\large
\let\large=\@large
\let\@tempLarge=\Large
\let\Large=\@Large
\let\@tempLARGE=\LARGE
\let\LARGE=\@LARGE
\let\@temphuge=\huge
\let\huge=\@huge
\let\@tempHuge=\Huge
\let\Huge=\@Huge
%usunięcie warningów podczas składania strony tytułowej
\newcount{\@temphbadness}
\newcount{\@tempvbadness}
\newlength{\@temphfuzz}
\@temphbadness=\hbadness
\@tempvbadness=\vbadness
\@temphfuzz\hfuzz
\hbadness=10000
\vbadness=10000
\hfuzz=400pt
%ustawienie nowych marginesów dla strony tytułowej
\newlength{\@temptextwidth}
\@temptextwidth=\textwidth
\textwidth=\paperwidth
\newlength{\@temptextheight}
\newlength{\@temptopmargin}
\@temptopmargin=\topmargin
\topmargin=-1in
\newlength{\@tempheadheight}
\@tempheadheight=\headheight
\headheight=0pt
\newlength{\@tempheadsep}
\@tempheadsep=\headsep
\headsep=0pt
\newlength{\@tempoddsidemargin}
\@tempoddsidemargin=\oddsidemargin
\oddsidemargin=-1in
\newlength{\@tempevensidemargin}
\@tempevensidemargin=\evensidemargin
\evensidemargin=-1in

\if@pl
\newcommand{\@university}{%
  \LARGE  POLITECHNIKA WROC\L{}AWSKA \\[0mm] %
  WYDZIA\L{} ELEKTRONIKI            %
  \vspace{-6mm}%
}
\newcommand{\@fieldtext}{\Large\sc Kierunek:}
\newcommand{\@specialisationtext}{\Large\sc Specjalno\'s\'c:}
\newcommand{\@authortext}{\Large{\sc Autor:}}
\fi
\if@en
\newcommand{\@university}{%
  \Large  \mbox{\hspace{-3mm}WROC\L{}AW UNIVERSITY OF SCIENCE AND TECHNOLOGY}\\[0mm]%
  FACULTY OF COMPUTER SCIENCE AND MANAGEMENT%
  \vspace{-6mm}%
}
\newcommand{\@fieldtext}{\Large\sc Field:}
\newcommand{\@specialisationtext}{\Large\sc Specialization:}
\newcommand{\@authortext}{\Large{\sc Author:}}
\fi



%właściwe składanie strony tytułowej
\begin{titlepage}% 

%\layout
\vbox{\vrule height44mm width0mm\\ \nopagebreak% odstęp od góry strony
\begin{minipage}[c][63mm]{\textwidth} %górna ramka z uczelnią, wydziałem, kierunkiem i specjalnością oraz tekst "PRACA DYPLOMOWA MAGISTERSKA" zdefiniowane z pływającymi odległościami i z możliwością wielolinijkowych kierunek i specjalność
\begin{center}\begin{minipage}[c][17mm]{16cm}
     \begin{center}                              %
         \@university%
     \end{center}                                %
   \mbox{}\hrulefill\mbox{}              %
\end{minipage}\\[11mm]
\begin{minipage}[c][\totalheight]{16cm}
\mbox{}
\vfill
%korekcja rozmieszczenia napisów Kierunek: i Specjalność: w zależności od wysokości (ilości linijek) w nazwie kierunku lub specjalności
\newlength{\@tempheightkier}
\newlength{\@tempheighttkier}
\settoheight{\@tempheighttkier}{\vbox{\@fieldtext}}
\settoheight{\@tempheightkier}{\vbox{\large \vrule height \@tempheighttkier width 0pt \@field}}
\settodepth{\@tempheighttkier}{\vbox{\large \vrule height \@tempheighttkier width 0pt \@field}}
\addtolength{\@tempheightkier}{\@tempheighttkier}
\settoheight{\@tempheighttkier}{\vbox{\@fieldtext}}
\addtolength{\@tempheightkier}{-\@tempheighttkier}
%
\newlength{\@tempheightspec}
\newlength{\@tempheighttspec}
\settoheight{\@tempheighttspec}{\vbox{\@specialisationtext}}
\settoheight{\@tempheightspec}{\vbox{\large \vrule height \@tempheighttspec width 0pt \@specialisation}}
\settodepth{\@tempheighttspec}{\vbox{\large \vrule height \@tempheighttspec width 0pt \@specialisation}}
\addtolength{\@tempheightspec}{\@tempheighttspec}
\settoheight{\@tempheighttspec}{\vbox{\@specialisationtext}}
\addtolength{\@tempheightspec}{-\@tempheighttspec}
%tabelka składająca kierunek i specjalność
\begin{tabular}{p{4.5cm}p{10.5cm}}
\parbox{4.5cm}{\@fieldtext \vrule depth \@tempheightkier width 0pt} & \parbox{10cm}{\large \vrule height \@tempheighttkier width 0pt \@field}\\
\parbox{4.5cm}{\@specialisationtext \vrule depth \@tempheightspec width 0pt } & \parbox{10cm}{\large \vrule height \@tempheighttspec width 0pt \@specialisation} 
\end{tabular}\mbox{}\\[5mm] \vfill
\begin{center}
\LARGE\bf \@naglowek
\end{center}\vspace{2cm}\vfill
\end{minipage}\end{center}
\end{minipage}\nopagebreak\linebreak
{\begin{minipage}[c][7.5cm]{7.3cm} %ramka pozycjonująca
\mbox{}
%\fbox{My}\hfill\fbox{My}
%\vfill
%\fbox{My}\hfill\fbox{My}
\end{minipage}}
{\begin{minipage}[c][7.5cm][c]{11.2cm} %ramka z tytułami i autorem, widoczna w okienku okładki
\begin{center}
\begin{minipage}[c][7.3cm][c]{10.6cm}
\begin{center}
\vfil
\if@pl
\large \@title
\vfil
\large \@engtitle
\fi
\if@en
\large \@engtitle
\vfil
\large \@title
\fi
\vfil
\@authortext\\
\large \@author
\vfil\mbox{}
\end{center}
\end{minipage}
\end{center}
\end{minipage}}\nolinebreak
{\begin{minipage}[c][7.5cm]{2.3cm} %ramka pozycjonująca
\mbox{}
\end{minipage}}\nopagebreak\linebreak
{\begin{minipage}[c][9.5cm]{8.4cm} %ramka pozycjonująca
\mbox{}
\end{minipage}}
{\begin{minipage}[c][9.5cm]{12.5cm} %ramka z promotorem i oceną
{\begin{minipage}[c][9.5cm]{10cm}
\vfill
{\Large\sc \@napisProwadzacy}\\[3mm]
{\large \@supervisor}\\
\vfill
\@guardian %tego nie ma jeżeli nie jest zdefiniowane, a nie powinno się definiować jeżeli prowadzący i opiekun to ta sama osoba
{\Large\sc \@napisOcena\\[20mm]}
\vfill\mbox{}
\end{minipage}}
\end{minipage}}
\begin{minipage}[c][2.0cm]{\paperwidth} % ramka stopka, rok wrzucany automatycznie lub z polecenia \date
\begin{center}\begin{minipage}[t][2.0cm]{16cm}
 \noindent
  \mbox{}\hrulefill\mbox{}\\[-9mm]
   \begin{center}\large WROC\L{}AW \@date \end{center}
\end{minipage}\end{center}
\end{minipage}}
\nopagebreak \vskip -30cm \pagebreak %zabieg nie pozwalający łamać strony

\end{titlepage}%koniec właściwego składania strony tytułowej
%
%powrót do wcześniejszych wartości aby znów zgłaszać błędy o Over i Under fullach
\hbadness=\@temphbadness
\vbadness=\@tempvbadness
\hfuzz\@temphfuzz
%powrót do standardowych marginesów itp
\topmargin=\@temptopmargin
\headheight=\@tempheadheight
\headsep=\@tempheadsep
\oddsidemargin=\@tempoddsidemargin
\evensidemargin=\@tempevensidemargin
\textwidth=\@temptextwidth
%powrót z rozmiaru 12pt do rozmiaru czcionki zależnego od wyboru
\let\normalsize=\@tempnormalsize
\let\small=\@tempsmall
\let\footnotesize=\@tempfootnotesize
\let\scriptsize=\@tempscriptsize
\let\tiny=\@temptiny
\let\large=\@templarge
\let\Large=\@tempLarge
\let\LARGE=\@tempLARGE
\let\huge=\@temphuge
\let\Huge=\@tempHuge

  \setcounter{footnote}{0}%
  \global\let\thanks\relax
  \global\let\maketitle\relax
  \global\let\@thanks\@empty
  \global\let\@author\@empty
  \global\let\@date\@empty
  \global\let\@title\@empty
  \global\let\title\relax
  \global\let\author\relax
  \global\let\date\relax
  \global\let\and\relax
}
%nowe polecenie dla złożenia opcjonalnej dedykacji
\newcommand{\dedication}[2]{%
\if@archive\else
  \if@openright\cleardoublepage\else\clearpage\fi
  \thispagestyle{empty}%
  \setcounter{page}\@ne
  \mbox{}\vfill
  \hfill
  \parbox{#1}{\itshape#2}\hspace{1.5cm}
  \if@openright\vspace{1.5cm}\cleardoublepage\else\vspace{5.5cm}\clearpage\fi
  \setcounter{page}\@ne
\fi
}
%
%kod nie zmieniony z klasy book.cls, czyli definicje poleceń podziału dokumentu i innych poleceń i otoczeń
\newcommand*\chaptermark[1]{}
\setcounter{secnumdepth}{2}
\newcounter {part}
\newcounter {chapter}
\newcounter {section}[chapter]
\newcounter {subsection}[section]
\newcounter {subsubsection}[subsection]
\newcounter {paragraph}[subsubsection]
\newcounter {subparagraph}[paragraph]
\renewcommand \thepart {\@Roman\c@part}
\renewcommand \thechapter {\@arabic\c@chapter}
\renewcommand \thesection {\thechapter.\@arabic\c@section}
\renewcommand\thesubsection   {\thesection.\@arabic\c@subsection}
\renewcommand\thesubsubsection{\thesubsection .\@arabic\c@subsubsection}
\renewcommand\theparagraph    {\thesubsubsection.\@arabic\c@paragraph}
\renewcommand\thesubparagraph {\theparagraph.\@arabic\c@subparagraph}
\newcommand\@chapapp{\chaptername}
\newcommand\frontmatter{%
    \cleardoublepage
  \@mainmatterfalse
  \pagenumbering{roman}}
\newcommand\mainmatter{%
    \cleardoublepage
  \@mainmattertrue
  \pagenumbering{arabic}}
\newcommand\backmatter{%
  \if@openright
    \cleardoublepage
  \else
    \clearpage
  \fi
  \@mainmatterfalse}
\newcommand\part{%
  \if@openright
    \cleardoublepage
  \else
    \clearpage
  \fi
  \thispagestyle{plain}%
  \if@twocolumn
    \onecolumn
    \@tempswatrue
  \else
    \@tempswafalse
  \fi
  \null\vfil
  \secdef\@part\@spart}

\def\@part[#1]#2{%
    \ifnum \c@secnumdepth >-2\relax
      \refstepcounter{part}%
      \addcontentsline{toc}{part}{\thepart\hspace{1em}#1}%
    \else
      \addcontentsline{toc}{part}{#1}%
    \fi
    \markboth{}{}%
    {\centering
     \interlinepenalty \@M
     \normalfont
     \ifnum \c@secnumdepth >-2\relax
       \huge\bfseries \partname\nobreakspace\thepart
       \par
       \vskip 20\p@
     \fi
     \Huge \bfseries #2\par}%
    \@endpart}
\def\@spart#1{%
    {\centering
     \interlinepenalty \@M
     \normalfont
     \Huge \bfseries #1\par}%
    \@endpart}
\def\@endpart{\vfil\newpage
              \if@twoside
               \if@openright
                \null
                \thispagestyle{empty}%
                \newpage
               \fi
              \fi
              \if@tempswa
                \twocolumn
              \fi}
\newcommand\chapter{\if@openright\cleardoublepage\else\clearpage\fi
                    \thispagestyle{empty}%
                    \global\@topnum\z@
                    \@afterindentfalse
                    \secdef\@chapter\@schapter}
\def\@chapter[#1]#2{\ifnum \c@secnumdepth >\m@ne
                       \if@mainmatter
                         \refstepcounter{chapter}%
                         \typeout{\@chapapp\space\thechapter.}%
                         \addcontentsline{toc}{chapter}%
                                   {\protect\numberline{\thechapter}#1}%
                       \else
                         \addcontentsline{toc}{chapter}{#1}%
                       \fi
                    \else
                      \addcontentsline{toc}{chapter}{#1}%
                    \fi
                    \chaptermark{#1}%
                    \addtocontents{lof}{\protect\addvspace{10\p@}}%
                    \addtocontents{lot}{\protect\addvspace{10\p@}}%
                    \if@twocolumn
                      \@topnewpage[\@makechapterhead{#2}]%
                    \else
                      \@makechapterhead{#2}%
                      \@afterheading
                    \fi}
\def\@makechapterhead#1{%
  \vspace*{50\p@}%
  {\parindent \z@ \raggedright \normalfont
    \ifnum \c@secnumdepth >\m@ne
      \if@mainmatter
        \huge\bfseries \@chapapp\space \thechapter
        \par\nobreak
        \vskip 20\p@
      \fi
    \fi
    \interlinepenalty\@M
    \Huge \bfseries #1\par\nobreak
    \vskip 40\p@
  }}
\def\@schapter#1{\if@twocolumn
                   \@topnewpage[\@makeschapterhead{#1}]%
                 \else
                   \@makeschapterhead{#1}%
                   \@afterheading
                 \fi}
\def\@makeschapterhead#1{%
  \vspace*{50\p@}%
  {\parindent \z@ \raggedright
    \normalfont
    \interlinepenalty\@M
    \Huge \bfseries  #1\par\nobreak
    \vskip 40\p@
  }}
\newcommand\section{\@startsection {section}{1}{\z@}%
                                   {-3.5ex \@plus -1ex \@minus -.2ex}%
                                   {2.3ex \@plus.2ex}%
                                   {\normalfont\Large\bfseries}}
\newcommand\subsection{\@startsection{subsection}{2}{\z@}%
                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
                                     {1.5ex \@plus .2ex}%
                                     {\normalfont\large\bfseries}}
\newcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}%
                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
                                     {1.5ex \@plus .2ex}%
                                     {\normalfont\normalsize\bfseries}}
\newcommand\paragraph{\@startsection{paragraph}{4}{\z@}%
                                    {3.25ex \@plus1ex \@minus.2ex}%
                                    {-1em}%
                                    {\normalfont\normalsize\bfseries}}
\newcommand\subparagraph{\@startsection{subparagraph}{5}{\parindent}%
                                       {3.25ex \@plus1ex \@minus .2ex}%
                                       {-1em}%
                                      {\normalfont\normalsize\bfseries}}
\if@twocolumn
  \setlength\leftmargini  {2em}
\else
  \setlength\leftmargini  {2.5em}
\fi
\leftmargin  \leftmargini
\setlength\leftmarginii  {2.2em}
\setlength\leftmarginiii {1.87em}
\setlength\leftmarginiv  {1.7em}
\if@twocolumn
  \setlength\leftmarginv  {.5em}
  \setlength\leftmarginvi {.5em}
\else
  \setlength\leftmarginv  {1em}
  \setlength\leftmarginvi {1em}
\fi
\setlength  \labelsep  {.5em}
\setlength  \labelwidth{\leftmargini}
\addtolength\labelwidth{-\labelsep}
\@beginparpenalty -\@lowpenalty
\@endparpenalty   -\@lowpenalty
\@itempenalty     -\@lowpenalty
\renewcommand\theenumi{\@arabic\c@enumi}
\renewcommand\theenumii{\@alph\c@enumii}
\renewcommand\theenumiii{\@roman\c@enumiii}
\renewcommand\theenumiv{\@Alph\c@enumiv}
\newcommand\labelenumi{\theenumi.}
\newcommand\labelenumii{(\theenumii)}
\newcommand\labelenumiii{\theenumiii.}
\newcommand\labelenumiv{\theenumiv.}
\renewcommand\p@enumii{\theenumi}
\renewcommand\p@enumiii{\theenumi(\theenumii)}
\renewcommand\p@enumiv{\p@enumiii\theenumiii}
\newcommand\labelitemi{\textbullet}
\newcommand\labelitemii{\normalfont\bfseries \textendash}
\newcommand\labelitemiii{\textasteriskcentered}
\newcommand\labelitemiv{\textperiodcentered}
\newenvironment{description}
               {\list{}{\labelwidth\z@ \itemindent-\leftmargin
                        \let\makelabel\descriptionlabel}}
               {\endlist}
\newcommand*\descriptionlabel[1]{\hspace\labelsep
                                \normalfont\bfseries #1}
\newenvironment{verse}
               {\let\\\@centercr
                \list{}{\itemsep      \z@
                        \itemindent   -1.5em%
                        \listparindent\itemindent
                        \rightmargin  \leftmargin
                        \advance\leftmargin 1.5em}%
                \item\relax}
               {\endlist}
\newenvironment{quotation}
               {\list{}{\listparindent 1.5em%
                        \itemindent    \listparindent
                        \rightmargin   \leftmargin
                        \parsep        \z@ \@plus\p@}%
                \item\relax}
               {\endlist}
\newenvironment{quote}
               {\list{}{\rightmargin\leftmargin}%
                \item\relax}
               {\endlist}

\newenvironment{titlepage}
    {%
      \cleardoublepage
      \thispagestyle{empty}%
      \setcounter{page}\@ne
    }%
    {\newpage
     \if@twoside\setcounter{page}\z@\else
        \setcounter{page}\@ne
     \fi
    }
\newcommand\appendix{\par
  \setcounter{chapter}{0}%
  \setcounter{section}{0}%
  \gdef\@chapapp{\appendixname}%
  \gdef\thechapter{\@Alph\c@chapter}}
\setlength\arraycolsep{5\p@}
\setlength\tabcolsep{6\p@}
\setlength\arrayrulewidth{.4\p@}
\setlength\doublerulesep{2\p@}
\setlength\tabbingsep{\labelsep}
\skip\@mpfootins = \skip\footins
\setlength\fboxsep{3\p@}
\setlength\fboxrule{.4\p@}
\@addtoreset {equation}{chapter}
\renewcommand\theequation
  {\ifnum \c@chapter>\z@ \thechapter.\fi \@arabic\c@equation}
\newcounter{figure}[chapter]
\renewcommand \thefigure
     {\ifnum \c@chapter>\z@ \thechapter.\fi \@arabic\c@figure}
\def\fps@figure{tbp}
\def\ftype@figure{1}
\def\ext@figure{lof}
\def\fnum@figure{\figurename\nobreakspace\thefigure}
\newenvironment{figure}
               {\@float{figure}}
               {\end@float}
\newenvironment{figure*}
               {\@dblfloat{figure}}
               {\end@dblfloat}
\newcounter{table}[chapter]
\renewcommand \thetable
     {\ifnum \c@chapter>\z@ \thechapter.\fi \@arabic\c@table}
\def\fps@table{tbp}
\def\ftype@table{2}
\def\ext@table{lot}
\def\fnum@table{\tablename\nobreakspace\thetable}
\newenvironment{table}
               {\@float{table}}
               {\end@float}
\newenvironment{table*}
               {\@dblfloat{table}}
               {\end@dblfloat}
\newlength\abovecaptionskip
\newlength\belowcaptionskip
\setlength\abovecaptionskip{10\p@}
\setlength\belowcaptionskip{0\p@}
%tutaj jest zmiana, zostały usunięte dwukropki
\long\def\@makecaption#1#2{%
  \vskip\abovecaptionskip
  \sbox\@tempboxa{#1~~#2}%
  \ifdim \wd\@tempboxa >\hsize
    #1~~#2\par%
  \else
    \global \@minipagefalse
    \hb@xt@\hsize{\hfil\box\@tempboxa\hfil}%
  \fi
  \vskip\belowcaptionskip}
\DeclareOldFontCommand{\rm}{\normalfont\rmfamily}{\mathrm}
\DeclareOldFontCommand{\sf}{\normalfont\sffamily}{\mathsf}
\DeclareOldFontCommand{\tt}{\normalfont\ttfamily}{\mathtt}
\DeclareOldFontCommand{\bf}{\normalfont\bfseries}{\mathbf}
\DeclareOldFontCommand{\it}{\normalfont\itshape}{\mathit}
\DeclareOldFontCommand{\sl}{\normalfont\slshape}{\@nomath\sl}
\DeclareOldFontCommand{\sc}{\normalfont\scshape}{\@nomath\sc}
\DeclareRobustCommand*\cal{\@fontswitch\relax\mathcal}
\DeclareRobustCommand*\mit{\@fontswitch\relax\mathnormal}
\newcommand\@pnumwidth{1.55em}
\newcommand\@tocrmarg{2.55em}
\newcommand\@dotsep{4.5}
\setcounter{tocdepth}{2}
\newcommand\tableofcontents{%
    \chapter*{\contentsname
        \@mkboth{%
           \MakeUppercase\contentsname}{\MakeUppercase\contentsname}}%
    \@starttoc{toc}%
    }
\newcommand*\l@part[2]{%
  \ifnum \c@tocdepth >-2\relax
    \addpenalty{-\@highpenalty}%
    \addvspace{2.25em \@plus\p@}%
    \setlength\@tempdima{3em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      {\leavevmode
       \large \bfseries #1\hfil \hb@xt@\@pnumwidth{\hss #2}}\par
       \nobreak
         \global\@nobreaktrue
         \everypar{\global\@nobreakfalse\everypar{}}%
    \endgroup
  \fi}
\newcommand*\l@chapter[2]{%
  \ifnum \c@tocdepth >\m@ne
    \addpenalty{-\@highpenalty}%
    \vskip 1.0em \@plus\p@
    \setlength\@tempdima{1.5em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      \leavevmode \bfseries
      \advance\leftskip\@tempdima
      \hskip -\leftskip
      #1\nobreak\hfil \nobreak\hb@xt@\@pnumwidth{\hss #2}\par
      \penalty\@highpenalty
    \endgroup
  \fi}
\newcommand*\l@section{\@dottedtocline{1}{1.5em}{2.3em}}
\newcommand*\l@subsection{\@dottedtocline{2}{3.8em}{3.2em}}
\newcommand*\l@subsubsection{\@dottedtocline{3}{7.0em}{4.1em}}
\newcommand*\l@paragraph{\@dottedtocline{4}{10em}{5em}}
\newcommand*\l@subparagraph{\@dottedtocline{5}{12em}{6em}}
\newcommand\listoffigures{%
    \chapter*{\listfigurename}%
      \@mkboth{\MakeUppercase\listfigurename}%
              {\MakeUppercase\listfigurename}%
    \@starttoc{lof}%
    }
\newcommand*\l@figure{\@dottedtocline{1}{1.5em}{2.3em}}
\newcommand\listoftables{%
    \chapter*{\listtablename}%
      \@mkboth{%
          \MakeUppercase\listtablename}%
         {\MakeUppercase\listtablename}%
    \@starttoc{lot}%
    }
\let\l@table\l@figure
\newdimen\bibindent
\setlength\bibindent{1.5em}
\newenvironment{thebibliography}[1]
     {\chapter*{\bibname}%
      \@mkboth{\MakeUppercase\bibname}{\MakeUppercase\bibname}%
      \list{\@biblabel{\@arabic\c@enumiv}}%
           {\settowidth\labelwidth{\@biblabel{#1}}%
            \leftmargin\labelwidth
            \advance\leftmargin\labelsep
            \@openbib@code
            \usecounter{enumiv}%
            \let\p@enumiv\@empty
            \renewcommand\theenumiv{\@arabic\c@enumiv}}%
      \sloppy
      \clubpenalty4000
      \@clubpenalty \clubpenalty
      \widowpenalty4000%
      \sfcode`\.\@m}
     {\def\@noitemerr
       {\@latex@warning{Empty `thebibliography' environment}}%
      \endlist}
\newcommand\newblock{\hskip .11em\@plus.33em\@minus.07em}
\let\@openbib@code\@empty
\newenvironment{theindex}
               {\twocolumn[\@makeschapterhead{\indexname}]%
                \@mkboth{\MakeUppercase\indexname}%
                        {\MakeUppercase\indexname}%
                \thispagestyle{plain}\parindent\z@
                \parskip\z@ \@plus .3\p@\relax
                \columnseprule \z@
                \columnsep 35\p@
                \let\item\@idxitem}
               {\clearpage}
\newcommand\@idxitem{\par\hangindent 40\p@}
\newcommand\subitem{\@idxitem \hspace*{20\p@}}
\newcommand\subsubitem{\@idxitem \hspace*{30\p@}}
\newcommand\indexspace{\par \vskip 10\p@ \@plus5\p@ \@minus3\p@\relax}
\renewcommand\footnoterule{%
  \kern-3\p@
  \hrule\@width.4\columnwidth
  \kern2.6\p@}
\@addtoreset{footnote}{chapter}
\newcommand\@makefntext[1]{%
    \parindent 1em%
    \noindent
    \hb@xt@1.8em{\hss\@makefnmark}#1}
\newcommand\contentsname{Contents}
\newcommand\listfigurename{List of Figures}
\newcommand\listtablename{List of Tables}
\newcommand\bibname{Bibliography}
\newcommand\indexname{Index}
\newcommand\figurename{Figure}
\newcommand\tablename{Table}
\newcommand\partname{Part}
\newcommand\chaptername{Chapter}
\newcommand\appendixname{Appendix}
\def\today{\ifcase\month\or
  January\or February\or March\or April\or May\or June\or
  July\or August\or September\or October\or November\or December\fi
  \space\number\day, \number\year}
\setlength\columnsep{10\p@}
\setlength\columnseprule{0\p@}
\pagestyle{headings}
\pagenumbering{arabic}
\if@twoside
\else
  \raggedbottom
\fi
\if@twocolumn
  \twocolumn
  \sloppy
  \flushbottom
\else
  \onecolumn
\fi

%poniżej kod usuwający paginę z pustych stron na końcu rozdziałów przy włączonej opcji openright, zaczerpnięte od American Mathematical Society ze strony http://www.ams.org/authors/author-faq.html
\let\cleardouble@page\cleardoublepage
\AtBeginDocument{%
  \ifx\cleardouble@page\cleardoublepage
    \def\cleardoublepage{\clearpage
      {\pagestyle{empty}\cleardouble@page}}%
  \fi
}
\endinput
%%
%% End of file `mgr.cls'.
