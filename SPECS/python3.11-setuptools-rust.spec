%global __python3 /usr/bin/python3.11
%global python3_pkgversion 3.11

%if 0%{?rhel}
%bcond_with tests
%else
%bcond_without tests
%endif

Name:           python%{python3_pkgversion}-setuptools-rust
Version:        1.5.2
Release:        1%{?dist}
Summary:        Setuptools Rust extension plugin

License:        MIT
URL:            https://github.com/PyO3/setuptools-rust
Source0:        %{pypi_source setuptools-rust}
BuildArch:      noarch
ExclusiveArch:  %{rust_arches}

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-rpm-macros
BuildRequires:  python%{python3_pkgversion}-setuptools > 46.1
BuildRequires:  python%{python3_pkgversion}-semantic_version >= 2.8.2
BuildRequires:  python%{python3_pkgversion}-wheel

Requires:       python%{python3_pkgversion}-semantic_version >= 2.8.2
Requires:       python%{python3_pkgversion}-setuptools >= 62.4
# RHEL: Dependency is missing
#BuildRequires:  python3dist(typing-extensions) >= 3.7.4.4
%if 0%{?fedora}
BuildRequires:  rust-packaging >= 1.45
%else
# RHEL has rust-toolset
BuildRequires:  rust-toolset >= 1.45
Requires:       rust-toolset >= 1.45
%endif
%if %{with tests}
BuildRequires:  rust-pyo3+default-devel
%endif

%description
Setuptools helpers for Rust Python extensions. Compile and distribute Python
extensions written in Rust as easily as if they were written in C.


%prep
%autosetup -n setuptools-rust-%{version}
# Remove bundled egg-info
rm -rf setuptools-rust.egg-info

%if ! 0%{?fedora}
# remove dependency on typing extensions and use
# stdlib instead
sed -i 's/typing_extensions.*$//g' setup.cfg

sed -i -e 's/typing_extensions/typing/' \
     setuptools_rust/setuptools_ext.py \
     setuptools_rust/build.py \
     setuptools_rust/extension.py

%endif


%build
%py3_build

%install
%py3_install

%check
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    %{__python3} -c "from setuptools_rust import RustExtension, version"

%if %{with tests}
cd examples/hello-world
%cargo_prep
PYTHONPATH=%{buildroot}%{python3_sitelib} %{__python3} setup.py build
cd ../..
%endif


%files -n python%{python3_pkgversion}-setuptools-rust
%doc README.md CHANGELOG.md
%license LICENSE
%{python3_sitelib}/setuptools_rust/
%{python3_sitelib}/setuptools_rust-%{version}-py%{python3_version}.egg-info/

%changelog
* Thu Nov 03 2022 Charalampos Stratakis <cstratak@redhat.com> - 1.5.2-1
- Initial import
- Fedora contributions by:
      Christian Heimes <cheimes@redhat.com>
      Gwyn Ciesla <limb@fedoraproject.org>
      Tomáš Hrnčiar <thrnciar@redhat.com>
