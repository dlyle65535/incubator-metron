#
#  Licensed to the Apache Software Foundation (ASF) under one or more
#  contributor license agreements.  See the NOTICE file distributed with
#  this work for additional information regarding copyright ownership.
#  The ASF licenses this file to You under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance with
#  the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
%define timestamp           %(date +%Y%m%d%H%M)
%define version             %{?_version}%{!?_version: UNKNOWN}
%define vendor_version      %{?_vendor_version}%{!?_vendor_version: UNKNOWN}
%define base_name           metron
%define name                %{base_name}-%{vendor_version}
%define versioned_app_name  %{base_name}-%{version}
%define buildroot           %{_topdir}/BUILDROOT/%{versioned_app_name}-root
%define installpriority     %{_priority} # Used by alternatives for concurrent version installs
%define __jar_repack        %{nil}
%define _rpmfilename        %%{ARCH}/%%{NAME}.%%{RELEASE}.%%{ARCH}.rpm

%define metron_home         /usr/metron/%{version}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Name:           %{base_name}
Version:        %{version}
Release:        %{timestamp}
BuildRoot:      %{buildroot}
BuildArch:      noarch
Summary:        Apache Metron provides a scalable advanced security analytics framework
License:        Apache2
Group:          Applications/Internet
Source0:        metron-enrichment-%{version}-archive.tar.gz

%description
Apache Metron provides a scalable advanced security analytics framework

%prep
rm -rf %{_rpmdir}/%{buildarch}/%{versioned_app_name}*
rm -rf %{_srcrpmdir}/%{versioned_app_name}*

%build
rm -fr %{_builddir}
mkdir -p %{_builddir}/%{versioned_app_name}

%clean
rm -fr %{buildroot}
rm -fr %{_builddir}/*

%install
rm -fr %{buildroot}
mkdir -p %{buildroot}%{metron_home}

tar -xzf %{SOURCE0} -C %{buildroot}%{metron_home}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

%package        enrichment
Summary:        Metron Enrichment Files
Group:          Applications/Internet

%description enrichment
This package installs the Metron Enrichment files %{metron_home}

%files enrichment
%defattr(644, root, root, 755)
%{metron_home}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

%changelog
* Fri Jul 12 2016 David Lyle <dlyle65535@gmail.com> - 0.2.1
- First packaging