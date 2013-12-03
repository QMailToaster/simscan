Name:		simscan
Summary:	Simscan for qmail-toaster
Version:	1.4.0
Release:	0%{?dist}
License:	GPLv2
Group:		Networking/Other
URL:		http://inter7.com/index.php?page=simscan
Source0:	http://downloads.sourceforge.net/project/simscan/simscan/simscan-1.4.0/%{name}-%{version}.tar.gz
Source1:	update-simscan
Source2:	simcontrol
Patch0:		simscan-1.4.0-combined.4.patch
Patch1:		simscan-o_create.patch
Patch2:		simscan-nouserchk.patch
Patch3:		simscan-noripchk.patch
Patch4:		simscan-nosapchk.patch
Patch5:		simscan-nocavdbchk.patch
Patch6:		simscan-nostlchk.patch
Requires:	clamav
Requires:	qmail
Requires:	ripmime
Requires:	spamassassin
Obsoletes:      simscan-toaster
BuildRoot:      %{_topdir}/BUILDROOT/%{name}-%{version}-%{release}.%{_arch}

%define qdir    /var/qmail
%define qbin    %{qdir}/bin
%define qcon    %{qdir}/control
%define qtcp    %{_sysconfdir}/tcprules.d/tcp.smtp
%define debug_package %{nil}


#-------------------------------------------------------------------------------
%description
#-------------------------------------------------------------------------------
SimScan is a simplified scanner for qmail similar to qmail-scanner and qscand.
It uses clamav, trophie, spamassassin, and/or dspam.
It also supports attachment blocking by extension.
Simscan is written entirely in C to ensure maximum speed.
There are options to allow simscan to scan per domain, and reject spam mail.


                Current settings
     ---------------------------------------
     user                  = clamav
     qmail directory       = /var/qmail
     work directory        = /var/qmail/simscan
     control directory     = /var/qmail/control
     qmail queue program   = /var/qmail/bin/qmail-queue
     clamdscan program     = /usr/bin/clamdscan
     clamav scan           = ON
     trophie scanning      = OFF
     attachement scan      = ON
     ripmime program       = /usr/bin/ripmime
     custom smtp reject    = ON
     drop message          = OFF
     regex scanner         = OFF
     quarantine processing = OFF
     domain based checking = ON
     add received header   = ON
     spam scanning         = ON
     spamassassin program  = /usr/bin/spamassassin
     spamc program         = /usr/bin/spamc
     spamc arguments       =
     spamc user            = OFF
     authenticated users scanned = OFF
     spam passthru         = OFF
     spam hits             = 40

#-------------------------------------------------------------------------------
%prep
#-------------------------------------------------------------------------------
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

#-------------------------------------------------------------------------------
%build
#-------------------------------------------------------------------------------
%configure \
      --enable-attach \
      --enable-clamdscan=/usr/bin/clamdscan \
      --enable-clamavdb-path=/usr/share/clamav \
      --enable-custom-smtp-reject \
      --enable-per-domain \
      --enable-qmaildir=/var/qmail \
      --enable-qmail-queue=/var/qmail/bin/qmail-queue \
      --enable-received \
      --enable-ripmime=/usr/bin/ripmime \
      --enable-sigtool-path=/usr/bin/sigtool \
      --enable-spam \
      --enable-spam-hits=40 \
      --enable-spamassassin-path=/usr/bin/spamassassin \
      --enable-spamc=/usr/bin/spamc \
      --enable-user=clamav
%{__make}

#-------------------------------------------------------------------------------
%install
#-------------------------------------------------------------------------------
rm -rf %{buildroot}

install -d %{buildroot}%{qdir}
install -d %{buildroot}%{qdir}/%{name}

install -Dp %{_sourcedir}/update-simscan  %{buildroot}%{qbin}
install -Dp %{_sourcedir}/simcontrol      %{buildroot}%{qcon}

install $RPM_BUILD_DIR/%{name}-%{version}/%{name}   %{buildroot}%{qbin}/%{name}
install $RPM_BUILD_DIR/%{name}-%{version}/simscanmk %{buildroot}%{qbin}/simscanmk

for i in AUTHORS ChangeLog INSTALL README TODO ssattach.example; do
  install -Dp $RPM_BUILD_DIR/%{name}-%{version}/$i \
        %{buildroot}%{_datadir}/doc/%{name}-%{version}/$i
done

#-------------------------------------------------------------------------------
%clean
#-------------------------------------------------------------------------------
rm -rf %{buildroot}

