
# conditional build
# _without_dist_kernel          without distribution kernel

%define		_kernel24	%(echo %{_kernel_ver} | grep -q '2\.[012]\.' ; echo $?)
%if %{_kernel24}
%define	_ver	1.02d
%else
%define	_ver	1.01d
%endif

Summary:	D-Link Sundance driver for Linux
Summary(pl):	Sterownik do karty D-Link Sundance dla Linuksa
Name:		kernel-net-sundance
Version:	%{_ver}
%define	_rel	7
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
# version 1.01d for kernel 2.2
Source0:	ftp://ftp.dlink.co.uk/pub/adapters/dfe-550tx/dlh5x-2.2.tgz
# version 1.02d for kernel 2.4
# from "ftp://ftp.dlink.co.uk/pub/adapters/dfe-580tx/linux 2.4x.tgz"
Source1:	dlink-sundance.tar.gz
Patch0:		%{name}-header.patch
%{!?_without_dist_kernel:BuildRequires:         kernel-headers }
BuildRequires:	%{kgcc_package}
Provides:	kernel(sundance)
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
D-Link Sundance driver for Linux. It supports D-Link DFE-550TX (Fast
Ethernet), DFE-530TXS (Fast Ethernet 10/100), DFE-550FX
(Fiber-optics), DFE-580TX (Quad Channel) and DL10050-based (Gigabit
Ethernet) cards.

%description -l pl
Sterownik do kart D-Link Sundance dla Linuksa. Obs³uguje karty D-Link
DFE-550TX (Fast Ethernet), DFE-530TXS (Fast Ethernet 10/100),
DFE-550FX (¶wiat³owodowe), DFE-580TX (4-portowe) oraz oparte na
DL10050 (Gigabit Ethernet).

%package -n kernel-smp-net-sundance
Summary:	D-Link Sundance driver for Linux SMP
Summary(pl):	Sterownik do karty D-Link Sundance dla Linuksa SMP
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Provides:	kernel(sundance)

%description -n kernel-smp-net-sundance
D-Link Sundance driver for Linux SMP. It supports D-Link DFE-550TX
(Fast Ethernet), DFE-530TXS (Fast Ethernet 10/100), DFE-550FX
(Fiber-optics), DFE-580TX (Quad Channel) and DL10050-based (Gigabit
Ethernet) cards.


%description -n kernel-smp-net-sundance -l pl
Sterownik do karty D-Link Sundance dla Linuksa SMP. Obs³uguje karty
D-Link DFE-550TX (Fast Ethernet), DFE-530TXS (Fast Ethernet 10/100),
DFE-550FX (¶wiat³owodowe), DFE-580TX (4-portowe) oraz oparte na
DL10050 (Gigabit Ethernet).

%prep
%if %{_kernel24}
%setup -q -T -b1 -n dlink-sundance
%else
%setup -q -c
%patch -p1
%endif

%build
%{__make} CC="%{kgcc}" \
	CFLAGS="%{rpmcflags} -D__KERNEL__ -DMODULE -D__SMP__ \
%ifarch %{ix86}
	-DCONFIG_X86_LOCAL_APIC \
%endif
	-Wall -I%{_kernelsrcdir}/include"
mv -f sundance.o sundance-smp
%{__make} clean
%{__make} CC="%{kgcc}" \
	CFLAGS="%{rpmcflags} -D__KERNEL__ -DMODULE -Wall -I%{_kernelsrcdir}/include"

%install
rm -rf $RPM_BUILD_ROOT

install -D sundance-smp $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/sundance.o
install -D sundance.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/sundance.o

%clean
rm -rf $RPM_BUILD_ROOT

%pre
FNAME="`find /lib/modules/%{_kernel_ver} -name sundance.o`"
if [ -f "$FNAME" ]; then
	mv -f "$FNAME" `echo "$FNAME" |sed 's/\.o/_old.o/'`
fi

%post
/sbin/depmod -a

%postun
FNAME="`find /lib/modules/%{_kernel_ver} -name sundance_old.o`"
if [ -f "$FNAME" ]; then
	mv -f "$FNAME" `echo "$FNAME" |sed 's/_old.o/\.o/'`
fi
/sbin/depmod -a

%pre	-n kernel-smp-net-sundance
FNAME="`find /lib/modules/%{_kernel_ver}smp -name sundance.o`"
if [ -f "$FNAME" ]; then
	mv -f "$FNAME" `echo "$FNAME" |sed 's/\.o/_old.o/'`
fi

%post	-n kernel-smp-net-sundance
/sbin/depmod -a

%postun	-n kernel-smp-net-sundance
FNAME="`find /lib/modules/%{_kernel_ver}smp -name sundance_old.o`"
if [ -f "$FNAME" ]; then
	mv -f "$FNAME" `echo "$FNAME" |sed 's/_old.o/\.o/'`
fi
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc readme.txt
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-net-sundance
%defattr(644,root,root,755)
%doc readme.txt
/lib/modules/%{_kernel_ver}smp/misc/*
