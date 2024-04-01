%global debug_package %{nil}
Name:           onnxruntime
Version:        1.17.1
Release:        1%{?dist}
Summary:        Open Source Machine Learning Inference and Training Acceleration

License:        MIT
URL:            https://github.com/microsoft/onnxruntime
Source0:        onnxruntime-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  python3-devel
Requires:       glibc

%description
ONNX Runtime is a performance-focused engine for ONNX models, which can be used for inferencing and training. It supports multiple platforms and hardware accelerations.

%prep
%setup -q -n onnxruntime-%{version}

%build
mkdir -p build && cd build
cmake ../cmake -DCMAKE_BUILD_TYPE=Release -Donnxruntime_BUILD_SHARED_LIB=ON
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

cd %{_builddir}/onnxruntime-%{version}/build
cmake --install . --prefix %{buildroot}/usr

%files
%license LICENSE
%doc README.md
/usr/include/onnxruntime/*
/usr/lib64/*
/usr/bin/*

%changelog
* Wed Feb 28 2024 JunjunLiu - 1.17.1-1
- Initial package creation

