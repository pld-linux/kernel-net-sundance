
# conditional build
# _without_dist_kernel          without distribution kernel

%define         _rel 1

Summary:	DLINK Sundance driver for Linux
Summary(pl):	Sterownik do karty Sundance dla Linuksa
Name:		kernel-net-sundance
Version:	1.02d
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
# from http://www.cbk.no/produkter/drivere/d-link/Adapters/DFE-580TX/Driver/linux.tgz
Source0:	dlink-sundance.tar.gz
%{!?_without_dist_kernel:BuildRequires:         kernel-headers }
BuildRequires:	%{kgcc_package}
Provides:	kernel(sundance)
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DLINK Sundance driver for Linux.

%description -l pl
Sterownik do karty Sundance dla Linuksa.

%package -n kernel-smp-net-sundance
Summary:	DLINK Sundance driver for Linux SMP
Summary(pl):	Sterownik do karty Sundance dla Linuksa SMP
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Provides:	kernel(sundance)

%description -n kernel-smp-net-sundance
DLINK Sundance driver for Linux SMP.

%description -n kernel-smp-net-sundance -l pl
Sterownik do karty Sundance dla Linuksa SMP.

%prep
%setup -q -n dlink-sundance

%build
%{__make} SMP=1 CC="%{kgcc} -DCONFIG_X86_LOCAL_APIC -DSTB_WA"
mv -f sundance.o sundance-smp
%{__make} clean
%{__make} CC="%{kgcc} -DSTB_WA"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc

install sundance-smp $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/sundance.o
install sundance.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/sundance.o

%clean
rm -rf $RPM_BUILD_ROOT

%pre
mv `find /lib/modules/%{_kernel_ver} -name sundance.o` `find /lib/modules/%{_kernel_ver} -name sundance.o|sed 's/\.o/_old.o/'`

%post
/sbin/depmod -a

%postun
mv `find /lib/modules/%{_kernel_ver} -name sundance_old.o` `find /lib/modules/%{_kernel_ver} -name sundance_old.o|sed 's/|old.o/.o/'`
/sbin/depmod -a

%post -n kernel-smp-net-sundance
/sbin/depmod -a

%postun -n kernel-smp-net-sundance
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc readme.txt
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-net-sundance
%defattr(644,root,root,755)
%doc readme.txt
/lib/modules/%{_kernel_ver}smp/misc/*
