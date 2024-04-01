%global debug_package %{nil}
Name:           tokenizers
Version:        0.15.2
Release:        1%{?dist}
Summary:        Tokenizers: Fast and Customizable Tokenizers
License:        MIT
URL:            https://github.com/huggingface/tokenizers
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires: rust >= 1.41.0

%description
The tokenizers library is a fast and efficient library to tokenize text and train new models. It is designed to be as fast as possible, and to provide the most efficient tokenization available.

%prep
%autosetup -n %{name}-%{version}

%build
export PATH="$HOME/.cargo/bin:$PATH"
%{__python3} -m pip wheel --no-deps --wheel-dir=. .

%install
export PATH="$HOME/.cargo/bin:$PATH"
WHEEL_FILE=$(ls *.whl)
%{__python3} -m pip install --no-deps --ignore-installed --root=%{buildroot} $WHEEL_FILE
find %{buildroot} -print

%files
/usr/lib64/python3.9/site-packages/%{name}*
/usr/lib64/python3.9/site-packages/%{name}-%{version}.dist-info/*

%changelog
* Wed Mar 27 2024 Junjun Liu - 0.15.2-1
- Initial package

