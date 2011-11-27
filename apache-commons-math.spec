%global base_name math
%global short_name commons-%{base_name}

Name:             apache-%{short_name}
Version:          2.2
Release:          3
Summary:          Java library of lightweight mathematics and statistics components

Group:            Development/Java
License:          ASL 1.1 and ASL 2.0 and BSD
URL:              http://commons.apache.org/%{base_name}/
Source0:          http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Patch0:           %{name}-2.2-remove_clirr_from_pom.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    java-devel >= 0:1.6.0
BuildRequires:    jpackage-utils
BuildRequires:    junit4
BuildRequires:    maven2 >= 2.2.1
BuildRequires:    maven-antrun-plugin
BuildRequires:    maven-assembly-plugin
BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-idea-plugin
BuildRequires:    maven-install-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-javadoc-plugin
BuildRequires:    maven-plugin-bundle
BuildRequires:    maven-resources-plugin
# Should be replaced by maven-surefire-plugin after f15 branch
BuildRequires:    maven-surefire-maven-plugin
BuildRequires:    maven-surefire-provider-junit4
Requires:         java >= 0:1.6.0
Requires:         jpackage-utils
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils
BuildArch:        noarch

%description
Commons Math is a library of lightweight, self-contained mathematics and
statistics components addressing the most common problems not available in the
Java programming language or Commons Lang.


%package javadoc
Summary:          Javadoc for %{name}
Group:            Development/Java
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{short_name}-%{version}-src
%patch0 -p1 -b .remove_clirr_from_pom


%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
mvn-jpp \
    -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
    install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -pm 644 target/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
(cd %{buildroot}%{_javadir} && for jar in *; do ln -sf ${jar} `echo $jar| sed  "s|apache-||g"`; done)

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{short_name}.pom
%add_to_maven_depmap org.apache.commons %{short_name} %{version} JPP %{short_name}

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}/


%clean
rm -rf %{buildroot}


%post
%update_maven_depmap


%postun
%update_maven_depmap


%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :


%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_javadocdir}/%{name}



