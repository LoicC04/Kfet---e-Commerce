% \iffalse meta-comment
%
% Copyright 1993 1994 1995 1996 1997 1998 1999 2000 2001 2002 2003 2004
% The LaTeX3 Project and any individual authors listed elsewhere
% in this file. 
% 
% This file is part of the LaTeX base system.
% -------------------------------------------
% 
% It may be distributed and/or modified under the
% conditions of the LaTeX Project Public License, either version 1.3
% of this license or (at your option) any later version.
% The latest version of this license is in
%    http://www.latex-project.org/lppl.txt
% and version 1.3 or later is part of all distributions of LaTeX 
% version 2003/12/01 or later.
% 
% This file has the LPPL maintenance status "maintained".
% 
% The list of all files belonging to the LaTeX base distribution is
% given in the file `manifest.txt'. See also `legal.txt' for additional
% information.
% 
% The list of derived (unpacked) files belonging to the distribution 
% and covered by LPPL is defined by the unpacking scripts (with 
% extension .ins) which are part of the distribution.
% 
% \fi
%%
%% Minimal LaTeX class file.
%%
% 
% Adaptation for use by Polytech 
% Copyright 2006 by Lissy Alexandre <lissyx@users.sourceforge.net>
% $Id: polytech-presentation.cls 55 2010-06-28 10:34:41Z 20403346t $

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{polytech-presentation}[2006/10/02 Standard LaTeX Presentation Class for Polytech]

%----------- Traitement des options
\RequirePackage{ifthen}
\newboolean{BUTF8}
\newboolean{BLatin1}
\newboolean{BNoTOC}

\DeclareOption{UTF8}{
	\setboolean{BUTF8}{true}%
}

\DeclareOption{Latin1}{
	\setboolean{BLatin1}{true}%
}

\DeclareOption{NoTOC}{
	\setboolean{BNoTOC}{true}
}

\DeclareOption{Compress}{
	\PassOptionsToClass{compress}{beamer}
}

\ProcessOptions
%------------- Chargement de beamer
\RequirePackage{atbegshi}
\LoadClass{beamer}

\ifthenelse{\boolean{BLatin1}}
{\RequirePackage[latin1]{inputenc}}
{
 \ifthenelse{\boolean{BUTF8}}
	{\RequirePackage[utf8]{inputenc}}
	{\RequirePackage[utf8]{inputenc}}
}
\RequirePackage{pgf}
\RequirePackage[french,english]{babel}
\RequirePackage{colortbl}
\RequirePackage{color}
\RequirePackage{lmodern}
\RequirePackage[T1]{fontenc} 
\RequirePackage{times}
\RequirePackage{beamerthemeboxes}

\mode<article> % only for the article version
{
  \RequirePackage{fullpage}
  \RequirePackage{hyperref}
}

\mode<presentation>
{
  \usetheme{Polytech}
  \usecolortheme{polytech}
  \usefonttheme[onlysmall]{structurebold}
}

%\setbeamercolor{math text}{fg=green!50!black}
%\setbeamercolor{normal text in math text}{parent=math text}

\setbeamercovered{dynamic}

%
% The following info should normally be given in you main file:
%
% \pgfdeclaremask{ptech}{epu-mask}
% \pgfdeclareimage[mask=ptech,width=4cm]{polytech-big}{EPU_FR}
\pgfdeclareimage[width=3cm]{polytech}{logos/Logo_Polytech_Tours}
\pgfdeclareimage[width=6cm]{polytech-big}{logos/Logo_Polytech_Tours}
% \logo{\pgfuseimage{polytech}}

\institute{
	\pgfuseimage{polytech-big} \\ 
	\'Ecole Polytechnique de l'Universit\'e de Tours \\
	D\'epartement Informatique
	}

% \pgfdeclareimage[mask=ptech,width=1.5cm]{polytech}{EPU_FR}

% \AtBeginSubsection[]
% {
% }
%
%\part<presentation>{Main Talk}
%
%\section[Models]{The Model of Overhead-Free Computation}
%
%\subsection[Standard Model]{The Standard Model of Linear Space}
%
%\begin{frame}
%  \frametitle{Definition of Overhead-Free Computations}
%  \begin{Definition}
%    A Turing machine is \alert{overhead-free} if
%    \begin{itemize}
%    \item
%      it has only a single tape,
%    \item
%      writes only on input cells,
%    \item
%      writes only symbols drawn from the input alphabet.
%    \end{itemize}
%  \end{Definition}
%\end{frame}
