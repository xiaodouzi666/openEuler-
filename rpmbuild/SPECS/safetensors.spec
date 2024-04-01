%global debug_package %{nil}
Name:           safetensors
Version:        0.4.2
Release:        1%{?dist}
Summary:        Safe and simple way to store and load tensors in an open file format
License:        Apache-2.0
URL:            https://github.com/huggingface/safetensors
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-numpy

%description
Safetensors is a new simple format for storing tensors safely (as opposed to pickle)
and that is still fast (zero-copy). It also supports memory mapping of the files for
even faster loads.

%prep
%autosetup -n %{name}-%{version}

%build
export PATH="$HOME/.cargo/bin:$PATH"
%{__python3} -m pip wheel --no-deps --wheel-dir=. .

%install
export PATH="$HOME/.cargo/bin:$PATH"
WHEEL_FILE=$(ls *.whl)
/usr/bin/python3 -m pip install --no-deps --ignore-installed --root=%{buildroot} safetensors-*.whl

%files
/usr/lib64/python3.9/site-packages/safetensors*
/usr/lib64/python3.9/site-packages/safetensors-0.4.2.dist-info/*

%changelog
* Wed Mar 27 2024 Junjun Liu - 0.4.2-1
- Initial package

