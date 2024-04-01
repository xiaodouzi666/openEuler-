Name:           huggingface_hub
Version:        0.22.0
Release:        1%{?dist}
Summary:        Hugging Face Hub API client

Group:          Development/Libraries
License:        Apache-2.0
URL:            https://github.com/huggingface/huggingface_hub
Source0:        huggingface_hub-0.22.0.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

%description
The Hugging Face Hub library allows you to interact with Hugging Face models & datasets.

%prep
%setup -q -n huggingface_hub-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --root=$RPM_BUILD_ROOT --skip-build

%files
/usr/bin/huggingface-cli
/usr/lib/python3.9/site-packages/huggingface_hub*

%changelog
* Wed Mar 27 2024 Junjun Liu <youremail@example.com> - 0.22.0-1
- Initial RPM release