#-------------------------------------------------------------------------------
%post
#-------------------------------------------------------------------------------

./%{qbin}/update-%{name}

#-------------------------------------------------------------------------------
%files 
#-------------------------------------------------------------------------------
%defattr(644,clamav,clamav)
%attr(0750,clamav,root) %dir %{qdir}/%{name}
%attr(4711,clamav,root) %{qbin}/%{name}
%attr(4755,root,root)   %{qbin}/simscanmk
%attr(0755,root,root)   %{qbin}/update-%{name}

%attr(0644,root,root)   %{_datadir}/doc/%{name}-%{version}/*

%attr(0644,clamav,root) %config(noreplace) %{qcon}/simcontrol

#-------------------------------------------------------------------------------
%changelog
#-------------------------------------------------------------------------------
* Sat Nov 16 2013 Eric Shubert <eric@datamatters.us> 1.4.0-0.qt
- Migrated to repoforge
- Removed -toaster designation
- Added CentOS 6 support
- Removed unsupported cruft
* Mon Mar 26 2012 Eric Shubert <ejs@shubes.net> 1.4.0-1.4.0
- Changed jms1 combined 3 patch to combined 4 patch
- Set o+s on simscanmk file so that non-root users can run it
- Added update-simscan script for running simscanmk from freshclam etc.
- Modified simcontrol file to be %config(noreplace)
* Thu Aug 13 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.0-1.3.8
- Changed minor version number to align with version changes and scripts
* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.0-1.3.1
- Changed spec file so that tcp.smtp file is no longer overwritten and a tcp.smtp.new is created
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Thu Jun 11 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.0-1.3.1
- Added Mandriva 2009 support
- Increased spam_hits to 40 from the original 20
* Thu Apr 23 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.0-1.3.0
- Merged the fork into the main QMT trunk. Thanks to Steve for the package and testing.
- Added Suse 11.1, Fedora 9, Fedora 9 x86_64, Fedora 10, and Fedora 10 x86_64 support
- Patched simscanmk.c to compile with new distro compiler flags (O_CREAT error)
* Wed May 7 2008 Steve Huff <shuff@vecna.org> 1.4.0-1.4.0
- Updated to simscan 1.4.0
- Added John Simpson's patch to support varying ClamAV update file locations
  (http://qmail.jms1.net/simscan/)
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 1.2-1.3.6
- Added CentOS 5 i386 support
- Added CentOS 5 x86_64 support
- Removed DKVERIFY - domainkeys now only signs outgoing mail
* Sat Mar 03 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.3.1-1.3.5
- Skipped RBL checks on localhost
- Modified DKVERIFY to safer defaults
* Thu Jan 11 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.3.1-1.3.4
- Added fix to allow building with ClamAV 0.90rc2 and above, which doesn't use daily.cvd and main.cvd
* Mon Jan 08 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.3.1-1.3.3
- Upgraded to Simscan 1.3.1
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.2-1.3.2
- Added Fedora Core 6 support
* Mon Jun 05 2006 Nick Hemmesch <nick@ndhsoft.com> 1.2-1.3.1
- Added per domain and spam hits to config
- Added SuSE 10.1 support
* Thu May 18 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.2-1.2.8
- Enabled simscan in configure line
- Added ripmime-toaster to Requires line
* Sat May 13 2006 Nick Hemmesch <nick@ndhsoft.com> 1.2-1.2.7
- Update to simscan-1.2
- Add Fedora Core 5 support
* Sun Nov 20 2005 Nick Hemmesch <nick@ndhsoft.com> 1.1-1.2.6
- Add SuSE 10.0 and Mandriva 2006.0 support
* Sat Oct 15 2005 Nick Hemmesch <nick@ndhsoft.com> 1.1-1.2.5
- Add Fedora Core 4 x86_64 support
* Sat Oct 01 2005 Nick Hemmesch <nick@ndhsoft.com> 1.1-1.2.4
- Add CentOS 4 x86_64 support
* Fri Jul 01 2005 Nick Hemmesch <nick@ndhsoft.com> 1.1-1.2.3
- Add support for Fedora Core 4
* Fri Jun 03 2005 Torbjorn Turpeinen <tobbe@nyvalls.se> 1.1-1.2.2
- Gnu/Linux Mandrake 10.0,10.1,10.2 support
* Sat May 28 2005 Nick Hemmesch <nick@ndhsoft.com> 1.1-1.2.1
- Initial simscan-toaster build
