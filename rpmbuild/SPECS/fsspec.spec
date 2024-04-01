Name:           fsspec
Version:        2024.3.1
Release:        1%{?dist}
Summary:        Filesystem interfaces for Python

License:        BSD
URL:            https://github.com/intake/filesystem_spec
Source0:        fsspec-2024.3.1.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%description
Fsspec is a Python package that provides a unified interface to filesystem operations, similar to `os.path`.

%prep
%autosetup -n fsspec-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --root $RPM_BUILD_ROOT

%files
%doc README.md
/usr/lib/python3.9/site-packages/fsspec*

%changelog
* Wed Mar 27 2024 Junjun Liu - 2024.3.1-1
- Initial package

