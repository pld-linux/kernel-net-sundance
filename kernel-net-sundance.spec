
# conditional build
# _without_dist_kernel          without distribution kernel

%define         _rel 1

Summary:	DLINK Sundance driver for Linux
Summary(pl):	Sterownik do karty Sundance
Name:		kernel-net-sundance
Version:	1.02d
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	dlink-sundance.tar.gz
%{!?_without_dist_kernel:BuildRequires:         kernel-headers }
BuildRequires:	%{kgcc_package}
Provides:	kernel(sundance)
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DLINK Sundance driver for Linux

%description -l pl
Sterownik do karty Sundance

%package -n kernel-smp-net-sundance
Summary:	DLINK Sundance driver for Linux SMP
Summary(pl):	Sterownik do karty Intel(R) PRO/100
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Obsoletes:	e100
Obsoletes:	linux-net-e100
Provides:	kernel(e100)

%description -n kernel-smp-net-sundance
DLINK Sundance driver for Linux SMP

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

%post
mv `find /lib/modules/%{_kernel_ver} -name sundance.o` `find /lib/modules/%{_kernel_ver} -name sundance.o|sed 's/\.o/_old.o/'`
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
