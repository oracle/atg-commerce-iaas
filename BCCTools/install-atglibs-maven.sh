#!/bin/sh

ATG_VERSION=11.1
ENDECA_NAV_VERSION=6.5.1

if [ x${DYNAMO_ROOT} = x ]; then
    echo "Your DYNAMO_ROOT directory isn't set. Exiting"
    exit 1
fi


mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=webui-preview-1_0 \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/WebUI/Preview/taglibs/webui-preview/lib/webui-preview-1_0.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=springtonucleus \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DAF/spring/lib/springtonucleus.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=dspjspTaglib1_0 \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DAS/taglib/dspjspTaglib/1.0/lib/dspjspTaglib1_0.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=ADC-classes \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/ADC/lib/classes.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=DAS-classes \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DAS/lib/classes.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=DAS-resources \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DAS/lib/resources.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=DPS-resources \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DPS/lib/resources.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=DSS-resources \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DSS/lib/resources.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=DCS-resources \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DCS/lib/resources.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=DAS-servlet \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DAS/lib/servlet.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=DASUI-uiclasses \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DAS-UI/lib/uiclasses.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=DCS-classes \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DCS/lib/classes.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=DPS-classes \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DPS/lib/classes.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=DSS-classes \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DSS/lib/classes.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=DCS-UI-classes \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DCS-UI/lib/classes.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=BCC-classes \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/BCC/lib/classes.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=SiteAdmin-classes \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/SiteAdmin/lib/classes.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=DPS-UI-classes \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DPS-UI/lib/classes.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=AssetUI-classes \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/AssetUI/lib/classes.jar


mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=json-taglib-0.4 \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DAS/taglib/json/0.4/lib/json-taglib-0.4.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=jstl-1.1 \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DAS/taglib/jstl/1.1/lib/jstl.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=standard-1.1 \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DAS/taglib/jstl/1.1/lib/standard.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=DAF-Search-Index \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DAF/Search/Index/lib/classes.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=DAF-Search-Base \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DAF/Search/Base/lib/classes.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=DAF-Search-Common \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DAF/Search/common/lib/classes.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=WebUI-classes \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/WebUI/lib/classes.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=DAF-Endeca-Assembler \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DAF/Endeca/Assembler/lib/classes.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=endeca-assembler-core \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DAF/Endeca/Assembler/lib/endeca_assembler_core-${ATG_VERSION}.0.jar

mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=endeca-assembler-navigation \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DAF/Endeca/Assembler/lib/endeca_assembler_navigation-${ATG_VERSION}.0.jar

# The naming of this jar does not match the rest of the ATG libraries. Keeping the maven version as 11.1 for consistency since it is part of the 11.1 product
mvn install:install-file \
  -DgroupId=atg \
  -DartifactId=endeca-navigation \
  -Dpackaging=jar \
  -Dversion=${ATG_VERSION} \
  -Dfile=${DYNAMO_ROOT}/DAF/Endeca/Assembler/lib/endeca_navigation-${ENDECA_NAV_VERSION}.jar



