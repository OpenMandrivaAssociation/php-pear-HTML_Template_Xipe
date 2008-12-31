%define		_class		HTML
%define		_subclass	Template
%define		_status		stable
%define		_pearname	%{_class}_%{_subclass}_Xipe

%define		_requires_exceptions pear())

Summary:	%{_pearname} - A simple, fast and powerful template engine
Name:		php-pear-%{_pearname}
Version:	1.7.6
Release:	%mkrel 10
License:	PHP License
Group:		Development/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tar.bz2
URL:		http://pear.php.net/package/HTML_Template_Xipe/	
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	dos2unix
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The template engine is a compiling engine, all templates are compiled
into PHP-files. This will make the delivery of the files faster on the
next request, since the template doesn't need to be compiled again. If
the template changes it will be recompiled.

There is no new template language to learn. Beside the default mode,
there is a set of constructs since version 1.6 which allow you to edit
your templates with WYSIWYG editors.

By default the template engine uses indention for building blocks (you
can turn that off). This feature was inspired by Python and by the
need I felt to force myself to write proper HTML-code, using proper
indentions, to make the code better readable.

Every template is customizable in multiple ways. You can configure
each template or an entire directory to use different delimiters,
caching parameters, etc. via either an XML-file or a XML-chunk which
you simply write anywhere inside the tpl-code.

Using the Cache the final file can also be cached (i.e. a resulting
HTML-file). The caching options can be customized as needed. The cache
can reduce the server load by very much, since the entire php-file
doesn't need to be processed again, the resulting client-readable data
are simply delivered right from the cache (the data are saved using
php's output buffering).

The template engine is prepared to be used for multi-language
applications too. If you i.e. use the PEAR::I18N for translating the
template, the compiled templates need to be saved under a different
name for each language. The template engine is prepared for that too,
it saves the compiled template including the language code if required
(i.e. a compiled index.tpl which is saved for english gets the
filename index.tpl.en.php).

In PEAR status of this package is: %{_status}.

%prep

%setup -q -c

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix -U

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/Xipe/Filter

install %{_pearname}-%{version}/*.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}
install %{_pearname}-%{version}/Xipe/*.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/Xipe
install %{_pearname}-%{version}/Xipe/Filter/*.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/Xipe/Filter

install -d %{buildroot}%{_datadir}/pear/packages
install -m0644 package.xml %{buildroot}%{_datadir}/pear/packages/%{_pearname}.xml

%post
if [ "$1" = "1" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear install --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi
if [ "$1" = "2" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear upgrade -f --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi

%preun
if [ "$1" = 0 ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear uninstall --nodeps -r %{_pearname}
	fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%dir %{_datadir}/pear/%{_class}/%{_subclass}/Xipe
%dir %{_datadir}/pear/%{_class}/%{_subclass}/Xipe/Filter
%{_datadir}/pear/%{_class}/%{_subclass}/*.php
%{_datadir}/pear/%{_class}/%{_subclass}/Xipe/*.php
%{_datadir}/pear/%{_class}/%{_subclass}/Xipe/Filter/*.php

%{_datadir}/pear/packages/%{_pearname}.xml


